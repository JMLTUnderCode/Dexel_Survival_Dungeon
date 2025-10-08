# **Dexel: Survival Dungeon** 🎮

Un intenso roguelike en 2D pixel donde la supervivencia depende de tu estrategia. Adéntrate en mazmorras procedurales llenas de enemigos IA y lucha por tu vida.

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

- **🔫 Combate dinámico 2D** - Control preciso con mouse y teclado
- **🤖 IA inteligente** - Enemigos que te persiguen, flanquean y emboscan
- **🎮 Controles fluidos** - Movimiento WASD, apuntado con mouse, recarga táctica
- **🏰 Mazmorras procedurales** - Cada partida es única con diferentes layouts y obstáculos
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

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el juego
python src/main.py

# Mediante el script directo
./game
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
├── src/                    # Código fuente
│   ├── main.py            # Punto de entrada
│   ├── game/              # Módulos del juego
│   │   ├── player.py      # Controlador del jugador
│   │   ├── enemies/       # Sistema de IA enemiga
│   │   ├── weapons/       # Gestión de armas y balas
│   │   ├── dungeon/       # Generación de mazmorras
│   │   └── assets/        # Manager de recursos
│   └── utils/             # Utilidades
├── assets/                # Recursos del juego
│   ├── sprites/           # Arte pixel art
│   ├── sounds/            # Efectos de sonido y música
│   └── fonts/             # Fuentes del juego
├── docs/                  # Documentación
└── requirements.txt       # Dependencias
```

## 🎨 **Tecnologías Utilizadas**

- **Python 3.8+** - Lenguaje principal
- **Pygame 2.5.0** - Motor gráfico y de audio
- **NumPy** - Cálculos matemáticos para IA y física
- **PyInstaller** - Empaquetado para distribución

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
