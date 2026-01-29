import pygame
from modules.gameMap import GameMap
from modules.config import SIZE_CELL, MARGIN, COLOR_BLACK, COLOR_WHITE


def handle_input(game_map):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game_map.move_player('UP')
            elif event.key == pygame.K_DOWN:
                game_map.move_player('DOWN')
            elif event.key == pygame.K_LEFT:
                game_map.move_player('LEFT')
            elif event.key == pygame.K_RIGHT:
                game_map.move_player('RIGHT')
    return True


def draw_ui(screen, ui_font, torch_timer, score):
    torch_text = ui_font.render(f'Torch: {int(torch_timer / 10)}', True, COLOR_WHITE)
    screen.blit(torch_text, (10, 10))

    score_text = ui_font.render(f'Score: ${score}', True, COLOR_WHITE)
    screen.blit(score_text, (10, 40))


def show_message(screen, font, title):
    text = font.render(title, True, COLOR_WHITE)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


def main():
    pygame.init()

    screen_width = 8 * SIZE_CELL + 2 * MARGIN
    screen_height = 8 * SIZE_CELL + 2 * MARGIN
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('DuckTales Maze')
    font = pygame.font.SysFont(None, 74)
    ui_font = pygame.font.SysFont(None, 36)

    game_map = GameMap()
    clock = pygame.time.Clock()

    running = True
    mummy_move_counter = 0
    mummy_speeds = {'patrol': 7, 'chase': 3}
    mummy_current_speed = mummy_speeds['patrol']
    torch_timer = 600

    while running:
        running = handle_input(game_map)
        if not running:
            break

        mummy_move_counter += 1
        if mummy_move_counter >= mummy_current_speed:
            mummy_state = game_map.move_mummy()
            mummy_move_counter = 0
            mummy_current_speed = mummy_speeds.get(mummy_state, mummy_speeds['patrol'])

        torch_timer -= 1

        screen.fill(COLOR_BLACK)
        game_map.draw_map(screen)
        draw_ui(screen, ui_font, torch_timer, game_map.player.get_score())
        pygame.display.flip()

        end_message = None
        if game_map.check_lose():
            end_message = '¡You Lose!'
        elif game_map.check_victory():
            end_message = '¡You Win!'
        elif torch_timer <= 0:
            end_message = 'Torch went out!'

        if end_message:
            running = False
            show_message(screen, font, end_message)

        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
