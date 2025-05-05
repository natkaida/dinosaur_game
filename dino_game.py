import pygame
import os
import random
import sys
pygame.init()





def load_image(filename):
    try:
        return pygame.image.load(os.path.join("assets", filename))
    except pygame.error as e:
        print(f"[Ошибка] Не удалось загрузить assets/{filename}: {e}")
        return None

def load_images(filenames):
    return [load_image(filename) for filename in filenames]

def load_resources():
    return {
        "running": load_images(["dino_run1.png", "dino_run2.png"]),
        "jumping": load_image("dino_jump.png"),
        "ducking": load_images(["dino_duck1.png", "dino_duck2.png"]),
        "small_cactus": load_images(["small_cactus1.png", "small_cactus2.png", "small_cactus3.png"]),
        "large_cactus": load_images(["large_cactus1.png", "large_cactus2.png", "large_cactus3.png"]),
        "ptero": load_images(["ptero1.png", "ptero2.png"]),
        "cloud": load_image("cloud.png"),
        "sand": load_image("sand.png")
    }

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")
icon_path = os.path.join("assets", "dino_icon.ico")  
icon_surface = pygame.image.load(icon_path)
pygame.display.set_icon(icon_surface)


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_duck = 340
    jump_VEL = 8.5

    def __init__(self, resources):
        self.duck_img = resources["ducking"]
        self.run_img = resources["running"]
        self.jump_img = resources["jumping"]

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.jump_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.update_hitbox()

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def update_hitbox(self):
        hitbox_width = int(self.dino_rect.width * 0.2)
        hitbox_height = int(self.dino_rect.height * 0.7)
        x_offset = int(self.dino_rect.width * 0.6)
        y_offset = int(self.dino_rect.height * 0.1)
        self.hitbox = pygame.Rect(
            self.dino_rect.x + x_offset,
            self.dino_rect.y + y_offset,
            hitbox_width,
            hitbox_height
        )

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_duck
        self.update_hitbox()
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.update_hitbox()
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.jump_VEL:
            self.dino_jump = False
            self.jump_vel = self.jump_VEL
        self.update_hitbox()

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


class cloud:
    def __init__(self, resources, game_speed):
        self.image = resources["cloud"]
        self.width = self.image.get_width()
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.game_speed = game_speed

    def update(self, game_speed):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type, game_speed):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.game_speed = game_speed
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.update_hitbox()

    def update_hitbox(self):
        hitbox_width = int(self.rect.width * 0.6)
        hitbox_height = int(self.rect.height * 0.8)
        x_offset = int(self.rect.width * 0.25)
        y_offset = int(self.rect.height * 0.1)
        self.hitbox = pygame.Rect(
            self.rect.x + x_offset,
            self.rect.y + y_offset,
            hitbox_width,
            hitbox_height
        )

    def update(self, game_speed):
        self.rect.x -= game_speed
        self.update_hitbox()
        return self.rect.x < -self.rect.width

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)
        pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)


class smallcactus(Obstacle):
    def __init__(self, image, game_speed):
        super().__init__(image, random.randint(0, 2), game_speed)
        self.rect.y = 325


class largecactus(Obstacle):
    def __init__(self, image, game_speed):
        super().__init__(image, random.randint(0, 2), game_speed)
        self.rect.y = 300


class ptero(Obstacle):
    def __init__(self, image, game_speed):
        super().__init__(image, 0, game_speed)
        self.rect.y = 250
        self.index = 0
        self.update_hitbox()

    def update_hitbox(self):
        hitbox_width = int(self.rect.width * 0.8)
        hitbox_height = int(self.rect.height * 0.8)
        x_offset = int(self.rect.width * 0.2)
        y_offset = int(self.rect.height * 0.25)
        self.hitbox = pygame.Rect(
            self.rect.x + x_offset,
            self.rect.y + y_offset,
            hitbox_width,
            hitbox_height
        )

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1
        pygame.draw.rect(screen, (0, 0, 255), self.hitbox, 2)


class Game:
    def __init__(self):
        self.resources = load_resources()
        self.game_speed = 20
        self.x_pos_sand = 0
        self.y_pos_sand = 380
        self.points = 0
        self.obstacles = []
        self.death_count = 0
        self.font = pygame.font.Font(os.path.join("assets", "CuteDino-G33gG.ttf"), 25)
        self.clock = pygame.time.Clock()
        self.player = Dinosaur(self.resources)
        self.cloud = cloud(self.resources, self.game_speed)
        self.paused = False

    def score(self):
        self.points += 1
        if self.points % 100 == 0 and self.game_speed < 50:
            self.game_speed += 1

        text = self.font.render("Points: " + str(self.points), True, (0, 0, 0))
        SCREEN.blit(text, (900, 40))

    def background(self):
        image_width = self.resources["sand"].get_width()
        SCREEN.blit(self.resources["sand"], (self.x_pos_sand, self.y_pos_sand))
        SCREEN.blit(self.resources["sand"], (image_width + self.x_pos_sand, self.y_pos_sand))
        if self.x_pos_sand <= -image_width:
            self.x_pos_sand = 0
        self.x_pos_sand -= self.game_speed

    def run_game(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if self.paused:
                        self.paused = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = True

            if self.paused:
                SCREEN.fill((255, 255, 255))  # белый фон
                pause_text = self.font.render("Paused. Press any key to resume...", True, (0, 0, 0))
                SCREEN.blit(pause_text, (350, 200))
                pygame.display.update()

                continue

            SCREEN.fill((255, 255, 255))
            userInput = pygame.key.get_pressed()

            self.player.draw(SCREEN)
            self.player.update(userInput)

            if len(self.obstacles) == 0:
                choice = random.randint(0, 2)
                if choice == 0:
                    self.obstacles.append(smallcactus(self.resources["small_cactus"], self.game_speed))
                elif choice == 1:
                    self.obstacles.append(largecactus(self.resources["large_cactus"], self.game_speed))
                else:
                    self.obstacles.append(ptero(self.resources["ptero"], self.game_speed))

            for obstacle in list(self.obstacles):
                obstacle.draw(SCREEN)
                if obstacle.update(self.game_speed):
                    self.obstacles.remove(obstacle)
                if self.player.hitbox.colliderect(obstacle.hitbox):
                    pygame.time.delay(2000)
                    self.death_count += 1
                    self.menu()
                    return

            self.background()
            self.cloud.draw(SCREEN)
            self.cloud.update(self.game_speed)
            self.score()

            self.clock.tick(30)
            pygame.display.update()

    def menu(self):
        run = True
        while run:
            SCREEN.fill((255, 255, 255))
#            font = pygame.font.Font(os.path.join("assets", "CuteDino-G33gG.ttf"), 25)
  #          self.font.render("Paused. Press any key to resume...", True, (0, 0, 0))

            if self.death_count == 0:
                text = self.font.render("Press any key to start!", True, (0, 0, 0))
            else:
                text = self.font.render("Press any Key to Restart", True, (0, 0, 0))
                score = self.font.render("Your Score: " + str(self.points), True, (0, 0, 0))
                SCREEN.blit(score, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))

            SCREEN.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            SCREEN.blit(self.resources["running"][0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.reset_game()
                    self.run_game()
                    return True

    def reset_game(self):
        self.game_speed = 20
        self.x_pos_sand = 0
        self.points = 0
        self.obstacles = []
        self.player = Dinosaur(self.resources)
        self.cloud = cloud(self.resources, self.game_speed)
        self.paused = False


def main():
    game = Game()
    game.menu()
    sys.exit()



if __name__ == "__main__":
    main()

