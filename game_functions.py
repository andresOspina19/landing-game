import pygame
import random

class GameState:
    def __init__(self, width=600, height=800, enemies=4):
        self.WIDTH = width
        self.HEIGHT = height
        self.ENEMIES = enemies
        
        # Colores
        self.WHITE = (255, 255, 255)
        self.RED = (200, 0, 0)
        
        # Constantes del juego
        self.GRAVITY = 0.3
        self.THRUST_POWER = -6
        self.LEFT_RIGHT_SPEED = 5

        # Se cargan las imagenes
        self.background_img = pygame.image.load("assets/background.png")
        self.background_img = pygame.transform.scale(self.background_img, (self.WIDTH, self.HEIGHT))

        self.rocket_img = pygame.image.load("assets/rocket.png")
        self.rocket_img = pygame.transform.scale(self.rocket_img, (40, 60))

        self.ufo_img = pygame.image.load("assets/ufo.png")
        self.ufo_img = pygame.transform.scale(self.ufo_img, (60, 30))
        
        # Se inicializa el estado del juego
        self.reset_game()
        
        # Se inicializa la plataforma
        self.platform = pygame.Rect(self.WIDTH // 2 - 50, self.HEIGHT - 40, 100, 10)
        
        # Se inicializan los tipos de letra
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 22)
        
        # Se inicializan los botones del menu
        self.button_play = pygame.Rect(self.WIDTH // 2 - 150, 300, 300, 50)
        self.button_instructions = pygame.Rect(self.WIDTH // 2 - 150, 370, 300, 50)
        self.button_exit = pygame.Rect(self.WIDTH // 2 - 150, 440, 300, 50)

    def set_background_image(self, screen, image):
        screen.blit(image, (0, 0))

    def reset_game(self):
        self.rocket_x = self.WIDTH // 2
        self.rocket_y = 100
        self.rocket_speed_y = 0
        self.fuel = 100
        self.game_over = False
        self.landed = False
        self.enemies = []
        
        for _ in range(self.ENEMIES):
            x = random.randint(0, self.WIDTH - 60)
            y = random.randint(200, 600)
            speed = random.choice([2, 3, 4])
            self.enemies.append({
                "rect": pygame.Rect(x, y, self.ufo_img.get_width(), self.ufo_img.get_height()),
                "speed": speed
            })

    def apply_gravity(self):
        self.rocket_speed_y += self.GRAVITY

    def control_rocket(self, keys):
        if keys[pygame.K_SPACE] and self.fuel > 0:
            self.rocket_speed_y = self.THRUST_POWER
            self.fuel -= 1
        if keys[pygame.K_LEFT]:
            self.rocket_x -= self.LEFT_RIGHT_SPEED
        if keys[pygame.K_RIGHT]:
            self.rocket_x += self.LEFT_RIGHT_SPEED

    def check_landing(self):
        rocket_rect = pygame.Rect(
            self.rocket_x,
            self.rocket_y,
            self.rocket_img.get_width(),
            self.rocket_img.get_height()
        )
        if rocket_rect.colliderect(self.platform):
            rocket_center_x = self.rocket_x + 20
            # Si el cohete esta entre los bordes de la plataforma, se considera que se aterrizo
            if self.platform.left + 10 < rocket_center_x < self.platform.right - 10:
                
                # Si la velocidad absoluta de la velocidad vertical es menor a 9, se considera que se aterrizo
                return abs(self.rocket_speed_y) < 9
        return False

    def draw_button(self, screen, rect, text):
        pygame.draw.rect(screen, self.WHITE, rect, border_radius=8)
        label = self.font.render(text, True, (0, 0, 0))
        screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

    def draw_main_menu(self, screen):
        self.set_background_image(screen, self.background_img)
        self.draw_button(screen, self.button_play, "JUGAR")
        self.draw_button(screen, self.button_instructions, "INSTRUCCIONES")
        self.draw_button(screen, self.button_exit, "SALIR")
        pygame.display.update()

    def draw_instructions(self, screen):
        self.set_background_image(screen, self.background_img)
        lines = [
            "Instrucciones:",
            "- Usa la flecha izquierda/derecha para mover el cohete",
            "- Mantén ESPACIO para usar el propulsor (consume combustible)",
            "- Evita los enemigos y aterriza suavemente sobre la plataforma",
            "",
            "Presiona ESC para volver al menú"
        ]
        for i, line in enumerate(lines):
            label = self.small_font.render(line, True, self.WHITE)
            screen.blit(label, (50, 150 + i * 40))
        pygame.display.update()

    def show_message(self, screen, text):
        screen.fill((0, 0, 0))
        label = self.font.render(text, True, self.WHITE)
        screen.blit(label, (self.WIDTH // 2 - label.get_width() // 2, self.HEIGHT // 2))
        pygame.display.update()
        pygame.time.wait(2000)

    def update_game_state(self, keys):
        self.control_rocket(keys)
        self.apply_gravity()
        self.rocket_y += self.rocket_speed_y

    def check_collisions(self):
        rocket_rect = pygame.Rect(
            self.rocket_x + 16,
            self.rocket_y + 20,
            self.rocket_img.get_width() - 30,
            self.rocket_img.get_height() - 35
        )
        
        # Se verifica si el cohete colisiona con los enemigos
        for enemy_data in self.enemies:
            enemy = enemy_data["rect"]
            speed = enemy_data["speed"]
            enemy.x += speed
            if enemy.x > self.WIDTH:
                enemy.x = -self.ufo_img.get_width()
            if enemy.colliderect(rocket_rect):
                self.game_over = True
                return True

        # Se verifica si el cohete colisiona con el suelo o la plataforma
        if self.rocket_y + self.rocket_img.get_height() >= self.HEIGHT or rocket_rect.colliderect(self.platform):
            if self.check_landing():
                self.landed = True
            self.game_over = True
            return True
            
        return False

    def draw_game(self, screen):
        self.set_background_image(screen, self.background_img)
        
        # Se dibuja el cohete
        screen.blit(self.rocket_img, (self.rocket_x, self.rocket_y))
        
        # Se dibuja la plataforma
        pygame.draw.rect(screen, self.WHITE, self.platform)
        
        # Se dibuja los enemigos usando la imagen de la UFO
        for enemy_data in self.enemies:
            screen.blit(self.ufo_img, enemy_data["rect"])
        
        # Se dibuja la barrita de combustible con el porcentaje de combustible que tiene el cohete
        pygame.draw.rect(screen, self.WHITE, (10, 10, 100, 10), 2)
        pygame.draw.rect(screen, self.WHITE, (10, 10, self.fuel, 10))

        # Se dibuja el texto del porcentaje de combustible que tiene el cohete
        fuel_text = self.small_font.render(f"{int(self.fuel)}%", True, self.WHITE)
        screen.blit(fuel_text, (120, 10))
        
        pygame.display.update()
