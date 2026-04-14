# Plan: Fixing PDF Generation with Premium Template

The user switched to a premium Typst template, but the Python engines (`ReportEngine` and `ComparadaReportEngine`) are still trying to use macro names or components that don't exist in the new template, leading to compilation failures.

## User Review Required

> [!IMPORTANT]
> The goal is to **preserve all existing content and sections** from the original reports while applying the new "Premium" aesthetic. I will ensure that no data is lost during the migration.

## Proposed Changes

### [Typst Template]

#### [MODIFY] [premium_template.typ](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/premium_template.typ)
- Add alias or implementations for missing macros used by the engines:
    - `chart_grid_2` (alias or new implementation using premium style)
    - `chart_block`
    - `tech_note`
    - `method_note`
- Ensure all components are compatible with the data structures passed from Python.

### [Report Engines]

#### [MODIFY] [report_comparada_engine.py](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/report_comparada_engine.py)
- Update macro calls to match `premium_template.typ` (e.g., `kpi_row` -> `kpi-row`).
- Fix structure to use `section-page` and other premium blocks consistently.
- Remove hardcoded styles that clash with the template.

#### [MODIFY] [report_engine.py](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/report_engine.py)
- Minor cleanup to ensure full compatibility.
- Use `styled-table` where appropriate.

## Open Questions

- No open questions at this time. The focus is on fix-and-polish.

## Verification Plan

### Automated Tests
- Create a script that simulates a full report generation (both standard and comparada) using dummy data.
- Verify that `typst.compile` succeeds for both.

### Manual Verification
- Ask the user to try generating a report from the UI to confirm it works in their environment.
