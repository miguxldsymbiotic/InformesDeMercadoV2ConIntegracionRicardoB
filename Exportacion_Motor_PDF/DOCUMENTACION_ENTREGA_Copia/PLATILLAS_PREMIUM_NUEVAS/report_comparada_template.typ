// ============================================================
// Informe Comparativo de Programa — Template Typst
// SymbioTIC by UNIMINUTO
// ============================================================

// --- Colores del diseño ---
#let color_primary   = rgb("#31497e")   // Azul: Programa Base
#let color_secondary = rgb("#674f95")   // Púrpura: Grupo Comparable
#let color_accent    = rgb("#ffa600")   // Ámbar: Acentos
#let color_bg        = rgb("#f8f9fa")   // Gris claro: Fondos
#let color_text      = rgb("#333333")   // Cuerpo de texto
#let color_border    = rgb("#E2E8F0")   // Líneas divisoras
#let color_light_purple = rgb("#faf7fc") // Fondo sutil púrpura

// --- Template principal ---
#let comparada_template(
  title: "Informe Comparativo de Programa",
  program_name: "",
  snies_code: "",
  institution: "",
  nivel: "",
  modalidad: "",
  sector: "",
  departamento: "",
  nbc: "",
  area: "",
  n_comparables: 0,
  criterios_str: "",
  company: "UNIMINUTO — SymbioTIC",
  logo: "logo_symbiotic.svg",
  date: "",
  body
) = {
  // ---------- Configuración de Página ----------
  set page(
    paper: "a4",
    margin: (x: 2cm, y: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 {
        set text(7.5pt, gray)
        grid(
          columns: (1fr, 1fr),
          align(left, [#text(fill: color_primary, weight: "bold", "SNIES " + snies_code) — #program_name]),
          align(right, company)
        )
        v(2pt)
        line(length: 100%, stroke: 0.5pt + color_border)
      }
    },
    footer: context {
      set text(7.5pt, gray)
      line(length: 100%, stroke: 0.5pt + color_border)
      v(2pt)
      grid(
        columns: (1fr, 1fr),
        align(left, [Generado: #date]),
        align(right, [Página #counter(page).display() de #context counter(page).final().first()])
      )
    },
  )

  // ---------- Fuentes y estilos globales ----------
  set text(font: "Trebuchet MS", size: 9.5pt, lang: "es", fill: color_text)

  set table(
    inset: 5pt,
    stroke: 0.5pt + color_border,
    fill: (x, y) => if y == 0 { color_bg } else { none },
  )
  show table.cell.where(y: 0): set text(weight: "bold", fill: color_primary, size: 8.5pt)

  show heading: set text(fill: color_primary)
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(0.8em)
    block(
      width: 100%,
      below: 0.8em,
      [
        #rect(width: 4pt, height: 1.2em, fill: color_primary)
        #h(8pt)
        #text(16pt, weight: "bold", fill: color_primary, it.body)
      ]
    )
    line(length: 100%, stroke: 1.5pt + color_primary)
    v(0.5em)
  }

  show heading.where(level: 2): it => {
    v(0.6em)
    text(12pt, weight: "bold", fill: color_primary, it.body)
    v(0.3em)
  }

  // ========== PORTADA ==========
  page(margin: (x: 2.5cm, y: 2cm))[
    #set align(center)
    #v(2cm)
    #if logo != none {
      image(logo, width: 40%)
    }

    #v(2fr)

    #rect(
      width: 100%,
      fill: color_primary,
      radius: 6pt,
      inset: 20pt,
      [
        #set text(white)
        #text(24pt, weight: "bold", title) \
        #v(0.3em)
        #text(14pt, weight: "light", style: "italic", program_name) \
        #v(0.1em)
        #text(12pt, "SNIES " + snies_code)
      ]
    )

    #v(1fr)

    // Ficha técnica en grid
    #rect(
      width: 100%,
      fill: color_bg,
      radius: 4pt,
      inset: 14pt,
      stroke: 0.5pt + color_border,
      [
        #set text(9pt)
        #set align(left)
        #grid(
          columns: (1fr, 1fr),
          gutter: 6pt,
          [#text(weight: "bold", fill: color_primary, "Institución: ") #institution],
          [#text(weight: "bold", fill: color_primary, "Nivel: ") #nivel],
          [#text(weight: "bold", fill: color_primary, "Modalidad: ") #modalidad],
          [#text(weight: "bold", fill: color_primary, "Sector: ") #sector],
          [#text(weight: "bold", fill: color_primary, "Departamento: ") #departamento],
          [#text(weight: "bold", fill: color_primary, "NBC: ") #nbc],
          [#text(weight: "bold", fill: color_primary, "Área de Conocimiento: ") #area],
          [#text(weight: "bold", fill: color_primary, "Grupo Comparable: ") #str(n_comparables) + " programas"],
        )
        #if criterios_str != "" {
          v(6pt)
          text(8pt, fill: gray, style: "italic", "Criterios: " + criterios_str)
        }
      ]
    )

    #v(1fr)

    #line(length: 100%, stroke: 2pt + color_primary)
    #v(0.5em)
    #text(10pt, company) \
    #text(10pt, date)

    #v(1fr)
  ]

  // ========== TABLA DE CONTENIDO ==========
  outline(indent: auto, depth: 2)
  pagebreak()

  // ========== CUERPO ==========
  body
}

// ============================================================
// COMPONENTES REUTILIZABLES
// ============================================================

// --- KPI Duo: Programa vs Comparable lado a lado ---
#let kpi_duo(label, val_prog, val_comp) = {
  rect(
    width: 100%,
    fill: color_bg,
    radius: 4pt,
    inset: 8pt,
    stroke: (left: 3pt + color_primary, rest: 0.5pt + color_border),
    [
      #text(6.5pt, weight: "bold", fill: gray, upper(label)) \
      #v(2pt)
      #grid(
        columns: (1fr, 1fr),
        gutter: 4pt,
        [
          #text(6pt, fill: color_primary, weight: "bold", "PROGRAMA") \
          #text(13pt, weight: "bold", fill: color_primary, val_prog)
        ],
        [
          #text(6pt, fill: color_secondary, weight: "bold", "COMPARABLE") \
          #text(13pt, weight: "bold", fill: color_secondary, val_comp)
        ]
      )
    ]
  )
}

// --- KPI Solo (para un solo valor) ---
#let kpi_solo(label, value, accent: color_primary) = {
  rect(
    width: 100%,
    fill: color_bg,
    radius: 4pt,
    inset: 8pt,
    stroke: (left: 3pt + accent),
    [
      #set align(left)
      #text(6.5pt, weight: "bold", fill: gray, upper(label)) \
      #v(2pt)
      #text(14pt, weight: "bold", fill: accent, value)
    ]
  )
}

// --- Grid de KPIs (configuración flexible) ---
#let kpi_row(..items) = {
  grid(
    columns: (1fr,) * items.pos().len(),
    gutter: 10pt,
    ..items
  )
}

// --- Layout a dos columnas ---
#let two_col(left_content, right_content, ratio: (1fr, 1fr)) = {
  grid(
    columns: ratio,
    gutter: 14pt,
    left_content,
    right_content
  )
}

// --- Nota Técnica ---
#let tech_note(body) = {
  rect(
    width: 100%,
    fill: rgb("#fef9e7"),
    radius: 4pt,
    inset: 10pt,
    stroke: (left: 3pt + color_accent),
    [
      #text(7.5pt, weight: "bold", fill: color_accent, "NOTA TÉCNICA") \
      #v(2pt)
      #text(8pt, style: "italic", fill: rgb("#666666"), body)
    ]
  )
}

// --- Nota Metodológica ---
#let method_note(body) = {
  rect(
    width: 100%,
    fill: rgb("#eef2ff"),
    radius: 4pt,
    inset: 10pt,
    stroke: none,
    [
      #text(7.5pt, weight: "bold", fill: color_primary, "NOTA METODOLÓGICA") \
      #v(2pt)
      #text(8pt, style: "italic", fill: rgb("#444466"), body)
    ]
  )
}

// --- Bloque de imagen con caption ---
#let chart_block(img_path, caption: none) = {
  block(
    width: 100%,
    spacing: 0pt,
    [
      #image(img_path, width: 100%)
      #if caption != none {
        v(2pt)
        text(7.5pt, fill: gray, style: "italic", caption)
      }
    ]
  )
}

// --- Grid de 2 gráficas ---
#let chart_grid_2(img1, img2, caption1: none, caption2: none) = {
  grid(
    columns: (1fr, 1fr),
    gutter: 12pt,
    chart_block(img1, caption: caption1),
    chart_block(img2, caption: caption2)
  )
}

// --- Grid de 3 gráficas ---
#let chart_grid_3(img1, img2, img3) = {
  grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 10pt,
    chart_block(img1),
    chart_block(img2),
    chart_block(img3)
  )
}

// --- Separador de sección ---
#let section_divider() = {
  v(0.5em)
  line(length: 100%, stroke: 1pt + color_border)
  v(0.5em)
}

// --- Fuente footer de gráfica ---
#let chart_source(text_content) = {
  text(7pt, fill: gray, style: "italic", text_content)
}
