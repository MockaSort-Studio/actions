# Assignment — Current Work Queue

## Status Legend
- [ ] pending
- [~] in progress
- [x] done

---

## Phase 0 — Environment Setup
- [~] Create CLAUDE.md, MEMORY.md, ASSIGNMENT.md
- [ ] Set up devcontainer with all required tools
- [ ] Add yamllint, shellcheck, actionlint, markdownlint configs
- [ ] Add ruff config (pyproject.toml or ruff.toml)
- [ ] Add .python-version file

## Phase 1 — Core Reusable Actions
- [ ] `build-bazel` — composite action for Bazel build + test
- [ ] `build-uv` — composite action for uv Python build + test
- [ ] `release-python` — reusable workflow for PyPI release
- [ ] `release-docs` — reusable workflow for MkDocs deploy to GitHub Pages
- [ ] `pr-comment-trigger` — action activated via PR comment using gh CLI

## Phase 2 — Quality Checks
- [ ] `lint-check` — linting action (shellcheck, ruff, yamllint, actionlint)
- [ ] `format-check` — formatting action (shfmt, ruff format)
- [ ] `loc-check` — lines-of-code counter with threshold enforcement

## Phase 3 — Deployment
- [ ] `deploy-site` — site deployment (target TBD)
- [ ] `deploy-backend-aws` — AWS backend deployment
- [ ] Additional deploy methods TBD

---

## Notes
- Start with devcontainer so all local testing and linting works first
- `act` must be able to run workflows inside the container
- All actions should be tested locally with act before merging
