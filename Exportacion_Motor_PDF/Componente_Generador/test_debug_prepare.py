import sys
import os
from pathlib import Path
import polars as pl
import datetime
from unittest import mock

sys.modules['shiny'] = mock.MagicMock()
sys.modules['shinywidgets'] = mock.MagicMock()
sys.modules['faicons'] = mock.MagicMock()

DASHBOARD_DIR = Path(r"c:\Users\migux\Downloads\nuevaPRUEBAinformeMERCADO\InformePDF\dashboard")
sys.path.append(str(DASHBOARD_DIR))

# Intercept and mock shiny reactive decorators before app imports
import shiny
shiny.reactive = mock.MagicMock()
shiny.reactive.calc = lambda f: f
shiny.reactive.effect = lambda f: f
shiny.reactive.event = lambda *args: lambda f: f
shiny.render = mock.MagicMock()
shiny.render.ui = lambda f: f
shiny.render.data_frame = lambda f: f
shiny.render.download = lambda **kwargs: lambda f: f
shiny.ui = mock.MagicMock()

import app
from report_engine import ReportEngine

class MockProgress:
    def set(self, val, message=None, detail=None):
        pass

def test_prepare_directly():
    
    # We must replicate the context that Shiny uses inside `server`
    with ReportEngine(DASHBOARD_DIR) as engine:
        p = MockProgress()
        
        # Override app functions to not depend on UI State (inputs)
        # We simulate the UI selection having all default values
        
        # We just need to load df_snies from app.py and pretend it's filtered
        app.filtered_snies = lambda: app.df_snies.head(100)
        app.filtered_ole_m0 = lambda: app.df_ole_m0.head(100)
        app.filtered_saber_latest = lambda: app.df_saber.head(100)
        app.valid_divipolas = lambda: app.df_cobertura["snies_divipola"].unique()
        
        # Copiamos integro el bloque fallido (desde "def calc_total_graduados_que_cotizan"...)
        def _get_oferta_table_typst():
            df = app.filtered_snies().select([
                "nombre_institucion", "programa_academico", "numero_creditos", "costo_matricula_estud_nuevos"
            ]).rename({
                "nombre_institucion": "Institución", "programa_academico": "Programa Académico",
                "numero_creditos": "Créditos", "costo_matricula_estud_nuevos": "Costo Matrícula"
            }).head(40)
            return engine.format_as_typst_table(df)

        print("Probando Tabla Oferta...")
        try:
            print("Result OK ->", len(_get_oferta_table_typst()))
        except Exception as e:
            import traceback; traceback.print_exc()
            
        def _get_saber_table_typst():
            df = app.filtered_saber_latest()
            if len(df) == 0: return engine.format_as_typst_table(pl.DataFrame())
            agg = df.group_by("codigo_snies_del_programa").agg([
                pl.col("pro_gen_punt_global").mean().round(1).alias("Puntaje Global"),
                pl.col("pro_gen_mod_razona_cuantitat_punt").mean().round(1).alias("Razonamiento"),
                pl.col("pro_gen_mod_lectura_critica_punt").mean().round(1).alias("Lectura"),
                pl.col("pro_gen_mod_ingles_punt").mean().round(1).alias("Inglés")
            ])
            df_nombres = app.df_snies.select([
                pl.col("codigo_snies_del_programa").cast(pl.Int64),
                "programa_academico"
            ]).unique()
            agg = agg.join(df_nombres, on="codigo_snies_del_programa", how="left").drop("codigo_snies_del_programa").rename({"programa_academico": "Programa"})
            agg = agg.select(["Programa", "Puntaje Global", "Razonamiento", "Lectura", "Inglés"]).head(40)
            return engine.format_as_typst_table(agg)
            
        print("Probando Tabla Saber...")
        try:
            print("Result OK ->", len(_get_saber_table_typst()))
        except Exception as e:
            import traceback; traceback.print_exc()

        def _get_ole_mobility_table_typst():
            df_m0_filt = app.filtered_ole_m0()
            if len(df_m0_filt) == 0: return engine.format_as_typst_table(pl.DataFrame())
            agg = df_m0_filt.group_by(["departamento_origen", "departamento_destino"]).agg(
                pl.col("graduados_que_cotizan").sum().alias("Cotizantes")
            ).sort("Cotizantes", descending=True).rename({
                "departamento_origen": "Depto. Graduación",
                "departamento_destino": "Depto. Destino Laboral"
            }).head(15)
            return engine.format_as_typst_table(agg)

        print("Probando Tabla Movilidad...")
        try:
            print("Result OK ->", len(_get_ole_mobility_table_typst()))
        except Exception as e:
            import traceback; traceback.print_exc()

if __name__ == "__main__":
    test_prepare_directly()
