FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG SHFMT_VERSION=v3.10.0
ARG ACTIONLINT_VERSION=1.7.7
ARG ACT_VERSION=0.2.74
ARG BAZELISK_VERSION=v1.25.0

# System packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    shellcheck \
    yamllint \
    curl \
    wget \
    unzip \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
      | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
      | tee /etc/apt/sources.list.d/github-cli.list \
    && apt-get update && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# Node.js + markdownlint (Claude Code extension runs in VS Code, not the container)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g markdownlint-cli2 \
    && rm -rf /var/lib/apt/lists/*

# uv (Python toolchain manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh

# ruff
RUN curl -LsSf https://astral.sh/ruff/install.sh | env RUFF_INSTALL_DIR=/usr/local/bin sh

# shfmt
RUN ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/') \
    && curl -fsSL "https://github.com/mvdan/sh/releases/download/${SHFMT_VERSION}/shfmt_${SHFMT_VERSION}_linux_${ARCH}" \
      -o /usr/local/bin/shfmt \
    && chmod +x /usr/local/bin/shfmt

# actionlint
RUN ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/') \
    && curl -fsSL "https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_linux_${ARCH}.tar.gz" \
      | tar -xz -C /usr/local/bin actionlint \
    && chmod +x /usr/local/bin/actionlint

# act (run GitHub Actions locally)
RUN curl -fsSL https://raw.githubusercontent.com/nektos/act/master/install.sh \
      | bash -s -- -b /usr/local/bin v${ACT_VERSION}

# bazelisk (Bazel version manager — aliased as bazel)
RUN ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/') \
    && curl -fsSL "https://github.com/bazelbuild/bazelisk/releases/download/${BAZELISK_VERSION}/bazelisk-linux-${ARCH}" \
      -o /usr/local/bin/bazelisk \
    && chmod +x /usr/local/bin/bazelisk \
    && ln -sf /usr/local/bin/bazelisk /usr/local/bin/bazel

# mkdocs + material theme
RUN UV_TOOL_BIN_DIR=/usr/local/bin uv tool install mkdocs --with mkdocs-material

# Sanity check — fail the build if anything is missing
RUN shellcheck --version \
    && shfmt --version \
    && yamllint --version \
    && actionlint --version \
    && ruff --version \
    && uv --version \
    && bazelisk version \
    && act --version \
    && gh --version \
    && mkdocs --version \
    && markdownlint-cli2 --version
