import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

def repl_px_line(m):
    full_match = m.group(0)
    if 'text=' in full_match:
        return full_match
    
    y_match = re.search(r'y=([\'\"]\w+[\'\"]|\w+)', full_match)
    if y_match:
        y_val = y_match.group(1)
        # remove text=... if existing? we already checked 'text='
        new_match = re.sub(r'markers=True', f'text={y_val}, markers=True', full_match)
        return new_match
    return full_match

new_content = re.sub(r'px\.line\([^)]+\)', repl_px_line, content)

lines = new_content.split('\n')
final_lines = []
for line in lines:
    final_lines.append(line)
    if re.search(r'^\s*fig\s*=\s*px\.line\(', line) and 'text=' in line:
        indent = line[:len(line) - len(line.lstrip())]
        # Just set textposition and use a default formatting which Plotly will auto-infer from hover (if not explicitly overridden)
        final_lines.append(indent + "fig.update_traces(textposition='top center', textfont=dict(size=12))")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(final_lines))

print('Patch applied successfully')
