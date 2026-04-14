import plotly.graph_objects as go
from kaleido.scopes.plotly import PlotlyScope
import time

def test_png():
    print(">>> Probando si PNG funciona mejor que SVG...")
    fig = go.Figure(data=[go.Bar(y=[1, 3, 2])])
    
    try:
        start = time.time()
        scope = PlotlyScope(mathjax=None)
        print("Transformando a PNG...")
        png_data = scope.transform(fig, format="png")
        print(f"ÉXITO PNG en {time.time()-start:.2f}s ({len(png_data)} bytes)")
        
        start = time.time()
        print("Transformando a SVG...")
        svg_data = scope.transform(fig, format="svg")
        print(f"ÉXITO SVG en {time.time()-start:.2f}s ({len(svg_data)} bytes)")
    except Exception as e:
        print(f"FALLO: {e}")

if __name__ == "__main__":
    test_png()
