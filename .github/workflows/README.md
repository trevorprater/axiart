# GitHub Actions Workflows

This directory contains CI/CD workflows for automated testing and validation.

## Workflows

### 🚀 CI (`ci.yml`)

**Triggers:** Push to `main`, Pull Requests to `main`

**Purpose:** Fast feedback on code quality and basic functionality

**Jobs:**
1. **build-and-test**
   - Builds Rust library with maturin
   - Runs all example scripts (Voronoi, L-Systems, Truchet)
   - Verifies SVG output files are created
   - Runs quick benchmark tests

2. **lint**
   - Checks Rust code formatting (`cargo fmt`)
   - Runs Rust linter (`cargo clippy`)
   - Enforces code quality standards

**Runtime:** ~5-10 minutes

---

### 🌍 Cross-Platform Tests (`test-matrix.yml`)

**Triggers:** Pull Requests to `main`, Manual dispatch

**Purpose:** Comprehensive testing across platforms and Python versions

**Test Matrix:**
- **Operating Systems:** Ubuntu, macOS, Windows
- **Python Versions:** 3.9, 3.10, 3.11, 3.12
- **Strategy:** Reduced matrix (newer Python on all OS, older on Ubuntu)

**Tests:**
- Pattern imports (VoronoiPattern, LSystemPattern, TruchetPattern)
- Pattern generation with quick parameters
- SVG output verification (Ubuntu only)

**Runtime:** ~15-25 minutes (runs in parallel)

---

## Adding New Tests

### To add a new example test:

Edit `ci.yml` in the "Run example scripts" step:

```yaml
- name: Run example scripts
  run: |
    cd examples
    uv run python example_voronoi.py
    uv run python example_lsystem.py
    uv run python example_truchet.py
    uv run python example_your_new_pattern.py  # Add here
```

### To add a new benchmark:

Edit `ci.yml` in the "Run benchmarks" step:

```yaml
- name: Run benchmarks (quick version)
  run: |
    timeout 60 uv run python test_voronoi.py
    timeout 60 uv run python test_your_benchmark.py  # Add here
```

### To modify test matrix:

Edit `test-matrix.yml` matrix section:

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest]  # Modify OS list
    python-version: ['3.11', '3.12']   # Modify Python versions
```

---

## Workflow Status

Check workflow status:
- In GitHub PR: See "Checks" tab
- In GitHub repo: Go to "Actions" tab
- Badge: Add to README.md:

```markdown
[![CI](https://github.com/trevorprater/axiart/actions/workflows/ci.yml/badge.svg)](https://github.com/trevorprater/axiart/actions/workflows/ci.yml)
```

---

## Local Testing

Before pushing, test locally:

```bash
# Check Rust formatting
cargo fmt --manifest-path axiart-core/Cargo.toml --check

# Run clippy
cargo clippy --manifest-path axiart-core/Cargo.toml --all-targets

# Build library
uv run maturin develop --release

# Run examples
cd examples
uv run python example_voronoi.py
uv run python example_lsystem.py
uv run python example_truchet.py
```

---

## Troubleshooting

### Workflow fails on "Build Rust library"

- Check that `Cargo.toml` dependencies are correct
- Verify Rust code compiles locally
- Check for platform-specific issues (Windows paths, etc.)

### Workflow fails on "Run example scripts"

- Verify examples work locally
- Check that all imports are correct
- Ensure SVG output paths are correct

### Workflow times out

- Reduce benchmark iterations
- Adjust timeout values in workflow
- Consider splitting long tests into separate jobs
