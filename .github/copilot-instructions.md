# Instrucciones de GitHub Copilot

Este archivo contiene las instrucciones que GitHub Copilot debe seguir al trabajar con este repositorio.

## Convenciones del Proyecto

### 1. Idioma por Defecto
- El idioma por defecto para comunicación es **español**.
- Todas las respuestas, explicaciones y descripciones deben estar en español.

### 2. Código en Inglés con Snake Case
- El código fuente debe estar escrito en **inglés**.
- Los nombres de **funciones** deben usar `snake_case`.
- Los nombres de **variables** deben usar `snake_case`.
- Los nombres de **clases** deben usar `PascalCase` (convención estándar).

#### Ejemplos:
```python
# ✅ Correcto
def calculate_player_damage():
    player_health = 100
    enemy_attack_power = 25
    return player_health - enemy_attack_power

# ❌ Incorrecto
def calcularDanoJugador():
    vidaJugador = 100
    poderAtaqueEnemigo = 25
    return vidaJugador - poderAtaqueEnemigo
```

### 3. Documentación y Comentarios en Español
- Todos los **comentarios** en el código deben estar en **español**.
- La **documentación** (docstrings, README, etc.) debe estar en **español**.

#### Ejemplos:
```python
def calculate_player_damage(player_health: int, enemy_attack: int) -> int:
    """
    Calcula el daño recibido por el jugador.
    
    Args:
        player_health: Vida actual del jugador.
        enemy_attack: Poder de ataque del enemigo.
    
    Returns:
        La vida restante del jugador después del ataque.
    """
    # Calcular el daño final aplicando la fórmula básica
    final_damage = enemy_attack
    
    # Retornar la vida restante (mínimo 0)
    return max(0, player_health - final_damage)
```

## Resumen de Convenciones

| Aspecto | Idioma | Formato |
|---------|--------|---------|
| Comunicación | Español | - |
| Nombres de funciones | Inglés | snake_case |
| Nombres de variables | Inglés | snake_case |
| Nombres de clases | Inglés | PascalCase |
| Comentarios | Español | - |
| Documentación | Español | - |
