
from .base_client import JiraBaseClient

class JiraAssetsClient(JiraBaseClient):
    def search_assets_by_type(self, object_type_name):
        endpoint = "/rest/assets/latest/aql/objects"
        params = {
            "objectSchemaId": 6,
            "iql": f'objectType = "{object_type_name}"',
            "includeTypeAttributes": True,
            "resultPerPage": 1000
        }
        return self.get(endpoint, params).get("objectEntries", [])
