# **Dexel: Survival Dungeon** 🎮

Un intenso roguelike en 2D pixel donde la supervivencia depende de tu estrategia. Adéntrate en niveles de mazmorras llenas de enemigos IA y lucha por tu vida.

## Índice
- [**Dexel: Survival Dungeon** 🎮](#dexel-survival-dungeon-)
  - [Índice](#índice)
  - [🎯 **Características Principales**](#-características-principales)
  - [🕹️ **Cómo Jugar**](#️-cómo-jugar)
  - [🚀 **Instalación y Ejecución**](#-instalación-y-ejecución)
    - [**Requisitos**](#requisitos)
    - [**Instalación rápida**](#instalación-rápida)
    - [**Descargar ejecutable**](#descargar-ejecutable)
    - [**Release**](#release)
  - [🏗️ **Estructura del Proyecto**](#️-estructura-del-proyecto)
  - [🎨 **Tecnologías Utilizadas**](#-tecnologías-utilizadas)
  - [🤝 **Contribuir**](#-contribuir)
  - [📋 **Roadmap**](#-roadmap)
  - [📄 **Licencia**](#-licencia)
  - [👨‍💻 **Desarrollador**](#-desarrollador)

## 🎯 **Características Principales**

- **🔫 Combate dinámico 2D** - Control preciso con mouse y teclado.
- **🤖 IA inteligente** - Enemigos que te persiguen, flanquean y emboscan.
- **🎮 Controles fluidos** - Movimiento WASD y apuntado con mouse.
- **✨ Pixel art optimizado** - Arte retro con animaciones smooth y rotaciones realistas

## 🕹️ **Cómo Jugar**

| Control | Acción |
|---------|--------|
| **WASD** | Movimiento del personaje |
| **Mouse** | Apuntar y rotar personaje |
| **Click izquierdo** | Atacar |
| **ESC** | Pausa/Menú |

## 🚀 **Instalación y Ejecución**

### **Requisitos**
- Python 3.8 o superior
- Sistema operativo: Windows, Linux o macOS

### **Instalación rápida**
```bash
# Clonar el repositorio
git clone https://github.com/tuusuario/dexel-survival-dungeon.git
cd dexel-survival-dungeon

# Activar environment
source env/bin/activate # Linux/MacOS
source env/Scripts/activate # Windows

# De no tener environment, crear uno
python -m venv env

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el juego
python src/main.py

# Mediante el script directo
./game # Linux/MacOS
./play.sh # Windows
```

### **Descargar ejecutable**
Ve a la [página oficial](https://jmltundercode.github.io/Dexel_Survival_Dungeon) y descarga el juego para tu sistema operativo preferido.

### **Release**

- Para la generación de nuevas versiones 
  ```sh
  git tag vx.y.z
  git push origin vx.y.z
  ```
  Ej.
  ```sh
  git tag v1.1.2
  git push origin v1.1.2
  ```
- Para remover un tag
  ```sh
  git tag -d <tag-name>
  git push origin --delete <tag-name>
  ```
  Ej.
  ```sh
  git tag -d v1.1.2
  git push origin --delete v1.1.2
  ```

## 🏗️ **Estructura del Proyecto**

```
dexel-survival-dungeon/
├── .github/                 # Guías y workflows
│   └── workflows/
│       ├── pages.yml        # Deploy de sitio web.
│       └── release.yml      # Deploy de releases.
├── LICENSE                  # Licencia explícita del juego.
├── play.sh                  # Ejecutar juego en windows.
├── game                     # Ejecutar juego en Linux/Mac.
├── requirements.txt         # Requirimientos necesarios para ejecución.
├── src/                     # Código fuente
│   ├── main.py              # Punto de entrada
│   ├── game.py              # Módulo principal
│   ├── ai/                  # Máquina de Estados (Comportamientos)
│   │   ├── behavior.py
│   │   ├── hsm.py
│   │   ├── hsm_builder.py
│   │   ├── actions.py
│   │   └── conditions.py
│   ├── algorithms/         # Algoritmos de movimientos, aliniamiento y seguimiendo.
│   ├── assets/             # Tokens y assets usados para entidades, mapas y animaciones.
│   ├── configs/            # Configuraciones generales del proyecto separadas por módulo y prósito.
│   │   └── package.py      # Empaquetador principal de configuraciones.
│   ├── data/               # Especificaciones y datos
│   │   └── enemies.py      # Definición de estadísticas de enemigos.
│   ├── entity/             # Entidades definidas dentro del juego.
│   │   ├── kinematic.py
│   │   ├── enemy.py
│   │   ├── player.py
│   │   ├── animation.py
│   │   └── entity_manager.py
│   ├── map/                # Mapa, caminos, malla de navegación y buscador de camino óptimo.
│   │   ├── map.py
│   │   ├── navmesh.py
│   │   ├── pathfinder.py
│   │   └── paths.py
│   ├── ui/                 # UI para debugging y pruebas.
│   │   ├── enemy_set.py
│   │   └── map_set.py
│   └── utils/              # Utilidad de búsqueda de archivos en diferentes sistemas.
├── tools/                  # Herramientas de chequeo.
│   └── ai_unused_finder.py # Búscador de elementos sin usar en la AI.
└── web/                    # Sitio web
    ├── index.html
    └── index.css
```

## 🎨 **Tecnologías Utilizadas**

- **Python 3.8+** - Lenguaje principal
- **Pygame 2.5.0** - Motor gráfico y de audio
- **NumPy 2.3.4** - Cálculos matemáticos para IA y física
- **PyInstaller 6.16.0** - Empaquetado para distribución
- **matplotlib 3.10.7** - Dibujado y posicionamiento en figuras.

## 🤝 **Contribuir**

¡Las contribuciones son bienvenidas! Si quieres ayudar a mejorar Dexel:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📋 **Roadmap**

- [x] Sistema básico de movimiento y ataque
- [x] IA enemiga básica (persecución y ataque)
- [ ] Arte pixel art y animaciones
- [ ] Sonidos y música
- [ ] Sistema de progresión y puntuación
- [ ] Generación procedural de mazmorras

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 **Desarrollador**

**Junior Miguel Lara Torres** - [GitHub Profile](https://github.com/jmltundercode)

¿Preguntas o sugerencias? ¡Abre un issue o contáctame!
