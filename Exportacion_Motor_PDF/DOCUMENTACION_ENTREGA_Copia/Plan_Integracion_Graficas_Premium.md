# Fixing Market Report Generation Incompleteness

The user reported that the reports generated with the premium template are incomplete and missing graphics. Investigation revealed that the test script being used (`test_snies_2051.py`) explicitly passes an empty `plots` dictionary, and the `ComparadaReportEngine` is missing the "Graduados" plot implementation in the "Tendencias de Matrícula" section.

## Proposed Changes

### [Component] Report Engine (`InformePDF/dashboard/report_comparada_engine.py`)

- **[MODIFY]** [report_comparada_engine.py](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/report_comparada_engine.py)
    - Add the missing `comp_graduados` plot in Section 2 (Tendencias de Matrícula).
    - Ensure consistent use of Typst function names (favoring hyphenated versions like `kpi-row` and `kpi-duo` to match the template's primary definitions).
    - Review and refine spacing (`v(10pt)`) for better visual alignment.

### [Component] Test Suite (`InformePDF/dashboard/test_snies_2051.py`)

- **[MODIFY]** [test_snies_2051.py](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/test_snies_2051.py)
    - Implement dummy chart generation using Plotly to test the full graphics pipeline.
    - Use `engine.export_figs_parallel` to generate SVG assets before calling `generate_report`.
    - Populate the `plots` dictionary in the data context with the generated SVG paths.

## Verification Plan

### Automated Tests
- Run the modified test script:
  ```bash
  python test_snies_2051.py
  ```
- Verify that the command completes without errors.
- Confirm that the output folder `C:\Users\migux\Downloads\pruebaspdfs` contains a PDF with content in all expected sections.

### Manual Verification
- Inspect the generated PDF to ensure:
    - Cover page displays correct program info.
    - All 8 sections mentioned in the index are present.
    - Charts for Matrícula, Costos, OLE, etc., are visible.
    - KPIs are populated correctly.
