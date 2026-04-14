import sys
from pathlib import Path
import plotly.graph_objects as go
import polars as pl
from report_engine import ReportEngine
import datetime
import shutil

def test_full_report_repaired():
    print(">>> Iniciando prueba de REPORTE FINAL (Motor Reparado)...")
    app_dir = Path("c:/Users/migux/Downloads/nuevaPRUEBAinformeMERCADO/InformePDF/dashboard")
    
    # Simular datos para un reporte real
    data_ctx = {
        "title": "Informe de Mercado - UNIMINUTO (Reparación Exitosa)",
        "date": datetime.datetime.now().strftime("%d/%m/%Y"),
        "institution": "CORPORACION UNIVERSITARIA MINUTO DE DIOS - UNIMINUTO",
        "program": "ADMINISTRACION DE EMPRESAS",
        "max_anno_snies": 2024,
        "max_anno_ole": 2023,
        "max_anno_spadies": 2022,
        "kpis_summary": [
            ("Programas Activos", "2.450"),
            ("Matrícula Total", "1.2M"),
            ("Tasa Empleabilidad", "82%"),
            ("Salario Promedio", "$2.8M")
        ],
        "sections": [
            {
                "title": "Tendencias de Matrícula",
                "intro": "Análisis de la evolución histórica de estudiantes de primer curso y matriculados.",
                "kpis": [("Crecimiento", "+5.2%"), ("Retención", "88%")],
                "plots": []
            },
            {
                "title": "Análisis de Empleabilidad",
                "intro": "Seguimiento laboral a graduados según datos del OLE.",
                "kpis": [("Vinculación", "78%"), ("Salarios", "$2.4M")],
                "plots": []
            }
        ]
    }

    with ReportEngine(app_dir) as engine:
        try:
            print("1. Generando gráficas reales...")
            # Gráfica 1
            fig1 = go.Figure(data=[go.Scatter(x=[2020, 2021, 2022, 2023, 2024], y=[100, 120, 115, 140, 155], mode='lines+markers', line=dict(color='#2563EB'))])
            fig1.update_layout(title="Evolución de Matrícula", margin=dict(l=40, r=40, t=40, b=40))
            
            # Gráfica 2
            fig2 = go.Figure(data=[go.Bar(x=["Públicas", "Privadas"], y=[75, 85], marker_color=['#1E3A5F', '#2563EB'])])
            fig2.update_layout(title="Empleabilidad por Sector", margin=dict(l=40, r=40, t=40, b=40))
            
            # Exportar (Debería funcionar en <1s ahora)
            path1 = engine.export_plotly_fig(fig1, "matricula_trend")
            path2 = engine.export_plotly_fig(fig2, "empleo_sector")
            
            data_ctx["sections"][0]["plots"] = [path1]
            data_ctx["sections"][1]["plots"] = [path2]
            
            print("2. Construyendo PDF con Typst...")
            pdf_path = engine.generate_report(data_ctx)
            
            output_dest = app_dir / "informe_reparado_final.pdf"
            shutil.copy2(pdf_path, output_dest)
            
            print(f"\n>>> ¡EXITO TOTAL!")
            print(f">>> Informe con gráficas generado en: {output_dest}")
            print(f">>> Tamaño del archivo: {Path(output_dest).stat().st_size} bytes")
            
        except Exception as e:
            print(f"\n>>> ERROR DURANTE LA PRUEBA REPARADA: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_full_report_repaired()
