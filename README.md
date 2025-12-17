# HMCTS Test Automation Challenge

Automation framework for exercising the [bstackdemo](https://bstackdemo.com) commerce site as part of the HMCTS automation challenge submission.  
It demonstrates BDD-style Selenium tests with multi-environment execution (local browsers, Selenium Grid in Docker, BrowserStack) and CI coverage.

---

## Table of contents
- [Test coverage](#test-coverage)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Running the tests](#running-the-tests)
- [Docker & Selenium Grid](#docker--selenium-grid)
- [BrowserStack](#browserstack)
- [CI pipeline](#ci-pipeline)
- [Reports & screenshots](#reports--screenshots)

---

## Test coverage
All user journeys are written in Gherkin under `tests/features` and executed via `pytest-bdd`.

| Feature file | Description | Markers |
| ------------ | ----------- | ------- |
| `login.feature` | Valid login flows, negative login validation, UI smoke checks | `login`, `login_valid`, `login_invalid`, `ui_baseline` |
| `checkout.feature` | Add-to-cart validations, enter shipping details, order summary validation, empty cart behaviour | `checkout`, `checkout_single_cart`, `checkout_shipping_details`, `checkout_empty_cart` |
| `e2e_purchase.feature` | End-to-end purchase scenarios (single & multi product) | `e2e`, `e2e_single_item`, `e2e_multi_item` |
| `tests/features/api_catalog.feature` | BrowserStack Demo catalog + sign-in API checks | `api`, `api_catalog`, `api_login` |

---

## Project structure
```
.
├── config/                # YAML config consumed by fixtures
├── pages/                 # Selenium Page Objects
├── tests/
│   ├── features/          # Gherkin scenarios
│   ├── step_definitions/  # pytest-bdd steps (with shared common steps)
│   └── conftest.py        # fixtures, hooks, screenshot handling
├── utils/driver_factory.py# Local/Grid/BrowserStack driver creation
├── Dockerfile             # Container image for running pytest
├── docker-compose.yml     # Selenium Grid (Chrome) + executor
├── .github/workflows/ci.yml# GitHub Actions pipeline
└── README.md
```

---

## Requirements
- Python 3.11+
- Google Chrome & ChromeDriver (for local default run)
- Docker + Docker Compose (optional, for containerized/Grid execution)
- BrowserStack account (optional for cloud runs)

Install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Configuration
Runtime settings reside in `config/config.yaml`. Key fields:

```yaml
base_url: "https://www.bstackdemo.com"
browser: "chrome-headless"        # chrome, firefox, chrome-headless, ...
run_mode: "local"                 # local, grid, browserstack
grid_url: "http://selenium:4444/wd/hub"
implicit_wait: 2
api_base_url: "https://www.bstackdemo.com/api"
```

All values can be overridden through environment variables at runtime:
| Env var | Description |
| ------- | ----------- |
| `BASE_URL` | Override AUT URL |
| `BROWSER` | Browser name/mode |
| `RUN_MODE` | `local` / `grid` / `browserstack` |
| `GRID_URL` | Grid endpoint when `run_mode=grid` |
| `IMPLICIT_WAIT` | Wait duration in seconds |
| `API_BASE_URL` | Override the BrowserStack Demo API endpoint |
| `BROWSERSTACK_USERNAME`/`BROWSERSTACK_ACCESS_KEY` | Required for BrowserStack execution |

---

## Running the tests
### Local browser (default: Chrome headless)
```bash
pytest
```
Run specific feature markers:
```bash
pytest -m checkout
pytest -m login_valid
```

### Local browser with GUI
```bash
export BROWSER=chrome
pytest
```

### API-only checks
```bash
pytest -m api
```
This executes the scenarios in `tests/features/api_catalog.feature` backed by the REST client and pytest-bdd steps.
Set `API_BASE_URL` if you want to point the service tests at a different backend.

### Static analysis (pylint)
```bash
pylint --rcfile=.pylintrc api pages tests utils
```
The `.pylintrc` keeps the run focused on true errors (E level) so CI can fail fast on syntax/import issues without overwhelming noise.

---

## Docker & Selenium Grid
The framework includes a single-command setup to spin up Selenium and run the suite inside containers.

```bash
docker compose up --abort-on-container-exit --exit-code-from tests
docker compose down -v  # cleanup
```

What happens:
1. `selenium/standalone-chrome` container provides the Grid at `http://selenium:4444/wd/hub`.
2. `tests` service builds the repo Dockerfile, overrides `RUN_MODE=grid`, and executes `pytest -v`.

Customize browsers by editing `docker-compose.yml` or passing env overrides (`BROWSER=firefox`, etc).

---

## BrowserStack
To run the suite in BrowserStack:
```bash
export RUN_MODE=browserstack
export BROWSERSTACK_USERNAME=<username>
export BROWSERSTACK_ACCESS_KEY=<access_key>
# optionally select browser (default: chrome)
export BROWSER="chrome"
pytest
```
Capabilities are defined in `utils/driver_factory.get_browserstack_driver`.

---

## CI pipeline
`/.github/workflows/ci.yml` runs for every push to `main` and for pull requests in GitHub:
- **Lint job** – installs Python dependencies and runs `pylint --rcfile=.pylintrc api pages tests utils` to catch syntax/import errors early.
- **Tests job** – depends on lint, then:
  1. Checks out the repository via `actions/checkout`.
  2. Sets up Docker Buildx so Compose builds work reliably on the hosted runner.
  3. Runs `docker compose build tests` followed by `docker compose up --abort-on-container-exit --exit-code-from tests` to execute the suite against the Selenium Grid service.
  4. Always performs `docker compose down -v` (even on failures) for cleanup.

Runner requirements: GitHub-hosted Ubuntu runners already ship with Docker + Compose, so the only configuration you need is to store BrowserStack credentials (if required) as Actions secrets.
The default pytest configuration runs with `-n auto`, so CI automatically parallelises tests across the runner via `pytest-xdist`.

---

## Reports & screenshots
- HTML reports: generated automatically at `reports/report.html` (configured via `pytest.ini`).
- Screenshots: captured on failure and linked directly within the HTML report via hooks in `tests/conftest.py`.
- Artifacts can be exposed in CI by archiving the `reports/` directory if needed.
- Accessibility: axe-core checks are wired up through the `the page should pass accessibility checks` step, but the login scenario invoking it is currently disabled; you can enable it when you want to review `reports/accessibility/*.json` outputs.

---

## Planned automation coverage
High-priority journeys identified for the next iteration are already stubbed as commented scenarios in the `tests/features` directory so they can be elaborated later:

- `product.feature`: search behaviour, vendor filters, price sort order, favourites panel, and product image health.
- `cart.feature`: removing items, handling empty-cart states, and verifying quantity-driven subtotal recalculations.
- `checkout.feature`: inline validation for required fields/invalid postcodes plus verifying product thumbnails in the summary.
- `offers_orders_favorites.feature`: offers carousel accuracy, historic orders table, and favourites persistence across reloads.
- `visual_checks.feature`: consistent footer links/illustrations and validating the `image_not_loading_user` persona renders actual images.

These scenarios remain commented (`@todo`) to avoid impacting the current green test suite while still documenting the design.

---

## Additional ideas / next steps
- Parallel execution using Selenium Grid with multiple nodes (with `pytest-xdist`).
- Parameterised BrowserStack runs that cover multiple OS/browser/version combinations via build matrices or env-driven capabilities.
- Visual regression snapshots using BrowserStack Percy or similar tooling.
- Security scanning with Snyk integrated into the CI pipeline.
- Static analysis (PyLint/flake8) to enforce code style and catch issues early.
- Allure reporting alongside pytest-html for richer historical dashboards.
- Secrets management for BrowserStack credentials in CI.
- Coverage overhaul with more negative/edge cases or API hooks.
