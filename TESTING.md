# Testing

## Layers

### Layer 1 — Static analysis (always, free)

```bash
actionlint
yamllint .
```

Catches structural errors, invalid refs, type mismatches before running anything.

### Layer 2 — Composite action tests (local, via `act`)

Test workflows exercise individual composite actions using local path references.
These run fully inside the devcontainer with no GitHub dependency.

```bash
# Test smoke-test-uv action (artifact mode)
act workflow_dispatch -W .github/workflows/test-smoke-test-uv.yml

# Override Python version
act workflow_dispatch -W .github/workflows/test-smoke-test-uv.yml \
  --input python-version=3.13
```

**What this tests:**
- `uv build` produces a valid wheel and sdist from `tests/fixtures/sample-package`
- Both artifacts install cleanly in an isolated environment
- `pytest` passes from each artifact

### Layer 3 — Reusable workflow integration tests (GitHub only)

`test-release-python.yml` and `test-release-container.yml` call the reusable
workflows with all destructive flags off (`publish-pypi: false`, `push: false`).

These require `mockasort-studio/actions` to be public on GitHub, because the
reusable workflows reference composite actions by their full org/repo path.

Trigger from the GitHub Actions UI via **Run workflow**, or with the `gh` CLI:

```bash
gh workflow run test-release-python.yml
gh workflow run test-release-container.yml
```

**What this tests:**
- Full job graph wires correctly (build → smoke-test → publish jobs)
- All action references resolve
- No actual publishing occurs

## Secrets

Copy `.secrets.example` to `.secrets` (gitignored) and fill in your token:

```bash
cp .secrets.example .secrets
```

`act` picks up `.secrets` automatically. The `GITHUB_TOKEN` value only needs
read access for local runs since all publish steps are disabled.

## Event payloads

Fake event payloads for `act` live in `tests/fixtures/events/`.

```bash
# Simulate a tag push
act push -W .github/workflows/test-release-python.yml \
  -e tests/fixtures/events/push-tag.json
```

## What cannot be tested locally

| Feature | Reason | Workaround |
|---|---|---|
| PyPI OIDC publish | Requires GitHub's OIDC token | `publish-pypi: false` |
| GHCR push | Requires registry auth | `push: false` |
| GitHub Release creation | Requires real tag + `contents: write` | `publish-github-release: false` |
| `actions-gh-pages` deploy | Requires real git remote | Skipped in dry-run |
