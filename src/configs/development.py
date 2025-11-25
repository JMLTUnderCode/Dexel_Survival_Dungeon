import os

DEBUG = None
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.strip().startswith("DEBUG="):
                _, value = line.strip().split("=", 1)
                DEBUG = value.strip().lower() == "true" or value.strip() == "1" or value.strip().lower() == "yes" or value.strip().lower() == "on"
                break
MAX_HSM_HISTORY_SIZE = 5