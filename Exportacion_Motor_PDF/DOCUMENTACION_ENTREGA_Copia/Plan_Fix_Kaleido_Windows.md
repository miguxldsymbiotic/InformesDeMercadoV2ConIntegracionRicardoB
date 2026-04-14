# Fix Kaleido Subprocess Error on Windows

I have diagnosed the `RuntimeError: Couldn't close or kill browser subprocess` you are encountering. This commonly happens on Windows when multiple headless browser instances (used by Kaleido to render charts) are launched simultaneously in different threads, causing them to lock each other out or fail to shut down properly.

## Proposed Changes

To resolve this and ensure stable PDF generation, I will implement a more robust export mechanism for Windows environments.

### 1. Dependency Correction
- **[MODIFY] [requirements.txt](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/requirements.txt)**
    - Pin `kaleido==0.2.1`. This is the stable version of the Plotly engine. The current `1.2.0` version in your environment seems to be a different package that is not fully compatible with Plotly's export engine on Windows.

### 2. Engine Parallelism Adjustment
- **[MODIFY] [report_engine.py](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/report_engine.py)**
- **[MODIFY] [report_comparada_engine.py](file:///c:/Users/migux/Downloads/INFORMES_MERCADO_VERSION2.0RICKY/InformePDF/dashboard/report_comparada_engine.py)**
    - Implement a safe `max_workers=1` (sequential mode) for Windows. While slower than the parallel mode used in Linux, it prevents the subprocess lockups you are seeing.
    - I will add a check using `os.name == 'nt'` to automatically use sequential mode on Windows while keeping parallel mode available for Linux/Cloud deployments.

## Verification Plan

### Automated Tests
1. Run the `diag_kaleido.py` script again after the fix to ensure sequential export works without errors.
2. Run a full PDF generation test from the Dashboard.

### Manual Verification
1. I will ask you to try generating a PDF again from the local application.
