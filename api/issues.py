from .base_client import JiraBaseClient
from datetime import datetime
import re

class JiraIssuesClient(JiraBaseClient):
    def search_issues(self, jql):
        result = self.get("/rest/api/2/search", {"jql": jql})
        return result.get("issues", [])

    def create_issue_for_certificate(self, project_key, summary, description, certificate, duedate=None, epic=None):
        fields = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Task"}
        }

        # Conditionally add the due date field
        if duedate:
            fields["duedate"] = duedate.strftime('%Y-%m-%d') + " 00:00:00"

        # Conditionally add the certificate field
        if certificate:
            fields["customfield_12101"] = [{
                "key": certificate
            }]

        # Conditionally add the certificate field
        if epic:
            fields["customfield_10108"] = epic

        return self.post("/rest/api/2/issue", {"fields": fields})
