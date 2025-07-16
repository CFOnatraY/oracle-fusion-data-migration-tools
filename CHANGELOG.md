# Changelog

All notable changes to this project will be documented in this file.

## [v1.0.0] - 2025-07-14

### Added
- Created full structure for `oracle-fusion-data-migration-tools` repository
- Added individual `README.md` files for each tool
- Added central `README.md` at project root
- Configured `.gitignore` to exclude environment files and system-specific artifacts
- Integrated support for `.env` files to manage sensitive credentials
- Added placeholder and batch processing scripts to `tools/` folders

### Changed
- Refactored multiple Python scripts to use environment variables instead of hardcoded values
- Restructured `utils/` and `oracle-fusion-data-migration-tools/` into separate repositories
- Migrated stable scripts from backup repo to final structure
- Renamed branches and folders for consistency

### Removed
- Removed unused or legacy test scripts
- Removed previous local-only backup files

---

This changelog format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).