import re

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

final_lines = []
for i, line in enumerate(lines):
    new_line = line
    
    # Arreglar la inyeccion de texto para px.line ignorado por el regex anterior
    if 'fig = px.line(' in new_line and 'markers=True' in new_line and 'text=' not in new_line:
        # Extraer 'y' sea lo que sea
        y_match = re.search(r'y=([\'\"])(.*?)\1', new_line)
        if y_match:
            y_val = y_match.group(2)
            new_line = new_line.replace('markers=True', f'text="{y_val}", markers=True')
        else:
            # Maybe y is a variable like y=column
            y_match2 = re.search(r'y=([a-zA-Z0-9_]+)', new_line)
            if y_match2:
                y_val = y_match2.group(1)
                new_line = new_line.replace('markers=True', f'text={y_val}, markers=True')
                
    final_lines.append(new_line)
    
    # Inyectar la actualizacion de trazas para px.line que acabamos de alterar o que ya estaban
    if 'fig = px.line(' in new_line and 'markers=True' in new_line:
        # Solo inyectar si la siguiente linea no es ya un fig.update_traces
        next_line = lines[i+1] if i+1 < len(lines) else ""
        if 'fig.update_traces(textposition' not in next_line:
            indent = new_line[:len(new_line) - len(new_line.lstrip())]
            
            y_match = re.search(r'y=([\'\"])(.*?)\1', new_line)
            y_name = y_match.group(2).lower() if y_match else ""
            if not y_match:
                y_match2 = re.search(r'y=([a-zA-Z0-9_]+)', new_line)
                y_name = y_match2.group(1).lower() if y_match2 else ""
            
            if any(k in y_name for k in ['tasa', 'porcentaje', 'retencion', 'ratio', 'desercion', 'participacion', 'empleabilidad']):
                template = "%{text:.1%}"
            elif any(k in y_name for k in ['salario']):
                template = "$%{text:,.0f}"
            elif any(k in y_name for k in ['puntaje', 'punt']):
                template = "%{text:.1f}"
            else:
                template = "%{text:,.0f}"
                
            final_lines.append(indent + f"fig.update_traces(textposition='top center', texttemplate='{template}', textfont=dict(size=11, color='#475569')) # auto")

    # Hacer las barras mas delgadas
    if 'def calc_plot_dist_empleabilidad_sexo():' in line or \
       'def calc_plot_dist_dependientes_sexo():' in line or \
       'def calc_plot_dist_empleabilidad():' in line or \
       'def calc_plot_dist_dependientes():' in line:
        pass # Not here, we will look for their fig.update_layout

for i, line in enumerate(final_lines):
    # Encontrar update_layouts de los OLE bars y añadir bargap
    if 'fig.update_layout(' in line and 'plot_bgcolor' in line:
        # Miremos unas lineas atras si se trata de px.bar
        is_ole_bar = False
        for j in range(max(0, i-5), i):
            if 'px.bar(' in final_lines[j] and 'text_auto=".1%"' in final_lines[j]:
                is_ole_bar = True
        if is_ole_bar:
            if 'bargap=' not in line:
                final_lines[i] = line.replace("fig.update_layout(", "fig.update_layout(bargap=0.4, ")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(final_lines))

print('Final patch applied')
