# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random

WIDTH = 360  # ширина игрового окна
HEIGHT = 480  # высота игрового окна
FPS = 30  # частота кадров в секунду

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (150, 0, 255)

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
all_guys = []
nerd_image = pygame.image.load('Nerd.png').convert_alpha()
hooligan_image = pygame.image.load('Hooligan.png').convert_alpha()

# Рендеринг
screen.fill(PURPLE)
# после отрисовки всего, переворачиваем экран
pygame.display.flip()
score = 0


class Guy(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group):
        pygame.sprite.Sprite.__init__(self)
        self.type_name = "Guy"
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.add(group)

    def get_type_name(self):
        return self.type_name


# "Хулиган"
class Hooligan(Guy):
    def __init__(self, group: pygame.sprite.Group):
        super().__init__(group)
        self.type_name = "Hooligan"
        self.image = pygame.transform.scale(hooligan_image, (60, 75))

        self.rect.center = (random.randint(0, 360), 0)

    def update(self):
        global score
        self.rect.y += 5
        if self.rect.y == HEIGHT:
            score += 1


# Игрок
class Player(Guy):
    def __init__(self, group: pygame.sprite.Group):
        super().__init__(group)
        self.type_name = "Player"
        self.image = pygame.transform.scale(nerd_image, (60, 75))
        # self.image.fill(GREEN)
        self.rect.center = (WIDTH / 2, HEIGHT - 60)

    def update(self):
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.x = min(self.rect.x + 2, WIDTH - 60)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.x = max(self.rect.x - 2, 0)


class TextSprite:
    def __init__(self, size: int, place_cord, message_str: str, colour):
        self.font = pygame.font.Font(None, size)
        self.message = self.font.render(message_str, True, colour)
        self.rect = self.message.get_rect(center=place_cord)
        self.text = message_str
        self.place_cord = place_cord

    def draw(self):
        global screen
        screen.blit(self.message, self.rect)

    def set_message(self, message_str):
        self.message = self.font.render(message_str, True, BLACK)
        self.rect = self.message.get_rect(center=self.place_cord)
        self.text = message_str


all_guys.append(Player(all_sprites))

game_status = True
hooligan_timer = 0
hooligan_limit = 80
chosen_lvl = 1
gio_message = TextSprite(54, (WIDTH / 2, HEIGHT / 2 - 30), "GAME IS OVER", BLACK)
pa_message = TextSprite(36, (WIDTH / 2, HEIGHT / 2 + 10), "Play again?", BLACK)
yes_message = TextSprite(36, (WIDTH / 2 - 40, HEIGHT / 2 + 50), "YES", BLACK)
no_message = TextSprite(36, (WIDTH / 2 + 40, HEIGHT / 2 + 50), "NO", BLACK)
score_message = TextSprite(36, (WIDTH - 60, 20), "SCORE: " + str(score), BLACK)
first_lvl_message = TextSprite(36, (WIDTH - 40, 50), "LVL-1", GREEN)
second_lvl_message = TextSprite(36, (WIDTH - 40, 80), "LVL-2", BLUE)
third_lvl_message = TextSprite(36, (WIDTH - 40, 110), "LVL-3", RED)
chosen_lvl_message = TextSprite(30, (85, 20), "CHOSEN LVL: " + str(chosen_lvl), RED)


def check_guys(guys_list):
    player = guys_list[0]
    for hooligan in guys_list:
        if hooligan.get_type_name() != "Player":
            if player.rect.colliderect(hooligan.rect):
                return False
    return True


def is_rectangle_clicked(pos, rect: pygame.rect):
    x1 = rect.x
    x2 = rect.x + rect.width
    y1 = rect.y
    y2 = rect.y + rect.height
    if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
        return True
    else:
        return False


# Цикл игры
running = True
while running:
    # держим цикл на правильной скорости
    clock.tick(FPS)

    # Название окна
    pygame.display.set_caption('Dodger')
    
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_status:
            if is_rectangle_clicked(event.pos, yes_message.rect):
                game_status = True
                hooligan_timer = 0
                all_guys.append(Player(all_sprites))
            elif is_rectangle_clicked(event.pos, no_message.rect):
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if is_rectangle_clicked(event.pos, first_lvl_message.rect):
                hooligan_limit = 60
                chosen_lvl = 1
            elif is_rectangle_clicked(event.pos, second_lvl_message.rect):
                hooligan_limit = 40
                chosen_lvl = 2
            elif is_rectangle_clicked(event.pos, third_lvl_message.rect):
                hooligan_limit = 25
                chosen_lvl = 3

    # Обновление
    if game_status:
        hooligan_timer += 1
        if hooligan_timer >= hooligan_limit:
            all_guys.append(Hooligan(all_sprites))
            hooligan_timer = 0
        game_status = check_guys(all_guys)
        if not game_status:
            if len(all_guys) > 0:
                for guy in all_guys:
                    guy.kill()
                all_guys.clear()

    all_sprites.update()
    screen.fill(PURPLE)
    if game_status:
        all_sprites.draw(screen)
    else:
        gio_message.draw()
        pa_message.draw()
        yes_message.draw()
        no_message.draw()
    score_message.set_message("SCORE: " + str(score))
    chosen_lvl_message.set_message("CHOSEN LVL: " + str(chosen_lvl))
    score_message.draw()
    first_lvl_message.draw()
    second_lvl_message.draw()
    third_lvl_message.draw()
    chosen_lvl_message.draw()

    # Визуализация (сборка)
    pygame.display.flip()


pygame.quit()
