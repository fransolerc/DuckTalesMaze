import pygame
from modules.gameMap import GameMap
from modules.config import SIZE_CELL, MARGIN, COLOR_BLACK, COLOR_WHITE


def main():
    pygame.init()

    screen_width = 8 * SIZE_CELL + 2 * MARGIN
    screen_height = 8 * SIZE_CELL + 2 * MARGIN
    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption('DuckTales Maze')

    game_map = GameMap()

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 74)
    ui_font = pygame.font.SysFont(None, 36)
    running = True

    # --- Control de velocidad de la momia ---
    mummy_move_counter = 0
    mummy_speed_patrol = 8  # Más lento cuando patrulla
    mummy_speed_chase = 6   # Más rápido cuando persigue
    mummy_current_speed = mummy_speed_patrol

    torch_timer = 600

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game_map.move_player('UP')
                elif event.key == pygame.K_DOWN:
                    game_map.move_player('DOWN')
                elif event.key == pygame.K_LEFT:
                    game_map.move_player('LEFT')
                elif event.key == pygame.K_RIGHT:
                    game_map.move_player('RIGHT')

        mummy_move_counter += 1
        if mummy_move_counter >= mummy_current_speed:
            mummy_state = game_map.move_mummy()
            mummy_move_counter = 0

            # Ajustar la velocidad para el próximo movimiento
            if mummy_state == 'chase':
                mummy_current_speed = mummy_speed_chase
            else:
                mummy_current_speed = mummy_speed_patrol

        torch_timer -= 1
        if torch_timer <= 0:
            running = False
            show_message(screen, font, 'Torch went out!')

        screen.fill(COLOR_BLACK)
        game_map.draw_map(screen)

        torch_text = ui_font.render(f'Torch: {int(torch_timer / 10)}', True, COLOR_WHITE)
        screen.blit(torch_text, (10, 10))

        score_text = ui_font.render(f'Score: ${game_map.player.get_score()}', True, COLOR_WHITE)
        screen.blit(score_text, (10, 40))

        pygame.display.flip()

        if game_map.check_lose():
            running = False
            show_message(screen, font, '¡You Lose!')

        if game_map.check_victory():
            running = False
            show_message(screen, font, '¡You Win!')

        clock.tick(10)

    pygame.quit()


def show_message(screen, font, title):
    text = font.render(title, True, COLOR_WHITE)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


if __name__ == "__main__":
    main()
