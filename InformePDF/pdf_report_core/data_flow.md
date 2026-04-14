# Flujo de Datos Técnico - Generación de Informe PDF

Este documento técnico detalla la arquitectura y el flujo de información implementado para la extraccion de datos, generación de gráficas y posterior ensamblaje del Informe PDF mediante plantillas Typst.

## 1. Fuentes de Datos (Capa de Ingesta)
El sistema se nutre de diversos archivos Parquet pre-procesados que contienen el consolidado estadístico. El motor en Pandas/Polars utiliza fundamentalmente:
- **`df_snies` / `df_pcurso` / `df_matricula` / `df_graduados`**: Contienen indicadores de entrada, matrícula y titulados (SNIES).
- **`df_ole` / `df_salarios`**: Indicadores del Observatorio Laboral para la Educación y cotizaciones laborales.
- **`df_desercion`**: KPIs de abandono inter-semestral y anual (SPADIES).
- **`df_saber`**: Resultados de la prueba del estado (Saber Pro).

## 2. Definición del Universo o Filtro Base
El paso crucial para inicializar el reporte recae en determinar sobre *qué* datos operará. En el entorno Shiny (y por extensión en la abstracción actual), se construye una lista de códigos DIVIPOLA (códigos territoriales) y filtros específicos mediante:
- Filtros por: `Sector`, `Nivel de Formación`, `Carácter Académico`.
- Extracción de llaves cruzadas (`valid_divipolas()`) para asegurar que todos los cruces apunten exactamente al grupo de IES, programas o sedes que el usuario seleccionó.

## 3. Procesamiento y Cálculo de KPIs (Capa Lógica)
Una extensa colección de funciones se encarga de agrupar y hacer cálculos matemáticos sobre el *universo filtrado*:
- **KPIs Resumidos**: Funciones tipo `calc_total_matriculados()` efectúan un `.group_by()` y retornan el valor de la última medición (o un promedio). 
- **Funciones de Tabla:** Funciones como `calc_table_pcurso()` estructuran el dataset final convirtiéndolo de Polars/Pandas a diccionarios que entrarán a Tipst en formato de grilla.
- **Gráficas Plotly (`calc_plot_*`)**: Cada sección temática (SNIES, OLE, Deserción, SaberPRO) está provista de constructores analíticos, por ejemplo `calc_plot_primer_curso_total()`, los cuales:
  1. Filtran los datos con los DIVIPOLAs y años relevantes.
  2. Inicializan objetos de `plotly.graph_objects` o `plotly.express`.
  3. Estilizan bajo reglas corporativas (Colores hexadecimales unificados).

## 4. Estructuración del Motor (`_prepare_report_content`)
Un método orquestador recauda absolutamente todos los gráficos y KPIs y los integra de la siguiente manera:
1. Instancia el manejador temporal `ReportEngine`.
2. Captura dinámicamente las gráficas exportándolas como imágenes PNG en Kaleido (`engine.export_plotly_fig()`).
3. Almacena temporalmente los PNGs generados en un directorio `/temp`.
4. Devuelve un gran diccionario maestro llamado `data_ctx` que contiene tuplas `(título, valor)` para los KPIs y arreglos de strings con las rutas de las imágenes exportadas, además de las tablas pre-renderizadas como macros Typst (ej., `engine.format_as_typst_table()`).

## 5. Compilación del Reporte PDF (Motor Typst)
El eslabón final y corazón visual del PDF involucra el `ReportEngine.generate_report(data_ctx)`:
1. El motor inyecta el diccionario `data_ctx` creando un objeto gigantesco en memoria basado en sintaxis Typst (un lenguaje de markup moderno).
2. Va construyendo el `.typ` intercalando `macros` personalizadas (como `#kpi_grid()` o `#plot_grid()`).
3. Emplea la librería `typst-py` (`import typst`) que compila nativamente este archivo temporal junto al `logo_symbiotic.svg` y `report_template.typ`.
4. El entorno compila sin bloqueos hacia un archivo `informe.pdf` binario que es entonces servido de vuelta al cliente para su descarga.
