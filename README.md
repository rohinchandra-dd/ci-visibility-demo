# Pulse Community — CI Visibility Demo

A **Forem-inspired community platform** built to demo Datadog **CI Pipeline Visibility**, **Test Optimization**, **Test Parallelization**, and **Test Impact Analysis**.

This repo contains a working full-stack app (FastAPI + React) with **~1,900 tests** across Python (pytest), JavaScript (Jest), and Playwright E2E — designed to show dramatic before/after CI improvements in customer demos.

## What this demonstrates

| Capability | How it's generated |
|------------|-------------------|
| **Pipeline Visibility** | Multi-job CI with lint, build, matrix parallelization, E2E |
| **Test Visibility** | Per-test traces via Datadog Test Optimization GitHub Action |
| **Test Parallelization** | `ddtest plan` → matrix → `ddtest run` (up to 8 nodes) |
| **Test Impact Analysis** | Small PRs skip unaffected tests (>80% reduction) |
| **Slow tests** | Analytics/search integration tests (~5 min serial) |
| **Flaky tests** | Notification/email tests (~38% failure rate) |

## Expected CI durations

| Workflow | Mode | Duration |
|----------|------|----------|
| `CI Baseline` | Serial, no TIA | ~25–35 min |
| `CI` | Parallelized (8 nodes) | ~4–6 min |
| `CI` + TIA | Small PR | ~1–3 min |

## Quick start

### Run the app

```bash
docker compose up --build
# API: http://localhost:8000/health
# UI:  http://localhost:5173
```

### Run tests locally

```bash
make install
make test          # fast tests only
make test-baseline # full suite (slow — ~30 min)
```

## Repository structure

```
ci-visibility-demo/
├── python/                    # FastAPI backend (Pulse API)
│   ├── src/
│   │   ├── api/               # REST endpoints
│   │   ├── core/              # Config, auth, database
│   │   ├── models/            # SQLAlchemy models
│   │   └── services/          # Domain logic (users, articles, comments, …)
│   └── tests/
│       ├── unit/              # ~800 fast unit tests
│       ├── api/               # FastAPI TestClient tests
│       ├── integration/       # DB-backed workflow tests
│       ├── slow/              # Analytics/search (~5 min serial)
│       ├── flaky/             # Notification delivery (~38% fail)
│       └── ddtest/excluded/   # TIA exclude-pattern canary
├── javascript/                # React frontend (Vite)
│   ├── src/                   # SPA components + API client
│   └── tests/
│       ├── unit/              # ~650 Jest tests
│       ├── integration/       # API client tests
│       ├── slow/              # Slow JS tests
│       ├── flaky/             # Flaky JS tests
│       └── e2e/               # Playwright (~21 tests)
├── .github/workflows/
│   ├── ci-baseline.yml        # "Before" demo — serial full suite
│   ├── ci.yml                 # "After" demo — ddtest parallel + TIA
│   ├── pr-checks.yml          # PR pipeline (lint → tests → report)
│   ├── python-tests.yml       # Full Python suite
│   ├── javascript-tests.yml   # Full JavaScript suite
│   ├── integration-suite.yml  # Slow integration pipeline
│   └── scheduled.yml          # Cron for flaky test history
├── docs/DEMO.md               # Step-by-step customer demo script
└── docker-compose.yml         # Postgres + API + frontend
```

## Datadog setup (datadoghq.com)

### 1. Push to GitHub

```bash
git remote add origin https://github.com/<your-org>/ci-visibility-demo.git
git push -u origin main
```

### 2. Enable Pipeline Visibility

1. **Software Delivery → CI Visibility → Add a Pipeline Provider → GitHub**
2. Install the Datadog GitHub App
3. Enable CI Visibility for this repository

### 3. Enable Test Visibility

1. Create an API key in **Organization Settings → API Keys**
2. Add GitHub secret `DD_API_KEY`
3. Workflows already include `datadog/test-visibility-github-action@v3`

### 4. Register for Test Optimization

After the first test run, register in **CI/CD Optimization → Settings → Repositories**:

- **Repository URL:** `https://github.com/<your-org>/ci-visibility-demo`
- **Default branch:** `main`

Then enable **Test Impact Analysis** and **Test Parallelization** for:
- `pulse-api`
- `pulse-frontend`
- `pulse-e2e`

### 5. Run demo workflows

| Workflow | When to use | Expected duration |
|----------|-------------|-------------------|
| `CI Baseline` | "Before" demo | ~25–35 min |
| `CI` | "After" demo with parallelization | ~4–6 min |
| `CI` on TIA demo PR | "After" with TIA | ~1–3 min |
| `PR Checks` | Day-to-day PR validation | ~3–5 min |
| `Scheduled Flaky Test Run` | Builds flaky history (every 4h) | ~1 min |

See [docs/DEMO.md](docs/DEMO.md) for the full customer demo script.

## Where to look in Datadog

### Pipeline Visibility
**Software Delivery → CI Visibility → Pipelines** — filter `@ci.env:ci-visibility-demo`

Compare `CI Baseline` (single job) vs `CI` (matrix parallelization).

### Test Optimization Explorer
**Software Delivery → Test Optimization → Explorer** — filter `env:ci-visibility-demo`

Sort by duration to find slow tests like `test_analytics_fibonacci_benchmark`.

### Flaky Tests
**Software Delivery → Test Optimization → Flaky Tests** — look for `test_payment_gateway_timeout` after ~5–10 scheduled runs.

## Demo branches for TIA

| Branch | Change | Impact |
|--------|--------|--------|
| `demo/tia-comment-fix` | Edit `services/comments.py` | Skips most tests |
| `demo/tia-shared-utils` | Edit `services/utils.py` | Runs cross-module tests |
| `demo/tia-frontend-only` | Edit `ArticleEditor.jsx` | Skips Python tests |

## Test services (DD_SERVICE values)

| Workflow | DD_SERVICE |
|----------|-----------|
| CI Baseline | `pulse-api-baseline`, `pulse-frontend-baseline`, `pulse-e2e-baseline` |
| CI (optimized) | `pulse-api`, `pulse-frontend`, `pulse-e2e` |
| PR Checks | `pr-checks-python`, `pr-checks-javascript` |
| Integration Suite | `integration-python`, `integration-javascript` |
| Scheduled | `scheduled-python-flaky`, `scheduled-javascript-flaky` |

All workflows use `DD_ENV=ci-visibility-demo`.

## Regenerating bulk tests

```bash
python3 scripts/generate_parametrized_tests.py
```

This regenerates parametrized unit/API tests used to reach demo-scale test volume. Do not edit `*_generated.py` / `generated.test.js` files by hand.
