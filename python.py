import pygame
import random
import sqlite3


pygame.init()
def res_from_bd():
    connect = sqlite3.connect("/Users/clix7631/PycharmProjects/testAPI/my_test.db")
    cur = connect.cursor()
    result = cur.execute("""SELECT pivo_score FROM game_now""").fetchall()
    return result[0][0]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
done = False
game_mode = False
cols = 10
rows = 10
a = 0
width = 600
height = 600
wr = width / cols
hr = height / rows
screen = pygame.display.set_mode([width, height])
screen_rect = screen.get_rect()
pygame.display.set_caption("Dimasik pivasik")
clock = pygame.time.Clock()
width2 = 50
height2 = 100
active_color = (13, 122, 58)
inactive_color = (13, 122, 58)
font = pygame.font.Font(None, 50)

img = pygame.image.load('/Users/clix7631/PycharmProjects/testAPI/photo_2024-02-25_21-39-47.jpg')
img2 = pygame.image.load('/Users/clix7631/PycharmProjects/testAPI/photo_2024-01-29_20-28-29.jpg')
img3 = pygame.image.load('/Users/clix7631/PycharmProjects/testAPI/photo_2024-01-02_16-47-27.jpg')
img = pygame.transform.scale(img, (55, 55))
img2 = pygame.transform.scale(img2, (600, 600))
img3 = pygame.transform.scale(img3, (60, 60))
my_font = pygame.font.SysFont('Comic Sans MS', 30)
my_font2 = pygame.font.SysFont('Comic Sans MS', 20)
my_font3 = pygame.font.SysFont('Comic Sans MS', 25)
follow = my_font.render("Лучшая игра на свете!", 1, (255, 0, 0), (0, 0, 0))
follow2 = my_font2.render("Продолжить игру", 1, (255, 0, 0))
follow3 = my_font2.render("Начать заново", 1, (255, 0, 0))
follow4 = my_font.render("Авторы: Лера и Федя", 1, (255, 0, 0), (0, 0, 0))
follow6 = my_font.render("Лабиринт димасика - пивасика", 1, (255, 0, 0), (0, 0, 0))

def added_to_bd():
    connect = sqlite3.connect("/Users/clix7631/PycharmProjects/testAPI/my_test.db")
    cur = connect.cursor()
    cur.execute("""UPDATE game_now SET pivo_score = pivo_score + 1""").fetchall()
    connect.commit()

def delet_result():
    connect = sqlite3.connect("/Users/clix7631/PycharmProjects/testAPI/my_test.db")
    cur = connect.cursor()
    cur.execute("""UPDATE game_now SET pivo_score = 0""").fetchall()
    connect.commit()

def start_ok():
    pep = res_from_bd()
    follow5 = my_font3.render(f"Димася уже выпил: {pep} пива", 1, (255, 0, 0), (0, 0, 0))
    screen.blit(follow, (100, 150))
    pygame.draw.rect(screen, (0, 255, 0), (300, 200, 200, 50), 500)
    screen.blit(follow2, (315, 205))
    pygame.draw.rect(screen, (0, 255, 0), (300, 270, 200, 50), 500)
    screen.blit(follow3, (330, 275))
    screen.blit(follow4, (250, 525))
    screen.blit(follow5, (200, 475))
    screen.blit(follow6, (100, 100))
class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.visited = False
        self.walls = [True, True, True, True]

    def show(self, color=BLACK):
        if self.walls[0]:
            pygame.draw.line(screen, color, [self.x * hr, self.y * wr], [self.x * hr + hr, self.y * wr], 2)
        if self.walls[1]:
            pygame.draw.line(screen, color, [self.x * hr + hr, self.y * wr], [self.x * hr + hr, self.y * wr + wr], 2)
        if self.walls[2]:
            pygame.draw.line(screen, color, [self.x * hr + hr, self.y * wr + wr], [self.x * hr, self.y * wr + wr], 2)
        if self.walls[3]:
            pygame.draw.line(screen, color, [self.x * hr, self.y * wr + wr], [self.x * hr, self.y * wr], 2)

    def show_block(self, color):
        if self.visited:
            pygame.draw.rect(screen, color, [self.x * hr + 2, self.y * wr + 2, hr - 2, wr - 2])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])


def breakwalls(a, b):
    if a.y == b.y and a.x > b.x:
        grid[b.x][b.y].walls[1] = False
        grid[a.x][a.y].walls[3] = False
    if a.y == b.y and a.x < b.x:
        grid[a.x][a.y].walls[1] = False
        grid[b.x][b.y].walls[3] = False
    if a.x == b.x and a.y < b.y:
        grid[b.x][b.y].walls[0] = False
        grid[a.x][a.y].walls[2] = False
    if a.x == b.x and a.y > b.y:
        grid[a.x][a.y].walls[0] = False
        grid[b.x][b.y].walls[2] = False


class Player:
    def __init__(self, x, y):
        self.rect = screen.blit(img, (x, y))
        self.x = int(x)
        self.y = int(y)
        self.colour = (255, 0, 0)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 5

    def draw(self, win):
        screen.blit(img, (self.rect))

    def update(self):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed

        self.x += self.velX
        self.y += self.velY

        self.rect = pygame.Rect(self.x, self.y, hr - 2, wr - 2)


if not game_mode:
    start_ok()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 500 > event.pos[0] > 300 and 250 > event.pos[1] > 200:
                    print(event.pos)
                    print("eeeeeeeee")
                    grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]
                    for i in range(rows):
                        for j in range(cols):
                            grid[i][j].add_neighbors()

                    current = grid[0][0]
                    visited = [current]
                    completed = False

                    player = Player(2, 2)
                    while not done:
                        clock.tick(60)
                        screen.fill(BLACK)
                        if not completed:
                            grid[current.x][current.y].visited = True
                            got_new = False
                            temp = 10

                            while not got_new and not completed:
                                r = random.randint(0, len(current.neighbors) - 1)
                                Tempcurrent = current.neighbors[r]
                                if not Tempcurrent.visited:
                                    visited.append(current)
                                    current = Tempcurrent
                                    got_new = True
                                if temp == 0:
                                    temp = 10
                                    if len(visited) == 0:
                                        completed = True
                                        break
                                    else:
                                        current = visited.pop()
                                temp = temp - 1

                            if not completed:
                                breakwalls(current, visited[len(visited) - 1])

                            current.visited = True
                            current.show_block(WHITE)

                        for i in range(rows):
                            for j in range(cols):
                                grid[i][j].show(WHITE)

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.KEYDOWN and completed:
                                if event.key == pygame.K_LEFT:
                                    player.left_pressed = True
                                if event.key == pygame.K_RIGHT:
                                    player.right_pressed = True
                                if event.key == pygame.K_UP:
                                    player.up_pressed = True
                                if event.key == pygame.K_DOWN:
                                    player.down_pressed = True
                            if event.type == pygame.KEYUP:
                                if event.key == pygame.K_LEFT:
                                    player.left_pressed = False
                                if event.key == pygame.K_RIGHT:
                                    player.right_pressed = False
                                if event.key == pygame.K_UP:
                                    player.up_pressed = False
                                if event.key == pygame.K_DOWN:
                                    player.down_pressed = False
                        player.rect.clamp_ip(screen_rect)

                        if player.x <= 2:
                            player.left_pressed = False
                            player.x = 2
                        if player.y <= 2:
                            player.up_pressed = False
                            player.y = 2
                        if player.x >= width - (wr - 2):
                            player.right_pressed = False
                            player.x = width - (wr - 2)
                        if player.y >= height - (wr - 2):
                            player.down_pressed = False
                            player.y = height - (wr - 2)
                        player_rect = screen.blit(img, (player.x, player.y, wr - 3, hr - 3))
                        xC, yC = int(player_rect.centerx / wr), int(player_rect.centery / hr)
                        x0, y0 = int(player_rect.left / wr), int(player_rect.top / hr)
                        x1, y1 = int(player_rect.right / wr), int(player_rect.bottom / hr)

                        if player.left_pressed and player_rect.x < xC * wr + 2:
                            if grid[xC][y0].walls[3] or grid[xC][y1].walls[3]:
                                player.x = xC * wr + 2
                                player.left_pressed = False
                            if player.y != yC * hr + 2 and grid[x0][y0].walls[2]:
                                player.x = xC * wr + 2
                                player.left_pressed = False

                        if player.right_pressed and player_rect.x > xC * wr + 2:
                            if grid[xC][y0].walls[1] or grid[xC][y1].walls[1]:
                                player.x = xC * wr + 2
                                player.right_pressed = False
                            if player.y != yC * hr + 2 and grid[x0 + 1][y0].walls[2]:
                                player.x = xC * wr + 2
                                player.right_pressed = False

                        if player.up_pressed and player_rect.y < yC * hr + 2:
                            if grid[x0][yC].walls[0] or grid[x1][yC].walls[0]:
                                player.y = yC * hr + 2
                                player.up_pressed = False
                            if player.x != xC * wr + 2 and grid[x0][y0].walls[3]:
                                player.y = yC * hr + 2
                                player.up_pressed = False

                        if player.down_pressed and player_rect.y > yC * hr + 2:
                            if grid[x0][yC].walls[2] or grid[x1][yC].walls[2]:
                                player.y = yC * hr + 2
                                player.down_pressed = False
                            if player.x != xC * wr + 2 and grid[x0][y0 + 1].walls[3]:
                                player.y = yC * hr + 2
                                player.down_pressed = False
                        screen.blit(img3, (540, 540))
                        if (player_rect.y <= 542 and player_rect.x <= 542) and \
                                (player_rect.y >= 482 and player_rect.x >= 482):
                            player.up_pressed = False
                            player.left_pressed = False
                            player.right_pressed = False
                            player.down_pressed = False
                            temp = 0
                            xC, yC = None, None
                            x0, y0 = None, None
                            x1, y1 = None, None
                            current = None
                            visited = None
                            added_to_bd()
                            player_rect = None
                            completed = False
                            got_new = False
                            done = False
                            Tempcurrent = None
                            r = None
                            game_mode = True
                            player.colour = (0, 0, 0)
                            screen.fill((0, 0, 0))
                            while a != 6:
                                start_ok()
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        if 500 > event.pos[0] > 300 and 250 > event.pos[1] > 200:
                                            print(event.pos)
                                            print("eeeeeeeee")
                                            grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]
                                            for i in range(rows):
                                                for j in range(cols):
                                                    grid[i][j].add_neighbors()

                                            current = grid[0][0]
                                            visited = [current]
                                            completed = False

                                            player = Player(2, 2)
                                            while not done:
                                                clock.tick(60)
                                                screen.fill(BLACK)
                                                if not completed:
                                                    grid[current.x][current.y].visited = True
                                                    got_new = False
                                                    temp = 10

                                                    while not got_new and not completed:
                                                        r = random.randint(0, len(current.neighbors) - 1)
                                                        Tempcurrent = current.neighbors[r]
                                                        if not Tempcurrent.visited:
                                                            visited.append(current)
                                                            current = Tempcurrent
                                                            got_new = True
                                                        if temp == 0:
                                                            temp = 10
                                                            if len(visited) == 0:
                                                                completed = True
                                                                break
                                                            else:
                                                                current = visited.pop()
                                                        temp = temp - 1

                                                    if not completed:
                                                        breakwalls(current, visited[len(visited) - 1])

                                                    current.visited = True
                                                    current.show_block(WHITE)

                                                for i in range(rows):
                                                    for j in range(cols):
                                                        grid[i][j].show(WHITE)

                                                for event in pygame.event.get():
                                                    if event.type == pygame.QUIT:
                                                        pygame.quit()
                                                    if event.type == pygame.KEYDOWN and completed:
                                                        if event.key == pygame.K_LEFT:
                                                            player.left_pressed = True
                                                        if event.key == pygame.K_RIGHT:
                                                            player.right_pressed = True
                                                        if event.key == pygame.K_UP:
                                                            player.up_pressed = True
                                                        if event.key == pygame.K_DOWN:
                                                            player.down_pressed = True
                                                    if event.type == pygame.KEYUP:
                                                        if event.key == pygame.K_LEFT:
                                                            player.left_pressed = False
                                                        if event.key == pygame.K_RIGHT:
                                                            player.right_pressed = False
                                                        if event.key == pygame.K_UP:
                                                            player.up_pressed = False
                                                        if event.key == pygame.K_DOWN:
                                                            player.down_pressed = False
                                                player.rect.clamp_ip(screen_rect)

                                                if player.x <= 2:
                                                    player.left_pressed = False
                                                    player.x = 2
                                                if player.y <= 2:
                                                    player.up_pressed = False
                                                    player.y = 2
                                                if player.x >= width - (wr - 2):
                                                    player.right_pressed = False
                                                    player.x = width - (wr - 2)
                                                if player.y >= height - (wr - 2):
                                                    player.down_pressed = False
                                                    player.y = height - (wr - 2)
                                                player_rect = pygame.Rect(player.x, player.y, wr - 3, hr - 3)
                                                xC, yC = int(player_rect.centerx / wr), int(player_rect.centery / hr)
                                                x0, y0 = int(player_rect.left / wr), int(player_rect.top / hr)
                                                x1, y1 = int(player_rect.right / wr), int(player_rect.bottom / hr)

                                                if player.left_pressed and player_rect.x < xC * wr + 2:
                                                    if grid[xC][y0].walls[3] or grid[xC][y1].walls[3]:
                                                        player.x = xC * wr + 2
                                                        player.left_pressed = False
                                                    if player.y != yC * hr + 2 and grid[x0][y0].walls[2]:
                                                        player.x = xC * wr + 2
                                                        player.left_pressed = False

                                                if player.right_pressed and player_rect.x > xC * wr + 2:
                                                    if grid[xC][y0].walls[1] or grid[xC][y1].walls[1]:
                                                        player.x = xC * wr + 2
                                                        player.right_pressed = False
                                                    if player.y != yC * hr + 2 and grid[x0 + 1][y0].walls[2]:
                                                        player.x = xC * wr + 2
                                                        player.right_pressed = False

                                                if player.up_pressed and player_rect.y < yC * hr + 2:
                                                    if grid[x0][yC].walls[0] or grid[x1][yC].walls[0]:
                                                        player.y = yC * hr + 2
                                                        player.up_pressed = False
                                                    if player.x != xC * wr + 2 and grid[x0][y0].walls[3]:
                                                        player.y = yC * hr + 2
                                                        player.up_pressed = False

                                                if player.down_pressed and player_rect.y > yC * hr + 2:
                                                    if grid[x0][yC].walls[2] or grid[x1][yC].walls[2]:
                                                        player.y = yC * hr + 2
                                                        player.down_pressed = False
                                                    if player.x != xC * wr + 2 and grid[x0][y0 + 1].walls[3]:
                                                        player.y = yC * hr + 2
                                                        player.down_pressed = False
                                                screen.blit(img3, (540, 540))
                                                if (player_rect.y <= 542 and player_rect.x <= 542) and \
                                                        (player_rect.y >= 482 and player_rect.x >= 482):
                                                    player.up_pressed = False
                                                    player.left_pressed = False
                                                    player.right_pressed = False
                                                    player.down_pressed = False
                                                    added_to_bd()
                                                    completed = False
                                                    got_new = False
                                                    game_mode = True
                                                    done = False
                                                    a += 1
                                                    player.colour = (0, 0, 0)
                                                    screen.fill((0, 0, 0))
                                                    start_ok()
                                                    while a != 6:
                                                        start_ok()
                                                        for event in pygame.event.get():
                                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                                if 500 > event.pos[0] > 300 and 250 > event.pos[
                                                                    1] > 200:
                                                                    grid = [[Spot(i, j) for j in range(cols)] for i in
                                                                            range(rows)]
                                                                    print(event.pos)
                                                                    print("eeeeeeeee")
                                                                    for i in range(rows):
                                                                        for j in range(cols):
                                                                            grid[i][j].add_neighbors()

                                                                    current = grid[0][0]
                                                                    visited = [current]
                                                                    completed = False

                                                                    player = Player(2, 2)
                                                                    while not done:
                                                                        clock.tick(60)
                                                                        screen.fill(BLACK)
                                                                        if not completed:
                                                                            grid[current.x][current.y].visited = True
                                                                            got_new = False
                                                                            temp = 10

                                                                            while not got_new and not completed:
                                                                                r = random.randint(0,
                                                                                                   len(current.neighbors) - 1)
                                                                                Tempcurrent = current.neighbors[r]
                                                                                if not Tempcurrent.visited:
                                                                                    visited.append(current)
                                                                                    current = Tempcurrent
                                                                                    got_new = True
                                                                                if temp == 0:
                                                                                    temp = 10
                                                                                    if len(visited) == 0:
                                                                                        completed = True
                                                                                        break
                                                                                    else:
                                                                                        current = visited.pop()
                                                                                temp = temp - 1

                                                                            if not completed:
                                                                                breakwalls(current,
                                                                                           visited[len(visited) - 1])

                                                                            current.visited = True
                                                                            current.show_block(WHITE)

                                                                        for i in range(rows):
                                                                            for j in range(cols):
                                                                                grid[i][j].show(WHITE)

                                                                        for event in pygame.event.get():
                                                                            if event.type == pygame.QUIT:
                                                                                pygame.quit()
                                                                            if event.type == pygame.KEYDOWN and completed:
                                                                                if event.key == pygame.K_LEFT:
                                                                                    player.left_pressed = True
                                                                                if event.key == pygame.K_RIGHT:
                                                                                    player.right_pressed = True
                                                                                if event.key == pygame.K_UP:
                                                                                    player.up_pressed = True
                                                                                if event.key == pygame.K_DOWN:
                                                                                    player.down_pressed = True
                                                                            if event.type == pygame.KEYUP:
                                                                                if event.key == pygame.K_LEFT:
                                                                                    player.left_pressed = False
                                                                                if event.key == pygame.K_RIGHT:
                                                                                    player.right_pressed = False
                                                                                if event.key == pygame.K_UP:
                                                                                    player.up_pressed = False
                                                                                if event.key == pygame.K_DOWN:
                                                                                    player.down_pressed = False
                                                                        player.rect.clamp_ip(screen_rect)

                                                                        if player.x <= 2:
                                                                            player.left_pressed = False
                                                                            player.x = 2
                                                                        if player.y <= 2:
                                                                            player.up_pressed = False
                                                                            player.y = 2
                                                                        if player.x >= width - (wr - 2):
                                                                            player.right_pressed = False
                                                                            player.x = width - (wr - 2)
                                                                        if player.y >= height - (wr - 2):
                                                                            player.down_pressed = False
                                                                            player.y = height - (wr - 2)
                                                                        player_rect = pygame.Rect(player.x, player.y,
                                                                                                  wr - 3, hr - 3)
                                                                        xC, yC = int(player_rect.centerx / wr), int(
                                                                            player_rect.centery / hr)
                                                                        x0, y0 = int(player_rect.left / wr), int(
                                                                            player_rect.top / hr)
                                                                        x1, y1 = int(player_rect.right / wr), int(
                                                                            player_rect.bottom / hr)

                                                                        if player.left_pressed and player_rect.x < xC * wr + 2:
                                                                            if grid[xC][y0].walls[3] or \
                                                                                    grid[xC][y1].walls[3]:
                                                                                player.x = xC * wr + 2
                                                                                player.left_pressed = False
                                                                            if player.y != yC * hr + 2 and \
                                                                                    grid[x0][y0].walls[2]:
                                                                                player.x = xC * wr + 2
                                                                                player.left_pressed = False

                                                                        if player.right_pressed and player_rect.x > xC * wr + 2:
                                                                            if grid[xC][y0].walls[1] or \
                                                                                    grid[xC][y1].walls[1]:
                                                                                player.x = xC * wr + 2
                                                                                player.right_pressed = False
                                                                            if player.y != yC * hr + 2 and \
                                                                                    grid[x0 + 1][y0].walls[2]:
                                                                                player.x = xC * wr + 2
                                                                                player.right_pressed = False

                                                                        if player.up_pressed and player_rect.y < yC * hr + 2:
                                                                            if grid[x0][yC].walls[0] or \
                                                                                    grid[x1][yC].walls[0]:
                                                                                player.y = yC * hr + 2
                                                                                player.up_pressed = False
                                                                            if player.x != xC * wr + 2 and \
                                                                                    grid[x0][y0].walls[3]:
                                                                                player.y = yC * hr + 2
                                                                                player.up_pressed = False

                                                                        if player.down_pressed and player_rect.y > yC * hr + 2:
                                                                            if grid[x0][yC].walls[2] or \
                                                                                    grid[x1][yC].walls[2]:
                                                                                player.y = yC * hr + 2
                                                                                player.down_pressed = False
                                                                            if player.x != xC * wr + 2 and \
                                                                                    grid[x0][y0 + 1].walls[3]:
                                                                                player.y = yC * hr + 2
                                                                                player.down_pressed = False
                                                                        screen.blit(img3, (540, 540))
                                                                        if (
                                                                                player_rect.y <= 542 and player_rect.x <= 542) and \
                                                                                (
                                                                                        player_rect.y >= 482 and player_rect.x >= 482):
                                                                            player.up_pressed = False
                                                                            player.left_pressed = False
                                                                            player.right_pressed = False
                                                                            player.down_pressed = False
                                                                            added_to_bd()
                                                                            completed = False
                                                                            got_new = False
                                                                            game_mode = True
                                                                            done = False
                                                                            a += 1
                                                                            player.colour = (0, 0, 0)
                                                                            screen.fill((0, 0, 0))
                                                                            start_ok()
                                                                            while a != 6:
                                                                                start_ok()
                                                                                for event in pygame.event.get():
                                                                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                                                                        if 500 > event.pos[
                                                                                            0] > 300 and 250 > \
                                                                                                event.pos[1] > 200:
                                                                                            print(event.pos)
                                                                                            grid = [[Spot(i, j) for j in
                                                                                                     range(cols)] for i
                                                                                                    in range(rows)]
                                                                                            print("eeeeeeeee")
                                                                                            for i in range(rows):
                                                                                                for j in range(cols):
                                                                                                    grid[i][
                                                                                                        j].add_neighbors()

                                                                                            current = grid[0][0]
                                                                                            visited = [current]
                                                                                            completed = False

                                                                                            player = Player(2, 2)
                                                                                            while not done:
                                                                                                clock.tick(60)
                                                                                                screen.fill(BLACK)
                                                                                                if not completed:
                                                                                                    grid[current.x][
                                                                                                        current.y].visited = True
                                                                                                    got_new = False
                                                                                                    temp = 10

                                                                                                    while not got_new and not completed:
                                                                                                        r = random.randint(
                                                                                                            0,
                                                                                                            len(current.neighbors) - 1)
                                                                                                        Tempcurrent = \
                                                                                                        current.neighbors[
                                                                                                            r]
                                                                                                        if not Tempcurrent.visited:
                                                                                                            visited.append(
                                                                                                                current)
                                                                                                            current = Tempcurrent
                                                                                                            got_new = True
                                                                                                        if temp == 0:
                                                                                                            temp = 10
                                                                                                            if len(visited) == 0:
                                                                                                                completed = True
                                                                                                                break
                                                                                                            else:
                                                                                                                current = visited.pop()
                                                                                                        temp = temp - 1

                                                                                                    if not completed:
                                                                                                        breakwalls(
                                                                                                            current,
                                                                                                            visited[
                                                                                                                len(visited) - 1])

                                                                                                    current.visited = True
                                                                                                    current.show_block(
                                                                                                        WHITE)

                                                                                                for i in range(rows):
                                                                                                    for j in range(
                                                                                                            cols):
                                                                                                        grid[i][j].show(
                                                                                                            WHITE)

                                                                                                for event in pygame.event.get():
                                                                                                    if event.type == pygame.QUIT:
                                                                                                        pygame.quit()
                                                                                                    if event.type == pygame.KEYDOWN and completed:
                                                                                                        if event.key == pygame.K_LEFT:
                                                                                                            player.left_pressed = True
                                                                                                        if event.key == pygame.K_RIGHT:
                                                                                                            player.right_pressed = True
                                                                                                        if event.key == pygame.K_UP:
                                                                                                            player.up_pressed = True
                                                                                                        if event.key == pygame.K_DOWN:
                                                                                                            player.down_pressed = True
                                                                                                    if event.type == pygame.KEYUP:
                                                                                                        if event.key == pygame.K_LEFT:
                                                                                                            player.left_pressed = False
                                                                                                        if event.key == pygame.K_RIGHT:
                                                                                                            player.right_pressed = False
                                                                                                        if event.key == pygame.K_UP:
                                                                                                            player.up_pressed = False
                                                                                                        if event.key == pygame.K_DOWN:
                                                                                                            player.down_pressed = False
                                                                                                player.rect.clamp_ip(
                                                                                                    screen_rect)

                                                                                                if player.x <= 2:
                                                                                                    player.left_pressed = False
                                                                                                    player.x = 2
                                                                                                if player.y <= 2:
                                                                                                    player.up_pressed = False
                                                                                                    player.y = 2
                                                                                                if player.x >= width - (
                                                                                                        wr - 2):
                                                                                                    player.right_pressed = False
                                                                                                    player.x = width - (
                                                                                                                wr - 2)
                                                                                                if player.y >= height - (
                                                                                                        wr - 2):
                                                                                                    player.down_pressed = False
                                                                                                    player.y = height - (
                                                                                                                wr - 2)
                                                                                                player_rect = pygame.Rect(
                                                                                                    player.x, player.y,
                                                                                                    wr - 3, hr - 3)
                                                                                                xC, yC = int(
                                                                                                    player_rect.centerx / wr), int(
                                                                                                    player_rect.centery / hr)
                                                                                                x0, y0 = int(
                                                                                                    player_rect.left / wr), int(
                                                                                                    player_rect.top / hr)
                                                                                                x1, y1 = int(
                                                                                                    player_rect.right / wr), int(
                                                                                                    player_rect.bottom / hr)

                                                                                                if player.left_pressed and player_rect.x < xC * wr + 2:
                                                                                                    if \
                                                                                                    grid[xC][y0].walls[
                                                                                                        3] or grid[xC][
                                                                                                        y1].walls[3]:
                                                                                                        player.x = xC * wr + 2
                                                                                                        player.left_pressed = False
                                                                                                    if player.y != yC * hr + 2 and \
                                                                                                            grid[x0][
                                                                                                                y0].walls[
                                                                                                                2]:
                                                                                                        player.x = xC * wr + 2
                                                                                                        player.left_pressed = False

                                                                                                if player.right_pressed and player_rect.x > xC * wr + 2:
                                                                                                    if \
                                                                                                    grid[xC][y0].walls[
                                                                                                        1] or grid[xC][
                                                                                                        y1].walls[1]:
                                                                                                        player.x = xC * wr + 2
                                                                                                        player.right_pressed = False
                                                                                                    if player.y != yC * hr + 2 and \
                                                                                                            grid[
                                                                                                                x0 + 1][
                                                                                                                y0].walls[
                                                                                                                2]:
                                                                                                        player.x = xC * wr + 2
                                                                                                        player.right_pressed = False

                                                                                                if player.up_pressed and player_rect.y < yC * hr + 2:
                                                                                                    if \
                                                                                                    grid[x0][yC].walls[
                                                                                                        0] or grid[x1][
                                                                                                        yC].walls[0]:
                                                                                                        player.y = yC * hr + 2
                                                                                                        player.up_pressed = False
                                                                                                    if player.x != xC * wr + 2 and \
                                                                                                            grid[x0][
                                                                                                                y0].walls[
                                                                                                                3]:
                                                                                                        player.y = yC * hr + 2
                                                                                                        player.up_pressed = False

                                                                                                if player.down_pressed and player_rect.y > yC * hr + 2:
                                                                                                    if \
                                                                                                    grid[x0][yC].walls[
                                                                                                        2] or grid[x1][
                                                                                                        yC].walls[2]:
                                                                                                        player.y = yC * hr + 2
                                                                                                        player.down_pressed = False
                                                                                                    if player.x != xC * wr + 2 and \
                                                                                                            grid[x0][
                                                                                                                y0 + 1].walls[
                                                                                                                3]:
                                                                                                        player.y = yC * hr + 2
                                                                                                        player.down_pressed = False
                                                                                                screen.blit(img3, (540, 540))
                                                                                                if (
                                                                                                        player_rect.y <= 542 and player_rect.x <= 542) and \
                                                                                                        (
                                                                                                                player_rect.y >= 482 and player_rect.x >= 482):
                                                                                                    player.up_pressed = False
                                                                                                    player.left_pressed = False
                                                                                                    player.right_pressed = False
                                                                                                    player.down_pressed = False
                                                                                                    completed = False
                                                                                                    got_new = False
                                                                                                    added_to_bd()
                                                                                                    game_mode = True
                                                                                                    done = False
                                                                                                    a += 1
                                                                                                    player.colour = (
                                                                                                    0, 0, 0)
                                                                                                    screen.fill(
                                                                                                        (0, 0, 0))
                                                                                                    start_ok()
                                                                                                    while a != 6:
                                                                                                        start_ok()
                                                                                                        for event in pygame.event.get():
                                                                                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                                                                                if 500 > \
                                                                                                                        event.pos[
                                                                                                                            0] > 300 and 250 > \
                                                                                                                        event.pos[
                                                                                                                            1] > 200:
                                                                                                                    print(
                                                                                                                        event.pos)
                                                                                                                    grid = [
                                                                                                                        [
                                                                                                                            Spot(
                                                                                                                                i,
                                                                                                                                j)
                                                                                                                            for
                                                                                                                            j
                                                                                                                            in
                                                                                                                            range(
                                                                                                                                cols)]
                                                                                                                        for
                                                                                                                        i
                                                                                                                        in
                                                                                                                        range(
                                                                                                                            rows)]
                                                                                                                    print(
                                                                                                                        "eeeeeeeee")
                                                                                                                    for i in range(
                                                                                                                            rows):
                                                                                                                        for j in range(
                                                                                                                                cols):
                                                                                                                            grid[
                                                                                                                                i][
                                                                                                                                j].add_neighbors()

                                                                                                                    current = \
                                                                                                                    grid[
                                                                                                                        0][
                                                                                                                        0]
                                                                                                                    visited = [
                                                                                                                        current]
                                                                                                                    completed = False

                                                                                                                    player = Player(
                                                                                                                        2,
                                                                                                                        2)
                                                                                                                    while not done:
                                                                                                                        clock.tick(
                                                                                                                            60)
                                                                                                                        screen.fill(
                                                                                                                            BLACK)
                                                                                                                        if not completed:
                                                                                                                            grid[
                                                                                                                                current.x][
                                                                                                                                current.y].visited = True
                                                                                                                            got_new = False
                                                                                                                            temp = 10

                                                                                                                            while not got_new and not completed:
                                                                                                                                r = random.randint(
                                                                                                                                    0,
                                                                                                                                    len(current.neighbors) - 1)
                                                                                                                                Tempcurrent = \
                                                                                                                                    current.neighbors[
                                                                                                                                        r]
                                                                                                                                if not Tempcurrent.visited:
                                                                                                                                    visited.append(
                                                                                                                                        current)
                                                                                                                                    current = Tempcurrent
                                                                                                                                    got_new = True
                                                                                                                                if temp == 0:
                                                                                                                                    temp = 10
                                                                                                                                    if len(visited) == 0:
                                                                                                                                        completed = True
                                                                                                                                        break
                                                                                                                                    else:
                                                                                                                                        current = visited.pop()
                                                                                                                                temp = temp - 1

                                                                                                                            if not completed:
                                                                                                                                breakwalls(
                                                                                                                                    current,
                                                                                                                                    visited[
                                                                                                                                        len(visited) - 1])

                                                                                                                            current.visited = True
                                                                                                                            current.show_block(
                                                                                                                                WHITE)

                                                                                                                        for i in range(
                                                                                                                                rows):
                                                                                                                            for j in range(
                                                                                                                                    cols):
                                                                                                                                grid[
                                                                                                                                    i][
                                                                                                                                    j].show(
                                                                                                                                    WHITE)

                                                                                                                        for event in pygame.event.get():
                                                                                                                            if event.type == pygame.QUIT:
                                                                                                                                pygame.quit()
                                                                                                                            if event.type == pygame.KEYDOWN and completed:
                                                                                                                                if event.key == pygame.K_LEFT:
                                                                                                                                    player.left_pressed = True
                                                                                                                                if event.key == pygame.K_RIGHT:
                                                                                                                                    player.right_pressed = True
                                                                                                                                if event.key == pygame.K_UP:
                                                                                                                                    player.up_pressed = True
                                                                                                                                if event.key == pygame.K_DOWN:
                                                                                                                                    player.down_pressed = True
                                                                                                                            if event.type == pygame.KEYUP:
                                                                                                                                if event.key == pygame.K_LEFT:
                                                                                                                                    player.left_pressed = False
                                                                                                                                if event.key == pygame.K_RIGHT:
                                                                                                                                    player.right_pressed = False
                                                                                                                                if event.key == pygame.K_UP:
                                                                                                                                    player.up_pressed = False
                                                                                                                                if event.key == pygame.K_DOWN:
                                                                                                                                    player.down_pressed = False
                                                                                                                        player.rect.clamp_ip(
                                                                                                                            screen_rect)

                                                                                                                        if player.x <= 2:
                                                                                                                            player.left_pressed = False
                                                                                                                            player.x = 2
                                                                                                                        if player.y <= 2:
                                                                                                                            player.up_pressed = False
                                                                                                                            player.y = 2
                                                                                                                        if player.x >= width - (
                                                                                                                                wr - 2):
                                                                                                                            player.right_pressed = False
                                                                                                                            player.x = width - (
                                                                                                                                    wr - 2)
                                                                                                                        if player.y >= height - (
                                                                                                                                wr - 2):
                                                                                                                            player.down_pressed = False
                                                                                                                            player.y = height - (
                                                                                                                                    wr - 2)
                                                                                                                        player_rect = pygame.Rect(
                                                                                                                            player.x,
                                                                                                                            player.y,
                                                                                                                            wr - 3,
                                                                                                                            hr - 3)
                                                                                                                        xC, yC = int(
                                                                                                                            player_rect.centerx / wr), int(
                                                                                                                            player_rect.centery / hr)
                                                                                                                        x0, y0 = int(
                                                                                                                            player_rect.left / wr), int(
                                                                                                                            player_rect.top / hr)
                                                                                                                        x1, y1 = int(
                                                                                                                            player_rect.right / wr), int(
                                                                                                                            player_rect.bottom / hr)

                                                                                                                        if player.left_pressed and player_rect.x < xC * wr + 2:
                                                                                                                            if \
                                                                                                                                    grid[
                                                                                                                                        xC][
                                                                                                                                        y0].walls[
                                                                                                                                        3] or \
                                                                                                                                            grid[
                                                                                                                                                xC][
                                                                                                                                                y1].walls[
                                                                                                                                                3]:
                                                                                                                                player.x = xC * wr + 2
                                                                                                                                player.left_pressed = False
                                                                                                                            if player.y != yC * hr + 2 and \
                                                                                                                                    grid[
                                                                                                                                        x0][
                                                                                                                                        y0].walls[
                                                                                                                                        2]:
                                                                                                                                player.x = xC * wr + 2
                                                                                                                                player.left_pressed = False

                                                                                                                        if player.right_pressed and player_rect.x > xC * wr + 2:
                                                                                                                            if \
                                                                                                                                    grid[
                                                                                                                                        xC][
                                                                                                                                        y0].walls[
                                                                                                                                        1] or \
                                                                                                                                            grid[
                                                                                                                                                xC][
                                                                                                                                                y1].walls[
                                                                                                                                                1]:
                                                                                                                                player.x = xC * wr + 2
                                                                                                                                player.right_pressed = False
                                                                                                                            if player.y != yC * hr + 2 and \
                                                                                                                                    grid[
                                                                                                                                        x0 + 1][
                                                                                                                                        y0].walls[
                                                                                                                                        2]:
                                                                                                                                player.x = xC * wr + 2
                                                                                                                                player.right_pressed = False

                                                                                                                        if player.up_pressed and player_rect.y < yC * hr + 2:
                                                                                                                            if \
                                                                                                                                    grid[
                                                                                                                                        x0][
                                                                                                                                        yC].walls[
                                                                                                                                        0] or \
                                                                                                                                            grid[
                                                                                                                                                x1][
                                                                                                                                                yC].walls[
                                                                                                                                                0]:
                                                                                                                                player.y = yC * hr + 2
                                                                                                                                player.up_pressed = False
                                                                                                                            if player.x != xC * wr + 2 and \
                                                                                                                                    grid[
                                                                                                                                        x0][
                                                                                                                                        y0].walls[
                                                                                                                                        3]:
                                                                                                                                player.y = yC * hr + 2
                                                                                                                                player.up_pressed = False

                                                                                                                        if player.down_pressed and player_rect.y > yC * hr + 2:
                                                                                                                            if \
                                                                                                                                    grid[
                                                                                                                                        x0][
                                                                                                                                        yC].walls[
                                                                                                                                        2] or \
                                                                                                                                            grid[
                                                                                                                                                x1][
                                                                                                                                                yC].walls[
                                                                                                                                                2]:
                                                                                                                                player.y = yC * hr + 2
                                                                                                                                player.down_pressed = False
                                                                                                                            if player.x != xC * wr + 2 and \
                                                                                                                                    grid[
                                                                                                                                        x0][
                                                                                                                                        y0 + 1].walls[
                                                                                                                                        3]:
                                                                                                                                player.y = yC * hr + 2
                                                                                                                                player.down_pressed = False
                                                                                                                        screen.blit(img3, (540, 540))
                                                                                                                        if (
                                                                                                                                player_rect.y <= 542 and player_rect.x <= 542) and \
                                                                                                                                (
                                                                                                                                        player_rect.y >= 482 and player_rect.x >= 482):
                                                                                                                            player.up_pressed = False
                                                                                                                            player.left_pressed = False
                                                                                                                            player.right_pressed = False
                                                                                                                            player.down_pressed = False
                                                                                                                            added_to_bd()
                                                                                                                            completed = False
                                                                                                                            got_new = False
                                                                                                                            game_mode = True
                                                                                                                            done = False
                                                                                                                            a += 1
                                                                                                                            player.colour = (
                                                                                                                                0,
                                                                                                                                0,
                                                                                                                                0)
                                                                                                                            screen.fill(
                                                                                                                                (
                                                                                                                                0,
                                                                                                                                0,
                                                                                                                                0))
                                                                                                                            screen.blit(img2, (0, 0))
                                                                                                                            s = pygame.mixer.music.load(
                                                                                                                                "zvyk_pip.mp3")
                                                                                                                            pygame.mixer.music.play(
                                                                                                                                -1)


                                                                                                                        player.draw(
                                                                                                                            screen)
                                                                                                                        player.update()
                                                                                                                        pygame.display.flip()
                                                                                                                elif 500 > \
                                                                                                                        event.pos[
                                                                                                                            0] > 300 and 320 > \
                                                                                                                        event.pos[
                                                                                                                            1] > 270:
                                                                                                                    delet_result()
                                                                                                                    start_ok()
                                                                                                            if event.type == pygame.MOUSEMOTION:
                                                                                                                if 500 > \
                                                                                                                        event.pos[
                                                                                                                            0] > 300 and 250 > \
                                                                                                                        event.pos[
                                                                                                                            1] > 200:
                                                                                                                    pygame.draw.rect(
                                                                                                                        screen,
                                                                                                                        (
                                                                                                                            255,
                                                                                                                            255,
                                                                                                                            255),
                                                                                                                        (
                                                                                                                        300,
                                                                                                                        200,
                                                                                                                        200,
                                                                                                                        50),
                                                                                                                        500)
                                                                                                                    screen.blit(
                                                                                                                        follow2,
                                                                                                                        (
                                                                                                                        315,
                                                                                                                        205))
                                                                                                                elif 500 > \
                                                                                                                        event.pos[
                                                                                                                            0] > 300 and 320 > \
                                                                                                                        event.pos[
                                                                                                                            1] > 270:
                                                                                                                    pygame.draw.rect(
                                                                                                                        screen,
                                                                                                                        (
                                                                                                                            255,
                                                                                                                            255,
                                                                                                                            255),
                                                                                                                        (
                                                                                                                        300,
                                                                                                                        270,
                                                                                                                        200,
                                                                                                                        50),
                                                                                                                        500)
                                                                                                                    screen.blit(
                                                                                                                        follow3,
                                                                                                                        (
                                                                                                                        330,
                                                                                                                        275))
                                                                                                                pygame.display.update()

                                                                                                player.draw(screen)
                                                                                                player.update()
                                                                                                pygame.display.flip()

                                                                                        if event.type == pygame.MOUSEMOTION:
                                                                                            if 500 > event.pos[
                                                                                                0] > 300 and 250 > \
                                                                                                    event.pos[
                                                                                                        1] > 200:
                                                                                                pygame.draw.rect(screen,
                                                                                                                 (255,
                                                                                                                  255,
                                                                                                                  255),
                                                                                                                 (300,
                                                                                                                  200,
                                                                                                                  200,
                                                                                                                  50),
                                                                                                                 500)
                                                                                                screen.blit(follow2,
                                                                                                            (315, 205))
                                                                                            elif 500 > event.pos[
                                                                                                0] > 300 and 320 > \
                                                                                                    event.pos[
                                                                                                        1] > 270:
                                                                                                pygame.draw.rect(screen,
                                                                                                                 (255,
                                                                                                                  255,
                                                                                                                  255),
                                                                                                                 (300,
                                                                                                                  270,
                                                                                                                  200,
                                                                                                                  50),
                                                                                                                 500)
                                                                                                screen.blit(follow3,
                                                                                                            (330, 275))
                                                                                            pygame.display.update()


                                                                                            player.draw(screen)
                                                                                            player.update()
                                                                                            pygame.display.flip()
                                                                                        elif 500 > event.pos[
                                                                                            0] > 300 and 320 > \
                                                                                                event.pos[1] > 270:
                                                                                            delet_result()
                                                                                            start_ok()
                                                                                    if event.type == pygame.MOUSEMOTION:
                                                                                        if 500 > event.pos[
                                                                                            0] > 300 and 250 > \
                                                                                                event.pos[1] > 200:
                                                                                            pygame.draw.rect(screen, (
                                                                                            255, 255, 255), (300, 200,
                                                                                                             200, 50),
                                                                                                             500)
                                                                                            screen.blit(follow2,
                                                                                                        (315, 205))
                                                                                        elif 500 > event.pos[
                                                                                            0] > 300 and 320 > \
                                                                                                event.pos[1] > 270:
                                                                                            pygame.draw.rect(screen, (
                                                                                            255, 255, 255), (300, 270,
                                                                                                             200, 50),
                                                                                                             500)
                                                                                            screen.blit(follow3,
                                                                                                        (330, 275))
                                                                                        pygame.display.update()

                                                                        player.draw(screen)
                                                                        player.update()
                                                                        pygame.display.flip()
                                                                elif 500 > event.pos[0] > 300 and 320 > event.pos[
                                                                    1] > 270:
                                                                    delet_result()
                                                                    start_ok()
                                                            if event.type == pygame.MOUSEMOTION:
                                                                if 500 > event.pos[0] > 300 and 250 > event.pos[
                                                                    1] > 200:
                                                                    pygame.draw.rect(screen, (255, 255, 255),
                                                                                     (300, 200, 200, 50), 500)
                                                                    screen.blit(follow2, (315, 205))
                                                                elif 500 > event.pos[0] > 300 and 320 > event.pos[
                                                                    1] > 270:
                                                                    pygame.draw.rect(screen, (255, 255, 255),
                                                                                     (300, 270, 200, 50), 500)
                                                                    screen.blit(follow3, (330, 275))
                                                                pygame.display.update()

                                                player.draw(screen)
                                                player.update()
                                                pygame.display.flip()
                                        elif 500 > event.pos[0] > 300 and 320 > event.pos[1] > 270:
                                            delet_result()
                                            start_ok()
                                    if event.type == pygame.MOUSEMOTION:
                                        if 500 > event.pos[0] > 300 and 250 > event.pos[1] > 200:
                                            pygame.draw.rect(screen, (255, 255, 255), (300, 200, 200, 50), 500)
                                            screen.blit(follow2, (315, 205))
                                        elif 500 > event.pos[0] > 300 and 320 > event.pos[1] > 270:
                                            pygame.draw.rect(screen, (255, 255, 255), (300, 270, 200, 50), 500)
                                            screen.blit(follow3, (330, 275))
                                        pygame.display.update()

                        player.draw(screen)
                        player.update()
                        pygame.display.flip()

                elif 500 > event.pos[0] > 300 and 320 > event.pos[1] > 270:
                    delet_result()
                    start_ok()
            if event.type == pygame.MOUSEMOTION:
                if 500 > event.pos[0] > 300 and 250 > event.pos[1] > 200:
                    pygame.draw.rect(screen, (255, 255, 255), (300, 200, 200, 50), 500)
                    screen.blit(follow2, (315, 205))
                elif 500 > event.pos[0] > 300 and 320 > event.pos[1] > 270:
                    pygame.draw.rect(screen, (255, 255, 255), (300, 270, 200, 50), 500)
                    screen.blit(follow3, (330, 275))

                pygame.display.update()
