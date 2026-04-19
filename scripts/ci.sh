#!/usr/bin/env bash
set -euo pipefail

echo "This is a template CI script."
echo "Replace scripts/ci.sh with the real commands for your repository."
echo

if [[ -f package.json ]]; then
  echo "Detected package.json. Example commands:"
  echo "  npm ci && npm run lint && npm test && npm run build"
  exit 0
fi

if [[ -f pyproject.toml ]]; then
  echo "Detected pyproject.toml. Example commands:"
  echo "  uv sync --frozen && pytest"
  echo "  # or your project-specific equivalent"
  exit 0
fi

if [[ -f Cargo.toml ]]; then
  echo "Detected Cargo.toml. Example commands:"
  echo "  cargo fmt --check && cargo test"
  exit 0
fi

if [[ -f go.mod ]]; then
  echo "Detected go.mod. Example commands:"
  echo "  go test ./..."
  exit 0
fi

if [[ -f pom.xml || -f build.gradle || -f build.gradle.kts ]]; then
  echo "Detected Java or Gradle build files. Example commands:"
  echo "  ./gradlew test"
  exit 0
fi

echo "No known build system detected. Replace this script before requiring the CI check."
