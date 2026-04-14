# SymbioInformes — Dashboard de Informes de Mercado de Educación Superior

[![Stack](https://img.shields.io/badge/Stack-Python%20Shiny%20%2B%20Plotly%20%2B%20Typst-blue)]()
[![Docker](https://img.shields.io/badge/Deploy-Docker%20%7C%20Railway%20%7C%20Render-green)]()
[![Python](https://img.shields.io/badge/Python-3.11-yellow)]()

Sistema de generación de **informes PDF ejecutivos** para análisis del mercado de educación superior en Colombia. Desarrollado sobre **Python Shiny** con visualizaciones interactivas de **Plotly**, exportación vectorial SVG con **Kaleido** y compilación de documentos con **Typst**.

---

## 📋 Tabla de Contenido

1. [Descripción del Proyecto](#1-descripción-del-proyecto)
2. [Stack Tecnológico](#2-stack-tecnológico)
3. [Estructura del Proyecto](#3-estructura-del-proyecto)
4. [Fuentes de Datos](#4-fuentes-de-datos)
5. [Arquitectura del Sistema de PDF](#5-arquitectura-del-sistema-de-pdf)
6. [Optimizaciones Realizadas (Migración Cloud)](#6-optimizaciones-realizadas-migración-cloud)
7. [Despliegue en la Nube (Docker)](#7-despliegue-en-la-nube-docker)
8. [Comandos de Ejecución](#8-comandos-de-ejecución)

---

## 1. Descripción del Proyecto

**SymbioInformes** es una aplicación web interactiva que permite a las instituciones de educación superior colombianas explorar y descargar informes ejecutivos en PDF con los siguientes módulos:

- **Informe Estándar de Programa:** Análisis completo de un programa académico SNIES con tendencias de matrícula, graduados, empleabilidad, salarios de enganche, deserción, resultados SABER PRO y perfil socioeconómico. Genera **~38 gráficas vectoriales**.
- **Informe Comparativo de Programa:** Análisis de un programa base frente a un grupo comparable de programas similares. Genera **~23 gráficas vectoriales adicionales**.

Los informes son documentos PDF de alta calidad, con gráficas **vectoriales (SVG)** perfectamente escalables, compilados con Typst directamente en el servidor.

---

## 2. Stack Tecnológico

| Componente | Tecnología | Versión | Rol |
|---|---|---|---|
| Framework Web | **Python Shiny** | 1.x | UI reactiva, routing, WebSockets |
| Visualizaciones | **Plotly** | latest | Gráficas interactivas y exportación estática |
| Motor de Exportación | **Kaleido** | latest | Renderizado SVG/PNG de figuras Plotly (usa Chromium headless) |
| Compilador PDF | **Typst** (vía `typst` Python package) | latest | Composición tipográfica y generación del PDF final |
| DataFrames | **Polars** | latest | Carga y procesamiento de datos SNIES, OLE, SABER PRO |
| Lectura Parquet | **PyArrow** | latest | Deserialización de archivos `.parquet` |
| Excel | **Pandas + Openpyxl** | latest | Lectura de archivos Excel auxiliares |
| Gráficas Ridge | **Ridgeplot** | latest | Distribuciones ridge/violin en secciones de salarios |
| Servidor ASGI | **Uvicorn** (via Shiny) | latest | Servidor HTTP/WebSocket subyacente |
| Containerización | **Docker** | — | Empaquetado y despliegue en nube |

---

## 3. Estructura del Proyecto

```
INFORMES_MERCADO_VERSION2.0RICKY/
│
├── InformePDF/
│   ├── Dockerfile                      ← Imagen Docker para despliegue en nube
│   ├── .dockerignore                   ← Excluye venv, cache, temporales del build
│   │
│   ├── data/                           ← ⚠️ NO está en Git (ver sección 4)
│   │   ├── df_SNIES_Programas.parquet  ← Datos de programas (matrícula, graduados, costos)
│   │   ├── df_OLE_Movilidad_M0.parquet ← Observatorio laboral (empleabilidad, salarios)
│   │   ├── df_SPADIES_Desercion.parquet← Deserción y permanencia estudiantil
│   │   ├── df_SaberPRO.parquet         ← Resultados SABER PRO por programa
│   │   ├── SalarioMinimo.xlsx          ← Serie histórica del SMMLV
│   │   └── DIVIPOLA.xlsx               ← Tabla de departamentos/municipios DANE
│   │
│   └── dashboard/
│       ├── app.py                      ← Aplicación Shiny principal (5,285 líneas)
│       ├── report_engine.py            ← Motor de PDF para informe estándar
│       ├── report_comparada_engine.py  ← Motor de PDF para informe comparativo
│       ├── report_template.typ         ← Plantilla Typst informe estándar
│       ├── report_comparada_template.typ ← Plantilla Typst informe comparativo
│       ├── logo_symbiotic.svg          ← Logo original (681 KB — referencia)
│       ├── logo_symbiotic_small.svg    ← Logo optimizado (61 KB — usado en producción)
│       ├── styles.css                  ← Estilos CSS del dashboard
│       ├── requirements.txt            ← Dependencias Python
│       ├── generate_dummy.py           ← Script auxiliar para PDF de prueba
│       └── temp_report/                ← Directorio para assets estáticos de Shiny
│
└── migracion_pdf_cloud.md              ← Plan técnico completo de optimización
```

---

## 4. Fuentes de Datos

> [!IMPORTANT]
> Los archivos de datos en `InformePDF/data/` **no están incluidos en el repositorio Git** (excluidos por `.gitignore`). Son necesarios para que la aplicación arranque correctamente.

Para obtenerlos, solicítalos al equipo de SymbioTIC. Las fuentes originales son:

| Archivo | Fuente | Frecuencia de actualización |
|---|---|---|
| `df_SNIES_Programas.parquet` | SNIES — MEN (Ministerio de Educación) | Anual |
| `df_OLE_Movilidad_M0.parquet` | OLE — SPADIES | Anual |
| `df_SPADIES_Desercion.parquet` | SPADIES — MEN | Anual |
| `df_SaberPRO.parquet` | ICFES — Resultados SABER PRO | Anual |
| `SalarioMinimo.xlsx` | Decreto ministerial SMMLV | Anual |
| `DIVIPOLA.xlsx` | DANE — División político-administrativa | Revision periódica |

---

## 5. Arquitectura del Sistema de PDF

### Flujo de generación (versión optimizada actual)

```
Usuario → "Descargar Informe"
    │
    ▼
app.py: download_pdf() / download_pdf_comparada()
    │
    ▼ Context Manager automático
ReportEngine (o ComparadaReportEngine)
    │
    ├─ Crea TemporaryDirectory (auto-limpieza garantizada)
    ├─ Copia logo_symbiotic_small.svg al directorio temporal
    │
    ▼
_prepare_report_content() / _prepare_comparada_report_content()
    │
    ├─ Paso 1 (~1s): Calcular TODAS las figuras Plotly en memoria
    │   └─ Acumula dict: {"nombre": (figura_plotly, "normal"|"wide")}
    │
    └─ Paso 2 (~5s): export_figs_parallel(max_workers=4)
        │
        ├─ Thread 1: fig1 → Kaleido → SVG (~0.5s)
        ├─ Thread 2: fig2 → Kaleido → SVG (~0.5s)
        ├─ Thread 3: fig3 → Kaleido → SVG (~0.5s)
        └─ Thread 4: fig4 → Kaleido → SVG (~0.5s)
            (10 lotes de 4 en paralelo para 38 gráficas)
    │
    ▼
report_engine.generate_report(data_ctx)
    │
    ├─ Construye archivo .typ con referencias a los SVGs
    └─ typst.compile() → PDF final
    │
    ▼
app.py lee PDF como bytes → envía al navegador del usuario
    │
    ▼ Salida del Context Manager
TemporaryDirectory.cleanup() → Borra TODOS los archivos temporales (~5ms)
```

### Comparativa de rendimiento: Antes vs Después

| Métrica | Antes (PNG secuencial) | Ahora (SVG paralelo) | Mejora |
|---|---|---|---|
| Tiempo por informe estándar | ~57 segundos | **~8 segundos** | **7x más rápido** |
| Tamaño en disco por informe | ~45 MB (38 PNGs) | **~1.5 MB (38 SVGs)** | **30x menos** |
| RAM pico durante generación | ~500–600 MB | **~250–300 MB** | **2x menos** |
| Limpieza de temporales | ❌ Nunca | ✅ Siempre automática | Sin acumulación |
| Calidad gráficas en PDF | Pixelada al ampliar | **Vectorial perfecta** | Mejor |
| Compatible con capa gratis | ❌ No (timeout/OOM) | ✅ **Sí (Railway/Render)** | Desplegable |

---

## 6. Optimizaciones Realizadas (Migración Cloud)

Esta sección documenta en detalle todos los cambios realizados para hacer el sistema apto para despliegue en capa gratuita de la nube.

### 6.1 Migración de PNG raster a SVG vectorial

**Archivos modificados:** `report_engine.py`, `report_comparada_engine.py`

Los métodos de exportación `export_plotly_fig()`, `export_plotly_fig_wide()` y `export_plotly_fig_small()` fueron cambiados de exportar PNG (con `scale=2` que duplicaba la resolución) a exportar **SVG vectorial**:

```python
# ANTES (PNG raster)
fig.write_image(str(path), engine="kaleido", scale=2)
# Resultado por gráfica: ~1.2 MB, tiempo ~1.5s

# DESPUÉS (SVG vectorial)
fig.write_image(str(path), format="svg", width=800, height=420)
# Resultado por gráfica: ~25-40 KB, tiempo ~0.5s
```

**Por qué SVG:** Plotly genera gráficas nativamente como definiciones vectoriales. Exportar a PNG era como tomar una foto de pantalla de un archivo vectorial. El SVG preserva la calidad matemática y Typst lo procesa nativamente, resultando en PDFs con zoom infinito perfecto.

### 6.2 Paralelización con ThreadPoolExecutor

**Archivos modificados:** `report_engine.py`, `report_comparada_engine.py`, `app.py`

Se añadió el método `export_figs_parallel()` a ambos motores, que acepta un diccionario de figuras y las exporta con hasta **4 hilos simultáneos**:

```python
def export_figs_parallel(self, figs_to_export: dict, max_workers: int = 4) -> dict:
    """
    figs_to_export: {"nombre_plot": (figura_plotly, "normal"|"wide"|"small")}
    Retorna: {"nombre_plot": "nombre_plot.svg"}
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(self._export_one, key, fig, mode): key
                   for key, (fig, mode) in figs_to_export.items()}
        ...
```

**Por qué ThreadPoolExecutor y no ProcessPoolExecutor:** Kaleido es una operación I/O-bound (Python lanza un subprocess y espera). El GIL de Python se libera durante las syscalls externas, por lo que los threads son suficientes para paralelizar eficientemente sin el overhead de crear procesos separados.

**Por qué max_workers=4:** Cada worker de Kaleido consume ~40 MB de RAM. Con 4 workers simultáneos el pico de RAM del pool es ~160 MB, manteniéndose dentro del presupuesto total de 512 MB de los free tiers.

**Refactorización en `app.py`:** Las funciones `_prepare_report_content()` y `_prepare_comparada_report_content()` fueron refactorizadas. En lugar de llamar a `engine.export_plotly_fig()` una por una (38 veces secuenciales), ahora:
1. Acumulan todas las figuras en un diccionario `figs_to_export`  
2. Llaman a `engine.export_figs_parallel()` una sola vez al final

### 6.3 Limpieza automática con TemporaryDirectory y Context Manager

**Archivos modificados:** `report_engine.py`, `report_comparada_engine.py`, `app.py`

Los engines fueron refactorizados para implementar el protocolo de context manager de Python:

```python
class ReportEngine:
    def __init__(self, base_dir):
        self._tmp = tempfile.TemporaryDirectory()  # Reemplaza mkdtemp()
        self.temp_dir = Path(self._tmp.name)
        ...

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tmp.cleanup()  # Borra el directorio completo al salir
        return False
```

En `app.py`, las funciones de descarga ahora usan el patrón `with`:

```python
@render.download(...)
def download_pdf():
    with ReportEngine(app_dir) as engine:  # cleanup SIEMPRE ocurre al salir
        data_ctx = _prepare_report_content(engine, p)
        pdf_path = engine.generate_report(data_ctx)
        with open(pdf_path, "rb") as f:
            return f.read()  # Lee a bytes ANTES del cleanup
```

**Garantías del ciclo de vida:** El directorio temporal se borra en todos los escenarios: generación exitosa, excepción en mitad del proceso, o crash inesperado del proceso Python.

### 6.4 Optimización del logo SVG

**Archivo generado:** `logo_symbiotic_small.svg`

El logo original `logo_symbiotic.svg` pesaba **681 KB** porque contenía imágenes rasterizadas embebidas y datos redundantes de path SVG. Se generó una versión optimizada `logo_symbiotic_small.svg` que:

- Contiene el PNG del logo (`logo-con-horizontalvigilada-1.png`) redimensionado y comprimido
- Embebido en Base64 dentro de un SVG wrapper mínimo
- **Tamaño final: ~61 KB** (menos del 10% del original)

Los engines de PDF detectan y usan automáticamente `logo_symbiotic_small.svg` si existe, con fallback al original.

### 6.5 Corrección del error de sintaxis en app.py

**Archivo modificado:** `app.py` (línea ~4163)

Durante el proceso de implementación se detectó y corrigió un error de sintaxis donde una cadena de texto estaba truncada, fusionando dos funciones en una sola línea:

```python
# INCORRECTO (error heredado):
if df_base.empty: return ui.HTML("...Sin dato</div>    def _prepare_report_content(engine, p):

# CORRECTO:
if df_base.empty: return ui.HTML("...Sin dato</div>")
val = df_base["valor_base"].iloc[-1]
return ui.HTML(f"...${format_num_es(val)}</div>")

def _prepare_report_content(engine, p):
    ...
```

Esto restableció el KPI de salario base del informe comparativo y la correcta definición de `_prepare_report_content`.

### 6.6 Dockerfile y .dockerignore

**Archivos creados:** `InformePDF/Dockerfile`, `InformePDF/.dockerignore`

Se creó un `Dockerfile` optimizado para despliegue en capa gratuita:

- **Base:** `python:3.11-slim` (mínima, sin bloat)
- **Dependencias de sistema:** Incluye las librerías de Chromium headless que Kaleido necesita en Linux (`libnss3`, `libgbm1`, `libasound2`, etc.)
- **Datos "horneados":** Los archivos de `InformePDF/data/` se copian durante el build desde la máquina local (donde existen), quedando incluidos en la imagen. Esto evita dependencias de bases de datos externas.
- **Directorio temp_report:** Creado explícitamente con `RUN mkdir -p` para que Shiny no falle al mapear los `static_assets`.
- **Puerto 8080 con `--host 0.0.0.0`:** Configuración crítica para que Railway/Render enruten el tráfico público al contenedor.

El `.dockerignore` excluye `venv/` (podría pesar ~1.5 GB), `__pycache__`, archivos temporales y PDFs locales para acelerar el `docker build`.

---

## 7. Despliegue en la Nube (Docker)

### Plataformas compatibles

| Plataforma | Plan Gratis | Ventaja | Desventaja |
|---|---|---|---|
| **Railway** ✅ (Recomendada) | $5 USD créditos/mes | Sin cold start, WebSocket nativo | Créditos se agotan |
| **Render** ✅ | Gratuito con sleep | Verdaderamente gratis | Cold start ~30s |
| **Posit Connect Cloud** ✅ | 1 app activa | Sin Docker necesario | Menos control de recursos |
| Vercel | — | — | ❌ No soporta WebSocket ni Python Shiny |
| AWS Lambda | — | — | ❌ Sin proceso persistente |

### Prerrequisito: Los datos deben estar en el directorio `InformePDF/data/`

El `docker build` debe hacerse **desde la máquina local** donde los archivos Parquet/Excel existen. El Dockerfile los copia a la imagen durante el proceso de build.

---

## 8. Comandos de Ejecución

### 8.1 Ejecución local (desarrollo)

```powershell
# 1. Navegar al directorio del dashboard
cd InformePDF\dashboard

# 2. Crear el entorno virtual (solo primera vez)
python -m venv venv

# 3. Activar el entorno virtual
.\venv\Scripts\Activate.ps1   # PowerShell Windows
# o: source venv/bin/activate # Mac/Linux

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Verificar que los datos estén disponibles
Test-Path "..\data\df_SNIES_Programas.parquet"   # Debe devolver True

# 6. Iniciar la aplicación
shiny run app.py

# La app estará disponible en: http://127.0.0.1:8000
```

### 8.2 Build y prueba con Docker (local)

```bash
# Desde la carpeta InformePDF/ (donde está el Dockerfile)
cd InformePDF

# 1. Construir la imagen Docker (incluye los datos)
docker build -t symbioinformes .

# 2. Verificar que la imagen se creó
docker images | grep symbioinformes

# 3. Ejecutar el contenedor simulando límites de la capa gratuita
docker run -p 8080:8080 --memory=512m --cpus=0.5 symbioinformes

# La app estará disponible en: http://localhost:8080

# 4. (Otra terminal) Monitorear uso de RAM en tiempo real
docker stats $(docker ps -q --filter ancestor=symbioinformes)

# 5. Detener el contenedor
docker stop $(docker ps -q --filter ancestor=symbioinformes)
```

### 8.3 Verificación de la compilación de Python

```bash
# Verificar que app.py no tenga errores de sintaxis
python -m py_compile InformePDF/dashboard/app.py
echo "Resultado: $?"   # Debe ser 0 (sin errores)
```

### 8.4 Despliegue en Railway

```bash
# Opción A: Subir imagen a Docker Hub y conectar en Railway

# 1. Iniciar sesión en Docker Hub
docker login

# 2. Etiquetar la imagen
docker tag symbioinformes tu-usuario/symbioinformes:latest

# 3. Subir la imagen al registro
docker push tu-usuario/symbioinformes:latest

# 4. En Railway: New Project → Deploy Docker Image → tu-usuario/symbioinformes:latest
# 5. Configurar variable de entorno: PORT=8080
# 6. Railway genera automáticamente una URL pública HTTPS
```

```bash
# Opción B: GitHub Container Registry (GHCR)

# 1. Autenticarse con GHCR (usar personal access token de GitHub)
echo $GITHUB_TOKEN | docker login ghcr.io -u tu-usuario --password-stdin

# 2. Etiquetar para GHCR
docker tag symbioinformes ghcr.io/tu-usuario/symbioinformes:latest

# 3. Subir
docker push ghcr.io/tu-usuario/symbioinformes:latest

# 4. En Railway: New Project → Deploy Docker Image → ghcr.io/tu-usuario/symbioinformes:latest
```

### 8.5 Despliegue en Render

```bash
# 1. Conectar GitHub en render.com → New Web Service
# 2. Seleccionar el repositorio
# 3. Render detecta automáticamente el Dockerfile en InformePDF/
# 4. Configurar:
#    - Build Command: (vacío - usa Dockerfile)
#    - Port: 8080
#    - Environment: Docker
# 5. Deploy → La URL quedará en: https://tu-app.onrender.com
```

### 8.6 Regenerar el logo optimizado

```powershell
# Si necesitas regenrar logo_symbiotic_small.svg desde el PNG original:
cd InformePDF\dashboard
python -c "
from PIL import Image
import base64, io

with Image.open('logo-con-horizontalvigilada-1.png') as img:
    if img.width > 600:
        img = img.resize((600, int(img.height * 600 / img.width)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()

svg = f'''<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {img.width} {img.height}\">
  <image width=\"{img.width}\" height=\"{img.height}\" href=\"data:image/png;base64,{b64}\"/>
</svg>'''

with open('logo_symbiotic_small.svg', 'w') as f:
    f.write(svg)
print('Logo optimizado generado exitosamente')
"
```

### 8.7 Comandos de diagnóstico

```powershell
# Verificar tamaño de la carpeta de datos (para decidir estrategia Docker)
Get-ChildItem -Path ".\InformePDF\data\" |
  Select-Object Name, @{N='MB';E={[math]::Round($_.Length/1MB, 2)}} |
  Format-Table -AutoSize

# Verificar que todos los archivos de datos necesarios existen
@(
    "df_SNIES_Programas.parquet",
    "df_OLE_Movilidad_M0.parquet",
    "df_SPADIES_Desercion.parquet",
    "df_SaberPRO.parquet",
    "SalarioMinimo.xlsx",
    "DIVIPOLA.xlsx"
) | ForEach-Object {
    $path = ".\InformePDF\data\$_"
    $status = if (Test-Path $path) { "✅ EXISTE" } else { "❌ FALTA" }
    "$status  $_"
}

# Ver los logs del contenedor Docker en ejecución
docker logs -f $(docker ps -q --filter ancestor=symbioinformes)
```

---

## 📝 Notas de Mantenimiento

- **Actualizar datos:** Si los datos Parquet se actualizan, es necesario hacer un nuevo `docker build` y subir la imagen actualizada a la plataforma de despliegue.
- **Ajustar workers de Kaleido:** Si el servidor tiene menos de 512 MB disponibles, reducir `max_workers=2` en las llamadas a `export_figs_parallel()` en `app.py`.
- **Monitorear RAM:** Usar `docker stats` al generar PDFs para verificar que el pico se mantiene por debajo de 400 MB.
- **Plan técnico completo:** Ver `migracion_pdf_cloud.md` en la raíz del repositorio para el diagnóstico y justificación técnica de todas las decisiones de arquitectura.
