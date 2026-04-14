import typst
from pathlib import Path

def test_typst_only():
    print(">>> Probando Typst solo (sin gráficas)...")
    content = '#set text(font: "Arial")\n= Prueba\nHola mundo.'
    output_pdf = Path("test_typst_only.pdf")
    
    with open("test_simple.typ", "w") as f:
        f.write(content)
        
    try:
        typst.compile("test_simple.typ", output=str(output_pdf))
        print(f"ÉXITO: Typst compiló {output_pdf.stat().st_size} bytes")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_typst_only()
