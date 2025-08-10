# Guidelines for LLM Contributors

## Context
- This repository explores how OpenAI's Codex and related models can analyse declarations from the *Haute Autorité pour la transparence de la vie publique* (HATVP), the French authority that enforces financial transparency for public officials.
- The goal is to extract structured data from XML declarations, analyze stock holdings and personal information, and produce transparency reports.

## Working Practices
1. **Search**: Use `rg` for code or text searches; avoid recursive `ls` or `grep` commands.
2. **Style**: Write Python 3 code following PEP 8. Prefer descriptive variable names and add docstrings for new functions.
3. **Testing**: Run `pytest` after any code change and ensure all tests pass. Add new tests when introducing features.
4. **Data handling**:
   - Treat personal information ethically; do not commit sensitive data.
   - Generated artifacts like CSVs under `pii/`, `stock_analysis/output/`, or figures in `report_assets/` should remain uncommitted.
5. **Documentation**: Update `README.md` or files in `documentation/` when changing data schemas or adding significant functionality.
6. **Commits**: Use present-tense, descriptive commit messages and keep the working tree clean.
7. **Environment**: If dependencies are missing, install them with `pip` and document the requirement.
8. **Pull Requests**: Provide a concise summary of changes and reference relevant tests or scripts used for verification.

## Tips
- Review existing scripts in `stock_analysis/`, `pii/`, and `avis/` to understand data pipelines.
- Large XML files live in `split_declarations/` and should not be modified unless necessary.
- For entity recognition work, see `avis/NER/readme_ner.md` for current progress.

## Further Context on HATVP
The HATVP collects and publishes asset and interest declarations from elected officials and senior civil servants to prevent conflicts of interest and promote public trust. Analyses in this repository aim to make these disclosures more accessible and to highlight potential risk areas.
