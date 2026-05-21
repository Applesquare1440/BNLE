# ===== DEBUG / DISPLAY =====
ENABLE_DISPLAY = False

# ===== SCHEDULER =====
# Active days (0=Monday, 6=Sunday)
ACTIVE_DAYS = [1, 2, 3, 4, 5, 6]  # Tuesday–Sunday

# Time window (24h format)
START_HOUR = 9
START_MINUTE = 30

END_HOUR = 19
END_MINUTE = 30

# Behavior outside schedule
PARK_ANGLE = 90          # neutral safe position
SLEEP_INTERVAL = 30       # seconds between checks when inactive


# ===== CAMERA =====
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
FPS_TARGET = 10

# ===== DETECTION =====
MODEL_PATH = "models/yolov8n.onnx"
DETECTION_INTERVAL = 5
CONF_THRESHOLD = 0.4
NMS_THRESHOLD = 0.45

# ===== TRACKING =====
USE_CSRT_FALLBACK = True

# ===== CONTROL =====
CP = 6
MAX_STEP = 30.0  # degrees per frame
DEAD_ZONE = 0.05  # 5%

SMOOTHING_ALPHA = 0.2 #lower smoothing with Cp

SERVO_MIN = 0
SERVO_MAX = 180
SERVO_CENTER = 90

GEAR_RATIO = 4.0
# ===== BEHAVIOR =====
TARGET_LOCK_TIME = 5.0
HOLD_TIME = 0.5
LOST_TIMEOUT = 2.0

# ===== IDLE SCAN =====
SCAN_SPEED = 0.25  # deg/frame
SCAN_MIN = 50
SCAN_MAX = 130

# ===== TARGET SELECTION =====
W_RECENCY = 2.0
W_SIZE = 1.0
W_CENTER = 0.5
