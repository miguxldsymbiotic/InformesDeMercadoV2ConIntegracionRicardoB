"""
Motor de generación de PDF para la pestaña "Tendencia Comparada".
Genera un informe profesional comparando un programa SNIES individual
contra su grupo comparable.
"""
import os
import typst
from pathlib import Path
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from kaleido.scopes.plotly import PlotlyScope

class ComparadaReportEngine:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self._tmp = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self._tmp.name)
        # Inicializar el scope de Kaleido para evitar reinicios lentos
        self.scope = PlotlyScope()
        
        # Copiar recursos al directorio temporal
        # Intentar usar el logo optimizado si existe
        logo_file = "logo_symbiotic_small.svg" if (self.base_dir / "logo_symbiotic_small.svg").exists() else "logo_symbiotic.svg"
        src_logo = self.base_dir / logo_file
        if src_logo.exists():
             shutil.copy2(src_logo, self.temp_dir / "logo_symbiotic.svg") # Guardar siempre con el mismo nombre para el template
             
        src_template = self.base_dir / "report_comparada_template.typ"
        if src_template.exists():
            shutil.copy2(src_template, self.temp_dir / "report_comparada_template.typ")
        premium_src = self.base_dir / "premium_template.typ"
        if premium_src.exists():
            shutil.copy2(premium_src, self.temp_dir / "premium_template.typ")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tmp.cleanup()
        return False

    def export_plotly_fig(self, fig, name):
        """Exporta una figura de Plotly a SVG en el directorio temporal con monitoreo."""
        path = self.temp_dir / f"{name}.svg"
        print(f"   [Comp-Engine] Exportando gráfica: {name}...")
        svg_data = self.scope.transform(fig, format="svg", width=700, height=420)
        with open(path, "wb") as f:
            f.write(svg_data)
        return f"{name}.svg"

    def export_plotly_fig_wide(self, fig, name):
        """Exporta una figura ancha a SVG."""
        path = self.temp_dir / f"{name}.svg"
        svg_data = self.scope.transform(fig, format="svg", width=960, height=400)
        with open(path, "wb") as f:
            f.write(svg_data)
        return f"{name}.svg"

    def export_plotly_fig_small(self, fig, name):
        """Exporta una figura pequeña a SVG."""
        path = self.temp_dir / f"{name}.svg"
        svg_data = self.scope.transform(fig, format="svg", width=450, height=350)
        with open(path, "wb") as f:
            f.write(svg_data)
        return f"{name}.svg"

    def export_figs_parallel(self, figs_dict, max_workers=None):
        """
        Exporta múltiples figuras en paralelo con monitoreo.
        """
        if max_workers is None:
            # En Windows (nt) usamos 2 para evitar errores de subproceso de Kaleido
            max_workers = 2 if os.name == 'nt' else 4
            
        print(f"   [Comp-Engine] Iniciando exportación de {len(figs_dict)} gráficas (Workers: {max_workers})...")
        results = {}
        def _export_one(item):
            name, (fig, mode) = item
            if mode == "wide":
                return name, self.export_plotly_fig_wide(fig, name)
            elif mode == "small":
                return name, self.export_plotly_fig_small(fig, name)
            return name, self.export_plotly_fig(fig, name)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_export_one, item): item[0] for item in figs_dict.items()}
            for future in as_completed(futures):
                name, path = future.result()
                if path:
                    results[name] = path
        
        print(f"   [Comp-Engine] Finalizada exportación de todas las gráficas.")
        return results

    @staticmethod
    def _escape_typst(text):
        """Escapa caracteres problemáticos para Typst."""
        if text is None:
            return "Sin dato"
        s = str(text)
        # Escapar caracteres especiales de Typst
        for ch in ['#', '$', '%', '&', '_', '{', '}', '~', '^', '\\']:
            s = s.replace(ch, f'\\{ch}')
        # Escapar comillas dobles dentro de strings
        s = s.replace('"', '\\"')
        return s

    def generate_report(self, ctx):
        """
        Genera el informe PDF comparativo.
        
        ctx: dict con claves:
          - program_info: dict (codigo, nombre, institucion, nivel, modalidad, sector, departamento, nbc, area)
          - comp_group_info: dict (n_programas, criterios_str)
          - kpis: dict con sub-dicts para cada sección
          - plots: dict con nombres de archivo PNG
          - date: str
        """
        pi = ctx.get("program_info", {})
        cg = ctx.get("comp_group_info", {})
        kpis = ctx.get("kpis", {})
        plots = ctx.get("plots", {})
        date_str = ctx.get("date", "")
        esc = self._escape_typst

        # ---------- Construcción del documento Typst ----------
        lines = []
        
        # Importar template
        lines.append('#import "premium_template.typ": *')
        lines.append('')
        lines.append('#show: project.with(')
        lines.append(f'  title: "Informe Comparativo de Mercado",')
        lines.append(f'  subtitle: "{esc(pi.get("nombre", ""))}",')
        lines.append(f'  description: "Análisis comparativo frente a un grupo de {cg.get("n_programas", 0)} programas del mismo NBC.",')
        lines.append(f'  institution: "{esc(pi.get("institucion", ""))}",')
        lines.append(f'  program: "{esc(pi.get("nombre", ""))} · {esc(str(pi.get("codigo", "")))}",')
        lines.append(f'  date: "{esc(date_str)}",')
        lines.append(')')
        lines.append('')
        
        # PÁGINA DE ÍNDICE
        lines.append(f'#section-page(num: "Índice", title: "Contenido del Informe")[')
        lines.append('  #v(20pt)')
        lines.append('  #block(stroke: 1pt + colors.borde, radius: 10pt, clip: true)[')
        lines.append('    #toc-item(num: "01", title: "Resumen Ejecutivo", page-num: "2")')
        lines.append('    #toc-item(num: "02", title: "Tendencias de Matrícula", page-num: "3")')
        lines.append('    #toc-item(num: "03", title: "Costos y Créditos", page-num: "4")')
        lines.append('    #toc-item(num: "04", title: "Observatorio Laboral", page-num: "5")')
        lines.append('    #toc-item(num: "05", title: "Salarios de Enganche", page-num: "6")')
        lines.append('    #toc-item(num: "06", title: "Permanencia y Deserción", page-num: "7")')
        lines.append('    #toc-item(num: "07", title: "Prueba SABER PRO", page-num: "8")')
        lines.append('    #toc-item(num: "08", title: "Perfil Socioeconómico", page-num: "9")')
        lines.append('  ]')
        lines.append(']')
        lines.append('')

        # ============================================================
        # SECCIÓN 1: RESUMEN EJECUTIVO
        # ============================================================
        lines.append('#section-page(num: "01", title: "Resumen Ejecutivo")[')
        lines.append(f'  #insight-box(icon: "📌", text-content: "Este informe presenta el análisis comparativo del programa {esc(pi.get("nombre", ""))} frente a un grupo de {cg.get("n_programas", 0)} programas similares.")')
        lines.append('')
        lines.append(f'  #intro-text[El análisis integra datos oficiales del SNIES, OLE, SPADIES e ICFES para ofrecer una visión integral del posicionamiento competitivo del programa.]')
        lines.append('')
        
        # KPIs resumen ejecutivo
        lines.append('  #v(10pt)')
        lines.append('  #kpi-row(')
        for label, val_prog, val_comp in kpis.get("resumen", []):
            lines.append(f'    kpi-duo(label: "{esc(label)}", val-prog: "{esc(val_prog)}", val-comp: "{esc(val_comp)}"),')
        lines.append('  )')
        lines.append('')
        
        lines.append('  #v(10pt)')
        lines.append('  #insight-box(border-c: "marino", text-content: "Los indicadores presentados comparan el programa seleccionado contra la tendencia central del grupo comparable.")')
        lines.append(']')
        lines.append('')

        # ============================================================
        # SECCIÓN 2: TENDENCIAS DE MATRÍCULA
        # ============================================================
        lines.append('#section-page(num: "02", title: "Tendencias de Matrícula")[')
        lines.append('  #intro-text[Evolución de estudiantes de primer curso, matriculados y graduados. La línea sólida representa el programa seleccionado y la línea punteada la mediana del grupo comparable.]')
        lines.append('')
        
        # KPIs matrícula
        lines.append('  #kpi-row(')
        for label, val_prog, val_comp in kpis.get("matricula", []):
            lines.append(f'    kpi-duo(label: "{esc(label)}", val-prog: "{esc(val_prog)}", val-comp: "{esc(val_comp)}"),')
        lines.append('  )')
        lines.append('  #v(10pt)')
        
        # Gráficos de matrícula
        if "comp_pcurso" in plots:
            lines.append(f'  #chart-wrap(title: "Estudiantes de Primer Curso", height: 180pt)[#image("{plots["comp_pcurso"]}")]')
            lines.append('  #v(10pt)')
        if "comp_matricula" in plots:
            lines.append(f'  #chart-wrap(title: "Estudiantes Matriculados", height: 180pt)[#image("{plots["comp_matricula"]}")]')
            lines.append('  #v(10pt)')
        if "comp_graduados" in plots:
            lines.append(f'  #chart-wrap(title: "Estudiantes Graduados", height: 180pt)[#image("{plots["comp_graduados"]}")]')
        lines.append(']')
        lines.append('')

        # ============================================================
        # SECCIÓN 3: COSTOS Y CRÉDITOS
        # ============================================================
        lines.append('#section-page(num: "03", title: "Costos y Créditos Académicos")[')
        lines.append('  #intro-text[Comparación de los costos de matrícula y número de créditos académicos del programa frente a la distribución de su grupo comparable y del universo de programas activos.]')
        lines.append('')
        
        # KPIs costos
        lines.append('  #kpi-row(')
        for label, val_prog, val_comp in kpis.get("costos", []):
            lines.append(f'    kpi-duo(label: "{esc(label)}", val-prog: "{esc(val_prog)}", val-comp: "{esc(val_comp)}"),')
        lines.append('  )')
        lines.append('  #v(10pt)')
        
        # Gráficos a 2 columnas
        if "comp_dist_costo" in plots and "comp_dist_creditos" in plots:
            lines.append(f'  #chart_grid_2("{plots["comp_dist_costo"]}", "{plots["comp_dist_creditos"]}", caption1: "Distribución de Costo de Matrícula (Solo Privados)", caption2: "Distribución de Número de Créditos")')
        elif "comp_dist_costo" in plots:
            lines.append(f'  #chart_block("{plots["comp_dist_costo"]}", caption: "Distribución de Costo de Matrícula (Solo Privados)")')
        elif "comp_dist_creditos" in plots:
            lines.append(f'  #chart_block("{plots["comp_dist_creditos"]}", caption: "Distribución de Número de Créditos")')
        lines.append('')
        
        lines.append('  #tech_note([')
        lines.append('    El costo de matrícula aplica exclusivamente para programas de instituciones privadas regulados por el SNIES. El fondo gris representa el universo de programas activos, la distribución púrpura es el Grupo Comparable, y la línea azul punteada marca el valor del Programa Seleccionado.')
        lines.append('  ])')
        lines.append(']')
        lines.append('')

        # ============================================================
        # SECCIÓN 4: OBSERVATORIO LABORAL
        # ============================================================
        lines.append('#section-page(num: "04", title: "Observatorio Laboral")[')
        lines.append('  #intro-text[Indicadores de vinculación laboral y empleabilidad de los graduados.]')
        lines.append('')
        
        # KPIs empleabilidad
        lines.append('  #kpi-row(')
        for label, val_prog, val_comp in kpis.get("ole", []):
            lines.append(f'    kpi-duo(label: "{esc(label)}", val-prog: "{esc(val_prog)}", val-comp: "{esc(val_comp)}"),')
        lines.append('  )')
        lines.append('  #v(10pt)')
        
        # Gráficos
        if "comp_ole_emp" in plots and "comp_ole_dep" in plots:
            lines.append(f'  #chart_grid_2("{plots["comp_ole_emp"]}", "{plots["comp_ole_dep"]}", caption1: "Tendencia de Empleabilidad — Fuente: OLE", caption2: "Dependientes sobre Cotizantes — Fuente: OLE")')
            lines.append('  #v(5pt)')
        
        if "comp_dist_emp" in plots:
            lines.append(f'  #chart_block("{plots["comp_dist_emp"]}", caption: "Distribución de Tasa de Empleabilidad — Fuente: OLE")')
        lines.append('')
        
        lines.append('  #method_note([')
        lines.append('    La Tasa de Empleabilidad se calcula como la proporción de graduados que registran cotización al sistema de seguridad social. La línea central representa el promedio del grupo comparable y la zona sombreada la dispersión muestral (±1 Desviación Estándar).')
        lines.append('  ])')
        lines.append(']')
        lines.append('')

        # ============================================================
        # SECCIÓN 5: SALARIO DE ENGANCHE
        # ============================================================
        lines.append('#section-page(num: "05", title: "Salario de Enganche")[')
        lines.append('  #intro-text[Análisis del ingreso de los graduados en su primer empleo formal, expresado en pesos constantes.]')
        lines.append('')
        
        # KPIs salario
        lines.append('  #kpi-row(')
        for label, val_prog, val_comp in kpis.get("salario", []):
            lines.append(f'    kpi-duo(label: "{esc(label)}", val-prog: "{esc(val_prog)}", val-comp: "{esc(val_comp)}"),')
        lines.append('  )')
        lines.append('  #v(10pt)')
        
        # Gráficos
        if "comp_sal_evol" in plots and "comp_sal_dist" in plots:
            lines.append(f'  #chart_grid_2("{plots["comp_sal_evol"]}", "{plots["comp_sal_dist"]}", caption1: "Evolución del Salario Promedio Estimado — Fuente: OLE", caption2: "Distribución por Rango Salarial — Fuente: OLE")')
        elif "comp_sal_evol" in plots:
            lines.append(f'  #chart_block("{plots["comp_sal_evol"]}", caption: "Evolución del Salario Promedio Estimado — Fuente: OLE")')
        lines.append(']')
        lines.append('')

        # ============================================================
        # SECCIÓN 6: DESERCIÓN
        # ============================================================
        lines.append('#section-page(num: "06", title: "Permanencia y Deserción")[')
        lines.append('  #intro-text[Análisis de la deserción anual. Esta métrica es crítica para entender la eficiencia interna de los programas y la retención estudiantil.]')
        lines.append('')
        
        # KPIs deserción
        lines.append('  #kpi-row(')
        for label, val_prog, val_comp in kpis.get("desercion", []):
            lines.append(f'    kpi-duo(label: "{esc(label)}", val-prog: "{esc(val_prog)}", val-comp: "{esc(val_comp)}"),')
        lines.append('  )')
        lines.append('  #v(10pt)')
        
        # Gráficos
        if "comp_des_trend" in plots and "comp_des_dist" in plots:
            lines.append(f'  #chart_grid_2("{plots["comp_des_trend"]}", "{plots["comp_des_dist"]}", caption1: "Tendencia Histórica de Deserción Anual — Fuente: SPADIES", caption2: "Distribución de Tasa de Deserción — Fuente: SPADIES")')
        elif "comp_des_trend" in plots:
            lines.append(f'  #chart_block("{plots["comp_des_trend"]}", caption: "Tendencia Histórica de Deserción Anual — Fuente: SPADIES")')
        lines.append('')
        
        lines.append('  #tech_note([')
        lines.append('    Para programas de Posgrado sin registro en SPADIES, se estima un proxy de deserción: (Matriculados\\_{t-1} + Primer Curso\\_{t} - Graduados\\_{t} - Matriculados\\_{t}) / (Matriculados\\_{t-1} + Primer Curso\\_{t})')
        lines.append('  ])')
        lines.append(']')
        lines.append('')

        # ============================================================
        # SECCIÓN 7: PRUEBA SABER PRO
        # ============================================================
        lines.append('#section-page(num: "07", title: "Prueba SABER PRO")[')
        lines.append('  #intro-text[Resultados de las pruebas SABER PRO que evalúan las competencias genéricas de los estudiantes. Esta sección aplica exclusivamente para programas de pregrado habilitados.]')
        lines.append('')
        
        # KPIs Saber PRO (3+3)
        if kpis.get("saber_row1"):
            lines.append('  #kpi-row(')
            for label, val_prog, val_comp in kpis["saber_row1"]:
                lines.append(f'    kpi-duo(label: "{esc(label)}", val-prog: "{esc(val_prog)}", val-comp: "{esc(val_comp)}"),')
            lines.append('  )')
            lines.append('  #v(5pt)')
        
        if kpis.get("saber_row2"):
            lines.append('  #kpi-row(')
            for label, val_prog, val_comp in kpis["saber_row2"]:
                lines.append(f'    kpi-duo(label: "{esc(label)}", val-prog: "{esc(val_prog)}", val-comp: "{esc(val_comp)}"),')
            lines.append('  )')
            lines.append('  #v(10pt)')
        
        # Gráficos SABER PRO (pares)
        saber_pairs = [
            ("comp_saber_global", "comp_saber_razona", "Puntaje Global", "Razonamiento Cuantitativo"),
            ("comp_saber_lectura", "comp_saber_ciuda", "Lectura Crítica", "Competencias Ciudadanas"),
            ("comp_saber_ingles", "comp_saber_escrita", "Inglés", "Comunicación Escrita"),
        ]
        for key1, key2, cap1, cap2 in saber_pairs:
            if key1 in plots and key2 in plots:
                lines.append(f'  #chart_grid_2("{plots[key1]}", "{plots[key2]}", caption1: "Evolución — {cap1}", caption2: "Evolución — {cap2}")')
                lines.append('  #v(5pt)')
            elif key1 in plots:
                lines.append(f'  #chart_block("{plots[key1]}", caption: "Evolución — {cap1}")')
                lines.append('  #v(5pt)')
        lines.append(']')
        lines.append('')

        # ============================================================
        # SECCIÓN 8: PERFIL SOCIOECONÓMICO
        # ============================================================
        lines.append('#section-page(num: "08", title: "Perfil Socioeconómico")[')
        lines.append('  #intro-text[Distribución sociodemográfica de los evaluados en la Prueba SABER PRO. Se compara la composición del programa seleccionado contra el grupo comparable en el último año disponible.]')
        lines.append('')
        
        demo_pairs = [
            ("comp_demo_sexo", "comp_demo_edad", "Distribución por Sexo", "Distribución por Grupo de Edad"),
            ("comp_demo_trabajo", "comp_demo_estrato", "Distribución por Horas de Trabajo", "Distribución por Estrato Social"),
        ]
        for key1, key2, cap1, cap2 in demo_pairs:
            if key1 in plots and key2 in plots:
                lines.append(f'  #chart_grid_2("{plots[key1]}", "{plots[key2]}", caption1: "{cap1} — Fuente: ICFES", caption2: "{cap2} — Fuente: ICFES")')
                lines.append('  #v(8pt)')
            elif key1 in plots:
                lines.append(f'  #chart_block("{plots[key1]}", caption: "{cap1} — Fuente: ICFES")')
                lines.append('  #v(8pt)')
        lines.append(']')
        lines.append('')

        # ============================================================
        # CONTRAPORTADA
        # ============================================================
        lines.append('#pagebreak()')
        lines.append('#set align(center)')
        lines.append('#v(6cm)')
        lines.append('#image("logo_symbiotic.svg", width: 30%)')
        lines.append('#v(2cm)')
        lines.append('#text(14pt, weight: "bold", fill: colors.marino, "SymbioTIC by UNIMINUTO")')
        lines.append('#v(0.5em)')
        lines.append('#text(10pt, fill: colors.pizarra, "Inteligencia Estratégica para la Educación Superior")')
        lines.append('#v(2cm)')
        lines.append('#rect(width: 80%, fill: colors.hielo, radius: 6pt, inset: 16pt, stroke: 0.5pt + colors.borde, [')
        lines.append('  #set text(8pt, fill: colors.pizarra)')
        lines.append('  #set align(left)')
        lines.append('  *Aviso Legal:* Este informe fue generado de forma automatizada a partir de datos oficiales de acceso público del Ministerio de Educación Nacional de Colombia (SNIES, OLE, SPADIES) y del ICFES. Los indicadores y visualizaciones son de carácter informativo y no constituyen asesoría oficial. La precisión de los datos depende de los reportes realizados por las instituciones de educación superior al sistema de información.')
        lines.append('])')
        lines.append('#v(1cm)')
        lines.append(f'#text(9pt, fill: colors.pizarra, "Generado el {esc(date_str)}")')
        lines.append('')

        # ---------- Escribir archivo Typst ----------
        typ_file_path = self.temp_dir / "report_comparada_instance.typ"
        with open(typ_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        # ---------- Compilar ----------
        output_pdf = self.temp_dir / "informe_comparada.pdf"
        try:
            typst.compile(str(typ_file_path), output=str(output_pdf))
        except Exception as e:
            raise RuntimeError(f"Error de compilación Typst (Comparada): {e}")

        if not output_pdf.exists() or output_pdf.stat().st_size == 0:
            raise RuntimeError("La compilación de Typst no generó un archivo PDF válido.")

        return str(output_pdf)

    def cleanup(self):
        """Elimina el directorio temporal."""
        try:
            self._tmp.cleanup()
        except:
            pass
