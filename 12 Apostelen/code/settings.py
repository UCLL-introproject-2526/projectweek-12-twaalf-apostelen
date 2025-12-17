import os

# code/ -> één map omhoog = Vampire survivor/
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

WIDTH, HEIGHT = 1280, 720
FPS = 60
TITLE = "12 Apostelen"

# Player
PLAYER_SPEED = 260
SPRINT_MULTIPLIER = 1.5

PLAYER_SCALE = 0.75
PLAYER_ANIMATION_SPEED = 10

PLAYER_HEALTH = 100

# Sprint / stamina
STAMINA_MAX = 1.0          # 1 seconde sprint
STAMINA_DRAIN = 1.0        # per seconde leeg
STAMINA_RECOVER = 0.2      # per seconde terug

# Bullets
BULLET_SPEED = 750
BULLET_COOLDOWN = 650      # ms (trager schieten)

# Enemies
ENEMY_SPEED = 150
ENEMY_DAMAGE_PER_SEC = 30  # damage per seconde bij aanraken
ENEMY_ANIMATION_SPEED = 8
SPAWN_INTERVAL = 1     # seconds
