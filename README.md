
# Jira Data Center Assets Automation

This Python framework automates certificate expiry tracking in Jira Assets.

## 🔧 Features

- Connects to Jira Data Center using API token
- Searches for expiring certificates (via Jira Insight/Assets)
- Automatically creates renewal issues
- Adds scheduled comment reminders at 90, 60, and every day within the last 30 days

## 🛠 Requirements

- Python 3.8+
- `.env` file with Jira credentials (token, URL, email)

## 📦 Install and Setup

```bash
# Clone the repository
git clone https://github.com/your-username/jira-data-center-assets-automation.git
cd jira-data-center-assets-automation

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ .env Configuration

```env
JIRA_BASE_URL=https://yourcompany.atlassian.net
JIRA_API_TOKEN=your_token_here
JIRA_EMAIL=you@yourcompany.com
```

## 🚀 Running the Script

```bash
python cli.py run CertificateExpiryChecker
```

This will check for expiring certificates and trigger appropriate Jira issue creation and reminders.

## 🧪 Running Tests

```bash
python -m unittest discover tests
```

## 📅 Scheduling

Run this via:
- Cron
- Azure Functions
- Apache Airflow
