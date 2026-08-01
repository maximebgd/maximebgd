#!/usr/bin/env python3
"""
Local runner: loads credentials from .env and regenerates dark_mode.svg and
light_mode.svg by running today.py, so you can preview the result before pushing.

Usage:
    python run_local.py

The .env file (git-ignored) must define:
    ACCESS_TOKEN=<github token>
    USER_NAME=<github username>
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(HERE, '.env')
PLACEHOLDER = 'ghp_your_token_here'


def load_env(path):
    """Parse a simple KEY=VALUE .env file (ignores blanks and # comments)."""
    values = {}
    if not os.path.exists(path):
        sys.exit(f"Error: {path} not found. Copy .env.example to .env and fill it in.")
    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def main():
    env_values = load_env(ENV_PATH)

    missing = [k for k in ('ACCESS_TOKEN', 'USER_NAME') if not env_values.get(k)]
    if missing:
        sys.exit(f"Error: missing {', '.join(missing)} in .env")
    if env_values['ACCESS_TOKEN'] == PLACEHOLDER:
        sys.exit("Error: ACCESS_TOKEN is still the placeholder. Put your real token in .env.")

    env = os.environ.copy()
    env.update(env_values)

    print(f"Generating SVGs for '{env_values['USER_NAME']}'...\n")
    result = subprocess.run([sys.executable, 'today.py'], cwd=HERE, env=env)
    if result.returncode != 0:
        sys.exit(result.returncode)

    darks = os.path.join(HERE, 'dark_mode.svg')
    lights = os.path.join(HERE, 'light_mode.svg')
    print("\nDone. Preview the results:")
    print(f"  open {darks}")
    print(f"  open {lights}")


if __name__ == '__main__':
    main()
