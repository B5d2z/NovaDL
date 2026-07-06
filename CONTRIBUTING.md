# Contributing to NovaDL

Thank you for considering contributing to NovaDL! We welcome contributions of all kinds.

## Code of Conduct

By participating, you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Report a Bug

Open an issue using the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) template.

### Suggest a Feature

Open an issue using the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template.

### Submit a Pull Request

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Install dependencies: `poetry install`
4. Make your changes
5. Run linting: `poetry run ruff check src/`
6. Run formatting: `poetry run black src/ tests/`
7. Run type checking: `poetry run mypy src/`
8. Run tests: `poetry run pytest`
9. Commit your changes: `git commit -m "feat: add my feature"`
10. Push: `git push origin feature/my-feature`
11. Open a Pull Request using the [template](.github/PULL_REQUEST_TEMPLATE.md)

## Development Setup

```bash
git clone https://github.com/Badr1Alanzi/novadl.git
cd novadl
poetry install
poetry run novadl --help
```

## Project Structure

```
src/novadl/
├── cli/              # Typer CLI commands and interface
├── core/             # Domain logic (entities, use cases, interfaces)
│   ├── entities/     # Data models
│   ├── use_cases/    # Business logic
│   └── interfaces/   # Abstract interfaces
├── infrastructure/   # External integrations
│   ├── downloader/   # yt-dlp integration
│   ├── config/       # Configuration management
│   ├── history/      # Download history
│   └── system/       # System utilities
├── presentation/     # Rich terminal output
└── utils/            # Shared utilities
```

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation
- `refactor:` — Code refactoring
- `test:` — Tests
- `chore:` — Maintenance
