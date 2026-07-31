# Customer Demo Script — Pulse Test Optimization

Use this script when demoing Datadog **Test Optimization**, **Test Parallelization**, and **Test Impact Analysis** to customers.

## Prerequisites

1. Repo pushed to GitHub with `DD_API_KEY` secret configured
2. Datadog GitHub App installed (Pipeline Visibility)
3. Repo registered in **CI/CD Optimization → Settings → Repositories**
4. Test Impact Analysis enabled for services: `pulse-api`, `pulse-frontend`, `pulse-e2e`

## Demo flow (~45 minutes)

### 1. Show the product (5 min)

```bash
docker compose up --build
```

Open http://localhost:5173 — create an account, publish an article, browse the feed. This establishes that this is a real application, not a toy test harness.

### 2. Baseline CI — the "before" (10 min setup, ~30 min run)

1. Go to **Actions → CI Baseline → Run workflow**
2. While it runs, open **Software Delivery → CI Visibility → Pipelines**
3. Filter: `env:ci-visibility-demo`
4. Point out:
   - Single job running all ~1,900 tests serially
   - Lint + build + Python + JavaScript + E2E stacked sequentially
   - Expected duration: **25–35 minutes**

> Talking point: "This is what your CI feels like today — every test runs on every PR."

### 3. Test Parallelization — the first win (5 min setup, ~5 min run)

1. Enable **Test Parallelization** in Datadog CI/CD Optimization settings
2. Run **Actions → CI** (optimized workflow)
3. Show Pipeline Visibility flame graph:
   - `build` job runs `ddtest plan`
   - `python-tests` and `javascript-tests` fan out across up to 8 matrix nodes
   - Expected duration: **4–6 minutes**

> Talking point: "Same tests, split intelligently across CI nodes — 5–8x faster."

### 4. Test Impact Analysis — the dramatic win (5 min)

1. Enable **Test Impact Analysis** in Datadog for `pulse-api` and `pulse-frontend`
2. Open a PR from branch `demo/tia-comment-fix` (one-line change to `comments.py`)
3. Run **CI** workflow on the PR
4. In **Test Optimization → Explorer**, filter `env:ci-visibility-demo` and show:
   - Skipped tests count (>80% of suite)
   - Only comment-related tests ran
   - Expected duration: **1–3 minutes**

### 5. Flaky tests and slow tests (5 min)

1. Open **Test Optimization → Flaky Tests** — show history from scheduled workflow
2. Open **Explorer → sort by Duration** — highlight slow tests:
   - `test_analytics_fibonacci_benchmark` (~5s)
   - `test_search_reindex` (~5–8s each)
   - Playwright E2E tests (~5s each)

### 6. Shared library change — broader impact (5 min)

Open PR from `demo/tia-shared-utils` (change to `services/utils.py`). Show that TIA runs a broader cross-module test set — still far fewer than the full suite.

## Demo branches

| Branch | File changed | Expected TIA impact |
|--------|-------------|---------------------|
| `demo/tia-comment-fix` | `python/src/services/comments.py` | Skips articles, auth, analytics tests |
| `demo/tia-shared-utils` | `python/src/services/utils.py` | Runs broad cross-module tests |
| `demo/tia-frontend-only` | `javascript/src/components/ArticleEditor.jsx` | Skips Python tests |
| `demo/tia-canary-excluded` | `python/tests/ddtest/excluded/` | Validates exclude pattern |

Create branches locally:

```bash
git checkout -b demo/tia-comment-fix
# Edit python/src/services/comments.py — add a docstring
git commit -am "Fix comment moderation message"
git push -u origin demo/tia-comment-fix
```

## Key Datadog filters

| View | Filter |
|------|--------|
| Pipelines | `@ci.env:ci-visibility-demo` |
| Test Explorer | `env:ci-visibility-demo` |
| Baseline runs | `service:pulse-api-baseline OR service:pulse-frontend-baseline` |
| Optimized runs | `service:pulse-api OR service:pulse-frontend` |

## Troubleshooting

- **No test traces?** Verify `DD_API_KEY` secret and `datadog/test-visibility-github-action@v3` in workflow
- **TIA not skipping?** Confirm repo registered and TIA enabled in Test Service Settings; need 3+ commits on default branch
- **ddtest plan fails?** Check `ddtrace>=4.11.0` and `dd-trace>=5.111.0` versions
- **Flaky test noise in PR Checks?** Expected — flaky tests fail ~38% of the time by design
