import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIND = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Don't touch them!")

BG = pygame.transform.scale(
    pygame.image.load("konoha.png").convert_alpha(), (WIDTH, HEIGHT)
)

NARUTO_WIDTH = 120
NARUTO_HEIGHT = 140
NARUTO_VEL = 5
SHURI_WIDTH = 60
SHURI_HEIGHT = 60
SHURI_VEL = 10


FONT = pygame.font.SysFont("comicsans", 30)
LOST_FONT = pygame.font.SysFont("urwbookman", 50)

naruto_img = pygame.transform.scale(
    pygame.image.load("naruto.png").convert_alpha(), (NARUTO_WIDTH, NARUTO_HEIGHT)
)

shuri_img = pygame.transform.scale(
    pygame.image.load("shuri.png").convert_alpha(), (SHURI_WIDTH, SHURI_HEIGHT)
)


def draw(naruto, elapsed_time, shuris):
    WIND.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIND.blit(time_text, (15, 15))
    WIND.blit(naruto_img, naruto)
    for shuri in shuris:
        WIND.blit(shuri_img, shuri)
    pygame.display.update()


def main():
    run = True

    naruto = naruto_img.get_rect(midbottom=(WIDTH // 2, HEIGHT))

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    shuri_add_increment = 2000
    shuri_count = 0
    shuris = []
    hit = False

    while run:
        shuri_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if shuri_count > shuri_add_increment:
            for _ in range(3):
                shuri_x = random.randint(SHURI_WIDTH // 2, WIDTH - SHURI_WIDTH // 2)
                shuri = shuri_img.get_rect(midtop=(shuri_x, -SHURI_HEIGHT))

                shuris.append(shuri)
            shuri_add_increment = max(200, shuri_add_increment - 50)
            shuri_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and naruto.x - NARUTO_VEL >= 0:
            naruto.x -= NARUTO_VEL
        if keys[pygame.K_RIGHT] and naruto.x + NARUTO_VEL + NARUTO_WIDTH <= WIDTH:
            naruto.x += NARUTO_VEL
        for shuri in shuris[:]:
            shuri.y += SHURI_VEL
            if shuri.y > HEIGHT:
                shuris.remove(shuri)
            elif shuri.y + shuri.height >= naruto.y and shuri.colliderect(naruto):
                shuris.remove(shuri)
                hit = True
                break
        if hit:
            lost_text = LOST_FONT.render("You Lost Naruto!", 1, "black")
            WIND.blit(
                lost_text,
                (
                    WIDTH / 2 - lost_text.get_width() / 2,
                    HEIGHT / 2 - lost_text.get_height() / 2 - 110,
                ),
            )
            pygame.display.update()
            pygame.time.delay(4000)
            break
        draw(naruto, elapsed_time, shuris)
    pygame.quit()


if __name__ == "__main__":
    main()
