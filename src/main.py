import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
 
from ui.ventana_main import VentanaPrincipal
 
if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()