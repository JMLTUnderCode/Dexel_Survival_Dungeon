import os
import sys

def resource_path_dir(relative_path: str) -> str:
    """
    Resuelve la ruta absoluta de un recurso relativo al proyecto.

    - En distribución (frozen) usa la carpeta del ejecutable (dirname(sys.executable)).
    - En desarrollo usa la carpeta `src/` (el padre de `utils/`) como base, de modo que
      resource_path("assets/...") -> <repo>/src/assets/...
    - Si no existe el path construido, intenta una ruta fallback relativa a este módulo.
    - Si ninguno existe lanza FileNotFoundError con información útil.
    """
    # 1) Si estamos "frozen" (PyInstaller onefile/onedir) resolvemos respecto al exe
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        # 2) En desarrollo: la raíz de recursos está en src/ (padre de utils/)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    candidate = os.path.join(base_dir, relative_path)
    if os.path.exists(candidate):
        return candidate

    # Fallback: intentar relativo al propio módulo utils/ (por compatibilidad)
    fallback = os.path.join(os.path.dirname(__file__), relative_path)
    if os.path.exists(fallback):
        return fallback

    # Ninguna ruta válida: informar claramente el fallo
    raise FileNotFoundError(
        f"Resource not found: tried\n  {candidate}\n  {fallback}\n"
        "Ensure the asset exists and that the distribution layout places the executable "
        "next to the 'assets' folder (or run in development from the repo root)."
    )