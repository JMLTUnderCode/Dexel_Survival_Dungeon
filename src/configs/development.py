import os

def extract_value_env(value) -> bool | int:
    # En caso de valor numerico
    if value.strip().isdigit():
        return int(value.strip())
    # En caso de booleano
    if value.strip().lower() in ["true", "yes", "on"]:
        return True
    return False

DEBUG = None

COLLISION_RECTS = None

ACTIVE_ALG = None

PATHFOLLOWER = None

NAV_MESH = None
NODE_LOCATION = None
PATHFINDER = None
TEMP_PATHFOLLOWER = None

HSM = None
ACTIVE_BEHAVIOR = None
MAX_HSM_HISTORY_SIZE = 0

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if (line.strip() == ""):
                continue
            field, value = line.strip().split("=", 1)
            match field:
                case "DEBUG":
                    DEBUG = extract_value_env(value)
                case "COLLISION_RECTS":
                    COLLISION_RECTS = extract_value_env(value)
                case "ACTIVE_ALG":
                    ACTIVE_ALG = extract_value_env(value)
                case "PATHFOLLOWER":
                    PATHFOLLOWER = extract_value_env(value)
                case "TEMP_PATHFOLLOWER":
                    TEMP_PATHFOLLOWER = extract_value_env(value)
                case "PATHFINDER":
                    PATHFINDER = extract_value_env(value)
                case "NAV_MESH":
                    NAV_MESH = extract_value_env(value)
                case "NODE_LOCATION":
                    NODE_LOCATION = extract_value_env(value)
                case "HSM":
                    HSM = extract_value_env(value)
                case "ACTIVE_BEHAVIOR":
                    ACTIVE_BEHAVIOR = extract_value_env(value)
                case "MAX_HSM_HISTORY_SIZE":
                    MAX_HSM_HISTORY_SIZE = extract_value_env(value)

        

