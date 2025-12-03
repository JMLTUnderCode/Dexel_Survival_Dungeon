from .tactical_profile import TacticalProfile

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PERFILES TÁCTICOS
# -----------------------------------------------------------------------------
# Escala aproximada: 
# Costo base de movimiento por tile ~= 16.0
# Un peso de -50.0 equivale a que la entidad está dispuesta a recorrer 
# ~3 tiles extra con tal de pasar por este punto.

# PERFIL HUNTER (Cazador)
# - Agresivo, rápido.
# - Prefiere 'narrow' para acorralar.
# - Prefiere 'exposed' para tener libertad de movimiento.
# - Evita 'sentry' (esquinas) porque limitan su huida.
HUNTER_COMBAT_PROFILE = TacticalProfile(weights={
    "narrow": -100.0,      # Medio Negativo (Prefiere: movilidad)
    "exposed": -200.0,     # Gran Negativo (Prefiere mucho: embudo)
    "sentry": 50.0,        # Pequeño Positivo (Evita: no le gusta arrinconarse)
    "cover": 0.0           # Indiferente
})

# PERFIL GUARDIAN (Defensor)
# - Defensivo, estático.
# - Odia 'exposed' (se siente vulnerable).
# - Ama 'sentry' (esquinas seguras para vigilar).
# - Evita 'narrow' levemente (prefiere tener visión clara).
GUARDIAN_COMBAT_PROFILE = TacticalProfile(weights={
    "narrow": 30.0,       # Pequeño Positivo (Evita levemente)
    "exposed": 100.0,     # Gran Positivo (Evita fuertemente: peligro)
    "sentry": -100.0,     # Gran Negativo (Prefiere mucho: posición segura)
    "cover": 0.0          # Indiferente
})

# PERFIL DE HUIDA (Tactical Flee)
# - Prioridad absoluta: Sobrevivir usando el entorno.
# - Cover/Sentry (Paredes/Esquinas): Gran Negativo (Preferidos para moverse protegido).
# - Exposed (Centro): Gran Positivo (Zona de muerte, evitar a toda costa).
# - Narrow: Neutro/Positivo (Puede ser peligroso si el jugador bloquea, pero útil para romper visión).
FLEE_PROFILE = TacticalProfile(weights={
    "narrow": 0.0,        # Indiferente
    "exposed": 200.0,     # EVITAR el centro abierto
    "sentry": 0.0,        # Indiferente
    "cover": -150.0       # Preferir moverse pegado a las paredes
})