import sys
import os

def resource_path(relative_path: str) -> str:
    """
    Devuelve la ruta absoluta al recurso tomando estrictamente la carpeta
    del juego como única fuente cuando el programa está distribuido como
    ejecutable. En desarrollo usa la carpeta del módulo.

    Reglas:
    - Si el ejecutable está "frozen" (PyInstaller/NSIS), la base es el
      directorio donde se encuentra el ejecutable: os.path.dirname(sys.executable)
    - En modo desarrollo la base es la carpeta del paquete: os.path.dirname(__file__)
    - No usa sys._MEIPASS ni AppData.
    """
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)