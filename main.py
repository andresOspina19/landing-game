import pygame
import sys
from game_functions import GameState

# Se inicializa el juego
pygame.init()
WIDTH, HEIGHT = 600, 800
ENEMIES = 6
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("¡Aterriza el Cohete! - Hecho por Andrés Ospina")
clock = pygame.time.Clock()

# Se inicializa la clase que maneja el estado del juego
game_state = GameState(WIDTH, HEIGHT, ENEMIES)

# Empieza en el menu principal
menu_state = "main"
running = True

def manage_menu(menu_state, game_state, screen):
    if menu_state == "main":
        game_state.draw_main_menu(screen)
    elif menu_state == "instrucciones":
        game_state.draw_instructions(screen)
    elif menu_state == "jugar":
        # Actualiza el estado del juego
        keys = pygame.key.get_pressed()
        game_state.update_game_state(keys)
        
        # Verifica si hay colisiones
        if game_state.check_collisions():
            pygame.time.wait(500)
            if game_state.landed:
                msg = "¡Aterrizaste!"
                game_state.show_message(screen, msg)
                pygame.time.delay(1000)
                menu_state = "main"
            else:
                msg = "¡Te estrellaste!"
                game_state.show_message(screen, msg)
                game_state.reset_game()
        else:
            game_state.draw_game(screen)
        
    return menu_state


def manage_events(menu_state, game_state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, menu_state
        elif event.type == pygame.MOUSEBUTTONDOWN and menu_state == "main":
            if game_state.button_play.collidepoint(event.pos):
                game_state.reset_game()
                menu_state = "jugar"
            elif game_state.button_instructions.collidepoint(event.pos):
                menu_state = "instrucciones"
            elif game_state.button_exit.collidepoint(event.pos):
                return False, menu_state
        elif event.type == pygame.KEYDOWN and menu_state == "instrucciones":
            if event.key == pygame.K_ESCAPE:
                menu_state = "main"
        
    return True, menu_state

# Empieza el bucle principal del juego
while running:
    clock.tick(60)
    menu_state = manage_menu(menu_state, game_state, screen)
    running, menu_state = manage_events(menu_state, game_state)
    

# Se cierra el juego
pygame.quit()
sys.exit()
