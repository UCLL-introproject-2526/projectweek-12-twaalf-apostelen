import os

BASE_DIR = os.path.dirname(__file__)

def asset(path):
    return os.path.join(BASE_DIR, path)



WIDTH, HEIGHT = 1280, 720
FPS = 60
TITLE = "12 Apostelen"

# Player
PLAYER_SPEED = 260
SPRINT_MULTIPLIER = 1.5
PLAYER_SCALE = 0.75
PLAYER_ANIMATION_SPEED = 10
PLAYER_HEALTH = 100

# Stamina
STAMINA_MAX = 1.0
STAMINA_DRAIN = 1.0
STAMINA_RECOVER = 0.1

# Bullets
BULLET_SPEED = 750
BULLET_COOLDOWN = 375
BULLET_SCALE = 0.65

# Enemies
ENEMY_SPEED = 140
ENEMY_DAMAGE_PER_SEC = 30
ENEMY_ANIMATION_SPEED = 15

# Waves
KILLS_PER_WAVE = 15          # aantal enemies per wave
WAVE_TEXT_TIME = 3           # seconden "WAVE X" tonen
WAVE_SPEED_INCREASE = 18
WAVE_SPAWN_DECREASE = 0.075
MIN_SPAWN_INTERVAL = 0.2

# Sound
WAVE_SOUND = 1.5
IMPACT_SOUND = 0.20
SHOOT_SOUND = 0.60
DIE_SOUND = 1
# Intro / controls
CONTROLS_TIME = 5.0   # seconden dat controls-scherm zichtbaar is
