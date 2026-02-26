# Flask Poll App — DevOps Lab Assignment 2

A simple Yes/No poll web app built with Python Flask, designed for Azure DevOps multi-stage CI/CD deployment to Azure App Service (DEV and STAGING environments).

## Project Structure

```
flask-poll-app/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── startup.txt             # Azure App Service startup command
├── azure-pipelines.yml     # Multi-stage CI/CD pipeline
├── templates/
│   ├── base.html           # Base layout template
│   ├── index.html          # Poll voting page
│   └── results.html        # Results page
└── tests/
    └── test_app.py         # Pytest unit tests
```

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
# App runs at http://localhost:8000
```

## Running Tests

```bash
pytest tests/ -v
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `ENV_LABEL` | Banner label shown on app | `DEV` |
| `ENV_COLOR` | Banner hex color | `#2196F3` |
| `SECRET_KEY` | Flask session secret | `dev-secret-key` |
| `PORT` | Port to run on | `8000` |

## Endpoints

| Route | Method | Description |
|---|---|---|
| `/` | GET | Poll voting page |
| `/vote` | POST | Submit vote |
| `/results` | GET | View results |
| `/health` | GET | Health check (used by pipeline smoke test) |
| `/reset` | POST | Reset session |

## Azure Deployment

This app deploys to two Azure App Service environments:
- **DEV** — Blue banner, for development testing
- **STAGING** — Orange banner, for pre-production validation

See `azure-pipelines.yml` for the full pipeline configuration.
