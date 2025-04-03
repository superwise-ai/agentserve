# GitHub Actions Workflows

This directory contains the GitHub Actions workflows for the project.

## Available Workflows

### Continuous Integration (`ci.yml`)
- Runs on every push and pull request
- Tests the package with pytest
- Checks code coverage and uploads to Codecov
- Runs code quality checks:
  - Black (code formatting)
  - isort (import sorting)
  - flake8 (linting)

### Release Pipeline (`release.yml`)
- Triggers on version tag pushes (e.g., v1.0.0)
- Builds the package
- Publishes to PyPI

### Documentation Pipeline (`docs.yml`)
- Builds documentation using MkDocs
- Deploys to GitHub Pages on main branch

## Required Secrets

The following secrets need to be set in your GitHub repository:

- `PYPI_API_TOKEN`: Your PyPI API token for package publishing
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

## Release Process

1. Update version in `pyproject.toml`
2. Create and push a new tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. The release pipeline will automatically:
   - Build the package
   - Run all tests
   - Publish to PyPI 