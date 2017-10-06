import pygame, time
from random import randint


def init():
    global balls, clock, display, start_time, rect, running, speed, size, step, width, height, n_balls, move_x, move_y, x, y
    balls = {}
    rect = []
    running = True
    speed = 7
    size = 50
    step = 10
    width = 1025
    height = 770
    n_balls = 6
    move_x = move_y = 0
    x = width / 2
    y = height / 2
    start_time = time.time()
    x = 0
    while x < n_balls:
        x += 1
        balls[x] = round5(randint(1, width - size)), round5(randint(1, height - size)), randint(0, 3)
    pygame.init()
    pygame.display.init()
    pygame.joystick.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode([width, height])
    display.fill((0, 0, 0))
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


def joystick():
    global x, y, move_x, move_y, running
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.joy == 0 and event.axis == 1:
                move_y = int(round(event.value * speed))
            elif event.joy == 0 and event.axis == 0:
                move_x = int(round(event.value * speed))
        elif event.type == pygame.KEYDOWN:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 7:
                running = False
    x += move_x
    y += move_y


def keyboard():
    global x, y, move_x, move_y
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_x -= 7
            elif event.key == pygame.K_d:
                move_x += 7
            elif event.key == pygame.K_w:
                move_y -= 7
            elif event.key == pygame.K_s:
                move_y += 7
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                move_x = 0
            elif event.key == pygame.K_w or event.key == pygame.K_a:
                move_y = 0
    x += move_x
    y += move_y


def round5(x, base=5):
    return int(base * round(float(x/base)))


def move():
    global balls, rect
    display.fill((0, 0, 0))
    for x in balls:
        if balls[x][2] == 0:
            balls[x] = balls[x][0] + step, balls[x][1], balls[x][2]
            item = pygame.draw.rect(display, (255, 0, 255), (balls[x][0], balls[x][1], size, size))
            rect.append(item)
        elif balls[x][2] == 1:
            balls[x] = balls[x][0] - step, balls[x][1], balls[x][2]
            item = pygame.draw.rect(display, (255, 0, 255), (balls[x][0], balls[x][1], size, size))
            rect.append(item)
        elif balls[x][2] == 2:
            balls[x] = balls[x][0], balls[x][1] + step, balls[x][2]
            item = pygame.draw.rect(display, (255, 0, 255), (balls[x][0], balls[x][1], size, size))
            rect.append(item)
        else:
            balls[x] = balls[x][0], balls[x][1] - step, balls[x][2]
            item = pygame.draw.rect(display, (255, 0, 255), (balls[x][0], balls[x][1], size, size))
            rect.append(item)


def bounce():
    global x, y, balls, player
    for item in balls:
        if balls[item][0] >= width - size:
            balls[item] = balls[item][0], balls[item][1] + step, 1
        elif balls[item][1] >= height - size:
            balls[item] = balls[item][0], balls[item][1] - step, 3
        elif balls[item][0] <= 0:
            balls[item] = balls[item][0] + step, balls[item][1], 0
        elif balls[item][1] <= 0:
            balls[item] = balls[item][0] - step, balls[item][1], 2
    if x >= width - size or x<=0 and y >= height - size or y <= 0:
        x = y = 0
    elif x >= width - size:
        x = width - size
    elif x <= 0:
        x = 0
    elif y >= height - size:
        y = height - size
    elif y <= 0:
        y = 0
    player = pygame.draw.rect(display, (255, 0, 0), (x, y, size, size))


def show_time():
    global time
    basicfont = pygame.font.SysFont(None, 72)
    text = basicfont.render(str(round(game_time)), True, (255, 0, 0), (0, 0, 0))
    textrect = text.get_rect()
    textrect.centerx = display.get_rect().centerx
    display.blit(text, textrect)


def get_time():
    global game_time, start_time
    game_time = time.time() - start_time


def smash():
    global balls, rect, running
    for item in rect:
        if player.colliderect(item):
            running = False
    rect = []


def main():
    init()
    while running:
        move()
        bounce()
        keyboard()
        get_time()
        show_time()
        smash()
        pygame.display.update()
        clock.tick(60)
    print("Score:", game_time)
    pygame.quit()


def computer():
    global x, y
    decision = randint(0, 3)
    if decision == 0:
        y += 5
    elif decision == 1:
        y -= 5
    elif decision == 2:
        x += 5
    else:
        x -= 5


if __name__ == "__main__":
    main()
