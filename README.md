# CI Visibility Demo

A sandbox repository for exploring Datadog **CI Pipeline Visibility** and **Test Optimization**. It runs multiple GitHub Actions workflows with intentionally slow and flaky tests across Python (pytest) and JavaScript (Jest).

## What this repo demonstrates

| Capability | How it's generated |
|------------|-------------------|
| **Pipeline Visibility** | Multiple workflows with multi-job pipelines, setup/teardown overhead, and varying job durations |
| **Test Visibility** | Per-test traces, durations, and failure stack traces via Datadog Test Optimization |
| **Slow tests** | 1 slow test per language (~5s) exercising real `app` code; former slow scenarios live as passing fast tests |
| **Flaky tests** | 1 flaky test per language (~40% failure rate); former flaky scenarios live as passing fast tests |

## Repository structure

```
ci-visibility-demo/
├── .github/workflows/
│   ├── pr-checks.yml          # Multi-job PR pipeline (lint → parallel tests → report)
│   ├── python-tests.yml       # Full Python test suite
│   ├── javascript-tests.yml   # Full JavaScript test suite
│   ├── integration-suite.yml  # Slow integration pipeline with setup/teardown
│   └── scheduled.yml          # Cron job for flaky test history on main
├── python/                    # pytest suite (fast, slow, flaky)
└── javascript/                # Jest suite (fast, slow, flaky)
```

## Setup checklist

### 1. Push this repo to GitHub

```bash
git init
git add .
git commit -m "Initial CI Visibility demo repo"
git remote add origin https://github.com/<your-org>/ci-visibility-demo.git
git push -u origin main
```

### 2. Enable Pipeline Visibility (GitHub App)

Pipeline traces are collected automatically via the Datadog GitHub App — no workflow changes needed.

1. In Datadog, go to **Software Delivery → CI Visibility → Add a Pipeline Provider → GitHub**
2. Install/configure the Datadog GitHub App on the account hosting this repo
3. Enable **CI Visibility** for this repository
4. Optionally enable **Job Logs Collection** for log correlation

Docs: [GitHub Actions Setup for CI Visibility](https://docs.datadoghq.com/continuous_integration/pipelines/github/)

### 3. Enable Test Visibility (agentless)

Test traces require the `DD_API_KEY` secret and the Datadog Test Visibility GitHub Action (already configured in workflows).

1. In Datadog, go to **Organization Settings → API Keys** and create or copy an API key
2. In GitHub, go to **Settings → Secrets and variables → Actions**
3. Add a repository secret named `DD_API_KEY` with your API key value
4. If your sandbox is not on US1, update `site:` in each workflow (e.g. `datadoghq.eu`)

Docs: [Datadog Test Visibility GitHub Action](https://github.com/DataDog/test-visibility-github-action)

### 4. Register the repository in Datadog (for future features)

After the first test run, register the repo in **CI/CD Optimization → Settings → Repositories**:

- **Repository URL:** `https://github.com/<your-org>/ci-visibility-demo`
- **Default branch:** `main`

This unlocks Intelligent Test Runner, Early Flake Detection, and Flaky Test Management when you're ready to add them.

### 5. Run workflows

Trigger workflows manually from the **Actions** tab, or push to `main` / open a PR:

| Workflow | Trigger | What to expect |
|----------|---------|----------------|
| `PR Checks` | push, PR | Multi-job pipeline; may fail due to flaky test (~40%) |
| `Python Tests` | push, PR | Full Python suite (33 fast + 1 slow + 1 flaky; ~5s slow portion) |
| `JavaScript Tests` | push, PR | Full JavaScript suite (33 fast + 1 slow + 1 flaky; ~5s slow portion) |
| `Integration Suite` | push to main | ~25s pipeline with setup overhead and one slow test per language |
| `Scheduled Flaky Test Run` | every 4 hours | Flaky tests only; builds flake history |

## Where to look in Datadog

### Pipeline Visibility

**Software Delivery → CI Visibility → Pipelines**

- Filter by repository: `ci-visibility-demo`
- Open `PR Checks` or `Integration Suite` to see job-level flame graphs
- Compare setup vs test time in `Integration Suite`

### Test Optimization Explorer

**Software Delivery → Test Optimization → Explorer**

Useful filters:

| Filter | Value |
|--------|-------|
| `env` | `ci-visibility-demo` |
| `service` | `python-tests`, `javascript-tests`, `pr-checks-python`, etc. |
| `@test.status` | `fail` |
| `@test.name` | `*payment_gateway*` |

### Flaky tests

After ~5–10 scheduled runs on `main`:

**Software Delivery → Test Optimization → Flaky Tests**

Look for `test_payment_gateway_timeout` and `payment gateway timeout` with mixed pass/fail on the default branch.

Former flaky scenarios (inventory, rate limits, notifications, sessions) now run as deterministic passing fast tests.

### Slow tests

**Software Delivery → Test Optimization → Explorer → sort by Duration**

Look for `test_analytics_fibonacci_benchmark` and `analytics fibonacci benchmark` (~5s each).

Former slow scenarios (user lookup, reports, checkout, bulk import, cache warmup) now run as deterministic passing fast tests.

## Running tests locally

### Python

```bash
cd python
pip install -r requirements.txt
pytest tests/ -v                    # all tests
pytest tests/ -v -m "not slow"      # skip slow tests
pytest tests/test_flaky.py -v       # flaky only
```

### JavaScript

```bash
cd javascript
npm install
npm test                            # all tests
npm run test:fast                   # fast only
npm run test:slow                   # slow only
npm run test:flaky                  # flaky only
```

## Workflows and test services

| Workflow | DD_SERVICE values |
|----------|-------------------|
| `python-tests.yml` | `python-tests` |
| `javascript-tests.yml` | `javascript-tests` |
| `pr-checks.yml` | `pr-checks-python`, `pr-checks-javascript` |
| `integration-suite.yml` | `integration-python`, `integration-javascript` |
| `scheduled.yml` | `scheduled-python-flaky`, `scheduled-javascript-flaky` |

All workflows use `DD_ENV=ci-visibility-demo`.

## Notes

- **Flaky tests will fail CI intermittently** — this is intentional for demo purposes.
- **Pipeline Visibility requires the GitHub App** — the API key alone only enables Test Visibility.
- **Jest requires `NODE_OPTIONS`** — workflows set `NODE_OPTIONS: -r ${{ env.DD_TRACE_PACKAGE }}` per the action docs.
- **Default branch matters** — flaky classification and the Pipeline List prioritize `main`. The scheduled workflow helps build history automatically.

## Future extensions

- **Early Flake Detection:** Add a new flaky test on a feature branch and enable EFD in repo settings
- **Intelligent Test Runner:** Enable ITR in CI/CD Optimization settings to skip unaffected tests
- **Flaky Test Management:** Quarantine, disable, or attempt-to-fix flaky tests from the Flaky Tests UI
- **Additional languages:** Add Go or Java test suites using the same action with `languages: go` or `languages: java`
