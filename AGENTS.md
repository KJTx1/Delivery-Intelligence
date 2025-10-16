# Repository Guidelines

## Project Structure & Module Organization
Core agent logic resides in `src/oci_delivery_agent`, with `handlers.py` providing the OCI Function entry point, `chains.py` defining the LangChain workflows, `tools.py` wrapping OCI services, and `config.py` managing typed settings. The deployable Fn Function scaffold lives in `delivery-function/` (notably `func.py`, `func.yaml`, and its `requirements.txt` mirror). Shared docs are under `docs/`, reference assets in `local_assets/`, and smoke tests in `tests/`. Keep new modules colocated with their runtime peers and mirror any additions into the Fn bundle when they are required in production.

## Build, Test, and Development Commands
- `fn -v deploy --app delivery-agent-app` deploys the function using Fn Project CLI.
- `cd delivery-function && fn -v deploy --app delivery-agent-app` performs a manual deploy using the Fn CLI context.
- `python -m pytest tests/` runs the lightweight regression suite; prefer the `-k` flag when targeting a single tool.
- `python tests/test_caption_tool.py` exercises the caption and damage tools end to end with local fallbacks.

## Coding Style & Naming Conventions
Write Python 3.10+ code with four-space indentation, type hints, and early returns for error paths, matching existing modules. Use `CamelCase` for classes, `snake_case` for functions and variables, and uppercase for configuration constants. Keep public tool interfaces returning JSON-serializable data and document any non-obvious behavior with concise docstrings. Run `ruff` or `black` locally before committing if you introduce formatting churn.

## Testing Guidelines
Target `pytest`-discoverable functions named `test_*`. Provide deterministic fixtures by seeding local image assets in `local_assets/deliveries/` and, when calling live OCI services, guard calls behind environment checks. Ensure new tools expose local fallbacks so `python tests/test_caption_tool.py` passes without cloud access. Aim for functional coverage of new chains and update assertions when structured JSON schemas change.

## Commit & Pull Request Guidelines
Follow Conventional Commits (`feat:`, `fix:`, `docs:`) as seen in `git log`. Group related edits and keep messages imperative (e.g., `feat: add damage scoring`). Every PR should describe runtime impact, list required OCI variables, link supporting issues, and include screenshots or JSON samples when vision outputs change. Request review before merging deployment-affecting changes.

## Security & Configuration Tips
Never commit `.env` or OCI credential files; extend `env.example` when adding required variables. Validate that exported artifacts omit secrets before deploying. When testing locally, set `LOCAL_ASSET_ROOT` to a sanitized directory to avoid leaking customer imagery, and double-check that timelines and bucket names point to non-production compartments.
