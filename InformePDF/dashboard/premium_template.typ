#let colors = (
  noche: rgb("#0D1B2A"),
  marino: rgb("#1E3A5F"),
  acento: rgb("#2563EB"),
  blanco: rgb("#FFFFFF"),
  hueso: rgb("#F8F9FB"),
  hielo: rgb("#EBF3FF"),
  pizarra: rgb("#64748B"),
  oscuro: rgb("#1E293B"),
  borde: rgb("#E2E8F0"),
  verde: rgb("#10B981"),
  rojo: rgb("#DC2626"),
  ambar: rgb("#F59E0B")
)

#let standard-footer() = context {
  set text(size: 8pt, fill: colors.pizarra)
  line(length: 100%, stroke: 0.5pt + colors.borde)
  v(2mm)
  grid(
    columns: (auto, 1fr, auto),
    column-gutter: 10pt,
    align(horizon)[ #image("logo_symbiotic_main.png", height: 12pt) ],
    align(horizon)[ #text(weight: 700, fill: colors.marino)[SymbioInformes] · Inteligencia Analítica Educativa ],
    align(horizon)[ Pág. #counter(page).display() ]
  )
}

#let project(
  title: "",
  subtitle: "",
  description: "",
  institution: "",
  program: "",
  date: "",
  body
) = {
  // SETTINGS GLOBALES
  set document(title: title)
  set text(font: ("Inter", "Helvetica", "Arial", "sans-serif"), fill: colors.oscuro, size: 10pt)
  
  // PORTADA
  page(
    paper: "a4",
    margin: (top: 28mm, bottom: 20mm, left: 18mm, right: 18mm),
    fill: gradient.linear(colors.noche, rgb("#0a2540"), rgb("#0D2B52"), angle: 145deg),
    header: none,
    footer: none,
  )[
    #set text(fill: colors.blanco)
    
    #place(top + left)[
      #image("logo_symbiotic_main.png", height: 65pt)
    ]
    
    #align(bottom)[
      #block[
        #box(fill: colors.acento.transparentize(75%), stroke: 1pt + colors.acento.transparentize(50%), radius: 1em, inset: (x: 12pt, y: 5pt))[
          #text(fill: rgb("#93C5FD"), weight: 600, size: 9pt, tracking: 1pt, upper(subtitle))
        ]
        
        #v(5mm)
        #text(weight: 900, size: 36pt, title)
        
        #v(2mm)
        #line(length: 50pt, stroke: 3pt + colors.acento)
        
        #v(5mm)
        #box(width: 85%)[
          #text(fill: rgb("#93C5FD"), size: 12pt, description)
        ]
        
        #v(10mm)
        #grid(
          columns: (auto, auto, auto),
          gutter: 32pt,
          [
            #text(size: 8pt, fill: colors.pizarra, weight: 600, tracking: 1pt, upper("Institución"))\
            #v(2pt)
            #text(size: 11pt, weight: 700, institution)
          ],
          [
            #text(size: 8pt, fill: colors.pizarra, weight: 600, tracking: 1pt, upper("Programa · SNIES"))\
            #v(2pt)
            #text(size: 11pt, weight: 700, program)
          ],
          [
            #text(size: 8pt, fill: colors.pizarra, weight: 600, tracking: 1pt, upper("Corte de datos"))\
            #v(2pt)
            #text(size: 11pt, weight: 700, date)
          ]
        )
      ]
    ]
  ]

  // Configuración base para el resto de páginas
  set page(
    paper: "a4",
    margin: (x: 18mm, top: 22mm, bottom: 20mm),
    fill: colors.hueso,
    header: none,
    footer: standard-footer()
  )
  counter(page).update(2)
  body
}

// MACROS COMPONENTES

#let section-page(num: "", title: "", bg: colors.hueso, body) = {
  page(
    fill: bg,
    header: none,
    footer: standard-footer()
  )[
    // Header block
    #place(top + left, dx: -18mm, dy: -22mm)[
      #block(
        width: 210mm,
        fill: if num == "Índice" { colors.noche } else if num == "Anexos" { colors.pizarra } else { colors.marino },
        inset: (x: 18mm, top: 14pt, bottom: 14pt)
      )[
        #set text(fill: colors.blanco)
        #grid(
          columns: (auto, 1fr),
          gutter: 10pt,
          align(horizon)[
            #if num not in ("Índice", "Anexos") [
              #text(fill: rgb("#60A5FA"), weight: 900, size: 18pt)[#num]
            ]
          ],
          align(horizon)[
            #text(weight: 700, size: 14pt, upper(title))
          ]
        )
        // El "corte" inclinado derecho
        #place(top + right, dx: 0pt, dy: 0pt)[
           #polygon(
             fill: bg,
             (0pt, 0pt),
             (28pt, 0pt),
             (28pt, 48pt), // Ajustado a la altura del bloque aproximadamente
           )
        ]
      ]
    ]
    #v(35pt)
    
    #body
  ]
}

#let insight-box(icon: "📌", text-content: "", border-c: "acento") = {
  let border-color = colors.at(border-c, default: colors.acento)
  block(
    fill: colors.hielo,
    stroke: (left: 4pt + border-color),
    radius: (right: 8pt),
    inset: 12pt,
    width: 100%,
    breakable: false
  )[
    #grid(
      columns: (auto, 1fr),
      column-gutter: 10pt,
      align(top)[#text(size: 14pt)[#icon]],
      align(horizon)[
        #text(size: 10pt, fill: colors.noche, weight: 500, text-content)
      ]
    )
  ]
}

#let intro-text(content) = [
  #text(size: 11pt, fill: colors.oscuro, content)
]

#let kpi-row(..cards) = {
  grid(
    columns: cards.pos().map(x => 1fr),
    gutter: 12pt,
    ..cards
  )
}

#let kpi-card(label: "", value: "", trend: "", type: "up") = {
  let trend-color = if type == "up" { colors.verde } else if type == "down" { colors.rojo } else { colors.pizarra }
  block(
    fill: colors.blanco,
    stroke: 1pt + colors.borde,
    radius: 8pt,
    inset: 12pt,
    width: 100%
  )[
    #text(size: 8pt, weight: 600, fill: colors.pizarra, tracking: 0.8pt, upper(label))\
    #v(4pt)
    #text(size: 20pt, weight: 800, fill: colors.acento)[#value]\
    #v(4pt)
    #text(size: 9pt, weight: 600, fill: trend-color)[#trend]
  ]
}

#let kpi-duo(label: "", val-prog: "", val-comp: "", trend: "", type: "up") = {
  let trend-color = if type == "up" { colors.verde } else if type == "down" { colors.rojo } else { colors.pizarra }
  block(
    fill: colors.blanco,
    stroke: 1pt + colors.borde,
    radius: 8pt,
    inset: 12pt,
    width: 100%
  )[
    #text(size: 8pt, weight: 600, fill: colors.pizarra, tracking: 0.8pt, upper(label))\
    #v(6pt)
    #grid(
      columns: (1fr, 1fr),
      gutter: 8pt,
      [
        #text(size: 7pt, weight: 700, fill: colors.marino, upper("Programa"))\
        #v(2pt)
        #text(size: 16pt, weight: 800, fill: colors.acento)[#val-prog]
      ],
      [
        #text(size: 7pt, weight: 700, fill: colors.pizarra, upper("Comparable"))\
        #v(2pt)
        #text(size: 16pt, weight: 800, fill: colors.marino)[#val-comp]
      ]
    )
    #if trend != "" [
      #v(4pt)
      #text(size: 8pt, weight: 600, fill: trend-color)[#trend]
    ]
  ]
}

#let chart-wrap(title: "", source: "", height: 160pt, body) = {
  block(
    fill: colors.blanco,
    stroke: 1pt + colors.borde,
    radius: 8pt,
    inset: 12pt,
    width: 100%,
    breakable: false
  )[
    #grid(
      columns: (1fr, auto),
      [#text(size: 11pt, weight: 700, fill: colors.marino, title)],
      [#text(size: 8pt, weight: 400, fill: colors.pizarra, source)]
    )
    #v(8pt)
    #block(height: height, width: 100%, align(center + horizon)[#body])
  ]
}

#let toc-item(num: "00", title: "", page-num: "", dark: false, bg: false) = {
  let num-bg = if dark { colors.pizarra } else { colors.marino }
  block(
    fill: if bg { colors.hielo } else { none },
    stroke: (bottom: 1pt + colors.borde),
    inset: (left: 14pt, right: 14pt, top: 10pt, bottom: 10pt),
    width: 100%
  )[
    #grid(
      columns: (auto, 1fr, auto),
      gutter: 14pt,
      align(horizon)[
        #box(fill: num-bg, radius: 4pt, inset: (x: 6pt, y: 4pt))[
          #text(fill: colors.blanco, weight: 800, size: 11pt)[#num]
        ]
      ],
      align(horizon)[
        #text(size: 12pt, weight: 600, fill: colors.oscuro)[#title]
      ],
      align(horizon)[
        #text(size: 10pt, weight: 700, fill: colors.acento)[Pág. #page-num]
      ]
    )
  ]
}

#let param-card(title: "", icon: "", items: (), style: "light") = {
  let bg = if style == "dark" { colors.noche } else if style == "blue" { colors.hielo } else { colors.blanco }
  let border-c = if style == "dark" { none } else if style == "blue" { colors.acento.transparentize(80%) } else { colors.borde }
  let title-c = if style == "dark" { rgb("#93C5FD") } else { colors.marino }
  let key-c = if style == "dark" { rgb("#93C5FD") } else { colors.pizarra }
  let val-c = if style == "dark" { colors.blanco } else { colors.oscuro }
  let icon-bg = if style == "dark" { colors.acento.transparentize(80%) } else { colors.hielo }
  
  block(
    fill: bg,
    stroke: if style != "dark" { 1pt + border-c } else { none },
    radius: 8pt,
    inset: 14pt,
    width: 100%,
    height: 100%
  )[
    #box(fill: icon-bg, radius: 4pt, inset: 6pt)[#text(size: 14pt, icon)]
    #v(6pt)
    #text(fill: title-c, weight: 700, size: 11pt)[#title]
    #v(6pt)
    
    #for item in items [
      #box(width: 100%, stroke: (bottom: 0.5pt + if style == "dark" { colors.blanco.transparentize(90%) } else { colors.borde }), inset: (bottom: 4pt))[
        #grid(
          columns: (1fr, auto),
          [#text(fill: key-c, size: 9pt)[#item.at(0)]],
          [#text(fill: val-c, weight: 600, size: 9pt)[#item.at(1)]]
        )
      ]
      #v(4pt)
    ]
  ]
}

#let styled-table(columns: 1, headers: (), rows: ()) = {
  table(
    columns: columns,
    stroke: none,
    fill: (x, y) => if y == 0 { colors.noche } else if calc.even(y) { colors.hielo } else { colors.blanco },
    
    ..headers.map(h => 
      table.cell(fill: colors.noche)[
        #text(fill: colors.blanco, weight: 600, size: 9pt)[#h]
      ]
    ),
    
    ..rows.flatten().map(cell => 
      table.cell(
        stroke: (bottom: 1pt + colors.borde),
        inset: 6pt
      )[
        #text(size: 9pt)[#cell]
      ]
    )
  )
}

#let risk-tag(content) = {
  box(fill: colors.rojo.transparentize(90%), radius: 100pt, inset: (x: 8pt, y: 4pt))[
    #text(size: 8pt, weight: 700, fill: colors.rojo)[⚑ #content]
  ]
}

#let ok-tag(content) = {
  box(fill: colors.verde.transparentize(90%), radius: 100pt, inset: (x: 8pt, y: 4pt))[
    #text(size: 8pt, weight: 700, fill: colors.verde)[✓ #content]
  ]
}

#let salary-highlight(value: "", label: "", dark: false) = {
  let bg = if dark { gradient.linear(colors.pizarra, colors.oscuro, angle: 135deg) } else { gradient.linear(colors.marino, colors.acento, angle: 135deg) }
  block(
    fill: bg,
    radius: 10pt,
    inset: 20pt,
    width: 100%,
    align: center
  )[
    #text(size: 28pt, weight: 900, fill: colors.blanco)[#value]\
    #v(4pt)
    #text(size: 8pt, weight: 600, fill: colors.blanco.transparentize(20%), tracking: 1pt, upper(label))
  ]
}

#let nota(body) = {
  v(10pt)
  line(length: 100%, stroke: 0.5pt + colors.borde)
  v(4pt)
  text(size: 8pt, fill: colors.pizarra, body)
}

// ALIASES Y COMPONENTES COMPATIBILIDAD
#let kpi_row = kpi-row
#let kpi_duo(..args) = {
  let pos = args.pos()
  if pos.len() >= 3 {
    kpi-duo(label: pos.at(0), val-prog: pos.at(1), val-comp: pos.at(2))
  } else {
    kpi-duo(..args)
  }
}
#let kpi_card(..args) = {
  let pos = args.pos()
  if pos.len() >= 2 {
    kpi-card(label: pos.at(0), value: pos.at(1))
  } else {
    kpi-card(..args)
  }
}

#let tech_note(body) = {
  block(
    fill: colors.ambar.transparentize(90%),
    stroke: (left: 4pt + colors.ambar),
    radius: (right: 6pt),
    inset: 12pt,
    width: 100%,
    [
      #text(size: 8pt, weight: 800, fill: colors.ambar, upper("Nota Técnica"))\
      #v(4pt)
      #text(size: 9pt, fill: colors.oscuro, body)
    ]
  )
}

#let method_note(body) = {
  block(
    fill: colors.marino.transparentize(95%),
    stroke: (left: 4pt + colors.marino),
    radius: (right: 6pt),
    inset: 12pt,
    width: 100%,
    [
      #text(size: 8pt, weight: 800, fill: colors.marino, upper("Nota Metodológica"))\
      #v(4pt)
      #text(size: 9pt, fill: colors.oscuro, body)
    ]
  )
}

#let chart_block(img-path, caption: none) = {
  block(width: 100%)[
    #chart-wrap(height: auto)[#image(img-path)]
    #if caption != none {
      v(-8pt)
      align(center)[#text(size: 8pt, fill: colors.pizarra, style: "italic", caption)]
    }
  ]
}

#let chart_grid_2(img1, img2, caption1: none, caption2: none) = {
  grid(
    columns: (1fr, 1fr),
    gutter: 12pt,
    chart_block(img1, caption: caption1),
    chart_block(img2, caption: caption2)
  )
}

#let chart_source(text-content) = {
  text(size: 8pt, fill: colors.pizarra, style: "italic", text-content)
}

// ── ÍNDICE CON PAGINADO AUTOMÁTICO ──────────────────────────────────────────
// Usa el sistema de labels de Typst para detectar la página real de cada sección.
// Uso: coloca #h(0pt)<sec-lbl> al inicio del cuerpo de cada section-page.
#let auto-toc-item(num: "00", title: "", target: none, dark: false, bg: false) = {
  let num-bg = if dark { colors.pizarra } else { colors.marino }
  block(
    fill: if bg { colors.hielo } else { none },
    stroke: (bottom: 1pt + colors.borde),
    inset: (left: 14pt, right: 14pt, top: 10pt, bottom: 10pt),
    width: 100%
  )[
    #grid(
      columns: (auto, 1fr, auto),
      gutter: 14pt,
      align(horizon)[
        #box(fill: num-bg, radius: 4pt, inset: (x: 6pt, y: 4pt))[
          #text(fill: colors.blanco, weight: 800, size: 11pt)[#num]
        ]
      ],
      align(horizon)[
        #text(size: 12pt, weight: 600, fill: colors.oscuro)[#title]
      ],
      align(horizon)[
        #context {
          let pg-text = if target != none {
            let els = query(target)
            if els.len() > 0 {
              "Pág. " + str(counter(page).at(els.first().location()).first())
            } else { "—" }
          } else { "—" }
          text(size: 10pt, weight: 700, fill: colors.acento)[#pg-text]
        }
      ]
    )
  ]
}
