import sys
import os

def resource_path(relative_path):
    """
    Devuelve la ruta absoluta al recurso, compatible con PyInstaller y modo desarrollo.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: recursos están en _MEIPASS
        base_path = sys._MEIPASS
    else:
        # Desarrollo: recursos relativos al archivo actual
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)