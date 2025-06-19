import pygame as pg
from random import randrange

pg.init()

window = 900
tile = 30

Range = (tile//2, window - tile//2, tile)
def get_random_position(): return [randrange(*Range), randrange(*Range)]


snake = pg.rect.Rect([0, 0, tile - 5, tile - 5])
snake.center = get_random_position()

length = 1
segments = [snake.copy()]
snake_dir = (0, 0)

time, time_step = 0, 120

food = snake.copy()
food.center = get_random_position()

screen = pg.display.set_mode([window]*2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

# -- WAITING FOR PLAYER TO START --
waiting = True
font = pg.font.SysFont(None, 72)
text = font.render("Press SPACE to start", True, 'red')
text_rect = text.get_rect(center=(window//2, window//2))

while waiting:
    screen.fill('darkgrey')
    screen.blit(text, text_rect)
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            waiting = False


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and dirs[pg.K_w]:
                snake_dir = (0, -tile)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_s and dirs[pg.K_s]:
                snake_dir = (0, tile)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_a and dirs[pg.K_a]:
                snake_dir = (-tile, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if event.key == pg.K_d and dirs[pg.K_d]:
                snake_dir = (tile, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

    screen.fill('darkblue')

    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1

    if snake.center == food.center:
        food.center = get_random_position()
        length += 1

    if snake.left < 0 or snake.right > window or snake.top < 0 or snake.bottom > window or self_eating:
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]

    pg.draw.rect(screen, 'red', food)

    [pg.draw.rect(screen, 'lightgreen', segment) for segment in segments]

    time_now = pg.time.get_ticks()

    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
    pg.display.flip()
    clock.tick(60)
