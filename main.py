import pygame
import random

COLS, ROWS = 9, 9
SQUARE_SIZE = 80
SIDEBAR_W = 300
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE
TURN = 1

# Game state: 'config', 'placing', 'running', 'ended'
GAME_STATE = 'config'

# Sidebar / game config
TIME_OPTIONS = [10 * 60, 5 * 60, 1 * 60, 0]  # last is custom (seconds)
selected_time_idx = 0
custom_minutes_input = ""
player_times = [0, 0]
show_env_during_placement = True
last_tick = None

# Placement phase data
placing_pools = {
    1: {1:1, 2:3, 3:2, 4:2, 5:1},
    2: {1:1, 2:3, 3:2, 4:2, 5:1},
}
placing_player = 1
placing_selected_piece = None
chosen_start_secs = None
placement_message = ""
placement_msg_timer = 0.0
winner = None


def wipe_board():
    global GLOBAL_REGISTER
    for r in range(ROWS):
        for c in range(COLS):
            GLOBAL_REGISTER[r][c] = [0, 0, 0, False, False]


def place_environment():
    """Place environment pieces randomly in the middle 5x9 area (rows 2..6, cols 0..8).
    Pieces: 3 forests (type 10), 2 mountains (12), 2 ponds (11).
    """
    wipe_board()  # start from empty board
    choices = [10] * 3 + [12] * 2 + [11] * 2
    positions = [(r, c) for r in range(2, 7) for c in range(COLS)]
    random.shuffle(positions)
    for i, piece in enumerate(choices):
        if i < len(positions):
            r, c = positions[i]
            GLOBAL_REGISTER[r][c] = [piece, 0, 0, False, False]

# GLOBAL REGISTER
# 0 -> type, 1 -> whos piece, 2 -> hp, 3 -> in forest?, 4 -> is discovered?
# ---------
# TYPE: 
#   Player pieces| 0=None 1=BASE 2=Troops 3=Tank 4=Drone 5=Artillery
#   Environmental pieces| 10=Forest 11=Pond 12=Mountain
# WHOSE PIECE:
#   0=None 1=Player1 2=Player2
# HP:
#   0=None 1-3=Piece HP
# IN FOREST:
#   False=No True=Yes
# IS DISCOVERED:
#   False=No True=Yes

GLOBAL_REGISTER = [[[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]]]

def get_square_under_mouse():
    x, y = pygame.mouse.get_pos()
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    if 0 <= col < COLS and 0 <= row < ROWS:
        return (row, col)
    return None


def piece_palette(owner):
    if owner == 1:
        return {
            "primary": (40, 90, 210),
            "dark": (20, 50, 120),
            "light": (150, 180, 255),
            "accent": (200, 200, 220),
        }
    if owner == 2:
        return {
            "primary": (210, 70, 70),
            "dark": (120, 30, 30),
            "light": (255, 160, 160),
            "accent": (220, 200, 200),
        }
    return {
        "primary": (110, 110, 110),
        "dark": (60, 60, 60),
        "light": (170, 170, 170),
        "accent": (200, 200, 200),
    }


def max_hp_for_type(t):
    return {
        1: 3,  # BASE
        2: 1,  # Troops
        3: 2,  # Tank
        4: 1,  # Drone
        5: 3,  # Artillery
    }.get(t, 1)

def get_move_guide(cords):
    global GLOBAL_REGISTER

    available = []

    match GLOBAL_REGISTER[cords[0]][cords[1]][0]:
        case 0:
            return None
        case 1:
            return None
        case 2:
            bvA = cords[0]
            bvB = cords[1]
            StartScopeA = bvA - 1 if bvA - 1 >= 0 else bvA
            StartScopeB = bvB - 1 if bvB - 1 >= 0 else bvB
            EndScopeA = bvA + 1 if bvA + 1 <= 8 else bvA
            EndScopeB = bvB + 1 if bvB + 1 <= 8 else bvB

            for i in range(StartScopeA, EndScopeA + 1, 1):
                for j in range(StartScopeB, EndScopeB + 1, 1):
                    if GLOBAL_REGISTER[i][j][0] == 0 or GLOBAL_REGISTER[i][j][0] == 10:
                        available.append((i, j))

        case 3:
            bvA = cords[0]
            bvB = cords[1]
            StartScopeA = bvA - 1 if bvA - 1 >= 0 else bvA
            StartScopeB = bvB - 1 if bvB - 1 >= 0 else bvB
            EndScopeA = bvA + 1 if bvA + 1 <= 8 else bvA
            EndScopeB = bvB + 1 if bvB + 1 <= 8 else bvB

            for i in range(StartScopeA, EndScopeA + 1, 1):
                for j in range(StartScopeB, EndScopeB + 1, 1):
                    if GLOBAL_REGISTER[i][j][0] == 0 or GLOBAL_REGISTER[i][j][0] == 10:
                        available.append((i, j))

        case 4:
            bvA = cords[0]
            bvB = cords[1]
            directions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),           (0, 1),
                (1, -1),  (1, 0),  (1, 1),
            ]

            for deltaA, deltaB in directions:
                for distance in range(1, 4):
                    i = bvA + (deltaA * distance)
                    j = bvB + (deltaB * distance)

                    if i < 0 or i > 8 or j < 0 or j > 8:
                        break

                    if GLOBAL_REGISTER[i][j][0] == 0 or GLOBAL_REGISTER[i][j][0] == 10:
                        available.append((i, j))
                    else:
                        break
        case 5:
            bvA = cords[0]
            bvB = cords[1]
            StartScopeA = bvA - 1 if bvA - 1 >= 0 else bvA
            StartScopeB = bvB - 1 if bvB - 1 >= 0 else bvB
            EndScopeA = bvA + 1 if bvA + 1 <= 8 else bvA
            EndScopeB = bvB + 1 if bvB + 1 <= 8 else bvB

            for i in range(StartScopeA, EndScopeA + 1, 1):
                for j in range(StartScopeB, EndScopeB + 1, 1):
                    if GLOBAL_REGISTER[i][j][0] == 0:
                        available.append((i, j))

    return available

def get_discover_guide(cords):
    global GLOBAL_REGISTER

    if cords is None:
        return None
    
    if GLOBAL_REGISTER[cords[0]][cords[1]][0] != 4:
        return None

    drone_owner = GLOBAL_REGISTER[cords[0]][cords[1]][1]
    available = []

    def is_enemy_at(row, col):
        return GLOBAL_REGISTER[row][col][0] in (1, 2, 3, 4, 5) and GLOBAL_REGISTER[row][col][1] != drone_owner

    bvA = cords[0]
    bvB = cords[1]
    StartScopeA = bvA - 1 if bvA - 1 >= 0 else bvA
    StartScopeB = bvB - 1 if bvB - 1 >= 0 else bvB
    EndScopeA = bvA + 1 if bvA + 1 <= 8 else bvA
    EndScopeB = bvB + 1 if bvB + 1 <= 8 else bvB

    for i in range(StartScopeA, EndScopeA + 1, 1):
        for j in range(StartScopeB, EndScopeB + 1, 1):
            if (i, j) != cords and is_enemy_at(i, j) and not GLOBAL_REGISTER[i][j][4]:
                available.append((i, j))

    return available

def get_shoot_guide(cords):
    global GLOBAL_REGISTER

    if cords is None:
        return None

    available = []

    shooter_type = GLOBAL_REGISTER[cords[0]][cords[1]][0]
    shooter_owner = GLOBAL_REGISTER[cords[0]][cords[1]][1]

    if shooter_type == 4:
        return None

    def is_enemy_at(row, col):
        return GLOBAL_REGISTER[row][col][0] in (1, 2, 3, 4, 5) and GLOBAL_REGISTER[row][col][1] != shooter_owner

    match GLOBAL_REGISTER[cords[0]][cords[1]][0]:
        case 0:
            return None
        case 1:
            return None
        case 2:
            bvA = cords[0]
            bvB = cords[1]
            StartScopeA = bvA - 1 if bvA - 1 >= 0 else bvA
            StartScopeB = bvB - 1 if bvB - 1 >= 0 else bvB
            EndScopeA = bvA + 1 if bvA + 1 <= 8 else bvA
            EndScopeB = bvB + 1 if bvB + 1 <= 8 else bvB

            for i in range(StartScopeA, EndScopeA + 1, 1):
                for j in range(StartScopeB, EndScopeB + 1, 1):
                    if (i, j) != cords and is_enemy_at(i, j):
                        available.append((i, j))

        case 3:
            bvA = cords[0]
            bvB = cords[1]
            directions = [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
            ]

            for deltaA, deltaB in directions:
                for distance in range(1, 3):
                    i = bvA + (deltaA * distance)
                    j = bvB + (deltaB * distance)

                    if i < 0 or i > 8 or j < 0 or j > 8:
                        break

                    if is_enemy_at(i, j):
                        available.append((i, j))

        case 4:
            bvA = cords[0]
            bvB = cords[1]
            StartScopeA = bvA - 1 if bvA - 1 >= 0 else bvA
            StartScopeB = bvB - 1 if bvB - 1 >= 0 else bvB
            EndScopeA = bvA + 1 if bvA + 1 <= 8 else bvA
            EndScopeB = bvB + 1 if bvB + 1 <= 8 else bvB

            for i in range(StartScopeA, EndScopeA + 1, 1):
                for j in range(StartScopeB, EndScopeB + 1, 1):
                    if (i, j) != cords and is_enemy_at(i, j) and GLOBAL_REGISTER[i][j][4]:
                        available.append((i, j))

        case 5:
            bvA = cords[0]
            bvB = cords[1]

            directions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),             (0, 1),
                (1, -1),  (1, 0),  (1, 1),
            ]

            for deltaA, deltaB in directions:
                for distance in range(1, 9):
                    i = bvA + (deltaA * distance)
                    j = bvB + (deltaB * distance)

                    if i < 0 or i > 8 or j < 0 or j > 8:
                        break

                    if is_enemy_at(i, j) and GLOBAL_REGISTER[i][j][4]:
                        available.append((i, j))

    return available

def display_pieces(screen):
    global GLOBAL_REGISTER
    global show_env_during_placement, GAME_STATE

    font = pygame.font.SysFont(None, 24)

    # use top-level piece_palette

    for row in range(ROWS):
        for col in range(COLS):
            piece_type = GLOBAL_REGISTER[row][col][0]
            owner = GLOBAL_REGISTER[row][col][1]
            if piece_type == 0:
                continue

            if piece_type == 10:
                # environmental piece: show only if configured during placement or if game already started
                if GAME_STATE == 'placing' and not show_env_during_placement:
                    continue
                tree_rect = pygame.Rect(col * SQUARE_SIZE + 22, row * SQUARE_SIZE + 18, 36, 44)
                pygame.draw.ellipse(screen, (34, 139, 34), tree_rect)
                pygame.draw.ellipse(screen, (20, 80, 20), tree_rect, 2)
                continue

            if piece_type == 11:
                if GAME_STATE == 'placing' and not show_env_during_placement:
                    continue
                pond_rect = pygame.Rect(col * SQUARE_SIZE + 22, row * SQUARE_SIZE + 18, 36, 44)
                pygame.draw.ellipse(screen, (34, 139, 238), pond_rect)
                pygame.draw.ellipse(screen, (20, 80, 238), pond_rect, 2)
                continue

            if piece_type == 12:
    
                if GAME_STATE == 'placing' and not show_env_during_placement:
                    continue

                snow_cap = [
                    (col * SQUARE_SIZE + 40, row * SQUARE_SIZE + 8),   
                    (col * SQUARE_SIZE + 26, row * SQUARE_SIZE + 28),  
                    (col * SQUARE_SIZE + 54, row * SQUARE_SIZE + 28),  
                ]
                mountain_body = [
                    (col * SQUARE_SIZE + 40, row * SQUARE_SIZE + 8),  
                    (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 58), 
                    (col * SQUARE_SIZE + 70, row * SQUARE_SIZE + 58),
                ]

                pygame.draw.polygon(screen, (105, 105, 105), mountain_body) 
                pygame.draw.polygon(screen, (70, 70, 70), mountain_body, 2)
                pygame.draw.polygon(screen, (235, 245, 255), snow_cap)
                pygame.draw.polygon(screen, (180, 200, 220), snow_cap, 1)
                continue

            center_x = col * SQUARE_SIZE + 40
            center_y = row * SQUARE_SIZE + 40
            palette = piece_palette(owner)
            color = palette["primary"]

            # ensure piece has HP initialized
            max_hp = max_hp_for_type(piece_type)
            if GLOBAL_REGISTER[row][col][2] == 0:
                GLOBAL_REGISTER[row][col][2] = max_hp

            if piece_type == 1:
                outer_rect = pygame.Rect(col * SQUARE_SIZE + 14, row * SQUARE_SIZE + 14, 52, 52)
                inner_rect = pygame.Rect(col * SQUARE_SIZE + 22, row * SQUARE_SIZE + 22, 36, 36)
                pygame.draw.rect(screen, color, outer_rect, border_radius=6)
                pygame.draw.rect(screen, (20, 20, 20), outer_rect, 3, border_radius=6)
                pygame.draw.rect(screen, (240, 240, 240), inner_rect, 2, border_radius=4)
                label = font.render("B", True, (255, 255, 255))
                screen.blit(label, (center_x - 6, center_y - 10))

            elif piece_type == 2:
                primary = palette["primary"]
                dark = palette["dark"]
                light = palette["light"]
                accent = palette["accent"]

                body_rect = pygame.Rect(col * SQUARE_SIZE + 27, row * SQUARE_SIZE + 28, 26, 24)
                pack_rect = pygame.Rect(col * SQUARE_SIZE + 21, row * SQUARE_SIZE + 31, 12, 18)
                helmet_rect = pygame.Rect(col * SQUARE_SIZE + 28, row * SQUARE_SIZE + 15, 24, 16)
                boots_left = pygame.Rect(col * SQUARE_SIZE + 28, row * SQUARE_SIZE + 52, 8, 8)
                boots_right = pygame.Rect(col * SQUARE_SIZE + 44, row * SQUARE_SIZE + 52, 8, 8)

                pygame.draw.rect(screen, dark, pack_rect, border_radius=3)
                pygame.draw.rect(screen, primary, body_rect, border_radius=4)
                pygame.draw.rect(screen, (20, 20, 20), body_rect, 2, border_radius=4)
                pygame.draw.rect(screen, primary, helmet_rect, border_radius=8)
                pygame.draw.rect(screen, (20, 20, 20), helmet_rect, 2, border_radius=8)
                pygame.draw.circle(screen, light, (center_x, row * SQUARE_SIZE + 28), 5)
                pygame.draw.line(screen, dark, (center_x - 2, row * SQUARE_SIZE + 33), (center_x + 12, row * SQUARE_SIZE + 46), 4)
                pygame.draw.line(screen, dark, (center_x + 10, row * SQUARE_SIZE + 35), (center_x + 24, row * SQUARE_SIZE + 29), 4)
                pygame.draw.line(screen, dark, (center_x + 12, row * SQUARE_SIZE + 32), (center_x + 30, row * SQUARE_SIZE + 22), 2)
                pygame.draw.line(screen, dark, (center_x - 4, row * SQUARE_SIZE + 50), (center_x - 8, row * SQUARE_SIZE + 59), 4)
                pygame.draw.line(screen, dark, (center_x + 10, row * SQUARE_SIZE + 50), (center_x + 14, row * SQUARE_SIZE + 59), 4)
                pygame.draw.rect(screen, (30, 30, 30), boots_left, border_radius=2)
                pygame.draw.rect(screen, (30, 30, 30), boots_right, border_radius=2)

            elif piece_type == 3:
                body_rect = pygame.Rect(col * SQUARE_SIZE + 16, row * SQUARE_SIZE + 26, 48, 24)
                turret_rect = pygame.Rect(col * SQUARE_SIZE + 28, row * SQUARE_SIZE + 16, 24, 24)
                pygame.draw.rect(screen, color, body_rect, border_radius=4)
                pygame.draw.rect(screen, (25, 25, 25), body_rect, 2, border_radius=4)
                pygame.draw.rect(screen, color, turret_rect, border_radius=12)
                pygame.draw.rect(screen, (25, 25, 25), turret_rect, 2, border_radius=12)
                pygame.draw.line(screen, (25, 25, 25), (center_x, center_y), (center_x, center_y - 18), 4)
                pygame.draw.line(screen, (25, 25, 25), (center_x - 18, center_y + 12), (center_x + 18, center_y + 12), 3)

            elif piece_type == 4:
                pygame.draw.circle(screen, color, (center_x, center_y), 18)
                pygame.draw.circle(screen, (25, 25, 25), (center_x, center_y), 18, 2)
                pygame.draw.line(screen, (25, 25, 25), (center_x - 22, center_y), (center_x + 22, center_y), 2)
                pygame.draw.line(screen, (25, 25, 25), (center_x, center_y - 22), (center_x, center_y + 22), 2)
                pygame.draw.circle(screen, (240, 240, 240), (center_x, center_y), 5)

            elif piece_type == 5:
                body_points = [
                    (center_x - 18, center_y + 16),
                    (center_x + 18, center_y + 16),
                    (center_x + 10, center_y - 12),
                    (center_x - 10, center_y - 12),
                ]
                pygame.draw.polygon(screen, color, body_points)
                pygame.draw.polygon(screen, (25, 25, 25), body_points, 2)
                pygame.draw.line(screen, (25, 25, 25), (center_x + 8, center_y - 8), (center_x + 28, center_y - 20), 4)
                pygame.draw.line(screen, (25, 25, 25), (center_x - 8, center_y + 4), (center_x + 8, center_y + 4), 3)
                label = font.render("A", True, (255, 255, 255))
                screen.blit(label, (center_x - 5, center_y - 10))

            # draw HP bar
            if piece_type not in [10, 11, 12]:
                cur_hp = GLOBAL_REGISTER[row][col][2]
                bar_w = 36
                bar_h = 6
                bar_x = center_x - bar_w // 2
                bar_y = row * SQUARE_SIZE + 62
                pygame.draw.rect(screen, (20, 20, 20), (bar_x, bar_y, bar_w, bar_h), 1)
                fill_w = 0
                if max_hp > 0:
                    fill_w = int(((cur_hp / max_hp) * (bar_w - 2)))
                if fill_w > 0:
                    pygame.draw.rect(screen, palette["accent"], (bar_x + 1, bar_y + 1, fill_w, bar_h - 2))

def draw_grid(screen, hovered, selected):
    isRev = False
    global GAME_STATE, placing_selected_piece, placing_player
    for row in range(ROWS):
        
        isRev = False if isRev else True
            
        for col in range(COLS):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            
            if (col % 2 != 0 and not isRev) or (col % 2 == 0 and isRev):
                color = (125, 206, 130)
            else:
                color = (255, 255, 255)

            if (row, col) == selected:
                color = (255, 215, 0)
            elif (row, col) == hovered:
                color = (220, 220, 100)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)
            # placement hover validation outline
            if GAME_STATE == 'placing' and placing_selected_piece is not None and hovered == (row, col):
                # valid if square empty and within player's two rows
                valid = False
                if GLOBAL_REGISTER[row][col][0] == 0:
                    if placing_player == 1:
                        valid = row >= ROWS - 2
                    else:
                        valid = row <= 1
                outline_color = (0, 200, 0) if valid else (200, 40, 40)
                pygame.draw.rect(screen, outline_color, rect, 3, border_radius=4)


def draw_sidebar(screen):
    # draw panel background
    panel_rect = pygame.Rect(WIDTH, 0, SIDEBAR_W, HEIGHT)
    pygame.draw.rect(screen, (40, 40, 40), panel_rect)

    font = pygame.font.SysFont(None, 22)
    big_font = pygame.font.SysFont(None, 28)

    # Turn display
    turn_color = piece_palette(TURN)["primary"]
    header_rect = pygame.Rect(WIDTH + 10, 10, SIDEBAR_W - 20, 60)
    pygame.draw.rect(screen, turn_color, header_rect, border_radius=6)
    pygame.draw.rect(screen, (15, 15, 15), header_rect, 2, border_radius=6)
    header_txt = big_font.render(f"Turn: Player {TURN}", True, (255, 255, 255))
    screen.blit(header_txt, (WIDTH + 20, 20))

    # timers
    def fmt_time(t):
        if t < 0:
            t = 0
        m = int(t) // 60
        s = int(t) % 60
        return f"{m:02d}:{s:02d}"

    # timers (moved slightly up to avoid overlapping placement text)
    p1_txt = font.render(f"Player 1: {fmt_time(player_times[0])}", True, (220, 220, 220))
    p2_txt = font.render(f"Player 2: {fmt_time(player_times[1])}", True, (220, 220, 220))
    screen.blit(p1_txt, (WIDTH + 15, 80))
    screen.blit(p2_txt, (WIDTH + 15, 108))

    # placement pools (when in placing state)
    pool_start_y = 170
    pool_h = 36
    pool_gap = 10
    piece_labels = {1: "Base", 2: "Troop", 3: "Tank", 4: "Drone", 5: "Artillery"}
    if GAME_STATE == 'placing':
        placing_lbl = font.render(f"Placing: Player {placing_player}", True, (240, 240, 240))
        screen.blit(placing_lbl, (WIDTH + 15, pool_start_y - 20))
        pools = placing_pools.get(placing_player, {})
        for idx, ptype in enumerate([1,2,3,4,5]):
            btn_rect = pygame.Rect(WIDTH + 20, pool_start_y + idx * (pool_h + pool_gap), SIDEBAR_W - 40, pool_h)
            # highlight if selected
            if placing_selected_piece == ptype:
                pygame.draw.rect(screen, (100, 100, 140), btn_rect, border_radius=6)
            else:
                pygame.draw.rect(screen, (60, 60, 60), btn_rect, border_radius=6)
            pygame.draw.rect(screen, (20, 20, 20), btn_rect, 2, border_radius=6)
            lbl_txt = font.render(f"{piece_labels[ptype]} x{pools.get(ptype,0)}", True, (240,240,240))
            screen.blit(lbl_txt, (btn_rect.x + 10, btn_rect.y + 8))
        # show placement message if present
        if placement_msg_timer > 0 and placement_message:
            msg_txt = font.render(placement_message, True, (255, 200, 60))
            screen.blit(msg_txt, (WIDTH + 15, pool_start_y + 6 * (pool_h + pool_gap)))

    # time options (positioned after placement pool) - only show in config or ended
    if GAME_STATE in ('config', 'ended'):
        opt_start_y = pool_start_y + (5 * (pool_h + pool_gap)) + 20
        opt_h = 36
        labels = ["10:00", "5:00", "1:00", "Custom"]
        for idx, lbl in enumerate(labels):
            btn_rect = pygame.Rect(WIDTH + 20, opt_start_y + idx * (opt_h + 8), SIDEBAR_W - 40, opt_h)
            if idx == selected_time_idx:
                pygame.draw.rect(screen, (80, 80, 80), btn_rect, border_radius=6)
            else:
                pygame.draw.rect(screen, (60, 60, 60), btn_rect, border_radius=6)
            pygame.draw.rect(screen, (20, 20, 20), btn_rect, 2, border_radius=6)
            lbl_txt = font.render(lbl, True, (240, 240, 240))
            screen.blit(lbl_txt, (btn_rect.x + 10, btn_rect.y + 8))
            if idx == 3:
                # show custom minutes input
                custom_txt = font.render(custom_minutes_input or "(mins)", True, (200, 200, 200))
                screen.blit(custom_txt, (btn_rect.right - 80, btn_rect.y + 8))

    # show environment toggle (placed after time options) - only show in config or ended
    if GAME_STATE in ('config', 'ended'):
        toggle_y = opt_start_y + len(labels) * (opt_h + 8) + 10
        toggle_rect = pygame.Rect(WIDTH + 20, toggle_y, 20, 20)
        pygame.draw.rect(screen, (255, 255, 255), toggle_rect, 2)
        if show_env_during_placement:
            pygame.draw.rect(screen, (100, 200, 100), (toggle_rect.x + 3, toggle_rect.y + 3, 14, 14))
        toggle_lbl = font.render("Show environment during placement", True, (220, 220, 220))
        screen.blit(toggle_lbl, (toggle_rect.right + 10, toggle_y - 2))

    # start / end button
    start_rect = pygame.Rect(WIDTH + 30, HEIGHT - 90, SIDEBAR_W - 60, 60)
    if GAME_STATE in ('config', 'ended'):
        pygame.draw.rect(screen, (80, 160, 80), start_rect, border_radius=6)
        start_txt = big_font.render("Start", True, (255, 255, 255))
        screen.blit(start_txt, (start_rect.x + (start_rect.width - start_txt.get_width()) // 2, start_rect.y + 10))
    elif GAME_STATE in ('placing','running'):
        pygame.draw.rect(screen, (160, 80, 80), start_rect, border_radius=6)
        end_txt = big_font.render("End Game", True, (255, 255, 255))
        screen.blit(end_txt, (start_rect.x + (start_rect.width - end_txt.get_width()) // 2, start_rect.y + 10))
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH + SIDEBAR_W, HEIGHT))
    pygame.display.set_caption("BaseHunt")
    clock = pygame.time.Clock()

    selected = None
    running = True
    global selected_time_idx, custom_minutes_input, player_times, show_env_during_placement, GAME_STATE, last_tick, TURN, winner
    global placing_player, placing_selected_piece, placing_pools, chosen_start_secs
    custom_input_active = False

    while running:
        # timing
        now = pygame.time.get_ticks()
        if last_tick is None:
            last_tick = now
        dt = (now - last_tick) / 1000.0
        last_tick = now
        if GAME_STATE == 'running' and player_times[TURN - 1] > 0:
            player_times[TURN - 1] -= dt
            if player_times[TURN - 1] <= 0:
                GAME_STATE = 'ended'

        # update placement message timer
        global placement_msg_timer, placement_message
        if placement_msg_timer > 0:
            placement_msg_timer -= dt
            if placement_msg_timer <= 0:
                placement_message = ""

        hovered = get_square_under_mouse()
        # only show move/shoot guides if a piece is selected and it belongs to the current player and game is running
        if selected and GAME_STATE == 'running' and GLOBAL_REGISTER[selected[0]][selected[1]][1] == TURN:
            available = get_move_guide(selected)
            shooting = get_shoot_guide(selected)
            discover = get_discover_guide(selected)
        else:
            available = None
            shooting = None
            discover = None

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # if click in sidebar area
                    if mouse_x >= WIDTH and mouse_x <= WIDTH + SIDEBAR_W:
                        rel_x = mouse_x - WIDTH
                        rel_y = mouse_y
                        # simple UI layout
                        # time options area (match draw_sidebar spacing)
                        pool_start_y = 170
                        pool_h = 36
                        pool_gap = 10
                        opt_start_y = pool_start_y + (5 * (pool_h + pool_gap)) + 20
                        opt_h = 36
                        for idx_pt, ptype in enumerate([1,2,3,4,5]):
                            pool_btn = pygame.Rect(WIDTH + 20, pool_start_y + idx_pt * (pool_h + pool_gap), SIDEBAR_W - 40, pool_h)
                            if pool_btn.collidepoint(mouse_x, mouse_y) and GAME_STATE == 'placing' and placing_pools.get(placing_player, {}).get(ptype,0) > 0:
                                placing_selected_piece = ptype
                        for idx in range(4):
                            btn_rect = pygame.Rect(WIDTH + 20, opt_start_y + idx * (opt_h + 8), SIDEBAR_W - 40, opt_h)
                            if GAME_STATE in ('config', 'ended') and btn_rect.collidepoint(mouse_x, mouse_y):
                                selected_time_idx = idx
                                # if custom button clicked, activate input
                                if idx == 3:
                                    custom_input_active = True
                                else:
                                    custom_input_active = False
                        # show env toggle area (compute like draw_sidebar)
                        toggle_y = opt_start_y + 4 * (opt_h + 8) + 10
                        toggle_rect = pygame.Rect(WIDTH + 20, toggle_y, 20, 20)
                        if GAME_STATE in ('config', 'ended') and toggle_rect.collidepoint(mouse_x, mouse_y):
                            show_env_during_placement = not show_env_during_placement
                        # start / end button
                        start_rect = pygame.Rect(WIDTH + 30, HEIGHT - 90, SIDEBAR_W - 60, 60)
                        if start_rect.collidepoint(mouse_x, mouse_y):
                            if GAME_STATE in ('config', 'ended'):
                                # start placement: determine start time but enter placing phase
                                if selected_time_idx < 3:
                                    secs = TIME_OPTIONS[selected_time_idx]
                                else:
                                    try:
                                        mins = int(custom_minutes_input) if custom_minutes_input != "" else 5
                                    except ValueError:
                                        mins = 5
                                    secs = mins * 60
                                # store chosen start seconds for later
                                chosen_start_secs = secs
                                # reset pools
                                placing_pools[1] = {1:1,2:3,3:2,4:2,5:1}
                                placing_pools[2] = {1:1,2:3,3:2,4:2,5:1}
                                # pick random player to place first
                                placing_player = random.choice([1,2])
                                placing_selected_piece = None
                                GAME_STATE = 'placing'
                                # set winner to None for new game
                                winner = None
                                # generate environment (wipes board first)
                                place_environment()
                                # don't set timers until placement finished
                                continue
                            else:
                                # during placing or running, this acts as "End Game"
                                GAME_STATE = 'ended'
                                # stop timers
                                player_times = [0,0]
                                chosen_start_secs = None
                                # wipe the board at game end
                                wipe_board()
                                # clear winner
                                winner = None
                                continue
                        continue

                    clicked = get_square_under_mouse()
                    if clicked == selected:
                        selected = None
                    else:
                        # Placement: if in placing phase and clicked on board
                        if GAME_STATE == 'placing' and clicked and placing_selected_piece is not None:
                            r, c = clicked
                            # restrict placement to player's two rows
                            allowed = False
                            if placing_player == 1:
                                allowed = r >= ROWS - 2
                            else:
                                allowed = r <= 1
                            if not allowed:
                                # show small message
                                placement_message = "Can't place there"
                                placement_msg_timer = 2.0
                                continue
                            if GLOBAL_REGISTER[r][c][0] == 0:
                                # place the piece
                                GLOBAL_REGISTER[r][c][0] = placing_selected_piece
                                GLOBAL_REGISTER[r][c][1] = placing_player
                                GLOBAL_REGISTER[r][c][2] = max_hp_for_type(placing_selected_piece)
                                GLOBAL_REGISTER[r][c][3] = False
                                GLOBAL_REGISTER[r][c][4] = False
                                # decrement pool
                                placing_pools[placing_player][placing_selected_piece] -= 1
                                # if this piece type depleted, auto-select next available
                                if placing_pools[placing_player][placing_selected_piece] <= 0:
                                    found = None
                                    for p in [1,2,3,4,5]:
                                        if placing_pools[placing_player].get(p,0) > 0:
                                            found = p
                                            break
                                    placing_selected_piece = found

                                # check if current player's pool is empty
                                remaining = sum(placing_pools[placing_player].values())
                                other = 2 if placing_player == 1 else 1
                                other_remaining = sum(placing_pools[other].values())
                                if remaining == 0:
                                    # switch to other player if they have pieces
                                    if other_remaining > 0:
                                        placing_player = other
                                    else:
                                        # both done -> start the main game
                                        secs = chosen_start_secs if chosen_start_secs else 5*60
                                        player_times = [secs, secs]
                                        GAME_STATE = 'running'
                                        TURN = 1
                                        last_tick = pygame.time.get_ticks()
                                # consume click
                                continue

                        # Shooting: if a shooting guide exists and clicked in it
                        if GAME_STATE == 'running' and shooting and clicked in shooting:
                            # shooter owner
                            shooter_owner = GLOBAL_REGISTER[selected[0]][selected[1]][1] if selected else TURN
                            # target info
                            tType = GLOBAL_REGISTER[clicked[0]][clicked[1]][0]
                            tOwner = GLOBAL_REGISTER[clicked[0]][clicked[1]][1]
                            tHP = GLOBAL_REGISTER[clicked[0]][clicked[1]][2]

                            # deal 1 damage
                            new_hp = tHP - 1
                            GLOBAL_REGISTER[clicked[0]][clicked[1]][2] = new_hp

                            # remove piece if HP <= 0
                            if new_hp <= 0:
                                # if base destroyed -> shooter wins
                                if tType == 1:
                                    winner = shooter_owner
                                    GAME_STATE = 'ended'
                                    player_times[0] = 0
                                    player_times[1] = 0
                                    # wipe the board at game end
                                    wipe_board()
                                else:
                                    GLOBAL_REGISTER[clicked[0]][clicked[1]] = [0,0,0,False,False]

                            # end turn only if game still running
                            if GAME_STATE == 'running':
                                TURN = 2 if TURN == 1 else 1
                            selected = None
                        
                        elif GAME_STATE == 'running' and discover and clicked in discover:

                            GLOBAL_REGISTER[clicked[0]][clicked[1]][4] = True

                            if GAME_STATE == 'running':
                                TURN = 2 if TURN == 1 else 1
                            selected = None

                        # Movement: if available moves and clicked in them
                        elif GAME_STATE == 'running' and available and clicked in available:
                            lType = GLOBAL_REGISTER[selected[0]][selected[1]][0]
                            lOwns = GLOBAL_REGISTER[selected[0]][selected[1]][1]
                            lHP = GLOBAL_REGISTER[selected[0]][selected[1]][2]
                            lForest = GLOBAL_REGISTER[selected[0]][selected[1]][3]
                            lDiscovered = GLOBAL_REGISTER[selected[0]][selected[1]][4]

                            GLOBAL_REGISTER[selected[0]][selected[1]][0] = 0
                            GLOBAL_REGISTER[selected[0]][selected[1]][1] = 0
                            GLOBAL_REGISTER[selected[0]][selected[1]][2] = 0
                            GLOBAL_REGISTER[selected[0]][selected[1]][3] = False
                            GLOBAL_REGISTER[selected[0]][selected[1]][4] = False

                            GLOBAL_REGISTER[clicked[0]][clicked[1]][0] = lType
                            GLOBAL_REGISTER[clicked[0]][clicked[1]][1] = lOwns
                            GLOBAL_REGISTER[clicked[0]][clicked[1]][2] = lHP
                            GLOBAL_REGISTER[clicked[0]][clicked[1]][3] = lForest
                            GLOBAL_REGISTER[clicked[0]][clicked[1]][4] = lDiscovered

                            # end turn after move
                            TURN = 2 if TURN == 1 else 1
                            selected = clicked

                        else:
                            # select the clicked square only if it belongs to current player or we're placing
                            if clicked:
                                owner = GLOBAL_REGISTER[clicked[0]][clicked[1]][1]
                                if GAME_STATE != 'running' or owner == TURN:
                                    selected = clicked
                                else:
                                    selected = None
                        

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    selected = None
                    custom_input_active = False
                if event.key == pygame.K_r:
                    print("Reset triggered")
                if event.key == pygame.K_q:
                    running = False
                # custom minutes input handling
                if custom_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        custom_minutes_input = custom_minutes_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        custom_input_active = False
                    else:
                        # accept digits
                        if event.unicode.isdigit():
                            custom_minutes_input += event.unicode

        screen.fill((30, 30, 30))

        draw_grid(screen, hovered, selected)

        draw_sidebar(screen)

        if available:
            for i in available:
                pixel_x = i[1] * SQUARE_SIZE + 40
                pixel_y = i[0] * SQUARE_SIZE + 40
                pygame.draw.circle(screen, "gray", (pixel_x, pixel_y), 8)

        display_pieces(screen)

        if shooting:
            for i in shooting:
                pixel_x = i[1] * SQUARE_SIZE + 40
                pixel_y = i[0] * SQUARE_SIZE + 40
                pygame.draw.circle(screen, (180, 40, 40), (pixel_x, pixel_y), 5)

        if discover:
            for i in discover:
                pixel_x = i[1] * SQUARE_SIZE + 40
                pixel_y = i[0] * SQUARE_SIZE + 40
                pygame.draw.circle(screen, (237, 231, 33), (pixel_x, pixel_y), 5)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

main()