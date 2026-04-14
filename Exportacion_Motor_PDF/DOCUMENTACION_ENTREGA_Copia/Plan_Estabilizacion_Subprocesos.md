# [Goal Description]

Integrate the new premium Typst template from the `PLANTILLAa` folder into the existing report generation engines (`ReportEngine` and `ComparadaReportEngine`) while maintaining the current system architecture. Before starting the integration, perform a Git push to a repository to backup the current state as requested by the user.

## User Review Required

> [!IMPORTANT]
> **Git Repository Clarification**: The current project folder is not a Git repository. To perform a "push", I need to either:
> 1. Initialize a new local repository and provide a remote URL.
> 2. Add these files to the existing repository detected at `C:\Users\migux`.
> Please provide the **GitHub/GitLab repository URL** where you'd like the code to be pushed.

> [!IMPORTANT]
> **Architectural Continuity**: The integration will preserve the current Python engines' logic and data flow, simply upgrading the Typst component mapping and visual style.

> [!CAUTION]
> Ensure all required fonts (specifically "Inter") are available on the system where PDF generation occurs, or the system will fallback to sans-serif defaults.

## Proposed Changes

### Phase 0: Git Backup
- Initialize a local Git repository in the project folder (if requested as a separate repo).
- Stage and commit all current files.
- Push to the remote URL provided by the user.

### Phase 1: Template System Updates

#### [MODIFY] [template.typ](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/PLANTILLAa/template.typ)
- Fix minor syntax errors (unclosed delimiters) if any (thorough review of brackets and parentheses).
- Add `kpi-duo` component to support side-by-side comparison (needed for `ComparadaReportEngine`).
- Add `method-box` or specialized `insight-box` variants if necessary.
- Ensure the `project` function correctly handles all metadata (Institution, Program, SNR, Date).

#### [MODIFY] [report_template.typ](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/report_template.typ)
- Replace content with a lightweight wrapper that imports and sets up the new `template.typ`.
- Keep the file as a bridge for the `ReportEngine`.

#### [MODIFY] [report_comparada_template.typ](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/report_comparada_template.typ)
- Replace content with a wrapper around the new `template.typ`.
- Implement `comparada_template` using the new design system components.

---

### Python Report Engines

#### [MODIFY] [report_engine.py](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/report_engine.py)
- Update `generate_report` to:
    - Call `#show: project.with(...)` instead of `template.with(...)`.
    - Wrap sections in `#section-page(...)`.
    - Use `kpi-card` and `kpi-row` for KPIs.
    - Use `insight-box` for methodological/technical notes.
    - Use `chart-wrap` for plotly exports.

#### [MODIFY] [report_comparada_engine.py](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/report_comparada_engine.py)
- Extensive refactoring of `generate_report` to match the new component hierarchy.
- Map `kpi_duo` to the new `kpi-duo` (to be added to `template.typ`).
- Ensure all comparative charts are wrapped in `chart-wrap` or similar dynamic grids.

## Open Questions

- Should I preserve the old templates as backups, or is it okay to overwrite them directly?
- Are there specific institution logos that need to be dynamically swapped, or should I stick to the `logo_symbiotic.svg` default?

## Verification Plan

### Automated Tests
- I will run the Python engines using a test script (or `generate_dummy.py` if available) to ensure `typst.compile` succeeds with the new syntax.
- I will check for any "unclosed delimiter" errors during the compilation phase.

### Manual Verification
- Review the generated PDF (informe.pdf) to ensure the layout matches the "premium" design.
- Verify that metadata (Institution, Program) appears correctly on the cover page.
