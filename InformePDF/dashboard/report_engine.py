import os
import typst
from pathlib import Path
import tempfile
import shutil
import concurrent.futures


class ReportEngine:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Pool de workers para exportación de gráficos en paralelo (1 para estabilidad en Windows Kaleido)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.futures = []

        # Estabilidad de Kaleido en Windows
        os.environ["KALEIDO_BROWSER_WAIT"] = "60"
        os.environ["KALEIDO_LOG_LEVEL"] = "1"
        os.environ["KALEIDO_DISABLE_GPU"] = "1"
        os.environ["KALEIDO_NO_SANDBOX"] = "1"

        # Logo pequeño (puede usarse en otros lugares)
        self.logo_path = self.base_dir / "logo_symbiotic_small.svg"
        if not self.logo_path.exists():
            self.logo_path = self.base_dir / "logo_symbiotic.svg"

        # Logo principal (para portada y footer)
        self.logo_main = self.base_dir / "logo_symbiotic_main.png"
        if not self.logo_main.exists():
            self.logo_main = self.base_dir / "logo_symbiotic_main.svg"

        # Copiar recursos al temp
        if self.logo_path.exists():
            shutil.copy2(self.logo_path, self.temp_dir / "logo_symbiotic.svg")
        if self.logo_main.exists():
            dest_name = self.logo_main.name
            shutil.copy2(self.logo_main, self.temp_dir / dest_name)
            
        template_src = self.base_dir / "premium_template.typ"
        if template_src.exists():
            shutil.copy2(template_src, self.temp_dir / "premium_template.typ")

    def export_plotly_fig(self, fig, name):
        """Exporta una figura de Plotly a SVG (más rápido y escalable)."""
        path = self.temp_dir / f"{name}.svg"
        try:
            fig.write_image(
                str(path), format="svg",
                width=900, height=540,
                engine="kaleido"
            )
            return f"{name}.svg"
        except Exception as e:
            print(f"[Engine] ERROR exportando {name}: {e}")
            # Placeholder de contingencia
            placeholder = (
                f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="420">'
                f'<rect width="800" height="420" fill="#f8f9fa"/>'
                f'<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" '
                f'font-family="sans-serif" font-size="14" fill="#64748B">Error: {name}</text></svg>'
            )
            path.write_text(placeholder, encoding="utf-8")
            return f"{name}.svg"

    def queue_plotly_fig(self, fig, name):
        """Exportación completamente síncrona saltándose el pool, para máxima estabilidad en Windows."""
        try:
            self.export_plotly_fig(fig, name)
        except Exception as e:
            print(f"Error secuencial en Kaleido: {e}")
        return f"{name}.svg"

    # ── TABLAS ──────────────────────────────────────────────────────────────

    def format_as_typst_table(self, df, columns=None):
        """Convierte un DataFrame Polars a sintaxis #styled-table de la plantilla premium."""
        if columns is None:
            columns = df.columns
        if df is None or len(df) == 0:
            return ""
        header = ", ".join([f'"{c}"' for c in columns])
        rows = []
        for row in df.select(columns).to_dicts():
            row_vals = []
            for v in row.values():
                val = str(v) if v is not None else ""
                val = val.replace('\\', '\\\\').replace('"', '\\"')
                row_vals.append(f'"{val}"')
            rows.append(", ".join(row_vals))
        return f'#styled-table(columns: {len(columns)}, headers: ({header}), rows: ({", ".join(rows)}))'

    # ── ESCAPE ──────────────────────────────────────────────────────────────

    def _esc_str(self, text):
        """Escapa texto para usarlo dentro de string literals Typst (entre comillas dobles)."""
        if text is None:
            return ""
        s = str(text)
        s = s.replace('\\', '\\\\')
        s = s.replace('"', '\\"')
        return s

    def _esc_content(self, text):
        """Escapa texto para usarlo dentro de bloques de contenido Typst [ ]."""
        if text is None:
            return ""
        s = str(text)
        s = s.replace('\\', '\\\\')
        s = s.replace('[', '\\[')
        s = s.replace(']', '\\]')
        s = s.replace('#', '\\#')
        return s

    # ── GENERACIÓN DEL INFORME ───────────────────────────────────────────────

    def generate_report(self, data_context):
        """Genera el informe PDF usando la plantilla premium."""
        # Esperar a que terminen todas las exportaciones paralelas de gráficas
        if self.futures:
            concurrent.futures.wait(self.futures)
            
        report_title = data_context.get("title", "Informe Ejecutivo de Educación Superior")
        date_str     = data_context.get("date", "2026")
        institution  = self._esc_str(data_context.get("institution", "Consolidado Nacional"))
        program      = self._esc_str(data_context.get("program",     "Todos los niveles"))
        snies_yr     = data_context.get("max_anno_snies",   "")
        ole_yr       = data_context.get("max_anno_ole",     "")
        spa_yr       = data_context.get("max_anno_spadies", "")
        sections     = data_context.get("sections", [])

        L = []  # líneas del .typ

        # ── Encabezado del documento ──
        L += [
            '#import "premium_template.typ": *',
            '#show: project.with(',
            f'  title: "{self._esc_str(report_title)}",',
            '  subtitle: "Mesa de Reportes Estratégica",',
            '  description: "Análisis integral del sector de educación superior bajo los filtros seleccionados.",',
            f'  institution: "{institution}",',
            f'  program: "{program}",',
            f'  date: "{date_str}",',
            ')',
            '',
        ]

        # ── ÍNDICE CON PAGINADO AUTOMÁTICO ──────────────────────────────────
        # auto-toc-item usa labels <sec-NN> colocados al inicio de cada sección
        L += [
            '#section-page(num: "Índice", title: "Contenido del Informe")[',
            '  #v(20pt)',
            '  #block(stroke: 1pt + colors.borde, radius: 10pt, clip: true)[',
            '    #auto-toc-item(num: "01", title: "Resumen Ejecutivo", target: <sec-01>)',
        ]
        for i, sec in enumerate(sections, 2):
            num_s = f"{i:02d}"
            ttl   = self._esc_str(sec.get("title", ""))
            L.append(f'    #auto-toc-item(num: "{num_s}", title: "{ttl}", target: <sec-{num_s}>)')
        L += ['  ]', ']', '']

        # ── Sección 01: Resumen Ejecutivo ──
        L += [
            '#section-page(num: "01", title: "Resumen Ejecutivo")[',
            '  #h(0pt)<sec-01>',   # label para auto-paginación del índice
            '',
            '  Este documento técnico presenta un análisis integral del sector de educación superior bajo los filtros seleccionados. Producido por *SymbioTIC* (Startup de UNIMINUTO), este informe traduce grandes volúmenes de datos en inteligencia estratégica para la toma de decisiones en instituciones y organismos gubernamentales.',
            '',
            '  #v(8pt)',
            '  == Fuentes de Información y Calidad de Datos',
            '',
            '  El análisis se sustenta en tres pilares de datos oficiales del Ministerio de Educación Nacional de Colombia, garantizando transparencia y rigor técnico:',
            '',
            f'  - *SNIES* (Sistema Nacional de Información de Educación Superior): #link("https://snies.mineducacion.gov.co/portal/")[Portal SNIES]. Es la fuente oficial de estadísticas sobre instituciones, programas académicos, matrícula y graduación. Corte: *{snies_yr}*.',
            f'  - *OLE* (Observatorio Laboral para la Educación): #link("https://ole.mineducacion.gov.co/portal/")[Portal OLE]. Monitorea la vinculación laboral de los graduados, capturando datos de cotizaciones al régimen de seguridad social. Corte: *{ole_yr}*.',
            f'  - *SPADIES* (Sistema para la Prevención de la Deserción): #link("https://www.mineducacion.gov.co/sistemasinfo/spadies/")[Portal SPADIES]. Analiza las trayectorias académicas para identificar riesgos de abandono y promover la permanencia. Corte: *{spa_yr}*.',
            '',
            '  #v(8pt)',
            '  #method_note([Los KPIs y visualizaciones presentados reflejan el comportamiento consolidado de los programas académicos capturados por los filtros activos. La integración de estas tres fuentes permite una visión 360° desde la oferta académica hasta la empleabilidad real de los egresados.])',
            '  #v(10pt)',
            '  #kpi-row(',
        ]
        for label, val in data_context.get("kpis_summary", []):
            L.append(f'    kpi-card(label: "{self._esc_str(label)}", value: "{self._esc_str(str(val))}"),')
        L += ['  )', ']', '']

        # ── Secciones dinámicas ──
        for i, sec in enumerate(sections, 2):
            num_s     = f"{i:02d}"
            sec_title = self._esc_str(sec.get("title", ""))
            sec_intro = self._esc_content(sec.get("intro", ""))
            plots     = sec.get("plots", [])
            kpis      = sec.get("kpis", [])
            table_str = sec.get("table", "")

            L.append(f'#section-page(num: "{num_s}", title: "{sec_title}")[')
            L.append(f'  #h(0pt)<sec-{num_s}>')   # label para auto-paginación del índice
            L.append('')

            # Texto introductorio — escrito directamente en el flujo de Typst
            if sec_intro:
                L += [
                    f'  {sec_intro}',
                    '',
                    '  #v(8pt)',
                ]

            # KPIs de la sección
            if kpis:
                L.append('  #kpi-row(')
                for lbl, v in kpis:
                    L.append(f'    kpi-card(label: "{self._esc_str(lbl)}", value: "{self._esc_str(str(v))}"),')
                L += ['  )', '  #v(10pt)', '']

            # Gráficas en grid de 2 columnas (fluye entre páginas naturalmente)
            if plots:
                if len(plots) == 1:
                    p = plots[0]
                    p_file  = p.get("file",    p) if isinstance(p, dict) else p
                    p_title = p.get("title", "Análisis") if isinstance(p, dict) else "Análisis"
                    p_ins   = p.get("insight", "")  if isinstance(p, dict) else ""
                    L += [
                        f'  #chart-wrap(title: "{self._esc_str(p_title)}", height: 240pt)[',
                        f'    #image("{p_file}")',
                        '  ]',
                    ]
                    if p_ins:
                        L.append(f'  #text(size: 8.5pt, style: "italic", fill: colors.pizarra)[{self._esc_content(p_ins)}]')
                    L += ['  #v(10pt)', '']
                else:
                    # Render pairs: chart + insight, side by side
                    pairs = [(plots[i], plots[i+1] if i+1 < len(plots) else None) for i in range(0, len(plots), 2)]
                    for left, right in pairs:
                        lf = left.get("file",  left)  if isinstance(left, dict) else left
                        lt = left.get("title", "Análisis") if isinstance(left, dict) else "Análisis"
                        li = left.get("insight", "")  if isinstance(left, dict) else ""
                        if right is not None:
                            rf = right.get("file",  right) if isinstance(right, dict) else right
                            rt = right.get("title", "Análisis") if isinstance(right, dict) else "Análisis"
                            ri = right.get("insight", "")  if isinstance(right, dict) else ""
                            L.append('  #grid(columns: (1fr, 1fr), gutter: 10pt,')
                            L.append(f'    chart-wrap(title: "{self._esc_str(lt)}", height: 150pt)[#image("{lf}")],')
                            L.append(f'    chart-wrap(title: "{self._esc_str(rt)}", height: 150pt)[#image("{rf}")],')
                            L.append('  )')
                            # insights below the grid row
                            if li or ri:
                                L.append('  #grid(columns: (1fr, 1fr), gutter: 10pt,')
                                li_esc = self._esc_content(li) if li else "—"
                                ri_esc = self._esc_content(ri) if ri else "—"
                                L.append(f'    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[{li_esc}]],')
                                L.append(f'    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[{ri_esc}]],')
                                L.append('  )')
                        else:
                            # Solo gráfica izquierda (número impar)
                            L.append('  #grid(columns: (1fr, 1fr), gutter: 10pt,')
                            L.append(f'    chart-wrap(title: "{self._esc_str(lt)}", height: 150pt)[#image("{lf}")],')
                            L.append('    [],')
                            L.append('  )')
                            if li:
                                L.append(f'  #text(size: 8.5pt, style: "italic", fill: colors.pizarra)[{self._esc_content(li)}]')
                        L += ['  #v(6pt)', '']

            # Tabla real — se pasa el contenido calculado por format_as_typst_table
            if table_str:
                L += ['  #v(6pt)', table_str, '']

            L += [']', '']

        # ── Compilar ──
        full_typ = "\n".join(L)

        # Debug: guardar copia para inspección
        debug_path = self.base_dir / "debug_last_report_instance.typ"
        try:
            debug_path.write_text(full_typ, encoding="utf-8")
        except Exception:
            pass

        # Escribir y compilar
        typ_file = self.temp_dir / "report_instance.typ"
        typ_file.write_text(full_typ, encoding="utf-8")

        output_pdf = self.temp_dir / "informe_premium.pdf"
        try:
            typst.compile(str(typ_file), output=str(output_pdf))
        except Exception as e:
            raise RuntimeError(f"Error de compilación Typst: {e}")

        if not output_pdf.exists() or output_pdf.stat().st_size == 0:
            raise RuntimeError("Typst no generó un PDF válido.")

        return str(output_pdf)

    def cleanup(self):
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass
