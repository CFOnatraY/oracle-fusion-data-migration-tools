# Changelog

All notable changes to this project will be documented in this file.

## [v1.1.0] - 2025-07-16

### Added
- Added working Selenium scripts for automating Pricing Strategies, Price Lists, and Discount Lists in Oracle Fusion (`tools/price_list_tool/`)
- Created localized `README.md` for the `price_list_tool` with setup and execution guidance
- Implemented `.pre-commit-config.yaml` and `.hooks/check_obfuscated_terms.sh` to enforce zero-trace policy using obfuscated terms
- Updated main `README.md` with new sections: Environment Recommendations and Internal Trace Prevention

### Changed
- Enhanced tool description in the Tools Overview table for `price_list_tool`
- Updated `requirements.txt` to include `webdriver-manager` dependency

---

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