from datetime import datetime

class TestJiraIssueService:
    def __init__(self, config):
        from services.base_service import BaseService
        self.base_service = BaseService(config)
        self.assets_client = self.base_service.assets_client
        self.issues_client = self.base_service.issues_client
        self.comments_client = self.base_service.comments_client

    def run(self):
        cert_name = "zorgplatform.zuyderland.nl"
        cert_key = "ICMT-272491"
        cert_expiry_date = datetime.fromisoformat("2025-05-24 00:00:00")

        issue = self.issues_client.create_issue_for_certificate(
            project_key="CMDB",
            summary=f'Renew certificate "{cert_name}" ({cert_key})',
            description=f'The certificate "{cert_name}" ({cert_key}) will expire on {cert_expiry_date.strftime("%d-%m-%Y")}.',
            #certificate=f'{cert_name} ({cert_key})',
            certificate=cert_key,
            duedate=cert_expiry_date,
            epic="CMDB-411"
        )

        print(issue)
