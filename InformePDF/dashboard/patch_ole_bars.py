import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

replacement_code = """
@reactive.calc
def calc_plot_dist_empleabilidad_sexo():
    import pandas as pd
    fs = filtered_snies()
    snies_codigos = fs["codigo_snies_del_programa"].unique()
    if len(snies_codigos) == 0: return go.Figure()
    max_anno_corte = df_ole_m0["anno_corte"].max()
    
    df_f = df_ole_m0.filter(pl.col("codigo_snies_del_programa").is_in(snies_codigos) & (pl.col("anno_corte") == max_anno_corte))
    if len(df_f) == 0: return go.Figure()
    
    agg = df_f.group_by("sexo").agg([
        pl.col("graduados_que_cotizan").sum().alias("num"),
        pl.col("graduados").sum().alias("den")
    ]).filter(pl.col("den") > 0).with_columns((pl.col("num") / pl.col("den")).alias("tasa")).to_pandas()
    
    if agg.empty: return go.Figure()
    fig = px.bar(agg, x="sexo", y="tasa", color="sexo", color_discrete_map=COLOR_SEXO, text_auto=".1%")
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', showlegend=False, margin=dict(l=20, r=20, t=20, b=20),
                      xaxis=dict(title="Sexo", gridcolor='#EEEEEE'),
                      yaxis=dict(title="Tasa de Empleabilidad", tickformat=".0%", gridcolor='#EEEEEE'))
    return fig

@reactive.calc
def calc_plot_dist_dependientes_sexo():
    import pandas as pd
    fs = filtered_snies()
    snies_codigos = fs["codigo_snies_del_programa"].unique()
    if len(snies_codigos) == 0: return go.Figure()
    max_anno_corte = df_ole_m0["anno_corte"].max()
    
    df_f = df_ole_m0.filter(pl.col("codigo_snies_del_programa").is_in(snies_codigos) & (pl.col("anno_corte") == max_anno_corte))
    if len(df_f) == 0: return go.Figure()
    
    agg = df_f.group_by("sexo").agg([
        pl.col("graduados_cotizantes_dependientes").sum().alias("num"),
        pl.col("graduados").sum().alias("den")
    ]).filter(pl.col("den") > 0).with_columns((pl.col("num") / pl.col("den")).alias("tasa")).to_pandas()
    
    if agg.empty: return go.Figure()
    fig = px.bar(agg, x="sexo", y="tasa", color="sexo", color_discrete_map=COLOR_SEXO, text_auto=".1%")
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', showlegend=False, margin=dict(l=20, r=20, t=20, b=20),
                      xaxis=dict(title="Sexo", gridcolor='#EEEEEE'),
                      yaxis=dict(title="Dependientes sobre Graduados", tickformat=".0%", gridcolor='#EEEEEE'))
    return fig

@reactive.calc
def calc_plot_dist_empleabilidad():
    import pandas as pd
    max_anno_corte = df_ole_m0["anno_corte"].max()
    
    fs = filtered_snies()
    snies_codigos = fs["codigo_snies_del_programa"].unique()
    df_total = pd.DataFrame()
    if len(snies_codigos) > 0:
        ole_nivel = df_ole_m0.filter(pl.col("codigo_snies_del_programa").is_in(snies_codigos) & (pl.col("anno_corte") == max_anno_corte))
        if len(ole_nivel) > 0:
            agg_total = ole_nivel.agg([pl.col("graduados_que_cotizan").sum().alias("num"), pl.col("graduados").sum().alias("den")]).filter(pl.col("den") > 0).with_columns((pl.col("num") / pl.col("den")).alias("tasa"))
            df_total = agg_total.to_pandas()
            df_total["grupo"] = "Programa Base"

    comp_codigos = comparable_snies_codigos()
    df_comp = pd.DataFrame()
    if len(comp_codigos) > 0:
        ole_comp = df_ole_m0.filter(pl.col("codigo_snies_del_programa").is_in(comp_codigos) & (pl.col("anno_corte") == max_anno_corte))
        if len(ole_comp) > 0:
            agg_comp = ole_comp.agg([pl.col("graduados_que_cotizan").sum().alias("num"), pl.col("graduados").sum().alias("den")]).filter(pl.col("den") > 0).with_columns((pl.col("num") / pl.col("den")).alias("tasa"))
            df_comp = agg_comp.to_pandas()
            df_comp["grupo"] = "Grupo Comparable"
            
    if df_total.empty and df_comp.empty: return go.Figure()
    
    dfs = []
    if not df_total.empty: dfs.append(df_total)
    if not df_comp.empty: dfs.append(df_comp)
    final_df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    
    if final_df.empty: return go.Figure()
    
    fig = px.bar(final_df, x="grupo", y="tasa", color="grupo", color_discrete_map={"Programa Base": "#31497e", "Grupo Comparable": "#674f95"}, text_auto=".1%")
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', showlegend=False, margin=dict(l=20, r=20, t=20, b=20),
                      xaxis=dict(title="", gridcolor='#EEEEEE'),
                      yaxis=dict(title="Tasa de Empleabilidad", tickformat=".0%", gridcolor='#EEEEEE'))
    return fig

@reactive.calc
def calc_plot_dist_dependientes():
    import pandas as pd
    max_anno_corte = df_ole_m0["anno_corte"].max()
    
    fs = filtered_snies()
    snies_codigos = fs["codigo_snies_del_programa"].unique()
    df_total = pd.DataFrame()
    if len(snies_codigos) > 0:
        ole_nivel = df_ole_m0.filter(pl.col("codigo_snies_del_programa").is_in(snies_codigos) & (pl.col("anno_corte") == max_anno_corte))
        if len(ole_nivel) > 0:
            agg_total = ole_nivel.agg([pl.col("graduados_cotizantes_dependientes").sum().alias("num"), pl.col("graduados").sum().alias("den")]).filter(pl.col("den") > 0).with_columns((pl.col("num") / pl.col("den")).alias("tasa"))
            df_total = agg_total.to_pandas()
            df_total["grupo"] = "Programa Base"

    comp_codigos = comparable_snies_codigos()
    df_comp = pd.DataFrame()
    if len(comp_codigos) > 0:
        ole_comp = df_ole_m0.filter(pl.col("codigo_snies_del_programa").is_in(comp_codigos) & (pl.col("anno_corte") == max_anno_corte))
        if len(ole_comp) > 0:
            agg_comp = ole_comp.agg([pl.col("graduados_cotizantes_dependientes").sum().alias("num"), pl.col("graduados").sum().alias("den")]).filter(pl.col("den") > 0).with_columns((pl.col("num") / pl.col("den")).alias("tasa"))
            df_comp = agg_comp.to_pandas()
            df_comp["grupo"] = "Grupo Comparable"
            
    if df_total.empty and df_comp.empty: return go.Figure()
    
    dfs = []
    if not df_total.empty: dfs.append(df_total)
    if not df_comp.empty: dfs.append(df_comp)
    final_df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    
    if final_df.empty: return go.Figure()
    fig = px.bar(final_df, x="grupo", y="tasa", color="grupo", color_discrete_map={"Programa Base": "#31497e", "Grupo Comparable": "#674f95"}, text_auto=".1%")
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', showlegend=False, margin=dict(l=20, r=20, t=20, b=20),
                      xaxis=dict(title="", gridcolor='#EEEEEE'),
                      yaxis=dict(title="Dependientes sobre Graduados", tickformat=".0%", gridcolor='#EEEEEE'))
    return fig
"""

# Remover los 4 calculos antiguos
code = re.sub(r'@reactive\.calc\s*\ndef calc_plot_dist_empleabilidad_sexo\(\).*?return fig\s*', '', code, flags=re.DOTALL)
code = re.sub(r'@reactive\.calc\s*\ndef calc_plot_dist_dependientes_sexo\(\).*?return fig\s*', '', code, flags=re.DOTALL)
code = re.sub(r'@reactive\.calc\s*\ndef calc_plot_dist_empleabilidad\(\).*?return fig\s*', '', code, flags=re.DOTALL)
code = re.sub(r'@reactive\.calc\s*\ndef calc_plot_dist_dependientes\(\):.*?return fig\s*', '', code, flags=re.DOTALL)

# Insert the replacement block somewhere safe
code = code.replace('@render_widget\ndef plot_dist_empleabilidad', replacement_code + '\n@render_widget\ndef plot_dist_empleabilidad')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Rewrite complete')
