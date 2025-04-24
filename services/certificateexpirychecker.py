from datetime import datetime

class CertificateExpiryCheckerService:
    def __init__(self, config):
        from services.base_service import BaseService
        self.base_service = BaseService(config)
        self.assets_client = self.base_service.assets_client
        self.issues_client = self.base_service.issues_client
        self.comments_client = self.base_service.comments_client

    def run(self):
        # Query the certificates in Jira Assets using the Jira API
        certificates = self.assets_client.search_assets_by_type("Certificate")

        for cert in certificates:
            # Generate an array with the attributes as a pair (name > value)
            fields = {}

            for certAttribute in cert.get('attributes', []):
                attr_name = certAttribute.get('objectTypeAttribute').get('name')
                attr_type = certAttribute.get('objectTypeAttribute').get('defaultType')
                attr_value = certAttribute.get('objectAttributeValues')[0].get('value')

                if attr_type and attr_type.get("name") == "DateTime":
                    attr_value = datetime.strptime(attr_value.split("T")[0], "%Y-%m-%d").date()

                fields[attr_name] = attr_value

            cert_key = cert.get("objectKey")
            cert_name = cert.get("name")
            cert_expiry_date = fields.get("Expiry Date")

            if cert_expiry_date:
                if cert_expiry_date.year < 1975:
                    #print(f"Expiry Date for {cert_name} is empty.")
                    continue
                elif cert_expiry_date.year > 2500:
                    #print(f"Expiry Date for {cert_name} does never expire.")
                    continue
                else:
                    cert_days_until_expiry = (cert_expiry_date - datetime.now().date()).days

                    # TODO: Add Business Logic around a Certificate
                    #print(f"Days until expiry for {cert_name}: {cert_days_until_expiry} days")

                    if cert_days_until_expiry < 0:
                        # TODO: Escalate to ICMT Management, a certificate is expired!
                        continue
                    elif cert_days_until_expiry <= 90:
                        # Check if there is already created an issue to process the certificate renewal
                        jql = f'project = "Assets CMDB" AND (summary ~ "Renew") AND (summary ~ "{cert_key}") AND statusCategory NOT IN (Done)'
                        existing_issues = self.issues_client.search_issues(jql)
                        if existing_issues:
                            issue = existing_issues[0]
                        else:
                            # Create a new Jira Issue
                            issue = self.issues_client.create_issue_for_certificate(
                                project_key="CMDB",
                                summary=f'Renew certificate "{cert_name}" ({cert_key})',
                                description=f'The certificate "{cert_name}" ({cert_key}) will expire on {cert_expiry_date.strftime("%d-%m-%Y")}.',
                                certificate=cert_key,
                                duedate=cert_expiry_date,
                                epic="CMDB-411"
                            )

                        # Get the comments that are added to the Issue
                        comments = self.comments_client.get_comments(issue["key"])                        
                        existing_bodies = [c.get("body", "") for c in comments]

                        # Generic comment format
                        def make_comment(days_left):
                            return f"Reminder: Certificate \"{cert_name}\" ({cert_key}) will expire in {days_left} day(s)."

                        # Between 90 and 31 days → Add 1 comment if it's 90 or 60 and hasn't been added yet
                        if 31 <= cert_days_until_expiry <= 90:
                            if cert_days_until_expiry in [90, 60]:
                                if not any(f"will expire in {cert_days_until_expiry} day(s)" in body and cert_key in body for body in existing_bodies):
                                    self.comments_client.add_comment(issue["key"], make_comment(cert_days_until_expiry))

                        # Between 30 and 0 days → Daily comment, but only once per day
                        elif 0 <= cert_days_until_expiry <= 30:
                            comment_today = make_comment(cert_days_until_expiry)
                            if not any(comment_today in body for body in existing_bodies):
                                self.comments_client.add_comment(issue["key"], comment_today)
