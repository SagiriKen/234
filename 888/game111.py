import pygame
import sys
import os
from level_data import obstacles1, obstacles2, obstacles3

pygame.init()
pygame.font.init()

font_name = os.path.join("777", "123.ttf")
font = pygame.font.Font(font_name, 36)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("闖關遊戲")

player_image = pygame.image.load(os.path.join("777", "man.png")).convert()
player_image = pygame.transform.scale(player_image, (50, 50))
background_image = pygame.image.load(os.path.join("777", "background.jpg")).convert()
obstacle_image = pygame.image.load(os.path.join("777", "a.png")).convert()
obstacle_image = pygame.transform.scale(obstacle_image, (100, 50))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
player_size = 50
player_x, player_y = 50, HEIGHT - player_size
player_speed = 5
player_jump = 15
gravity = 1
falling_speed = gravity
is_jumping = False
jump_speed = player_jump
on_ground = False
current_level = 1
game_active = False
obstacles = []
goal = pygame.Rect(WIDTH - 100, 50, 50, 50)


def load_level(level):
    global obstacles
    if level == 1:
        obstacles = obstacles1
    elif level == 2:
        obstacles = obstacles2
    elif level == 3:
        obstacles = obstacles3

def start_screen():
    screen.fill(WHITE)
    text = font.render("請選擇關卡1~3", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

def game_screen():
    screen.blit(background_image, (0, 0))
    
    screen.blit(player_image, (player_x, player_y))
    
    pygame.draw.rect(screen, RED, goal)
    
    for obs in obstacles:
        screen.blit(obstacle_image, obs.topleft)

    level_text = font.render(f"Level: {current_level}", True, BLACK)
    screen.blit(level_text, (10, 10))

def check_collisions(player_rect):
    global player_y, on_ground, is_jumping, falling_speed
    on_ground = False

    for obs in obstacles:
        if player_rect.colliderect(obs):
            if player_rect.bottom <= obs.top + 10 and player_y < obs.top:
                player_y = obs.top - player_size
                on_ground = True
                is_jumping = False
                falling_speed = gravity
                break

    if player_y + player_size >= HEIGHT:
        player_y = HEIGHT - player_size
        on_ground = True
        is_jumping = False
        falling_speed = gravity

def main():
    global player_x, player_y, is_jumping, jump_speed, on_ground, current_level, game_active, falling_speed
    clock = pygame.time.Clock()
    input_text = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if input_text.isdigit():
                            current_level = int(input_text)
                            load_level(current_level)
                            player_x, player_y = 50, HEIGHT - player_size
                            game_active = True
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and on_ground:
                        is_jumping = True
                        jump_speed = player_jump
                        on_ground = False

        keys = pygame.key.get_pressed()
        if game_active:
            if keys[pygame.K_a]:
                player_x -= player_speed
            if keys[pygame.K_d]:
                player_x += player_speed

            if is_jumping:
                player_y -= jump_speed
                jump_speed -= gravity
                if jump_speed < -player_jump:
                    is_jumping = False
                    jump_speed = player_jump

            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            check_collisions(player_rect)

            if not on_ground and not is_jumping:
                player_y += falling_speed
                falling_speed += gravity

            player_x = max(0, min(WIDTH - player_size, player_x))
            player_y = min(HEIGHT - player_size, player_y)

            if player_rect.colliderect(goal):
                print(f"Level {current_level} completed!")
                game_active = False

        if game_active:
            game_screen()
        else:
            start_screen()
            input_display = font.render(input_text, True, BLACK)
            screen.blit(input_display, (WIDTH // 2 - input_display.get_width() // 2, HEIGHT // 2 + 40))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
