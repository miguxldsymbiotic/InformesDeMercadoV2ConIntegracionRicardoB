#import "premium_template.typ": *
#show: project.with(
  title: "Informe Ejecutivo de Educación Superior",
  subtitle: "Mesa de Reportes Estratégica",
  description: "Análisis integral del sector de educación superior bajo los filtros seleccionados.",
  institution: "Consolidado Nacional",
  program: "Todos los niveles",
  date: "14/04/2026",
)

#section-page(num: "Índice", title: "Contenido del Informe")[
  #v(20pt)
  #block(stroke: 1pt + colors.borde, radius: 10pt, clip: true)[
    #auto-toc-item(num: "01", title: "Resumen Ejecutivo", target: <sec-01>)
    #auto-toc-item(num: "02", title: "Tendencias SNIES (Oferta y Demanda)", target: <sec-02>)
    #auto-toc-item(num: "03", title: "Observatorio Laboral para la Educación (OLE)", target: <sec-03>)
    #auto-toc-item(num: "04", title: "Salarios de Enganche", target: <sec-04>)
    #auto-toc-item(num: "05", title: "Permanencia y Deserción (SPADIES)", target: <sec-05>)
    #auto-toc-item(num: "06", title: "Excelencia Académica (Prueba SABER PRO)", target: <sec-06>)
    #auto-toc-item(num: "07", title: "Perfil Socio-demográfico de los Evaluados", target: <sec-07>)
  ]
]

#section-page(num: "01", title: "Resumen Ejecutivo")[
  #h(0pt)<sec-01>

  Este documento técnico presenta un análisis integral del sector de educación superior bajo los filtros seleccionados. Producido por *SymbioTIC* (Startup de UNIMINUTO), este informe traduce grandes volúmenes de datos en inteligencia estratégica para la toma de decisiones en instituciones y organismos gubernamentales.

  #v(8pt)
  == Fuentes de Información y Calidad de Datos

  El análisis se sustenta en tres pilares de datos oficiales del Ministerio de Educación Nacional de Colombia, garantizando transparencia y rigor técnico:

  - *SNIES* (Sistema Nacional de Información de Educación Superior): #link("https://snies.mineducacion.gov.co/portal/")[Portal SNIES]. Es la fuente oficial de estadísticas sobre instituciones, programas académicos, matrícula y graduación. Corte: *2024.0*.
  - *OLE* (Observatorio Laboral para la Educación): #link("https://ole.mineducacion.gov.co/portal/")[Portal OLE]. Monitorea la vinculación laboral de los graduados, capturando datos de cotizaciones al régimen de seguridad social. Corte: *2022*.
  - *SPADIES* (Sistema para la Prevención de la Deserción): #link("https://www.mineducacion.gov.co/sistemasinfo/spadies/")[Portal SPADIES]. Analiza las trayectorias académicas para identificar riesgos de abandono y promover la permanencia. Corte: *2023*.

  #v(8pt)
  #method_note([Los KPIs y visualizaciones presentados reflejan el comportamiento consolidado de los programas académicos capturados por los filtros activos. La integración de estas tres fuentes permite una visión 360° desde la oferta académica hasta la empleabilidad real de los egresados.])
  #v(10pt)
  #kpi-row(
    kpi-card(label: "Instituciones", value: "1"),
    kpi-card(label: "Programas", value: "1"),
    kpi-card(label: "Matrícula Total", value: "921"),
    kpi-card(label: "Tasa Empleabilidad", value: "88,9%"),
  )
]

#section-page(num: "02", title: "Tendencias SNIES (Oferta y Demanda)")[
  #h(0pt)<sec-02>

  Esta sección analiza la evolución de la matrícula, los estudiantes de primer curso y los graduados. Permite identificar el flujo de entrada y salida del sistema de educación superior.

  #v(8pt)
  #kpi-row(
    kpi-card(label: "Primer Curso", value: "333"),
    kpi-card(label: "Matriculados", value: "921"),
    kpi-card(label: "Graduados", value: "198"),
  )
  #v(10pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Primer Curso Total", height: 150pt)[#image("pcurso_total.svg")],
    chart-wrap(title: "Matriculados Total", height: 150pt)[#image("matricula_total.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En esta gráfica se muestra la evolución total de estudiantes de Primer Curso entre 2016.0 y 2024.0. Durante el período, el indicador disminuyó un 63.0% ↓, pasando de 899 a 333 estudiantes.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[Esta gráfica presenta la evolución total de la matrícula entre 2016.0 y 2024.0. La matrícula decreció un 63.0% ↓, pasando de 2.488 a 921 matriculados.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Graduados Total", height: 150pt)[#image("graduados_total.svg")],
    chart-wrap(title: "Primer Curso por Sexo", height: 150pt)[#image("pcurso_sexo.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[Esta gráfica muestra la tendencia histórica de graduados entre 2016.0 y 2024.0. La graduación disminuyó un 24.4% ↓, con 198 graduados en el último año.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[Comparativa de Primer Curso por sexo en 2024.0: FEMENINO: 193 (58.0%), MASCULINO: 140 (42.0%). El grupo con mayor participación fue FEMENINO.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Matriculados por Sexo", height: 150pt)[#image("matricula_sexo.svg")],
    chart-wrap(title: "Graduados por Sexo", height: 150pt)[#image("graduados_sexo.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[Comparativa de Matriculados por sexo en 2024.0: FEMENINO: 536 (58.1%), MASCULINO: 386 (41.9%). El grupo con mayor participación fue FEMENINO.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[Comparativa de Graduados por sexo en 2024.0: FEMENINO: 124 (62.6%), MASCULINO: 74 (37.4%). El grupo con mayor participación fue FEMENINO.]],
  )
  #v(6pt)

]

#section-page(num: "03", title: "Observatorio Laboral para la Educación (OLE)")[
  #h(0pt)<sec-03>

  Métricas de vinculación laboral y movilidad de los graduados. Se analiza la capacidad de inserción en el mercado formal y el comportamiento geográfico de la fuerza laboral.

  #v(8pt)
  #kpi-row(
    kpi-card(label: "Tasa Empleabilidad", value: "88,9%"),
    kpi-card(label: "Retención Local", value: "56,8%"),
    kpi-card(label: "Ratio Migratorio", value: "1,00"),
  )
  #v(10pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Tasa de Empleabilidad", height: 150pt)[#image("ole_emp_total.svg")],
    chart-wrap(title: "Asalariados Dependientes", height: 150pt)[#image("ole_dep_total.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En el 2022, la Tasa de Empleabilidad muestra: : 88.9%.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En el 2022, la Tasa de Asalariados Dependientes muestra: : 83.3%.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Empleabilidad por Sexo", height: 150pt)[#image("ole_emp_sexo.svg")],
    chart-wrap(title: "Dependientes por Sexo", height: 150pt)[#image("ole_dep_sexo.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En el 2022, la Empleabilidad por Sexo muestra: FEMENINO: 89.6%. MASCULINO: 87.9%. La diferencia entre grupos es de 1.8%.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En el 2022, la Tasa de Dependientes por Sexo muestra: FEMENINO: 84.6%. MASCULINO: 81.5%. La diferencia entre grupos es de 3.1%.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Dist. Empleabilidad", height: 150pt)[#image("ole_dist_emp.svg")],
    chart-wrap(title: "Dist. Dependientes", height: 150pt)[#image("ole_dist_dep.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Dist. Empleabilidad (Sexo)", height: 150pt)[#image("ole_dist_emp_sexo.svg")],
    chart-wrap(title: "Dist. Dependientes (Sexo)", height: 150pt)[#image("ole_dist_dep_sexo.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Movilidad Departamental", height: 150pt)[#image("ole_mobility.svg")],
    [],
  )
  #text(size: 8.5pt, style: "italic", fill: colors.pizarra)[El mapa de movilidad departamental muestra una retención local del 56,8%. El ratio migratorio indica que por cada egresado que llega, 1,00 salen de la región de estudio.]
  #v(6pt)

]

#section-page(num: "04", title: "Salarios de Enganche")[
  #h(0pt)<sec-04>

  Análisis del ingreso de los graduados en su primer empleo formal. Se presentan distribuciones por rangos de SMMLV y evolución histórica ajustada.

  #v(8pt)
  #kpi-row(
    kpi-card(label: "Salario Promedio", value: "$ 2.154.868"),
    kpi-card(label: "Brecha Género (F)", value: "$ 2.084.559"),
    kpi-card(label: "Brecha Género (M)", value: "$ 2.225.177"),
  )
  #v(10pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Distribución Salarial", height: 150pt)[#image("sal_dist_total.svg")],
    chart-wrap(title: "Distribución Salarial (Sexo)", height: 150pt)[#image("sal_dist_sexo.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Evolución Salarial", height: 150pt)[#image("sal_evol_total.svg")],
    [],
  )
  #text(size: 8.5pt, style: "italic", fill: colors.pizarra)[La evolución salarial entre 2022 y 2022 muestra un salario promedio de 2154868.1 SMMLV en el último año.]
  #v(6pt)

]

#section-page(num: "05", title: "Permanencia y Deserción (SPADIES)")[
  #h(0pt)<sec-05>

  Análisis de la deserción anual promedio. Esta métrica es crítica para entender la eficiencia interna de los programas y la retención estudiantil.

  #v(8pt)
  #kpi-row(
    kpi-card(label: "Tasa Deserción", value: "9,7%"),
  )
  #v(10pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Distribución Tasa Deserción", height: 150pt)[#image("des_dist.svg")],
    chart-wrap(title: "Tendencia Deserción Histórica", height: 150pt)[#image("des_trend.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[La tendencia histórica de deserción entre 2016 y 2023 registró una tasa del 9.7% en el último período. La deserción aumentó un 3.4% ↑ respecto al inicio del período.]],
  )
  #v(6pt)

]

#section-page(num: "06", title: "Excelencia Académica (Prueba SABER PRO)")[
  #h(0pt)<sec-06>

  Resultados de las pruebas de Estado que evalúan las competencias genéricas de los estudiantes de último año. El puntaje global es un indicador de la calidad educativa.

  #v(8pt)
  #kpi-row(
    kpi-card(label: "Puntaje Global Promedio", value: "139,9"),
  )
  #v(10pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Puntaje Global", height: 150pt)[#image("saber_trend.svg")],
    chart-wrap(title: "Distribución Puntaje", height: 150pt)[#image("saber_dist.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[El puntaje global en Saber PRO entre 2016 y 2024 fue de 139.9 puntos en el último año. La tendencia muestra una reducción del 4.0% ↓ en el período.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Evaluados por Sexo", height: 150pt)[#image("saber_count_sexo.svg")],
    chart-wrap(title: "Evaluados por Edad", height: 150pt)[#image("saber_count_edad.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, la distribución por sexo muestra que 'FEMENINO' concentra el 60.7% de los evaluados (156 personas).]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, la distribución por grupo de edad muestra que '(15,25\]' concentra el 56.6% de los evaluados (146 personas).]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Puntaje Global por Sexo", height: 150pt)[#image("saber_global_sexo.svg")],
    chart-wrap(title: "Puntaje Global por Edad", height: 150pt)[#image("saber_global_edad.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Punt Global', el grupo 'MASCULINO' lideró con 143.2 puntos. Resto de grupos: FEMENINO: 137.8 puntos.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Punt Global', el grupo 'ND' lideró con 144.0 puntos. Resto de grupos: (15,25\]: 141.6, (25,35\]: 138.5, (35,45\]: 129.8, (45,55\]: 141.0 puntos.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Razonamiento Cuant. (Sexo)", height: 150pt)[#image("saber_razona_sexo.svg")],
    chart-wrap(title: "Razonamiento Cuant. (Edad)", height: 150pt)[#image("saber_razona_edad.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Mod Razona Cuantitat', el grupo 'MASCULINO' lideró con 146.7 puntos. Resto de grupos: FEMENINO: 136.6 puntos.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Mod Razona Cuantitat', el grupo '(45,55\]' lideró con 147.0 puntos. Resto de grupos: (15,25\]: 141.0, (25,35\]: 140.5, (35,45\]: 133.3, ND: 123.0 puntos.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Lectura Crítica (Sexo)", height: 150pt)[#image("saber_lectura_sexo.svg")],
    chart-wrap(title: "Lectura Crítica (Edad)", height: 150pt)[#image("saber_lectura_edad.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Mod Lectura Critica', el grupo 'MASCULINO' lideró con 145.4 puntos. Resto de grupos: FEMENINO: 142.6 puntos.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Mod Lectura Critica', el grupo 'ND' lideró con 162.0 puntos. Resto de grupos: (15,25\]: 146.4, (25,35\]: 141.0, (35,45\]: 131.1, (45,55\]: 137.0 puntos.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Competencias Ciudadanas (Sexo)", height: 150pt)[#image("saber_ciuda_sexo.svg")],
    chart-wrap(title: "Competencias Ciudadanas (Edad)", height: 150pt)[#image("saber_ciuda_edad.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Mod Competen Ciudada', el grupo 'MASCULINO' lideró con 144.2 puntos. Resto de grupos: FEMENINO: 134.6 puntos.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Mod Competen Ciudada', el grupo 'ND' lideró con 149.0 puntos. Resto de grupos: (15,25\]: 140.7, (25,35\]: 135.9, (35,45\]: 128.9, (45,55\]: 131.0 puntos.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Inglés (Sexo)", height: 150pt)[#image("saber_ingles_sexo.svg")],
    chart-wrap(title: "Inglés (Edad)", height: 150pt)[#image("saber_ingles_edad.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Mod Ingles', el grupo 'MASCULINO' lideró con 151.1 puntos. Resto de grupos: FEMENINO: 143.5 puntos.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Mod Ingles', el grupo 'ND' lideró con 199.0 puntos. Resto de grupos: (15,25\]: 147.3, (25,35\]: 146.8, (35,45\]: 127.1, (45,55\]: 166.0 puntos.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Comunicación Escrita (Sexo)", height: 150pt)[#image("saber_escrita_sexo.svg")],
    chart-wrap(title: "Comunicación Escrita (Edad)", height: 150pt)[#image("saber_escrita_edad.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Mod Comuni Escrita', el grupo 'FEMENINO' lideró con 131.7 puntos. Resto de grupos: MASCULINO: 128.5 puntos.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[En 2024, dentro de la dimensión 'Mod Comuni Escrita', el grupo '(15,25\]' lideró con 132.2 puntos. Resto de grupos: (25,35\]: 128.1, (35,45\]: 128.2, (45,55\]: 125.0, ND: 86.0 puntos.]],
  )
  #v(6pt)

]

#section-page(num: "07", title: "Perfil Socio-demográfico de los Evaluados")[
  #h(0pt)<sec-07>

  Caracterización demográfica y socioeconómica de los estudiantes que presentaron la prueba en el último año. Incluye la distribución por sexo, grupo de edad, carga laboral y estrato de vivienda.

  #v(8pt)
  #kpi-row(
    kpi-card(label: "Total de Evaluados", value: "257"),
    kpi-card(label: "Programas Académicos", value: "1"),
  )
  #v(10pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Estudiantes por Sexo", height: 150pt)[#image("demo_sexo.svg")],
    chart-wrap(title: "Estudiantes por Edad", height: 150pt)[#image("demo_edad.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Estudiantes por Trabajo", height: 150pt)[#image("demo_trabajo.svg")],
    chart-wrap(title: "Estudiantes por Estrato", height: 150pt)[#image("demo_estrato.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[No se encontraron datos disponibles para este indicador con los filtros seleccionados.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Tendencia por Sexo", height: 150pt)[#image("demo_sexo_trend.svg")],
    chart-wrap(title: "Tendencia por Edad", height: 150pt)[#image("demo_edad_trend.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[La tendencia por sexo entre 2016 y 2024 muestra que el grupo dominante es 'FEMENINO'. Este grupo creció un 8.1% ↑ en el período.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[La tendencia por edad entre 2016 y 2024 muestra que el grupo dominante es '(15,25\]'. Este grupo creció un 7.8% ↑ en el período.]],
  )
  #v(6pt)

  #grid(columns: (1fr, 1fr), gutter: 10pt,
    chart-wrap(title: "Tendencia por Trabajo", height: 150pt)[#image("demo_trabajo_trend.svg")],
    chart-wrap(title: "Tendencia por Estrato", height: 150pt)[#image("demo_estrato_trend.svg")],
  )
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[La tendencia por carga laboral entre 2016 y 2024 muestra que el grupo dominante es 'Más de 30 horas'. Este grupo creció un 3.8% ↑ en el período.]],
    [#text(size: 8.5pt, style: "italic", fill: colors.pizarra)[La tendencia por estrato entre 2016 y 2024 muestra que el grupo dominante es '2'. Este grupo decreció un 1.4% ↓ en el período.]],
  )
  #v(6pt)

]
