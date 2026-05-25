import pygame

COLS, ROWS = 9, 9
SQUARE_SIZE = 80
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE
TURN = 0

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

GLOBAL_REGISTER = [[[4,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [2,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[10,1,0,False,False], [2,1,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[2,1,0,False,False], [1,0,0,False,False], [5,0,0,False,False], [3,0,0,False,False], [4,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]]]

def get_square_under_mouse():
    x, y = pygame.mouse.get_pos()
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    if 0 <= col < COLS and 0 <= row < ROWS:
        return (row, col)
    return None

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

def get_shoot_guide(cords):
    global GLOBAL_REGISTER

    if cords is None:
        return None

    available = []

    def is_piece_at(row, col):
        return GLOBAL_REGISTER[row][col][0] in (1, 2, 3, 4, 5)

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
                    if (i, j) != cords and is_piece_at(i, j):
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

                    if is_piece_at(i, j):
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
                    if (i, j) != cords and is_piece_at(i, j):
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

                    if is_piece_at(i, j):
                        available.append((i, j))

    return available

def display_pieces(screen):
    global GLOBAL_REGISTER

    font = pygame.font.SysFont(None, 24)

    def piece_color(owner):
        if owner == 1:
            return (40, 90, 210)
        if owner == 2:
            return (210, 70, 70)
        return (110, 110, 110)

    for row in range(ROWS):
        for col in range(COLS):
            piece_type = GLOBAL_REGISTER[row][col][0]
            owner = GLOBAL_REGISTER[row][col][1]
            if piece_type == 0 or piece_type == 10:
                continue

            center_x = col * SQUARE_SIZE + 40
            center_y = row * SQUARE_SIZE + 40
            color = piece_color(owner)

            if piece_type == 1:
                outer_rect = pygame.Rect(col * SQUARE_SIZE + 14, row * SQUARE_SIZE + 14, 52, 52)
                inner_rect = pygame.Rect(col * SQUARE_SIZE + 22, row * SQUARE_SIZE + 22, 36, 36)
                pygame.draw.rect(screen, color, outer_rect, border_radius=6)
                pygame.draw.rect(screen, (20, 20, 20), outer_rect, 3, border_radius=6)
                pygame.draw.rect(screen, (240, 240, 240), inner_rect, 2, border_radius=4)
                label = font.render("B", True, (255, 255, 255))
                screen.blit(label, (center_x - 6, center_y - 10))

            elif piece_type == 2:
                army_green = (92, 112, 62)
                army_dark = (46, 56, 32)
                army_light = (138, 156, 92)
                rifle_color = (54, 36, 22)

                body_rect = pygame.Rect(col * SQUARE_SIZE + 27, row * SQUARE_SIZE + 28, 26, 24)
                pack_rect = pygame.Rect(col * SQUARE_SIZE + 21, row * SQUARE_SIZE + 31, 12, 18)
                helmet_rect = pygame.Rect(col * SQUARE_SIZE + 28, row * SQUARE_SIZE + 15, 24, 16)
                boots_left = pygame.Rect(col * SQUARE_SIZE + 28, row * SQUARE_SIZE + 52, 8, 8)
                boots_right = pygame.Rect(col * SQUARE_SIZE + 44, row * SQUARE_SIZE + 52, 8, 8)

                pygame.draw.rect(screen, army_dark, pack_rect, border_radius=3)
                pygame.draw.rect(screen, army_green, body_rect, border_radius=4)
                pygame.draw.rect(screen, (20, 20, 20), body_rect, 2, border_radius=4)
                pygame.draw.rect(screen, army_green, helmet_rect, border_radius=8)
                pygame.draw.rect(screen, (20, 20, 20), helmet_rect, 2, border_radius=8)
                pygame.draw.circle(screen, army_light, (center_x, row * SQUARE_SIZE + 28), 5)
                pygame.draw.line(screen, army_dark, (center_x - 2, row * SQUARE_SIZE + 33), (center_x + 12, row * SQUARE_SIZE + 46), 4)
                pygame.draw.line(screen, rifle_color, (center_x + 10, row * SQUARE_SIZE + 35), (center_x + 24, row * SQUARE_SIZE + 29), 4)
                pygame.draw.line(screen, rifle_color, (center_x + 12, row * SQUARE_SIZE + 32), (center_x + 30, row * SQUARE_SIZE + 22), 2)
                pygame.draw.line(screen, army_dark, (center_x - 4, row * SQUARE_SIZE + 50), (center_x - 8, row * SQUARE_SIZE + 59), 4)
                pygame.draw.line(screen, army_dark, (center_x + 10, row * SQUARE_SIZE + 50), (center_x + 14, row * SQUARE_SIZE + 59), 4)
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

def draw_grid(screen, hovered, selected):
    isRev = False
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
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH + 300, HEIGHT))
    pygame.display.set_caption("BaseHunt")
    clock = pygame.time.Clock()

    selected = None
    running = True

    while running:
        hovered = get_square_under_mouse()
        available = get_move_guide(selected) if selected else None
        shooting = get_shoot_guide(selected) if selected else None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = get_square_under_mouse()
                    if clicked == selected:
                        selected = None
                    else:

                        if available and clicked in available:
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

                        selected = clicked
                        

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    selected = None
                if event.key == pygame.K_r:
                    print("Reset triggered")
                if event.key == pygame.K_q:
                    running = False

        screen.fill((30, 30, 30))

        draw_grid(screen, hovered, selected)

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

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

main()