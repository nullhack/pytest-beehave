# Changelog

All notable changes to pytest-beehave will be documented in this file.

## [v0.1.20260421] — Initial Beta — 2026-04-21

### Added
- Initial beta release of pytest-beehave
- pytest plugin that runs acceptance criteria stub generation as part of the pytest lifecycle
- Auto-ID assignment and generic step docstrings
- `stub_format` config key under `[tool.beehave]` — controls output format of generated test stubs (`"functions"` or `"classes"`)
- `pytest --beehave-hatch` generates bee-themed feature files
- Terminal steps display and HTML acceptance criteria column
- Deprecated marker sync for `Example:` blocks

> **Note**: This is a beta release. The project is undergoing extensive rebuild. APIs and behaviour may change without notice.
