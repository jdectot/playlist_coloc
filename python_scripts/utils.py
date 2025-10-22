from envparse import env
from pathlib import Path
import os

def get_env_var(var_name: str) -> str:
    env_path = Path(__file__)
    env.read_envfile(os.path.join(env_path, ".env"))
    try:
        return str(env(var_name))
    except KeyError:
        print("Environment Variable RECORDING_FOLDER not defined")