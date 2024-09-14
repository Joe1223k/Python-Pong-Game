import pygame, sys, random

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = screen_width/2 - 10
    ball.y = random.randint(10, 100)
    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])

def point_won(winner):
    global cpu_points, player_points
    if winner == "cpu":
        cpu_points += 1
    if winner == "player":
        player_points += 1

    reset_ball()

def check_game_over():
    global game_state
    winning_score = 10
    if cpu_points >= winning_score:
        game_state = GAME_OVER
        return "CPU Wins!"
    elif player_points >= winning_score:
        game_state = GAME_OVER
        return "Player Wins!"
    return None

def reset_game():
    global cpu_points, player_points, game_state
    cpu_points = 0
    player_points = 0
    game_state = TITLE_SCREEN
    reset_ball()

def animate_ball():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    # Get point
    if ball.right >= screen_width:
        point_won("cpu")
    if ball.left <= 0:
        point_won("player")

    if ball.colliderect(player):
        ball.right = player.left - 1
        ball_speed_x *= -1
    if ball.colliderect(cpu):
        ball.left = cpu.right + 1
        ball_speed_x *= -1

    winner = check_game_over()
    return winner

def animate_player():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def animate_cpu():
    global cpu_speed
    cpu.y += cpu_speed
    if ball.centery <= cpu.centery:
        cpu_speed = -3
    if ball.centery >= cpu.centery:
        cpu_speed = 3

    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height

def display_title_screen():
    title_font = pygame.font.Font(None, 70)
    instruction_font = pygame.font.Font(None, 40)

    title_surface = title_font.render("Python Pong", True, "white")
    instruction_surface = instruction_font.render("PRESS ENTER", True, "white")

    title_rect = title_surface.get_rect(center=(screen_width/2, screen_height/3))
    instruction_rect = instruction_surface.get_rect(center=(screen_width/2, screen_height/4 * 3))

    screen.fill("black")
    screen.blit(title_surface, title_rect)
    screen.blit(instruction_surface, instruction_rect)
    pygame.display.update()

def display_game_over(winner_message):
    game_over_font = pygame.font.Font(None, 70)
    instruction_font = pygame.font.Font(None, 40)

    game_over_surface = game_over_font.render("Game Over", True, "white")
    winner_surface = game_over_font.render(winner_message, True, "white")
    instruction_surface = instruction_font.render("PRESS ENTER", True, "white")

    game_over_rect = game_over_surface.get_rect(center=(screen_width/2, screen_height/4))
    winner_rect = winner_surface.get_rect(center=(screen_width/2, screen_height/2))
    instruction_rect = instruction_surface.get_rect(center=(screen_width/2, screen_height/4 * 3))

    screen.fill("black")
    screen.blit(game_over_surface, game_over_rect)
    screen.blit(winner_surface, winner_rect)
    screen.blit(instruction_surface, instruction_rect)
    pygame.display.update()

pygame.init()

# Screen settings
screen_width = 640
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Python Pong")
clock = pygame.time.Clock()

# Game objects
ball = pygame.Rect(0, 0, 15, 15)
ball.center = (screen_width/2, screen_height/2)
cpu = pygame.Rect(0, 0, 10, 50)
cpu.center = (20, screen_height/2)
player = pygame.Rect(0, 0, 10, 50)
player.center = (screen_width-20, screen_height/2)

# Game settings
ball_speed_x = 4
ball_speed_y = 4
player_speed = 0
cpu_speed = 0

# Game state
TITLE_SCREEN = 0
GAME_ACTIVE = 1
GAME_OVER = 2
game_state = TITLE_SCREEN

# Score
cpu_points = 0
player_points = 0
score_font = pygame.font.Font(None, 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Title input
        if game_state == TITLE_SCREEN:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = GAME_ACTIVE
        # Game input
        elif game_state == GAME_ACTIVE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_speed = -3
                if event.key == pygame.K_DOWN:
                    player_speed = 3
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_speed = 0
                if event.key == pygame.K_DOWN:
                    player_speed = 0
        # Game over input
        elif game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()

    #  Draw title screen
    if game_state == TITLE_SCREEN:
        display_title_screen()

    # Draw game objects
    elif game_state == GAME_ACTIVE:
        winner_message = animate_ball()
        animate_player()
        animate_cpu()
    
        screen.fill("black")
        cpu_score_surface = score_font.render(str(cpu_points), True, "white")
        player_score_surface = score_font.render(str(player_points), True, "white")
        screen.blit(cpu_score_surface, (screen_width/4, 10))
        screen.blit(player_score_surface, (screen_width/4 * 3, 10))

        pygame.draw.aaline(screen, "white", (screen_width/2, 0), (screen_width/2, screen_height))
        pygame.draw.ellipse(screen, "white", ball)
        pygame.draw.rect(screen, "red", cpu)
        pygame.draw.rect(screen, "green", player)

        if winner_message:
            game_state = GAME_OVER

    # Draw game over
    elif game_state == GAME_OVER:
        display_game_over(winner_message)

    # Display update (FPS 60)
    pygame.display.update()
    clock.tick(60)