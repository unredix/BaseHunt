import pygame

COLS, ROWS = 9, 9
SQUARE_SIZE = 80
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE

def get_square_under_mouse():
    x, y = pygame.mouse.get_pos()
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    if 0 <= col < COLS and 0 <= row < ROWS:
        return (row, col)
    return None

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
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
                    if clicked == selected:
                        selected = None
                    else:
                        selected = clicked
                        print(f"Selected: row={selected[0]}, col={selected[1]}")

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