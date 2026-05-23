import pygame

COLS, ROWS = 9, 9
SQUARE_SIZE = 80
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE

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
                   [[0,0,0,False,False], [2,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[10,1,0,False,False], [2,1,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[2,1,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]]]

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

    return available

def display_pieces(screen):
    global GLOBAL_REGISTER

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

            if GLOBAL_REGISTER[row][col][0] == 2:
                pygame.draw.line(screen, "black", (col *SQUARE_SIZE + 10, (row + 1) * SQUARE_SIZE - 10), (col *SQUARE_SIZE + 70, (row + 1) * SQUARE_SIZE - 10), 5)
                pygame.draw.line(screen, "black", (SQUARE_SIZE * col + 40, row * SQUARE_SIZE + SQUARE_SIZE - 10), (SQUARE_SIZE * col + 40, row * SQUARE_SIZE + 5), 5)
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

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

main()