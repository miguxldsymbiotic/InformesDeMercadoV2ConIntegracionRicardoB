import sys
from pathlib import Path
import plotly.graph_objects as go
from report_engine import ReportEngine

def test_diag():
    print("Iniciando diagnóstico del motor de reportes...")
    app_dir = Path("c:/Users/migux/Downloads/nuevaPRUEBAinformeMERCADO/InformePDF/dashboard")
    engine = ReportEngine(app_dir)
    
    try:
        print("1. Probando exportación de gráfica (Kaleido/SVG)...")
        fig = go.Figure(data=[go.Bar(y=[2, 3, 1])])
        fig.update_layout(title="Prueba Diagnóstico")
        path = engine.export_plotly_fig(fig, "test_plot")
        print(f"   - ÉXITO: Gráfica exportada en {path}")
        
        print("2. Probando generación de contenido Typst...")
        data_ctx = {
            "title": "Informe Diagnóstico",
            "date": "13/04/2026",
            "institution": "Institución de Prueba",
            "program": "Programa de Prueba",
            "kpis_summary": [("KPI 1", "100"), ("KPI 2", "50%")],
            "sections": [
                {
                    "title": "Sección 1",
                    "intro": "Introducción de prueba",
                    "kpis": [("Sub KPI", "10")],
                    "plots": [path]
                }
            ],
            "max_anno_snies": 2024,
            "max_anno_ole": 2023,
            "max_anno_spadies": 2022
        }
        
        pdf_path = engine.generate_report(data_ctx)
        print(f"   - ÉXITO: PDF generado en {pdf_path}")
        
    except Exception as e:
        print(f"   - ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # engine.cleanup() # Comentar para ver los archivos temporales si falla
        pass

if __name__ == "__main__":
    test_diag()
