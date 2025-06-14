# Changelog

All notable changes to the PyCppSQLJS project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial setup for documentation files (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`, `SPEC.md`).
- Basic PyCppSQLJS interpreter with support for variables, expressions, and functions.
- Windows file association for `.pcsj` files.
- Initial advanced features simulation (classes, async/await, SQL-like queries, error handling, lambdas, template literals, native interop).

### Changed

- Renamed `run_pcsj.py` to `pcsj_interpreter.py`.

### Fixed

- Addressed `SyntaxError` in `pcsj_interpreter.py` due to extraneous tool communication tags (manual fix required). 