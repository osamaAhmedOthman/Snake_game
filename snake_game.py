import pygame
import random
from collections import deque


pygame.init()


WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS


WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
DARKER_GREEN = (0, 100, 0)
RED = (200, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Snake Game")
clock = pygame.time.Clock()


font = pygame.font.SysFont("arial", 24)


background_image = pygame.image.load("resources/background.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

food_img = pygame.image.load("resources/apple.jpg").convert_alpha()  
food_img = pygame.transform.scale(food_img, (CELL_SIZE, CELL_SIZE))

obstacle_img = pygame.image.load("resources/Untitled.jpg").convert_alpha()  
obstacle_img = pygame.transform.scale(obstacle_img, (CELL_SIZE, CELL_SIZE))

snake = [(COLS // 1.75, ROWS // 2)]
score = 0
high_score = 0
game_started = False
obstacles = [(5, 5), (6, 5), (7, 5), (10, 10), (10, 11), (10, 12)]

def reset_game():
    global snake, score, food, game_started
    snake = [(COLS // 1.5, ROWS // 2)]
    score = 0
    food = spawn_food()
    game_started = False

def spawn_food():
    while True:
        f = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if f not in snake and f not in obstacles:
            return f

food = spawn_food()

def bfs(start, goal, snake_body):
    queue = deque()
    queue.append((start, []))
    visited = set()
    visited.add(start)

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in visited and (nx, ny) not in snake_body and (nx, ny) not in obstacles:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
    return []

def move_snake():
    global snake, food, score, high_score, game_started
    path = bfs(snake[0], food, snake)
    if path:
        next_cell = path[0]
        if next_cell in obstacles:
            game_started = False
            high_score = max(high_score, score)
            return
        snake.insert(0, next_cell)
        if next_cell == food:
            score += 1
            food = spawn_food()
        else:
            snake.pop()
    else:
        game_started = False
        high_score = max(high_score, score)

def draw():
    screen.blit(background_image, (0, 0))

    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    for ox, oy in obstacles:
        screen.blit(obstacle_img, (ox * CELL_SIZE, oy * CELL_SIZE))

    if len(snake) > 1:
        pygame.draw.lines(screen, GREEN, False, [(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2) for x, y in snake], CELL_SIZE)

        head_x, head_y = snake[0]
        head_pos = (head_x * CELL_SIZE + CELL_SIZE // 2, head_y * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(screen, DARK_GREEN, head_pos, CELL_SIZE // 2)

        dx = snake[0][0] - snake[1][0]
        dy = snake[0][1] - snake[1][1]

        eye_offset = CELL_SIZE // 5
        if dx == 1:
            eye1 = (head_pos[0] + eye_offset, head_pos[1] - eye_offset)
            eye2 = (head_pos[0] + eye_offset, head_pos[1] + eye_offset)
        elif dx == -1:
            eye1 = (head_pos[0] - eye_offset, head_pos[1] - eye_offset)
            eye2 = (head_pos[0] - eye_offset, head_pos[1] + eye_offset)
        elif dy == 1:
            eye1 = (head_pos[0] - eye_offset, head_pos[1] + eye_offset)
            eye2 = (head_pos[0] + eye_offset, head_pos[1] + eye_offset)
        else:
            eye1 = (head_pos[0] - eye_offset, head_pos[1] - eye_offset)
            eye2 = (head_pos[0] + eye_offset, head_pos[1] - eye_offset)

        pygame.draw.circle(screen, WHITE, eye1, CELL_SIZE // 10)
        pygame.draw.circle(screen, WHITE, eye2, CELL_SIZE // 10)

        tail_x, tail_y = snake[-1]
        tail_pos = (tail_x * CELL_SIZE + CELL_SIZE // 2, tail_y * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(screen, DARKER_GREEN, tail_pos, CELL_SIZE // 3)
    else:
        x, y = snake[0]
        head_pos = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(screen, GREEN, head_pos, CELL_SIZE // 2)

    fx, fy = food
    screen.blit(food_img, (fx * CELL_SIZE, fy * CELL_SIZE))

    score_text = font.render(f"Score: {score}  High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    start_rect = pygame.Rect(WIDTH - 210, 10, 60, 30)
    stop_rect = pygame.Rect(WIDTH - 140, 10, 60, 30)
    reset_rect = pygame.Rect(WIDTH - 70, 10, 60, 30)

    pygame.draw.rect(screen, (0, 255, 0), start_rect)
    pygame.draw.rect(screen, (255, 0, 0), stop_rect)
    pygame.draw.rect(screen, (0, 0, 255), reset_rect)

    start_text = font.render("Start", True, (0, 0, 0))
    stop_text = font.render("Stop", True, (0, 0, 0))
    reset_text = font.render("Reset", True, (255, 255, 255))

    screen.blit(start_text, (WIDTH - 205, 10))
    screen.blit(stop_text, (WIDTH - 135, 10))
    screen.blit(reset_text, (WIDTH - 65, 10))

    pygame.display.flip()
    return start_rect, stop_rect, reset_rect


running = True
while running:
    clock.tick(10)

    start_rect, stop_rect, reset_rect = draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                game_started = True
            elif stop_rect.collidepoint(event.pos):
                game_started = False
            elif reset_rect.collidepoint(event.pos):
                reset_game()

    if game_started:
        move_snake()

pygame.quit()