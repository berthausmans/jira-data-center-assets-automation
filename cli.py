import importlib
import logging
import sys
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class JiraConfig:
    base_url: str
    api_token: str
    email: str

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def run_service(service_name, config):
    try:
        module_path = "services." + service_name.lower()
        class_name = service_name + "Service"
        module = importlib.import_module(module_path)
        service_class = getattr(module, class_name)
        service_instance = service_class(config)
        logger.info(f"Starting service: {service_name}")
        service_instance.run()
        logger.info(f"Service {service_name} completed successfully.")
    except ModuleNotFoundError:
        logger.error(f"Service module '{module_path}' not found.")
    except AttributeError:
        logger.error(f"Service class '{class_name}' not found in '{module_path}'.")
    except Exception as e:
        logger.exception(f"An error occurred while running service '{service_name}': {e}")

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "run":
        service_to_run = sys.argv[2]
        config = JiraConfig(
            base_url=os.getenv("JIRA_BASE_URL"),
            api_token=os.getenv("JIRA_API_TOKEN"),
            email=os.getenv("JIRA_EMAIL")
        )
        run_service(service_to_run, config)
    else:
        logger.info("Usage: python cli.py run <ServiceName>")
