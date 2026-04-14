# Stable Image Generation via PlotlyScope

I have identified that the standard `fig.write_image` command is hanging on your computer. This usually happens when the higher-level Plotly functions lose communication with the Kaleido subprocess on Windows.

To fix this, I will refactor the rendering engines to use **`PlotlyScope`**. This is a more robust, lower-level approach that keeps a single stable connection to the renderer, which is the recommended solution for persistent hangs on Windows environments.

## Proposed Changes

### 1. Refactor Report Engines
- **[MODIFY] [report_engine.py](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/report_engine.py)**
- **[MODIFY] [report_comparada_engine.py](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/report_comparada_engine.py)**
    - Add a `self.scope = PlotlyScope()` in the `__init__` or `__enter__` method.
    - Change the image export logic to use `self.scope.transform(fig, format='svg')`.
    - This bypasses the erratic standard `write_image` logic and uses a dedicated, stable rendering channel.

## Verification Plan

### Automated Tests
1. Created a simplified test script `test_scope.py` to verify that `PlotlyScope` can save an image successfully before applying it to the main code.

### Manual Verification
1. I will ask you to restart the dashboard and try generating a PDF.
2. We will monitor the console for any "Success" or "Error" messages I will add for logging.
