import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.ventana_main import VentanaPrincipal

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()