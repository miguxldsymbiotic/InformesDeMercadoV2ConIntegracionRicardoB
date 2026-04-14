import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

def patch_histogram(m):
    full = m.group(0)
    if 'text_auto=' not in full:
        # Añadir text_auto='.1f' de forma segura
        # El regex extrae todo hasta el penúltimo char asumiendo que termina en )
        inside = full[13:-1]
        return f"px.histogram({inside}, text_auto='.1f')"
    return full

new_content = re.sub(r'px\.histogram\([^)]+\)', patch_histogram, content)

# Tambien asegurarnos de que la posición del texto en histogramas sea visible
lines = new_content.split('\n')
final_lines = []
for line in lines:
    final_lines.append(line)
    if re.search(r'^\s*fig\s*=\s*px\.histogram\(', line):
        indent = line[:len(line) - len(line.lstrip())]
        final_lines.append(indent + "fig.update_traces(textposition='outside', textfont=dict(size=11, color='#475569'))")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(final_lines))

print('Histograms patched')
