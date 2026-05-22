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
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[2,1,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]],
                   [[2,1,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False], [0,0,0,False,False]]]

def get_square_under_mouse():
    x, y = pygame.mouse.get_pos()
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    if 0 <= col < COLS and 0 <= row < ROWS:
        return (row, col)
    return None

def show_move_guide(cords):
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
                    if GLOBAL_REGISTER[i][j][0] == 0:
                        available.append((i, j))

    print(available)
    

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = get_square_under_mouse()
                    print(clicked)
                    if clicked == selected:
                        selected = None
                    else:
                        selected = clicked
                        if selected:
                            print(f"Selected: row={selected[0]}, col={selected[1]}")
                            show_move_guide((selected[0], selected[1]))


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    selected = None
                if event.key == pygame.K_r:
                    print("Reset triggered")
                if event.key == pygame.K_q:
                    running = False

        screen.fill((30, 30, 30))
        draw_grid(screen, hovered, selected)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()