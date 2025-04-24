
from .base_client import JiraBaseClient

class JiraCommentsClient(JiraBaseClient):
    def get_comments(self, issue_key):
        result = self.get(f"/rest/api/2/issue/{issue_key}/comment")
        return result.get("comments", [])

    def add_comment(self, issue_key, body):
        data = {"body": body}
        return self.post(f"/rest/api/2/issue/{issue_key}/comment", data)
