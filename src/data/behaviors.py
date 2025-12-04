from configs.package import CONF

class BehaviorsData:
    """
    DOCUMENTACIÓN: HUNTER

    Resumen
        Comportamiento 'hunter' (cazador) para enemigos. Diseñado como una HSM (máquina de estados
        jerárquica) con tres estados de alto nivel: EstadoVida (submáquina: Cazar/Atacar), Huyendo y Curarse.
        Objetivo: patrullar/buscar al jugador, perseguir y atacar si se detecta, huir cuando la vida es baja,
        y curarse/esperar en un anchor seguro hasta recuperarse.

    Parámetros principales (params)
        - vision_range (px): distancia máxima para ver al jugador.
        - vision_fov_deg (deg): ángulo del cono de visión.
        - attack_range (px): distancia de melee/ataque.
        - flee_threshold (0..1): fracción de vida para entrar en Huyendo.
        - restore_threshold (0..1): fracción de vida para salir de Curarse (restaurar historial).
        - heal_rate_per_sec: fracción de max_health curada por segundo durante Curarse.
        - safe_distance (px): distancia objetivo para calcular safe_anchor (sitio seguro).
        - player_lost_timeout (s): tiempo para considerar que el jugador se perdió.
        - patrol_path_nodes (int): número mínimo de nodos deseados para patrulla aleatoria.
        - face_range_multiplier: multiplica vision_range para decidir cuándo "mirar" al jugador.
        - check_los_throttle (s): throttling para checks de línea de visión.
        - scan_duration (s): duración del escaneo visual al llegar a un punto de patrulla.
        - arrival_threshold (px): umbral de distancia para considerar que se llegó a un punto.

    Estados y semántica
      - EstadoVida (composite, history=deep)
        - Subestados: Cazar (patrullar / vigilar), Atacar (perseguir / golpear)
        - Guarda historial profundo para restaurar comportamiento tras Curarse.

      - EstadoVida.Cazar (Vigilar / patrullar)
        - Patrulla (navmesh o ruta aleatoria) y chequea visibilidad del jugador.
        - No sustituye la ruta guardian (si existe) a menos que corresponda.

      - EstadoVida.Atacar
        - Persecución activa del jugador; intenta ataques cuerpo a cuerpo en rango.
        - Si se pierde visión por un tiempo, vuelve a patrullar.

      - Huyendo
        - Evadir cuando hp bajo. Guarda prev_algorithm para restaurar.
        - Monitoriza distancia al jugador para decidir cuándo detener huida.

      - Curarse
        - Permanece estático (o mirando hacia jugador/anchor), se cura progresivamente.
        - Monitoriza presencia del jugador para interrumpir si aparece amenaza.

    Transiciones críticas (resumen práctico)
        - Vigilar + PlayerVisible -> Atacar
        - Vigilar + IsFarFromProtectionZone -> RegresarAZona (si hay path guardian)
        - Atacar + PlayerNotVisibleFor + IsAtProtectionZone -> Vigilar
        - Atacar + PlayerNotVisibleFor + IsFarFromProtectionZone -> RegresarAZona
        - RegresarAZona + IsAtProtectionZone -> Vigilar
        - RegresarAZona + PlayerVisible -> Atacar
        - Huyendo + PlayerFar -> Curarse
        - Curarse + PlayerVisible -> Huyendo
        - Curarse + HealthAbove -> EstadoVida (restaurando historial previo)
    """
    HUNTER = {
        "name": "hunter",
        "debug": {"show_state_over_entity": True},
        "params": {
            "vision_range": 300.0,
            "vision_fov_deg": 120.0,
            "attack_range": 48.0,
            "flee_threshold": 0.30,
            "restore_threshold": 0.70,
            "heal_rate_per_sec": 0.05,
            "safe_distance": 450.0,
            "player_lost_timeout": 2.0,
            "patrol_path_nodes": 20,
            "face_range_multiplier": 2,
            "check_los_throttle": 0.12,
            "scan_duration": 6.0,
            "arrival_threshold": 15.0
        },
        "root": "EstadoVida",
        "states": {
            # Nivel 1: EstadoVida (subMáquina)
            "EstadoVida": {
                "type": "composite",
                "initial": "Cazar",
                "history": "deep",
                "substates": ["Cazar", "Atacar"],
                "entry": ["record_last_state_start"],
                "exit": [],
                "transitions": [
                    # Si la vida baja, huir
                    {"to": "Huyendo", "cond": "HealthBelow", "priority": 200}
                ]
            },

            # Nivel 0: EstadoVida.Cazar (patrullar / buscar)
            "EstadoVida.Cazar": {
                "type": "leaf",
                "entry": ["start_random_patrol"],
                "update": ["patrol_tick", "throttle_check_player_visibility"],
                "exit": ["stop_patrol"],
                "transitions": [
                    # Si el jugador es visible, atacar
                    {"to": "EstadoVida.Atacar", "cond": "PlayerVisible", "priority": 100},
                ]
            },

            # Nivel 0: EstadoVida.Atacar (perseguir y golpear)
            "EstadoVida.Atacar": {
                "type": "leaf",
                "entry": ["start_pursue_target"],
                "update": ["pursue_tick", "try_melee_attack", "throttle_check_player_visibility"],
                "exit": ["stop_pursue"],
                "transitions": [
                    # Si el jugador no es visible por un tiempo, volver a cazar
                    {"to": "EstadoVida.Cazar", "cond": "PlayerNotVisibleFor", "priority": 100},
                ]
            },

            # Nivel 1: Huyendo (evadir al enemigo)
            "Huyendo": {
                "type": "leaf",
                #"entry": ["start_evade_from_player", "set_behavior_flag_fleeing"],
                #"update": ["evade_tick"],
                "entry": ["start_tactical_flee", "set_behavior_flag_fleeing"],
                "update": ["tactical_flee_tick"], # Usar tick táctico
                "exit": ["stop_evade", "clear_behavior_flag_fleeing"],
                "transitions": [
                    # Si el jugador está lejos, pasar a curarse
                    #{"to": "Curarse", "cond": "PlayerFar", "priority": 200}
                    {"to": "Curarse", "cond": "PathFinished", "priority": 200}
                ]
            },

            # Nivel 1: Curarse (quedarse estático, Face al enemigo, curarse)
            "Curarse": {
                "type": "leaf",
                "entry": ["face_towards_safe_anchor", "stop_movement", "start_heal_tick"],
                "update": ["face_towards_safe_anchor", "heal_tick", "monitor_player_presence"],
                "exit": ["stop_heal_tick", "clear_safe_anchor"],
                "transitions": [
                    # Si la entidad se ha recuperado suficiente vida
                    {"to": "EstadoVida", "cond": "HealthAbove", "priority": 300, "restore_history": True},
                    # Si el jugador aparece mientras se cura
                    {"to": "Huyendo", "cond": "PlayerVisible", "priority": 600}
                ]
            },
        },
    }

    """
    DOCUMENTACIÓN: GUARDIAN

    Resumen
        Comportamiento 'guardian' para enemigos. Diseñado para proteger un camino (Path)
        que representa la "zona" defendida. El guardian patrulla sobre un path definido (si existe)
        y gestiona retorno cuando se aleja del camino. Si no hay path, se comporta como patrulla
        aleatoria. Incluye lógica de persecución/ataque, huida y curado similar a HUNTER pero
        con énfasis en mantener/volver al path protegido.

    Parámetros principales (params)
        - vision_range (px): distancia máxima para ver al jugador.
        - vision_fov_deg (deg): ángulo del cono de visión.
        - attack_range (px): distancia de melee/ataque.
        - flee_threshold (0..1): fracción de vida para entrar en Huyendo.
        - restore_threshold (0..1): fracción de vida para salir de Curarse.
        - heal_rate_per_sec: fracción de max_health curada por segundo durante Curarse.
        - safe_distance (px): distancia objetivo para calcular safe_anchor (sitio seguro).
        - player_lost_timeout (s): tiempo para considerar que el jugador se perdió.
        - patrol_path_nodes (int): nodos deseados para patrulla aleatoria.
        - face_range_multiplier: multiplica vision_range para decidir cuándo "mirar" al jugador.
        - check_los_throttle (s): throttling para checks de línea de visión.
        - protection_margin (px): distancia al punto MÁS CERCANO del Path que define
            si la entidad está "sobre" su ruta patrulla (p.ej. 40 px).
        - arrival_threshold (px): umbral de llegada usado por la ruta de retorno (p.ej. 40 px).
        - scan_duration (s): duración del escaneo visual al llegar a un punto del path.

    Estados y semántica
      - EstadoVida (composite, history=deep)
        - Subestados: Vigilar, Atacar, RegresarAZona
        - Guarda historial profundo para restaurar comportamiento tras Curarse.

      - EstadoVida.Vigilar (Patrulla guardian / Vigilar)
        - Si la entidad tiene un Path (entity.path) lo usa como ruta guardian.
        - is_on_guardian_path = True indica que la entidad sigue el path protegido.
        - Si la entidad se aleja más que protection_margin del punto MÁS CERCANO del path,
          la condición IsFarFromProtectionZone dispara el retorno.

      - EstadoVida.Atacar
        - Igual que hunter: perseguir y atacar, pero al perder objetivo decide volver
          al path guardian si está lejos de él.

      - EstadoVida.RegresarAZona (volver al camino protegido)
        - Genera un FollowPath temporal (entity.temp_follow_path) desde la posición actual
          hacia el punto MÁS CERCANO del Path guardian_original_path.
        - Usa arrival_threshold para decidir llegada por proximidad; al llegar restaura
          PATH_FOLLOWING sobre el path guardian.

      - Huyendo
        - Evadir cuando hp bajo. Guarda prev_algorithm para restaurar.
        - Monitoriza distancia al jugador para decidir cuándo detener huida.

      - Curarse
        - Permanece estático (o mirando hacia jugador/anchor), se cura progresivamente.
        - Monitoriza presencia del jugador para interrumpir si aparece amenaza.

    Transiciones críticas (resumen práctico)
        - Vigilar + PlayerVisible -> Atacar
        - Vigilar + IsFarFromProtectionZone -> RegresarAZona
        - Atacar + PlayerNotVisibleAndAtProtectionZone -> Vigilar
        - Atacar + PlayerNotVisibleAndFarFromProtectionZone -> RegresarAZona
        - RegresarAZona + IsAtProtectionZone -> Vigilar
        - RegresarAZona + PlayerVisible -> Atacar
        - Huyendo + PlayerFar -> Curarse
        - Curarse + PlayerVisible -> Huyendo
        - Curarse + HealthAbove -> EstadoVida (restaurando historial)
    """
    GUARDIAN = {
        "name": "guardian",
        "debug": {"show_state_over_entity": True},
        "params": {
            "vision_range": 300.0,
            "vision_fov_deg": 120.0,
            "attack_range": 48.0,
            "flee_threshold": 0.30,
            "restore_threshold": 0.70,
            "heal_rate_per_sec": 0.05,
            "safe_distance": 450.0,
            "player_lost_timeout": 2.0,
            "face_range_multiplier": 2,
            "check_los_throttle": 0.25,
            "protection_margin": 40.0,
            "arrival_threshold": 40.0,
            "scan_duration": 6.0,
        },
        "root": "EstadoVida",
        "states": {
            # Nivel 1: EstadoVida (subMáquina)
            "EstadoVida": {
                "type": "composite",
                "initial": "Vigilar",
                "history": "deep",
                "substates": ["Vigilar", "Atacar", "RegresarAZona"],
                "entry": ["record_last_state_start"],
                "update": ["monitor_player_presence"],
                "exit": [],
                "transitions": [
                    # Si la vida baja, huir
                    {"to": "Huyendo", "cond": "HealthBelow", "priority": 600}
                ]
            },

            # Nivel 0: EstadoVida.Vigilar (Vigila un camino)
            "EstadoVida.Vigilar": {
                "type": "leaf",
                "entry": ["start_guardian_patrol"],
                "update": ["patrol_tick", "throttle_check_player_visibility"],
                "exit": ["stop_patrol"],
                "transitions": [
                    # Si el jugador es visible, atacar
                    {"to": "EstadoVida.Atacar", "cond": "PlayerVisible", "priority": 150},
                    # Si está lejos de la zona protegida, regresar a la zona
                    {"to": "EstadoVida.RegresarAZona", "cond": "IsFarFromProtectionZone", "priority": 300},
                ]
            },

            # Nivel 0: EstadoVida.Atacar (perseguir y golpear al enemigo)
            "EstadoVida.Atacar": {
                "type": "leaf",
                "entry": ["start_pursue_target"],
                "update": ["pursue_tick", "try_melee_attack", "throttle_check_player_visibility"],
                "exit": ["stop_pursue"],
                "transitions": [
                    # Si el jugador no es visible y está en la zona protegida, volver a vigilar
                    {"to": "EstadoVida.Vigilar", "cond": "PlayerNotVisibleAndAtProtectionZone", "priority": 150},
                    # Si el jugador no es visible y está lejos de la zona protegida, regresar a la zona
                    {"to": "EstadoVida.RegresarAZona", "cond": "PlayerNotVisibleAndFarFromProtectionZone", "priority": 300},
                ]
            },

            # Nivel 0: EstadoVida.RegresarAZona (volver al camino de patrullaje)
            "EstadoVida.RegresarAZona": {
                "type": "leaf",
                "entry": ["return_to_protection_zone"],
                "update": ["guardian_return_tick"],
                "exit": [],
                "transitions": [
                    # Si ha llegado a la zona protegida, volver a vigilar
                    {"to": "EstadoVida.Vigilar", "cond": "IsAtProtectionZone", "priority": 200},
                    # Si el jugador es visible, atacar
                    {"to": "EstadoVida.Atacar", "cond": "PlayerVisible", "priority": 350},
                ]
            },

            # Nivel 1: Huyendo (evadir al enemigo)
            "Huyendo": {
                "type": "leaf",
                #"entry": ["start_evade_from_player", "set_behavior_flag_fleeing"],
                #"update": ["evade_tick"],
                "entry": ["start_tactical_flee", "set_behavior_flag_fleeing"],
                "update": ["tactical_flee_tick"], # Usar tick táctico
                "exit": ["stop_evade", "clear_behavior_flag_fleeing"],
                "transitions": [
                    # Si el jugador está lejos, pasar a curarse
                    #{"to": "Curarse", "cond": "PlayerFar", "priority": 200}
                    {"to": "Curarse", "cond": "PathFinished", "priority": 200}
                ]
            },

            # Nivel 1: Curarse (quedarse estático, Face al enemigo, curarse)
            "Curarse": {
                "type": "leaf",
                "entry": ["face_towards_safe_anchor", "stop_movement", "start_heal_tick"],
                "update": ["face_towards_safe_anchor", "heal_tick", "monitor_player_presence"],
                "exit": ["stop_heal_tick", "clear_safe_anchor"],
                "transitions": [
                    # Si la entidad se ha recuperado suficiente vida
                    {"to": "EstadoVida", "cond": "HealthAbove", "priority": 300, "restore_history": True},
                    # Si el jugador aparece mientras se cura
                    {"to": "Huyendo", "cond": "PlayerVisible", "priority": 600}
                ]
            },
        }
    }

    """
    DOCUMENTACIÓN: INVOKER BOSS

    Resumen
        Comportamiento del jefe "boss_reposition_invoker". Diseñado para:
        - Permanecer inicialmente en estado Atento (pre-combate) mirando en una dirección fija.
        - Entrar en combate (EstadoVida) al ver al jugador o tras recibir un golpe sorpresa.
        - Alternar entre ataques cuerpo a cuerpo (AtacarMele) y a distancia (AtacarRange).
        - Reposicionarse a boss_position, invocar aliados y regenerarse manteniendo facing cuando aplica.

    Parámetros principales (params)
        - vision_range (px): alcance máximo de detección visual del jugador.
        - vision_fov_deg (deg): apertura del cono de visión.
        - player_seen_memory (s): tiempo de "memoria" tras perder visión.
        - dist_for_mele (px): umbral de distancia para preferir melee frente a ranged.
        - boss_position (x,y): posición donde reposicionarse, invocar y regenerar.
        - allies_for_invocation (int): cantidad total de aliados a crear en Invocar.
        - time_for_invocation (s): duración en la que se distribuyen los spawns.
        - timeout_invocations (s): lifetime de cada aliado invocado (expiración).
        - perc_regenerate (0..1): fracción de vida a recuperar durante Regenerar.
        - time_for_regeneration (s): duración del proceso de regeneración.
        - lost_health_trigger_pct (0..1): fracción de vida perdida que fuerza Reposicionar.
        - check_los_throttle (s): throttling para checks de línea de visión.
        - attention_direction (str): dirección cardinal ("N","S","E","W") usada en Atento.
        - attention_distance (px): distancia para generar el punto de facing en Atento.
        - recent_damage_threshold (float): umbral mínimo de HP perdido para considerar golpe sorpresa.
        - recent_damage_window (s): ventana temporal durante la cual RecentlyDamaged sigue siendo True.
        - arrival_threshold (px): umbral de llegada usado por las transiciones IsAtBossPosition / Reposicionar.

    Estados y semántica
      - Atento (leaf, root inicial)
          Estado PRE-COMBATE. Boss estático mirando en la dirección configurada (start_attention_facing).
          Sirve para detección inicial y para ser sorprendido por un golpe (RecentlyDamaged).
          No forma parte del history de EstadoVida para evitar restauraciones a Atento.

      - EstadoVida (composite, history="deep")
          Submáquina de COMBATE. Contiene AtacarMele y AtacarRange.
          Mantiene historial profundo entre subestados de combate para restaurar la modalidad de ataque.

      - AtacarMele (leaf)
          Persecución y ataque cuerpo a cuerpo. Usa start_pursue_target / pursue_tick / try_melee_attack.
          Cambia a ranged si el jugador está lejos o a Reposicionar si pierde demasiada vida.

      - AtacarRange (leaf)
          Modo a distancia: boss queda estático (FACE) y lanza efectos a distancia periódicos
          (start_boss_range_attack_mode / boss_range_attack_tick). Vuelve a melee si el jugador se acerca.

      - Reposicionar (leaf)
          Pathfinding hacia boss_position (start_return_to_boss_position / return_to_boss_tick).
          Al llegar transiciona a Invocar.

      - Invocar (leaf)
          Genera aliados distribuidos en time_for_invocation. Los aliados usan algoritmo PURSUE
          hacia el jugador y tienen lifetime = timeout_invocations. Spawns realizados mediante manager.spawn_enemy.

      - Regenerar (leaf)
          El boss permanece en boss_position, estático y mirando al jugador (start_regeneration / regen_tick).
          Recupera vida progresivamente y, al terminar, vuelve a EstadoVida restaurando el history previo.

    Transiciones críticas (resumen práctico)
        - Atento + PlayerVisible -> EstadoVida.AtacarMele o EstadoVida.AtacarRange (según distancia)
        - Atento + RecentlyDamaged -> EstadoVida.AtacarMele o EstadoVida.AtacarRange (sorpresa por daño)
        - EstadoVida.AtacarMele -> EstadoVida.AtacarRange cuando PlayerBeyondMelee
        - EstadoVida.AtacarRange -> EstadoVida.AtacarMele cuando PlayerWithinMelee
        - EstadoVida.* -> Reposicionar si LostHealthSinceLastRestoreAtLeast (perdida significativa)
        - Reposicionar -> Invocar cuando IsAtBossPosition
        - Invocar -> Regenerar cuando InvocationFinished
        - Regenerar -> EstadoVida (restore_history=True) cuando RegenerationFinished
    """
    INVOKER_BOSS = {
        "name": "invoker boss",
        "debug": {"show_state_over_entity": True},
        "params": {
            "vision_range": 500.0,
            "vision_fov_deg": 120.0,
            "player_seen_memory": 0.5,
            "dist_for_mele": 200.0,
            "boss_position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*55, CONF.MAIN_WIN.RENDER_TILE_SIZE*47),
            "allies_for_invocation": 4,
            "time_for_invocation": 6.0,
            "timeout_invocations": 14.0,
            "perc_regenerate": 0.18,
            "time_for_regeneration": 8.0,
            "lost_health_trigger_pct": 0.25,
            "check_los_throttle": 0.12,
            "attention_direction": "W",
            "attention_distance": 10.0,
            "recent_damage_threshold": 1.0,
            "recent_damage_window": 1.0,
            "arrival_threshold": 24.0
        },
        "root": "Atento",
        "states": {
            # Nivel 1: Atento - boss quieto mirando en dirección configurada (puede ser sorprendido)
            "Atento": {
                "type": "leaf",
                "entry": ["start_attention_facing"],
                "update": ["record_health_tick", "throttle_check_player_visibility", "monitor_player_presence"],
                "exit": [],
                "transitions": [
                    # si el jugador es visible -> EstadoVida
                    {"to": "EstadoVida", "cond": "PlayerVisible", "priority": 250},
                    # si el boss fue dañado recientemente -> EstadoVida
                    {"to": "EstadoVida", "cond": "RecentlyDamaged", "priority": 400},
                ]
            },

            # Nivel 1: EstadoVida - composite que alterna entre melee y ranged
            "EstadoVida": {
                "type": "composite",
                "initial": "AtacarRange",
                "history": "deep",
                "substates": ["AtacarMele", "AtacarRange"],
                "entry": ["record_last_state_start"],
                "update": ["monitor_player_presence"],
                "exit": [],
                "transitions": [
                    # si acumula pérdida de vida >= lost_health_trigger_pct -> Reposicionar
                    {"to": "Reposicionar", "cond": "LostHealthSinceLastRestoreAtLeast", "priority": 300}
                ]
            },

            # Nivel 0: EstadoVida.AtacarMele - perseguir y golpear cuerpo a cuerpo
            "EstadoVida.AtacarMele": {
                "type": "leaf",
                "entry": ["start_pursue_target"],
                "update": ["record_health_tick", "pursue_tick", "try_melee_attack", "throttle_check_player_visibility"],
                "exit": ["stop_pursue"],
                "transitions": [
                    # si el player está visible y más lejos que dist_for_mele -> cambiar a ranged
                    {"to": "EstadoVida.AtacarRange", "cond": "PlayerBeyondMelee", "priority": 150},
                ]
            },

            # Nivel 0: EstadoVida.AtacarRange - ataques a distancia (lanza figura / AOE proyectil)
            "EstadoVida.AtacarRange": {
                "type": "leaf",
                "entry": ["start_boss_range_attack_mode"],
                "update": ["record_health_tick", "boss_range_attack_tick", "throttle_check_player_visibility"],
                "exit": ["stop_boss_range_attack_mode"],
                "transitions": [
                    # si el player está visible y dentro de melee -> volver a melee
                    {"to": "EstadoVida.AtacarMele", "cond": "PlayerWithinMelee", "priority": 150},
                ]
            },

            # Nivel 1: Reposicionar - pathfinding hacia boss_position + pathfollowing
            "Reposicionar": {
                "type": "leaf",
                "entry": ["start_return_to_boss_position"],
                "update": ["return_to_boss_tick", "throttle_check_player_visibility", "record_health_tick"],
                "exit": ["stop_return_to_boss_position"],
                "transitions": [
                    # Cuando alcanza boss_position -> Invocar
                    {"to": "Invocar", "cond": "IsAtBossPosition", "priority": 200},
                ]
            },

            # Nivel 1: Invocar - generar aliados que persiguen al player
            "Invocar": {
                "type": "leaf",
                "entry": ["start_invocation"],
                "update": ["invocation_tick"],
                "exit": ["stop_invocation"],
                "transitions": [
                    # Cuando concluye el proceso de invocación -> Regenerar
                    {"to": "Regenerar", "cond": "InvocationFinished", "priority": 250}
                ]
            },

            # Nivel 1: Regenerar - aplica regeneración de perc_regenerate en time_for_regeneration
            "Regenerar": {
                "type": "leaf",
                "entry": ["start_regeneration"],
                "update": ["regen_tick", "face_towards_safe_anchor", "monitor_player_presence"],
                "exit": ["stop_regeneration", "reset_lost_health_accum"],
                "transitions": [
                    # Al completar la regeneración, volver al EstadoVida (restaurando historia)
                    {"to": "EstadoVida", "cond": "RegenerationFinished", "priority": 300, "restore_history": True}
                ]
            },
        }
    }