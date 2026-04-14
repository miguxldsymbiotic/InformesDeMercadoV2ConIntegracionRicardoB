import plotly.graph_objects as go
from kaleido.scopes.plotly import PlotlyScope
import time
import os

def test_research():
    print(">>> Diagnosticando Kaleido con diferentes configuraciones...")
    fig = go.Figure(data=[go.Bar(y=[1, 3, 2])])
    
    # Intento 1: Con mathjax=None
    print("\n[Prueba 1] PlotlyScope(mathjax=None)...")
    try:
        start = time.time()
        scope = PlotlyScope(mathjax=None)
        print(f"Scope inicializado en {time.time()-start:.2f}s")
        svg = scope.transform(fig, format="svg")
        print(f"ÉXITO prueba 1 en {time.time()-start:.2f}s")
    except Exception as e:
        print(f"FALLO prueba 1: {e}")

    # Intento 2: Sin scope (pio directo)
    import plotly.io as pio
    print("\n[Prueba 2] pio.to_image(engine='kaleido')...")
    try:
        start = time.time()
        svg = pio.to_image(fig, format="svg", engine="kaleido")
        print(f"ÉXITO prueba 2 en {time.time()-start:.2f}s")
    except Exception as e:
        print(f"FALLO prueba 2: {e}")

if __name__ == "__main__":
    test_research()
