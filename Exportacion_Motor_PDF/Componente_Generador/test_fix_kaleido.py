import plotly.graph_objects as go
from kaleido.scopes.plotly import PlotlyScope
import time
from pathlib import Path

def test_fix():
    print(">>> Probando exportación con PlotlyScope.transform (Alternativa a write_image)...")
    fig = go.Figure(data=[go.Bar(y=[1, 3, 2])])
    
    start_time = time.time()
    try:
        print("Iniciando Scope...")
        scope = PlotlyScope()
        print(f"Scope iniciado en {time.time() - start_time:.2f}s")
        
        print("Transformando a SVG...")
        # Intentar transformar con un timeout manual si es posible (aunque scope.transform suele ser bloqueante)
        svg_data = scope.transform(fig, format="svg", width=800, height=420)
        print(f"ÉXITO: Generados {len(svg_data)} bytes en {time.time() - start_time:.2f}s")
        
        with open("test_fix_output.svg", "wb") as f:
            f.write(svg_data)
        print("Archivo guardado: test_fix_output.svg")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_fix()
