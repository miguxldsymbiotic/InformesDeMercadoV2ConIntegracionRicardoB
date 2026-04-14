import pandas as pd
import polars as pl
import plotly.graph_objects as go
import plotly.express as px
import datetime

# Constantes visuales exportadas de la abstracción
COLOR_SEXO = {'FEMENINO': '#674f95', 'MASCULINO': '#31497e', 'NO BINARIO': '#00B4D8'}

class ReportDataFetcher:
    """
    Clase abstracta e independiente encargada de procesar DataFrames, generar visualizaciones
    y consolidar los datos que serán inyectados al ReportEngine de Typst.
    Esta clase desliga la generación del PDF de la interfaz web Reactiva (Shiny/Dash).
    """
    
    def __init__(self, df_snies, df_pcurso, df_matricula, df_graduados, df_ole, df_desercion, df_saber):
        self.df_snies = df_snies
        self.df_pcurso = df_pcurso
        self.df_matricula = df_matricula
        self.df_graduados = df_graduados
        self.df_ole = df_ole
        self.df_desercion = df_desercion
        self.df_saber = df_saber

    # -- UTILS --
    def format_num_es(self, val, decimals=0):
        if pd.isna(val) or val is None: return "Sin dato"
        formatter = f"{{:,.{decimals}f}}"
        return formatter.format(val).replace(",", "X").replace(".", ",").replace("X", ".")

    def format_pct_es(self, val, decimals=1):
        if pd.isna(val) or val is None: return "Sin dato"
        formatter = f"{{:,.{decimals}%}}"
        return formatter.format(val).replace(",", "X").replace(".", ",").replace("X", ".")

    # -- EJEMPLOS DE EXTRACCIÓN Y CÁLCULO DE GRÁFICAS (CAPA LOGICA Aislada) --
    
    def calc_plot_primer_curso_total(self, divipolas):
        if len(divipolas) == 0: return go.Figure()
        
        # Filtro y agregación en Polars
        df_filtered = self.df_pcurso.filter(
            pl.col("snies_divipola").is_in(divipolas) & (pl.col("anno") >= 2016)
        ).group_by("anno").agg(pl.col("primer_curso_sum").sum()).sort("anno")
        
        if len(df_filtered) == 0: return go.Figure()
        
        fig = px.line(df_filtered.to_pandas(), x="anno", y="primer_curso_sum", markers=True)
        fig.update_traces(marker=dict(size=9, color="white", line=dict(width=1.5, color="#31497e")), line=dict(width=2, color="#31497e"))
        fig.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', separators=",.",
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(title="Año", tickmode="linear"),
            yaxis=dict(title="Primer Curso")
        )
        return fig
        
    def calc_plot_primer_curso_sexo(self, divipolas):
        if len(divipolas) == 0: return go.Figure()
        
        df_filtered = self.df_pcurso.filter(
            pl.col("snies_divipola").is_in(divipolas) & (pl.col("anno") >= 2016)
        ).group_by(["anno", "sexo"]).agg(pl.col("primer_curso_sum").sum()).sort(["sexo", "anno"])
        
        if len(df_filtered) == 0: return go.Figure()
        
        fig = px.line(df_filtered.to_pandas(), x="anno", y="primer_curso_sum", color="sexo", color_discrete_map=COLOR_SEXO, markers=True)
        fig.update_traces(marker=dict(size=9), line=dict(width=2))
        return fig

    def calc_table_graduados(self, divipolas):
        # Transforma el Polars Dataframe a algo que será leído por typst macro table()
        df_filtered = self.df_graduados.filter(
            pl.col("snies_divipola").is_in(divipolas)
        ).group_by("anno").agg(pl.col("graduados_sum").sum()).sort("anno")
        return df_filtered.to_pandas()

    def calc_kpi_empleabilidad(self, divipolas, max_anno):
        # Lógica cruda para el KPI
        df_filtered = self.df_ole.filter(
            pl.col("snies_divipola").is_in(divipolas) & (pl.col("anno") == max_anno)
        )
        if len(df_filtered) == 0: return "0%"
        mean_val = df_filtered["graduados_que_cotizan"].mean() / 100.0 # dummy asumption
        return self.format_pct_es(mean_val)

    # ... Aquí irían todos los más de 50 cálculos calc_* transcritos desde app.py sin dependencias Shiny ...

    # -- ORQUESTADOR PRINCIPAL --
    def prepare_report_content(self, engine, divipolas, meta_config):
        """
        Ejecuta todas las consultas parametrizadas, guarda las imágenes vía `engine`
        y ensambla el `data_ctx` maestro asincrónico independiente.
        
        :param engine: Instancia de ReportEngine.
        :param divipolas: Lista de identificadores de territorios e instituciones a filtrar.
        :param meta_config: Diccionario con variables maestras (ej., max_anno_snies).
        """
        print("[Log] Ensamblando métricas maestras...")
        
        # 1. Preparar Datos Generales y Ejecutar Consultas
        data_ctx = {
            "max_anno_snies": meta_config.get("max_anno_snies"),
            "max_anno_ole": meta_config.get("max_anno_ole"),
            "max_anno_spadies": meta_config.get("max_anno_desercion"),
            "date": datetime.datetime.now().strftime("%d/%m/%Y"),
            "kpis_summary": [
                ("Instituciones", "45 (MOCK)"),
                ("Programas", "120 (MOCK)"),
                ("Tasa Empleabilidad", self.calc_kpi_empleabilidad(divipolas, meta_config.get("max_anno_ole")))
            ],
            "sections": []
        }
        
        # SECCIÓN 1: TENDENCIAS SNIES
        snies_plots = []
        try:
            snies_plots.append(engine.export_plotly_fig(self.calc_plot_primer_curso_total(divipolas), "pcurso_total"))
            snies_plots.append(engine.export_plotly_fig(self.calc_plot_primer_curso_sexo(divipolas), "pcurso_sexo"))
            # Sucesivamente para todas las gráficas analíticas...
        except Exception as e:
            print(f"[Warn] Error generando gráfico de primer curso: {e}")

        data_ctx["sections"].append({
            "title": "Tendencias SNIES (Oferta y Demanda)",
            "intro": "Esta sección analiza la evolución de la matrícula, los estudiantes de primer curso y los graduados.",
            "kpis": [
                ("Primer Curso", "8,500 (MOCK)"),
                ("Graduados", "2,300 (MOCK)")
            ],
            "plots": snies_plots,
            "table": f'''
#v(1em)
== Detalle de Graduados Consolidados
{engine.format_as_typst_table(pl.from_pandas(self.calc_table_graduados(divipolas)))}
            '''
        })
        
        # Más secciones... (OLE, SPADIES, Saber PRO)
        
        return data_ctx
