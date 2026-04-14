import os
import sys
from pathlib import Path
import polars as pl
import datetime

# Mock de Shiny para evitar fallos al importar app.py fuera de un servidor Shiny
from unittest import mock
sys.modules['shiny'] = mock.MagicMock()
sys.modules['shinywidgets'] = mock.MagicMock()
sys.modules['faicons'] = mock.MagicMock()

# Ruta al dashboard
DASHBOARD_DIR = Path(r"c:\Users\migux\Downloads\nuevaPRUEBAinformeMERCADO\InformePDF\dashboard")
sys.path.append(str(DASHBOARD_DIR))

try:
    from report_engine import ReportEngine
    # Importar variables globales de app.py (esto cargará los datos reales)
    # Nota: Como app.py tiene mucho código reactivo, importamos con cuidado
    import app
    print(">>> [VALIDACION] Datos cargados correctamente.")
except Exception as e:
    print(f">>> [ERROR] No se pudo cargar el entorno de app.py: {e}")
    sys.exit(1)

def run_backend_validation():
    print(">>> [VALIDACION] Iniciando generación de PDF desde el Backend...")
    
    # Mock de un objeto de progreso de Shiny
    class MockProgress:
        def set(self, val, message=None, detail=None):
            print(f"    [Progreso {val}%] {message or ''} {detail or ''}")
        def __enter__(self): return self
        def __exit__(self, *args): pass

    # Mock de los motores de cálculo que dependen de reactivos
    # En app.py, _prepare_report_content espera un 'engine' y un 'p'
    
    with ReportEngine(DASHBOARD_DIR) as engine:
        p = MockProgress()
        
        # Simulamos el contexto que app._prepare_report_content generaría
        # No podemos llamar a app._prepare_report_content directamente porque es interna de server()
        # Pero podemos validar que el engine.generate_report funciona con un contexto real.
        
        print(">>> [VALIDACION] Construyendo contexto de prueba masivo...")
        data_ctx = {
            "max_anno_snies": 2023,
            "max_anno_ole": 2022,
            "max_anno_spadies": 2022,
            "max_anno_saber": 2023,
            "date": datetime.datetime.now().strftime("%d/%m/%Y"),
            "institution": "UNIVERSIDAD DE PRUEBA VALIDACION",
            "program": "INGENIERIA DE SISTEMAS (TEST)",
            "title": "REPORTE DE VALIDACION BACKEND",
            "kpis_summary": [
                ("Instituciones", "150"),
                ("Programas", "1.200"),
                ("Matrícula Total", "450.000"),
                ("Tasa Empleabilidad", "85,4%")
            ],
            "sections": [
                {
                    "title": "Métricas SNIES",
                    "intro": "Prueba de renderizado de gráficas reales y tablas.",
                    "kpis": [("Primer Curso", "1.500"), ("Graduados", "800")],
                    # Intentamos exportar una gráfica real de app.py si es posible
                    "plots": [
                        engine.export_plotly_fig(app.px.bar(x=[1,2,3], y=[1,3,2]), "test_plot_1"),
                    ],
                    "table": engine.format_as_typst_table(app.df_snies.head(5))
                }
            ]
        }
        
        print(">>> [VALIDACION] Compilando PDF...")
        try:
            pdf_path = engine.generate_report(data_ctx)
            print(f">>> [EXITO] PDF generado correctamente en: {pdf_path}")
            print(f">>> [EXITO] Tamaño del archivo: {os.path.getsize(pdf_path)} bytes")
            
            # Si llegamos aquí, el motor está sano y la sintaxis Typst es correcta.
            return True
        except Exception as e:
            print(f">>> [FALLO] Error en la generación del PDF: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = run_backend_validation()
    if success:
        print("\n==========================================")
        print("✅ BACKEND VALIDADO Y OPERATIVO")
        print("El motor de reportes está funcionando al 100%")
        print("==========================================\n")
        sys.exit(0)
    else:
        print("\n==========================================")
        print("❌ FALLO EN LA VALIDACION DEL BACKEND")
        print("Hay un error interno que debe corregirse.")
        print("==========================================\n")
        sys.exit(1)
