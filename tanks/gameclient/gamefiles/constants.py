import os
BLACK = (0,0,0)
FPS = 25
WINDOW_SIZE = (500, 500)
PICTURE_FOLDER = os.path.join(os.path.dirname(__file__), "pictures")
TANKUP_FILE = os.path.join(PICTURE_FOLDER, "tanku.png")
TANKDOWN_FILE = os.path.join(PICTURE_FOLDER, "tankd.png")
TANKLEFT_FILE = os.path.join(PICTURE_FOLDER, "tankl.png")
TANKRIGHT_FILE = os.path.join(PICTURE_FOLDER, "tankr.png")
PLAYER_SPEED = 15