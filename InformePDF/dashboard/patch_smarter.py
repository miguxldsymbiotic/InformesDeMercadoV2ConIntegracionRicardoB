import re
import os

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

def inject_text_config(m):
    full_match = m.group(0)
    
    # Extraer la variable 'y'
    y_match = re.search(r'y=([\'\"])(.*?)\1', full_match)
    if not y_match:
        # Algunos px.line pueden no tener y explícito si se pasa un array, saltar
        return full_match
    
    y_val = y_match.group(2)
    
    # Asegurarnos de que tenga text= asociado a la misma variable
    if 'text=' not in full_match:
        modified_match = re.sub(r'markers=True', f'text="{y_val}", markers=True', full_match)
    else:
        modified_match = full_match
        
    return modified_match

# 1. Modificamos los px.line para asegurar text=y
content = re.sub(r'px\.line\([^)]+\)', inject_text_config, content)

# 2. Inyectar o reemplazar las actualizaciones de las trazas
lines = content.split('\n')
final_lines = []
skip_next_update_traces = False

for i, line in enumerate(lines):
    if skip_next_update_traces and 'fig.update_traces' in line and '# agregado auto' in line:
        continue # saltar inyecciones previas si las hay
        
    final_lines.append(line)
    
    if re.search(r'^\s*fig\s*=\s*px\.line\(', line) and 'text=' in line:
        indent = line[:len(line) - len(line.lstrip())]
        
        # Obtener el nombre de la variable y para deducir el formato
        y_match = re.search(r'y=([\'\"])(.*?)\1', line)
        if y_match:
            y_name = y_match.group(2).lower()
            
            if any(k in y_name for k in ['tasa', 'porcentaje', 'retencion', 'ratio', 'desercion', 'participacion', 'empleabilidad']):
                template = "%{text:.1%}"
            elif any(k in y_name for k in ['salario']):
                template = "$%{text:,.0f}" # o formato simple
            elif any(k in y_name for k in ['puntaje', 'punt']):
                template = "%{text:.1f}"
            else:
                template = "%{text:,.0f}" # Cantidades absolutas (sum, len, etc)
            
            # Formato custom para que los miles tengan punto si se puede
            # En plotly D3 d3-format, , es para separar miles. 
            # Reemplazaremos comas por puntos en post de frontend, pero texttemplate no permite replace.
            # Por ahora ,.0f es estandar claro.
            
            final_lines.append(indent + f"fig.update_traces(textposition='top center', texttemplate='{template}', textfont=dict(size=11, color='#475569'))")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(final_lines))

print('Smarter Patch applied successfully')
