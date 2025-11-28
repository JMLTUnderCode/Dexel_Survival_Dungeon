import os
import sys

def resource_path_dir(relative_path: str) -> str:
    """
    Descripción
        FUNCIÓN: Esta función intenta resolver una ruta absoluta para recursos referenciados
        por su ruta relativa dentro del repositorio. Maneja dos escenarios principales:
            - Ejecución empaquetada (frozen) donde los recursos están junto al ejecutable.
            - Desarrollo local donde los recursos se encuentran en la carpeta `src/`.

        Si ninguna ruta existe, se lanza FileNotFoundError con información útil.

    Argumentos
        - relative_path (str): Ruta relativa dentro del árbol de recursos (ej. assets/tiles/tile.png).

    Retorno
        - str: Ruta absoluta al recurso.

    Excepciones
        - FileNotFoundError: Si no se encuentra ninguna de las rutas candidate/fallback.
    """
    # 1. Si estamos en una distribución "frozen" (p. ej. PyInstaller), usar la carpeta del ejecutable
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        # 2. En desarrollo: la raíz de recursos está en src/ (padre del módulo utils/)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # 3. Construir la ruta candidata y verificar existencia
    candidate = os.path.join(base_dir, relative_path)
    if os.path.exists(candidate):
        return candidate

    # 4. Fallback: intentar resolver relativo al propio módulo utils/ (por compatibilidad)
    fallback = os.path.join(os.path.dirname(__file__), relative_path)
    if os.path.exists(fallback):
        return fallback

    # 5. Si ninguna ruta existe, informar claramente el fallo con las rutas intentadas
    raise FileNotFoundError(
        "Recurso no encontrado. Se intentaron las rutas:\n"
        f"  {candidate}\n"
        f"  {fallback}\n\n"
        "Verifique que el recurso exista y que la estructura de distribución coloque la carpeta "
        "'assets' accesible desde la ubicación del ejecutable o desde el directorio 'src/'."
    )