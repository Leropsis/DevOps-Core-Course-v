# LAB03 - Continuous Integration (CI/CD)

## Overview
- **Testing framework:** pytest. It has concise assertions, great fixtures, and strong FastAPI support via TestClient
- **Coverage:** Tests verify `GET /`, `GET /health`, and 404 responses. They assert required JSON fields and data types.
- **Workflow triggers:** Runs on push and pull request changes inside `lab_solutions/lab1/app_python/`.
- **Versioning strategy:** CalVer (`YYYY.MM.DD`). It is simple for a service that is continuously deployed without strict release cycles.

## Workflow Evidence
- **Successful workflow run:** https://github.com/Leropsis/DevOps-Core-Course-v/actions/runs/<run-id>
- **Docker image:** https://hub.docker.com/r/chupapupa/devops-info-service/tags
- **Status badge:** Added in `app_python/README.md`

### Local test run
```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

## Best Practices Implemented
- **Dependency caching:** `actions/setup-python` with pip cache to reduce install time on repeated runs.
- **Fail fast:** If lint or tests fail, the workflow stops and Docker build is skipped.
- **Job dependencies:** Docker build job depends on tests (`needs: test`).
- **Least privilege:** Workflow permissions set to `contents: read`.
- **Path filters:** CI only runs when app files or the workflow change.
- **Concurrency:** Cancels previous runs on the same branch to avoid duplicate work.
- **Security scan:** Snyk scan on dependencies with a high severity threshold.

## Key Decisions
- **Versioning Strategy:** CalVer for date-based releases that are easy to trace and automate.
- **Docker Tags:** `${VERSION}` and `latest` for clear versioned releases plus a default tag.
- **Workflow Triggers:** Path filters prevent unnecessary runs when unrelated files change.
- **Test Coverage:** Focus on endpoint behavior and response structure.

## Challenges
- **Snyk setup:** Requires a `SNYK_TOKEN` GitHub secret. After adding the token, the scan runs successfully.
- **Docker Hub auth:** Requires `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets for pushing images.
