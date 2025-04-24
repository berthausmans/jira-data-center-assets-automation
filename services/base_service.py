
from api.issues import JiraIssuesClient
from api.comments import JiraCommentsClient
from api.assets import JiraAssetsClient

class BaseService:
    def __init__(self, config):
        self.config = config
        self.issues_client = JiraIssuesClient(config)
        self.comments_client = JiraCommentsClient(config)
        self.assets_client = JiraAssetsClient(config)

    def run(self):
        raise NotImplementedError("Subclasses should implement the `run` method.")
