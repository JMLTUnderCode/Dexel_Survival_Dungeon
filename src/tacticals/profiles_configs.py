from .tactical_profile import TacticalProfile
from configs.package import CONF

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PERFILES TÁCTICOS
# -----------------------------------------------------------------------------

# PERFIL HUNTER (Cazador)
HUNTER_COMBAT_PROFILE = TacticalProfile(weights={
    CONF.TACTICAL.TYPES.NARROW: -100.0,   # Medio Negativo (Prefiere: batalla en embudos)
    CONF.TACTICAL.TYPES.EXPOSED: -200.0,  # Gran Negativo (Prefiere mucho: busca zonas abiertas)
    CONF.TACTICAL.TYPES.SENTRY: 100.0,    # Medio Positivo (Evita: no le gustan las paredes)
    CONF.TACTICAL.TYPES.COVER: 200.0      # Gran Positivo (Evita mucho: no le gustan las esquinas)
})

# PERFIL GUARDIAN (Defensor)
GUARDIAN_COMBAT_PROFILE = TacticalProfile(weights={
    CONF.TACTICAL.TYPES.NARROW: 50.0,     # Pequeño Positivo (Evita levemente: batalla en embudos)
    CONF.TACTICAL.TYPES.EXPOSED: 200.0,   # Gran Positivo (Evita fuertemente zonas abiertas)
    CONF.TACTICAL.TYPES.SENTRY: -200.0,   # Gran Negativo (Prefiere mucho: posición cubierta)
    CONF.TACTICAL.TYPES.COVER: -100.0     # Medio Negativo (Prefiere: moverse por las esquinas)
})

# PERFIL DE HUIDA (Tactical Flee)
FLEE_PROFILE = TacticalProfile(weights={
    CONF.TACTICAL.TYPES.NARROW: 200.0,   # Medio Positivo (Evita mucho: se acorralado en embudos)
    CONF.TACTICAL.TYPES.EXPOSED: 200.0,   # Gran Positivo (Evita mucho: zonas abiertas)
    CONF.TACTICAL.TYPES.SENTRY: -200.0,   # Gran Negativo (Prefiere mucho: posición cubierta)
    CONF.TACTICAL.TYPES.COVER: -200.0     # Gran Negativo (Prefiere mucho: moverse por las esquinas)
})