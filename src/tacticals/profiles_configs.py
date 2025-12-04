from .tactical_profile import TacticalProfile
from configs.package import CONF

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PERFILES TÁCTICOS
# -----------------------------------------------------------------------------

# PERFIL HUNTER (Cazador)
HUNTER_COMBAT_PROFILE = TacticalProfile(weights={
    CONF.TACTICAL.TYPES.NARROW: -100.0,   # Medio Negativo (Prefiere: batalla en embudos)
    CONF.TACTICAL.TYPES.EXPOSED: -200.0,  # Gran Negativo (Prefiere mucho: busca zonas abiertas)
    CONF.TACTICAL.TYPES.SENTRY: 50.0,     # Pequeño Positivo (Evita: no le gustan las paredes)
    CONF.TACTICAL.TYPES.COVER: 0.0        # Indiferente
})

# PERFIL GUARDIAN (Defensor)
GUARDIAN_COMBAT_PROFILE = TacticalProfile(weights={
    CONF.TACTICAL.TYPES.NARROW: 50.0,     # Pequeño Positivo (Evita levemente embudo)
    CONF.TACTICAL.TYPES.EXPOSED: 200.0,   # Gran Positivo (Evita fuertemente zonas abiertas)
    CONF.TACTICAL.TYPES.SENTRY: -200.0,   # Gran Negativo (Prefiere mucho: posición cubierta)
    CONF.TACTICAL.TYPES.COVER: 0.0        # Indiferente
})

# PERFIL DE HUIDA (Tactical Flee)
FLEE_PROFILE = TacticalProfile(weights={
    CONF.TACTICAL.TYPES.NARROW: -100.0,   # Medio Negativo (Prefiere embudos para cortar visión)
    CONF.TACTICAL.TYPES.EXPOSED: 200.0,   # Gran Positivo (Evitar fuertemente zonas abiertas)
    CONF.TACTICAL.TYPES.SENTRY: -100.0,   # Medio Negativo (Prefiere posición cubierta)
    CONF.TACTICAL.TYPES.COVER: -200.0     # Gran Negativo (Prefiere moverse por las esquinas)
})