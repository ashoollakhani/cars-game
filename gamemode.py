import random
from car import Car
import pygame
import sys

street_position = 0
pygame.mixer.init()
car_crash_sound = pygame.mixer.Sound("music/car_crash.wav")
driving_sound = pygame.mixer.Sound("music/driving.wav")
explosion_sound = pygame.mixer.Sound("music/explosion.wav")


def pause_screen(screen):
    """
       Display the pause screen on the provided Pygame screen.

       Parameters:
       - screen (pygame.Surface): The Pygame screen.
    """
    paused_image = pygame.image.load("Images/pause.png")
    screen.blit(paused_image, (0, 0))


class Bomb(pygame.sprite.Sprite):
    def __init__(self, width, height, y, image):
        """
                    Initialize a Bomb sprite.

                    Parameters:
                    - width (int): The width of the bomb.
                    - height (int): The height of the bomb.
                    - y (int): The initial y-coordinate of the bomb - height.
                    - image (str): The file path for the image of the bomb.
        """
        super().__init__()
        self.image = pygame.image.load(image)
        scale_factor = 2.5
        self.image = pygame.transform.scale(self.image, (int(width * scale_factor), int(height * scale_factor)))
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([100, 200, 300, 400])  # Random X position
        self.rect.y = y
        self.speed = 3

    def moveDown(self):
        self.rect.y += self.speed

    def respawn(self):
        self.rect.y = -300
        self.rect.x = random.choice([100, 200, 300, 400])  # Random X position


class Projectile(pygame.sprite.Sprite):

    def __init__(self, image_path, speed, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def moveUp(self):
        #Move the projectile sprite upward.

        self.rect.y -= self.speed


def special_game_mode(color1_flag=None, color2_flag=None):
    """
            Start a special game mode

        Parameters:
        - color1_flag (str, optional): The color flag for player's car. (faiscamcqueen.png if left as None)
        - color2_flag (str, optional): The color flag for player's car in case color1_flag is not specifed
    """
    from interface import interface
    pygame.init()

    background_image = pygame.image.load("Images/background.png")
    pygame.image.load("Images/crash.png")

    GREEN, BLACK, GREY, WHITE, RED, PURPLE, YELLOW, CYAN, BLUE = (20, 255, 140), (0, 0, 0), (210, 210, 210), (
        255, 255, 255), (255, 0, 0), (255, 0, 255), (255, 255, 0), (0, 255, 255), (100, 100, 255)
    colorList = (RED, GREEN, PURPLE, YELLOW, CYAN, BLUE, BLACK)

    SCREENWIDTH, SCREENHEIGHT = 1000, 700
    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Car Racing")

    clock = pygame.time.Clock()
    carryOn, playerCar_speed, timer, time_second, score = True, 5, 0, 0, 0

    image_list = ["Images/faisca.png", "Images/faisca2.png", "Images/faisca3.png", "Images/faisca4.png",
                  "Images/truck.png", "Images/dinoco.png", "Images/hicks.png", "Images/crewchief.png",
                  "Images/mater.png", "Images/tractor.png", "Images/truck2.png", ]

    def initialize_car(color, width, height, speed, x, y, image):
        car = Car(color, width, height, speed, image=image)
        car.rect.x = x
        car.rect.y = y
        return car

    if color1_flag is None:
        if color2_flag is not None:
            color1_flag = color2_flag

    # Color of the Car
    if color1_flag is not None:
        if color1_flag == "red":
            playerCar = initialize_car(RED, 69, 150, 0, 400, SCREENHEIGHT - 150, 'Images/red_mcqueen.png')
        elif color1_flag == "green":
            playerCar = initialize_car(GREEN, 69, 150, 0, 400, SCREENHEIGHT - 150, 'Images/green_mcqueen.png')
        elif color1_flag == "blue":
            playerCar = initialize_car(BLUE, 69, 150, 0, 400, SCREENHEIGHT - 150, 'Images/blue_mcqueen.png')
        elif color1_flag == "yellow":
            playerCar = initialize_car(YELLOW, 69, 150, 0, 400, SCREENHEIGHT - 150, 'Images/yellow_mcqueen.png')
    else:
        playerCar = initialize_car(RED, 69, 150, 0, 400, SCREENHEIGHT - 150, 'Images/faiscamcqueen.png')

    car1 = initialize_car(PURPLE, 80, 130, 1, 100, -100, "Images/faisca.png")
    car2 = initialize_car(YELLOW, 80, 130, 2, 250, -600, "Images/faisca2.png")
    car3 = initialize_car(CYAN, 80, 130, 4, 400, -300, "Images/faisca3.png")
    car4 = initialize_car(BLUE, 80, 130, 5, 550, -900, "Images/faisca.png")

    bomb_image = "Images/bomb.png"
    bomb = Bomb(30, 30, random.randint(50, 600), bomb_image)
    all_bombs = pygame.sprite.Group(bomb)

    all_sprites_list = pygame.sprite.Group(playerCar, car1, car2, car3, car4)
    all_coming_cars = pygame.sprite.Group(car1, car2, car3, car4)
    projectiles_list = pygame.sprite.Group()

    playerCar.last_shot_time = 0

    font = pygame.font.SysFont("arial black", 30)
    text = font.render("Time: ", True, (255, 255, 255), (0, 0, 0))
    pos_text = text.get_rect()
    pos_text.center = (800, 50)

    timer = 0
    time_second = 0
    score = 0

    score_font = pygame.font.SysFont("arial black", 30)

    interface_image_1 = pygame.image.load("Images/shield.png")
    interface_image_2 = pygame.image.load("Images/size_reduction.png")
    interface_image_3 = pygame.image.load("Images/double.png")
    interface_image_4 = pygame.image.load("Images/slow_down.png")

    paused = False
    resume_button = pygame.Rect(SCREENWIDTH // 2 - 132, SCREENHEIGHT // 2 - 83, 255, 62)
    exit_button = pygame.Rect(SCREENWIDTH // 2 - 132, SCREENHEIGHT // 2 + 10, 255, 62)
    countdown_font = pygame.font.Font(None, 64)
    driving_sound.play(-1)

    while carryOn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if paused and resume_button.collidepoint(event.pos):
                    paused = not paused
                    # let user shoot only once a second
                    countdown_seconds = 3
                    while countdown_seconds > 0:
                        pause_screen(screen)
                        countdown_text = countdown_font.render(str(countdown_seconds), True, (255, 255, 255))
                        screen.blit(countdown_text, (SCREENWIDTH // 2 - 10, SCREENHEIGHT // 2 - 200))
                        pygame.display.flip()
                        pygame.time.delay(1000)
                        countdown_seconds -= 1

                    driving_sound.play(-1)

                if exit_button.collidepoint(event.pos):
                    carryOn = False
                    interface()

        if paused:
            driving_sound.stop()
            pause_screen(screen)
            pygame.display.flip()

        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and playerCar.rect.x > 50:
                playerCar.moveLeft(5)
            if keys[pygame.K_RIGHT] and playerCar.rect.x < 550:
                playerCar.moveRight(5)
            if keys[pygame.K_SPACE]:
                # Check if enough time has passed since the last shot (1 second cooldown)
                current_time = pygame.time.get_ticks()
                if current_time - playerCar.last_shot_time >= 1000:
                    projectile_image = "Images/proj2.png"
                    # Calculate the x-coordinate so that the projectile starts from the center of the player's car
                    projectile_x = playerCar.rect.x + (playerCar.rect.width // 2) - (5 // 2) - 20
                    projectile = Projectile(projectile_image, 8, projectile_x, playerCar.rect.y)
                    projectiles_list.add(projectile)
                    # Update the last shot time
                    playerCar.last_shot_time = current_time
            if playerCar.slowdown:
                playerCar_speed = 1
            else:
                playerCar_speed = 5

            if playerCar.small:
                playerCar.resize(69 / 2, 150 / 2)
            else:
                playerCar.resize(69, 150)

            pygame.draw.rect(screen, BLACK, [0, 0, SCREENWIDTH, 5])  # Top barrier
            pygame.draw.rect(screen, BLACK, [0, SCREENHEIGHT - 5, SCREENWIDTH, 5])  # Bottom barrier

            pygame.draw.rect(screen, GREY, [50, 0, 600, 700])

            line_positions = [200, 350, 500]
            line_y_positions = [-50, -150, -250, -350, -450, -550, -650]
            global street_position
            street_position += 3.1
            street_position %= 700

            yellow_line_y = 0
            yellow_line_y_end = SCREENHEIGHT
            pygame.draw.line(screen, YELLOW, [50, yellow_line_y], [50, yellow_line_y_end], 10)
            pygame.draw.line(screen, YELLOW, [650, yellow_line_y], [650, yellow_line_y_end], 10)

            # moving street effect
            for x in line_positions:
                for i, y in enumerate(line_y_positions):
                    y_pos = (y + street_position) % 700

                    pygame.draw.line(screen, WHITE, [x, y_pos], [x, y_pos + 60], 7)
                    pygame.draw.line(screen, WHITE, [x, y_pos - 700], [x, y_pos - 640], 7)
                    pygame.draw.line(screen, WHITE, [x, y_pos + 700], [x, y_pos + 760], 7)

            if timer < 60:
                timer += 1
            else:
                time_second += 1
                text = font.render("Time: " + str(time_second), True, (255, 255, 255), (0, 0, 0))
                timer = 0

            for car in all_coming_cars:
                car.moveBackward(playerCar_speed)
                if car.rect.y >= SCREENHEIGHT:
                    car.repaint(random.choice(colorList))
                    car.changeSpeed(random.randint(1, 5))
                    Si = (random.randrange(60, 100) / 100)
                    car.resize(80 * Si, 150 * Si)
                    car.rect.y = random.randint(-300, 0)
                    all_coming_cars.add(car)
                    car.reimage(random.choice(image_list))

            projectiles_list.update()
            projectiles_list.draw(screen)
            for projectile in projectiles_list:
                projectile.moveUp()

            bomb.moveDown()
            if bomb.rect.y >= SCREENHEIGHT:
                bomb.respawn()

            if pygame.sprite.collide_mask(playerCar, bomb) is not None:
                carryOn = False  # Game over when the player hits the bomb
                explosion_sound.play()
                continue  # Skip checking projectile collisions to avoid shooting over the bomb

            bomb_hit_list = pygame.sprite.spritecollide(bomb, projectiles_list, True)
            for _ in bomb_hit_list:
                carryOn = False  # Game over when the projectile hits the bomb
                explosion_sound.play()
                break  # Exit the loop since the game ended

            all_bombs.update()  # update bomb position
            all_bombs.draw(screen)  # draw bombs on the screen

            for projectile in projectiles_list:
                car_hit_list = pygame.sprite.spritecollide(projectile, all_coming_cars, True)
                for hit_car in car_hit_list:
                    projectiles_list.remove(projectile)
                    score += 100
                    respawn_car(hit_car.rect.x)  # Pass the x-coordinate of the hit car to the respawn function

            def respawn_car(x_position):
                car = initialize_car(random.choice(colorList), 80, 130, random.randint(1, 5), x_position, -300,
                                     random.choice(image_list))
                all_coming_cars.add(car)
                all_sprites_list.add(car)

            all_sprites_list.update()

            for car in all_coming_cars:
                if not playerCar.invincible and pygame.sprite.collide_mask(playerCar, car) is not None:
                    carryOn = False
                    pygame.draw.rect(screen, BLACK, [60, 0, 400, 500])
                    car_crash_sound.play()

            score_text = score_font.render(f"Score: {score}", True, (255, 255, 255), (0, 0, 0))
            score_rect = score_text.get_rect(center=(800, 100))
            screen.blit(score_text, score_rect)

            T = [0, 0]
            if playerCar.invincible:
                screen.blit(pygame.transform.scale(interface_image_1, (100, 100)), (800, 300))
                color = BLUE
                T.append(time_second)
            elif playerCar.small:
                screen.blit(pygame.transform.scale(interface_image_2, (100, 100)), (800, 300))
                color = PURPLE
                T.append(time_second)

                playerCar.rect.width = 69 // 2
                playerCar.rect.height = 150 // 2
            elif playerCar.double:
                screen.blit(pygame.transform.scale(interface_image_3, (100, 100)), (800, 300))
                color = YELLOW
                T.append(time_second)
            elif playerCar.slowdown:
                screen.blit(pygame.transform.scale(interface_image_4, (100, 100)), (800, 300))
                color = GREEN
                T.append(time_second)
            else:
                color = RED
                playerCar.rect.width = 69
                playerCar.rect.height = 150

            screen.blit(text, pos_text)

            all_sprites_list.update()

            all_sprites_list.draw(screen)

            if playerCar.invincible or playerCar.small or playerCar.double or playerCar.slowdown:
                pygame.draw.rect(screen, color, playerCar.rect, width=4)

            pygame.display.flip()

            screen.blit(background_image, (0, 0))

            clock.tick(60)

    driving_sound.stop()
    font = pygame.font.SysFont("arial black", 30)
    game_over = pygame.image.load("Images/4.png")
    screen.blit(game_over, (0, 0))
    time_elapsed_text = font.render(f"{time_second} seconds", True, WHITE)
    time_elapsed_rect = time_elapsed_text.get_rect(center=(SCREENWIDTH // 2 + 100, SCREENHEIGHT // 2 - 46))

    score_text_gameover = font.render(f"{score}", True, WHITE)
    score_rect_gameover = score_text_gameover.get_rect(center=(SCREENWIDTH // 2 - 67, SCREENHEIGHT // 2 + 10))

    screen.blit(time_elapsed_text, time_elapsed_rect)
    screen.blit(score_text_gameover, score_rect_gameover)
    pygame.display.flip()

    inGameOverScreen = True
    go_to_interface = False

    play_again_button = pygame.Rect(SCREENWIDTH // 2 - 115, SCREENHEIGHT // 2 + 138, 255, 62)
    goto_interface_button = pygame.Rect(SCREENWIDTH // 2 - 175, SCREENHEIGHT // 2 + 237, 370, 62)

    while inGameOverScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    special_game_mode(color1_flag, color2_flag)
                    inGameOverScreen = False
                elif event.key == pygame.K_n:
                    go_to_interface = True
                    inGameOverScreen = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_button.collidepoint(event.pos):
                    special_game_mode(color1_flag, color2_flag)
                    inGameOverScreen = False
                elif goto_interface_button.collidepoint(event.pos):
                    go_to_interface = True
                    inGameOverScreen = False

    if go_to_interface:
        interface()


pygame.quit()
