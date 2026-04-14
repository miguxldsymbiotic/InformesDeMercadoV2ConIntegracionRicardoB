import os
import typst
from pathlib import Path
import tempfile
import shutil
import polars as pl
from kaleido.scopes.plotly import PlotlyScope

from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuración de estabilidad para Kaleido en Windows
os.environ["KALEIDO_BROWSER_WAIT"] = "60"
os.environ["KALEIDO_LOG_LEVEL"] = "1"
os.environ["KALEIDO_DISABLE_GPU"] = "1"  # Desactivar GPU (evita cuelgues en Windows)
os.environ["KALEIDO_NO_SANDBOX"] = "1"   # Desactivar sandbox si es necesario

class ReportEngine:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self._tmp = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self._tmp.name)
        
        # Inicializar el scope de Kaleido, desactivando mathjax para no crashear en Windows
        self.scope = PlotlyScope(mathjax=None)
        
        # Asegurar que el logo y el template estén accesibles
        self.logo_path = self.base_dir / "logo_symbiotic_small.svg"
        if not self.logo_path.exists():
             self.logo_path = self.base_dir / "logo_symbiotic.svg"
        self.template_path = self.base_dir / "report_template.typ"
        
        # Copiar recursos necesarios al directorio temporal
        if self.logo_path.exists():
            shutil.copy2(self.logo_path, self.temp_dir / "logo_symbiotic.svg")
        if self.template_path.exists():
            shutil.copy2(self.template_path, self.temp_dir / "report_template.typ")
        premium_src = self.base_dir / "premium_template.typ"
        if premium_src.exists():
            shutil.copy2(premium_src, self.temp_dir / "premium_template.typ")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Asegurar cierre de Kaleido para evitar procesos huérfanos
        try:
            if hasattr(self, 'scope'):
                del self.scope
        except:
            pass
        self._tmp.cleanup()
        return False

    def export_plotly_fig(self, fig, filename_prefix):
        """
        Exporta una figura de Plotly a PNG usando scope persistente sin Timeouts para dejar que Chromium inicie.
        """
        path = self.temp_dir / f"{filename_prefix}.png"
        print(f"   [Engine] Exportando gráfica: {filename_prefix} (PNG)...")
        
        try:
            # Replicamos el 'scale=2' con resolución subyacente para máxima nitidez y compatibilidad.
            img_data = self.scope.transform(fig, format="png", width=1400, height=840)
            with open(path, "wb") as f:
                f.write(img_data)
            print(f"   [Engine] EXITO: {filename_prefix} generada.")
        except Exception as e:
            print(f"   [Engine] ERROR Crítico exportando {filename_prefix}: {e}")
            # Placeholder por si una figura falla
            placeholder = f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="420"><rect width="800" height="420" fill="#f8f9fa"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#64748B">Error: {filename_prefix}</text></svg>'
            path_svg = self.temp_dir / f"{filename_prefix}.svg"
            with open(path_svg, "w", encoding="utf-8") as f:
                f.write(placeholder)
            return f"{filename_prefix}.svg"
            
        return f"{filename_prefix}.png"

    def export_figs_parallel(self, figs_dict, max_workers=None):
        """
        Exporta múltiples figuras. En Windows usamos modo secuencial (max_workers=1) para máxima estabilidad.
        """
        if max_workers is None:
            # Forzamos 1 en Windows para evitar bloqueos del motor de gráficas
            max_workers = 1 if os.name == 'nt' else 4
            
        print(f"   [Engine] Iniciando exportación de {len(figs_dict)} gráficas (Modo estable: {os.name})...")
        results = {}
        def _export_one(item):
            name, (fig, mode) = item
            return name, self.export_plotly_fig(fig, name)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_export_one, item): item[0] for item in figs_dict.items()}
            for future in as_completed(futures):
                name, path = future.result()
                if path:
                    results[name] = path
        
        print(f"   [Engine] Finalizada exportación de todas las gráficas.")
        return results

    def format_as_typst_table(self, df):
        """Convierte un DataFrame de Polars a sintaxis de tabla de Typst."""
        if df is None or len(df) == 0:
            return "// Sin datos para tabla"
        
        columns = df.columns
        header = ", ".join([f'"{c}"' for c in columns])
        rows = []
        for row in df.to_dicts():
            row_vals = []
            for v in row.values():
                val = str(v) if v is not None else ""
                # Escapar comillas dobles en valores de celda
                val = val.replace('"', '\\"')
                row_vals.append(f'"{val}"')
            rows.append(", ".join(row_vals))
        
        table_str = f'#styled-table(columns: {len(columns)}, headers: ({header}), rows: ({", ".join(rows)}))'
        return table_str

    def _escape_typst(self, text):
        """Escapa caracteres problemáticos para Typst."""
        if text is None: return ""
        s = str(text)
        for ch in ['#', '$', '%', '&', '_', '{', '}', '~', '^', '\\']:
            s = s.replace(ch, f'\\{ch}')
        s = s.replace('"', '\\"')
        return s

    def generate_report(self, data_context):
        """Genera el informe PDF con monitoreo de compilación."""
        print(f"   [Engine] Construyendo documento Typst para: {data_context.get('title', 'Sin Título')}...")
        # Metadata del informe
        title = data_context.get("title", "Informe de Mercado de Educación Superior")
        date_str = data_context.get("date", "2026-03-30")
        
        # Construcción del contenido Typst
        typ_lines = [
            f'#import "premium_template.typ": *',
            f'#show: project.with(',
            f'  title: "{title}",',
            f'  subtitle: "Informe Ejecutivo de Mercado",',
            f'  description: "Análisis integral del sector de educación superior bajo los filtros seleccionados.",',
            f'  institution: "{data_context.get("institution", "Institución")}",',
            f'  program: "{data_context.get("program", "Programa")}",',
            f'  date: "{date_str}",',
            f')',
            '',
            f'#section-page(num: "Índice", title: "Contenido del Informe")[',
            '  #v(20pt)',
            '  #block(stroke: 1pt + colors.borde, radius: 10pt, clip: true)[',
            '    #toc-item(num: "01", title: "Resumen Ejecutivo", page-num: "2")',
            '  ]',
            ']',
            '',
            # ============================================================
            # SECCIÓN 1: RESUMEN EJECUTIVO (Restaurado con Metadatos)
            # ============================================================
            f'#section-page(num: "01", title: "Resumen Ejecutivo")[',
            '  #insight-box(',
            '    icon: "📌",',
            f'    text-content: "Este informe técnico traduce grandes volúmenes de datos en inteligencia estratégica para {self._escape_typst(data_context.get("institution", "la institución"))}.",',
            '    border-c: "marino"',
            '  )',
            '  #v(10pt)',
            '  #intro-text[',
            '    El análisis se sustenta en tres pilares de datos oficiales del Ministerio de Educación Nacional de Colombia, garantizando transparencia y rigor técnico:',
            '  ]',
            '',
            # Enlaces y fechas de corte (Original)
            f'  - *SNIES*: Fuente oficial de estadísticas de instituciones y programas. Corte: *{data_context.get("max_anno_snies", "N/A")}*.',
            f'  - *OLE*: Monitorea vinculación laboral y cotizaciones. Corte: *{data_context.get("max_anno_ole", "N/A")}*.',
            f'  - *SPADIES*: Análisis de trayectorias y riesgo de deserción. Corte: *{data_context.get("max_anno_spadies", "N/A")}*.',
            '',
            '  #tech_note([',
            '    Los KPIs y visualizaciones reflejan el comportamiento consolidado bajo los filtros activos. La integración de estas fuentes permite una visión 360° desde la oferta académica hasta la empleabilidad real.',
            '  ])',
            '  #v(10pt)',
            '  #kpi-row('
        ]
        
        # Agregar KPIs del resumen
        kpis = data_context.get("kpis_summary", [])
        for label, val in kpis:
            typ_lines.append(f'    kpi-card(label: "{label}", value: "{val}"),')
        typ_lines.append('  )')
        typ_lines.append(']')
        typ_lines.append('')
        
        # Secciones dinámicas (Optimizado para flujo continuo)
        for i, section in enumerate(data_context.get("sections", []), 2):
            num_str = f"{i:02d}"
            title = self._escape_typst(section["title"])
            typ_lines.append(f'#section-page(num: "{num_str}", title: "{title}")[')
            typ_lines.append(f'  #intro-text[{section["intro"]}]')
            typ_lines.append('')
            
            if "kpis" in section:
                typ_lines.append('  #v(10pt)')
                typ_lines.append('  #kpi-row(')
                for label, val in section["kpis"]:
                    typ_lines.append(f'    kpi-card(label: "{label}", value: "{val}"),')
                typ_lines.append('  )')
                typ_lines.append('')
            
            if "plots" in section:
                typ_lines.append('  #v(10pt)')
                plots = section["plots"]
                # Lógica inteligente para distribución de gráficos
                if len(plots) >= 6:
                    # Layout 3 columnas (muy denso)
                    typ_lines.append('  #grid(columns: (1fr, 1fr, 1fr), gutter: 8pt,')
                    for p in plots:
                        typ_lines.append(f'    chart-wrap(title: "Distribución", height: 110pt)[#image("{p}")] ,')
                    typ_lines.append('  )')
                elif len(plots) > 1:
                    # Layout 2 columnas
                    typ_lines.append('  #grid(columns: (1fr, 1fr), gutter: 12pt,')
                    for p in plots:
                        typ_lines.append(f'    chart-wrap(title: "Tendencia", height: 160pt)[#image("{p}")] ,')
                    typ_lines.append('  )')
                elif len(plots) == 1:
                    typ_lines.append(f'  #chart-wrap(title: "{title}", height: 260pt)[#image("{plots[0]}")]')
            
            if "table" in section:
                typ_lines.append('  #v(10pt)')
                typ_lines.append(section["table"])
            
            # Nota técnica de la sección (Restaurada)
            typ_lines.append('  #v(10pt)')
            typ_lines.append('  #tech_note([')
            typ_lines.append(f'    Los datos de {title} provienen de registros oficiales consolidados y reflejan el comportamiento bajo los filtros de segmentación aplicados.')
            typ_lines.append('  ])')

            typ_lines.append(']')
            typ_lines.append('')

        # Escribir archivo Typst
        typ_file_path = self.temp_dir / "report_instance.typ"
        with open(typ_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(typ_lines))
        
        # Compilar
        output_pdf = self.temp_dir / "informe.pdf"
        print(f"   [Engine] Compilando con Typst...")
        try:
            typst.compile(str(typ_file_path), output=str(output_pdf))
            print(f"   [Engine] Compilación exitosa: {output_pdf.stat().st_size} bytes.")
        except Exception as e:
            print(f"   [Engine] ERROR Crítico en compilación: {e}")
            raise RuntimeError(f"Error de compilación Typst: {e}")
            
        if not output_pdf.exists() or output_pdf.stat().st_size == 0:
            raise RuntimeError("La compilación de Typst no generó un archivo PDF válido.")
            
        return str(output_pdf)

    def cleanup(self):
        """Elimina el directorio temporal."""
        try:
            self._tmp.cleanup()
        except:
            pass
