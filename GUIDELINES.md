# Repository Guidelines

## Project Structure & Module Organization
The project is organized into development and production environments:

**Development Environment** (`development/`):
- Core agent logic resides in `development/src/oci_delivery_agent/`
- `handlers.py` provides the OCI Function entry point
- `chains.py` defines the LangChain workflows
- `tools.py` wraps OCI services
- `config.py` manages typed settings
- Test files in `development/tests/`
- Sample assets in `development/assets/`
- Configuration in `development/.env`

**Production Environment** (`delivery-function/`):
- Deployable Fn Function scaffold with `func.py`, `func.yaml`, `requirements.txt`
- Source code in `delivery-function/src/oci_delivery_agent/`
- Docker container for OCI Functions deployment

**Shared Resources**:
- Documentation in `docs/`
- Virtual environment in `venv/` (for development only)
- Environment template in `env.example`

## Build, Test, and Development Commands

**Development Commands**:
```bash
# Activate virtual environment
source venv/bin/activate

# Navigate to development directory
cd development

# Run tests
python tests/test_caption_tool.py
python tests/test_damage_samples.py
```

**Production Deployment**:
```bash
# Deploy to OCI Functions
cd delivery-function
fn -v deploy --app delivery-agent-app
```

**Development Workflow**:
1. Edit code in `development/src/oci_delivery_agent/`
2. Test with `development/tests/`
3. Sync to production: `cp -r development/src/oci_delivery_agent/* delivery-function/src/oci_delivery_agent/`
4. Deploy from `delivery-function/`

## Coding Style & Naming Conventions
Write Python 3.10+ code with four-space indentation, type hints, and early returns for error paths, matching existing modules. Use `CamelCase` for classes, `snake_case` for functions and variables, and uppercase for configuration constants. Keep public tool interfaces returning JSON-serializable data and document any non-obvious behavior with concise docstrings. Run `ruff` or `black` locally before committing if you introduce formatting churn.

## Testing Guidelines
Target `pytest`-discoverable functions named `test_*` in `development/tests/`. Provide deterministic fixtures by seeding local image assets in `development/assets/deliveries/` and, when calling live OCI services, guard calls behind environment checks. Ensure new tools expose local fallbacks so `python tests/test_caption_tool.py` passes without cloud access. Aim for functional coverage of new chains and update assertions when structured JSON schemas change.

**Test Environment**:
- Use `development/.env` for local configuration
- Test files automatically load environment variables
- Assets are located in `development/assets/`
- Virtual environment provides isolated Python environment

## Commit & Pull Request Guidelines
Follow Conventional Commits (`feat:`, `fix:`, `docs:`) as seen in `git log`. Group related edits and keep messages imperative (e.g., `feat: add damage scoring`). Every PR should describe runtime impact, list required OCI variables, link supporting issues, and include screenshots or JSON samples when vision outputs change. Request review before merging deployment-affecting changes.

## Security & Configuration Tips
Never commit `.env` or OCI credential files; extend `env.example` when adding required variables. Validate that exported artifacts omit secrets before deploying. When testing locally, set `LOCAL_ASSET_ROOT` to a sanitized directory to avoid leaking customer imagery, and double-check that timelines and bucket names point to non-production compartments.

**Environment Configuration**:
- **Development**: Use `development/.env` for local testing
- **Production**: Set environment variables in OCI Console → Functions → Configuration
- **Virtual Environment**: Only used for development, not for OCI Functions deployment
- **Asset Management**: Development uses `development/assets/`, production uses OCI Object Storage
