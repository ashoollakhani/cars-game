import random
from car import Car
from powerups import *
import sys

import pygame.mixer

pygame.mixer.init()
car_crash_sound = pygame.mixer.Sound("music/car_crash.wav")
driving_sound = pygame.mixer.Sound("music/driving.wav")

street_position = 0


def pause_screen(screen):
    paused_image = pygame.image.load("Images/pause.png")
    screen.blit(paused_image, (0, 0))


def car_racing(difficulty=1, color1_flag=None, color2_flag=None):
    """
           Main function for the car racing game.

           Args:
               difficulty (int): Difficulty level of the game (1, 2, or 3).
               color1_flag (str): Flag specifying the color of the player's car.
               color2_flag (str): Flag specifying the color of the player's car (fallback if color1_flag is None).
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
                  "Images/truck.png","Images/dinoco.png","Images/hicks.png","Images/crewchief.png",
                  "Images/mater.png","Images/tractor.png","Images/truck2.png",]

    def initialize_car(color, width, height, speed, x, y, image):
        """
                Makes a car object with the specified parameters.

                Args:
                    color (tuple): RGB tuple representing the color of the car.
                    width (int): Width of the car.
                    height (int): Height of the car.
                    speed (int): Initial speed of the car.
                    x (int): Initial x-coordinate of the car.
                    y (int): Initial y-coordinate of the car.
                    image (str): Path to the image file for the car.

                Returns:
                    Car: Car object.
        """
        car = Car(color, width, height, speed, image=image)
        car.rect.x = x
        car.rect.y = y
        return car

    if color1_flag is None:
        if color2_flag is not None:
            color1_flag = color2_flag

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

    # Initialization of enemy cars
    car1 = initialize_car(PURPLE, 80, 130, 1, 100, -100, "Images/faisca.png")
    car2 = initialize_car(YELLOW, 80, 130, 2, 250, -600, "Images/faisca2.png")
    car3 = initialize_car(CYAN, 80, 130, 4, 400, -300, "Images/faisca3.png")
    car4 = initialize_car(BLUE, 80, 130, 5, 550, -900, "Images/faisca.png")

    # Initialization of powerups
    invincibility_power_up = InvincibilityPowerUp(YELLOW, 50, 50, 2, image="Images/shield.png")
    double_power_up = DoublePowerUp(GREEN, 50, 50, 2, image="Images/double.png")
    small_power_up = SmallPowerUp(RED, 50, 50, 2, image="Images/size_reduction.png")
    slowdown_power_up = SlowdownPowerUp(BLUE, 50, 50, 2, image="Images/slow_down.png")

    # group them
    all_sprites_list = pygame.sprite.Group(playerCar, car1, car2, car3, car4)
    all_coming_cars = pygame.sprite.Group(car1, car2, car3, car4)

    font = pygame.font.SysFont("arial black", 30)
    text = font.render("Time: ", True, (255, 255, 255), (0, 0, 0))
    pos_text = text.get_rect()
    pos_text.center = (800, 50)

    timer = 0
    time_second = 0
    score = 0
    power_up_caught = False
    active_power_up = None

    score_font = pygame.font.SysFont("arial black", 30)

    # spawn random weighted powerup on a random position
    for _ in range(1):
        power_up_types = [invincibility_power_up, double_power_up, small_power_up, slowdown_power_up]
        weights = [0.1, 0.1, 0.3, 0.2]
        power_up = random.choices(power_up_types, weights)[0]
        power_up.rect.x = random.randint(100, 400)
        power_up.rect.y = -300
        all_sprites_list.add(power_up)

    interface_image_1 = pygame.image.load("Images/shield.png")
    interface_image_2 = pygame.image.load("Images/size_reduction.png")
    interface_image_3 = pygame.image.load("Images/double.png")
    interface_image_4 = pygame.image.load("Images/slow_down.png")

    paused = False
    resume_button = pygame.Rect(SCREENWIDTH // 2 - 132, SCREENHEIGHT // 2 - 83, 255, 62)
    exit_button = pygame.Rect(SCREENWIDTH // 2 - 132, SCREENHEIGHT // 2 + 10, 255, 62)
    countdown_font = pygame.font.Font(None, 64)

    # infinite loop driving_sound when ingame
    driving_sound.play(-1)
    # Carryon to be true until the player crashes (on the condition they don't have invicibility active)
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

                    countdown_seconds = 3

                    # While loop that counts down and ends when the countdown (countdown_seconds) is done (equal to 0)
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
            pause_screen(screen)
            pygame.display.flip()
            driving_sound.stop()

        else:
            # Player Movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and playerCar.rect.x > 50:
                playerCar.moveLeft(5)
            if keys[pygame.K_RIGHT] and playerCar.rect.x < 550:
                playerCar.moveRight(5)
            if keys[pygame.K_UP] and playerCar.rect.y > 0 and playerCar_speed < 10:
                playerCar_speed += 0.1
                playerCar.moveForward(playerCar_speed)
                for car in all_coming_cars:
                    car.adjust_enemy_speed(0.1)
            if keys[pygame.K_DOWN] and playerCar.rect.y < 500 and playerCar_speed > 0:
                playerCar_speed -= 0.1
                playerCar.moveBackward(playerCar_speed)
                for car in all_coming_cars:
                    car.adjust_enemy_speed(-0.1)
            if playerCar.slowdown:
                playerCar_speed = 1
            else:
                playerCar_speed = 5

            if playerCar.small:
                playerCar.resize(int(69 / 2), int(150 / 2))
            else:
                playerCar.resize(69, 150)

            pygame.draw.rect(screen, GREY, [50, 0, 600, 700])

            # Positions for spawning enemy cars
            line_positions = [200, 350, 500]
            line_y_positions = [-50, -150, -250, -350, -450, -550, -650]
            global street_position
            street_position += 3.1
            street_position %= 700

            yellow_line_y = 0
            yellow_line_y_end = SCREENHEIGHT
            pygame.draw.line(screen, YELLOW, [50, yellow_line_y], [50, yellow_line_y_end], 10)
            pygame.draw.line(screen, YELLOW, [650, yellow_line_y], [650, yellow_line_y_end], 10)

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

            score_text = score_font.render(f"Score: {score}", True, (255, 255, 255), (0, 0, 0))
            score_rect = score_text.get_rect(center=(800, 100))
            screen.blit(score_text, score_rect)

            # make the enemy cars move in-game
            # working with difficulty, impacts the car speed
            for car in all_coming_cars:
                car.moveBackward(playerCar_speed)
                if car.rect.y >= SCREENHEIGHT:
                    if power_up == double_power_up and active_power_up == double_power_up:
                        score += 200
                    else:
                        score += 100
                    if difficulty == 1:
                        car.repaint(random.choice(colorList))
                        car.changeSpeed(random.randint(1, 3))
                        Si = (random.randrange(60, 100) / 100)
                        car.resize(80 * Si, 150 * Si)
                        car.rect.y = random.randint(-300, 0)
                        all_coming_cars.add(car)
                        car.reimage(random.choice(image_list))
                    if difficulty == 2:
                        car.repaint(random.choice(colorList))
                        car.changeSpeed(random.randint(3, 7))
                        Si = (random.randrange(60, 100) / 100)
                        car.resize(80 * Si, 150 * Si)
                        car.rect.y = random.randint(-300, 0)
                        all_coming_cars.add(car)
                        car.reimage(random.choice(image_list))
                    if difficulty == 3:
                        car.repaint(random.choice(colorList))
                        car.changeSpeed(random.randint(7, 10))
                        Si = (random.randrange(60, 100) / 100)
                        car.resize(80 * Si, 150 * Si)
                        car.rect.y = random.randint(-300, 0)
                        all_coming_cars.add(car)
                        car.reimage(random.choice(image_list))

            power_up.moveBackward(playerCar_speed)

            if power_up.rect.y >= SCREENHEIGHT:
                if pygame.sprite.collide_rect(playerCar, power_up):
                    power_up.apply_power_up(playerCar)

                else:
                    if random.random() < 0.003:
                        active_power_up = None
                        power_up_types = [invincibility_power_up, double_power_up, small_power_up, slowdown_power_up]
                        weights = [0.1, 0.1, 0.3, 0.2]
                        power_up = random.choices(power_up_types, weights)[0]
                        power_up.rect.x = random.randint(100, 400)
                        power_up.rect.y = -300
                        all_sprites_list.add(power_up)

            if pygame.sprite.collide_rect(playerCar, power_up):
                if not power_up_caught:
                    active_power_up = power_up
                    power_up_caught = True
                    if power_up == invincibility_power_up:
                        power_up.apply_power_up_1(playerCar)
                    elif power_up == double_power_up:
                        power_up.apply_power_up_2(playerCar)
                    elif power_up == slowdown_power_up:
                        power_up.apply_power_up_4(playerCar)
                    elif power_up == small_power_up:
                        power_up.apply_power_up_3(playerCar)
                    all_sprites_list.remove(power_up)

            if power_up_caught and random.random() < 0.103:  # TODO might be here
                power_up_types = [invincibility_power_up, double_power_up, small_power_up, slowdown_power_up]
                weights = [0.1, 0.1, 0.3, 0.2]
                power_up = random.choices(power_up_types, weights)[0]
                power_up.rect.x = random.randint(100, 400)
                power_up.rect.y = -300
                all_sprites_list.add(power_up)
                active_power_up = None
                power_up_caught = False

            all_sprites_list.update()

            playerCar.update_invincibility()
            playerCar.update_double()
            playerCar.update_small()
            playerCar.update_slowdown()

            for car in all_coming_cars:
                if not playerCar.invincible and pygame.sprite.collide_mask(playerCar, car) is not None:
                    carryOn = False
                    car_crash_sound.play()
                    pygame.draw.rect(screen, BLACK, [60, 0, 400, 500])

            if playerCar.invincible:
                screen.blit(pygame.transform.scale(interface_image_1, (100, 100)), (800, 300))
                color = BLUE

            elif playerCar.small:
                screen.blit(pygame.transform.scale(interface_image_2, (100, 100)), (800, 300))
                color = PURPLE

                playerCar.rect.width = 69 // 2
                playerCar.rect.height = 150 // 2
            elif playerCar.double:
                screen.blit(pygame.transform.scale(interface_image_3, (100, 100)), (800, 300))
                color = YELLOW

            elif playerCar.slowdown:
                screen.blit(pygame.transform.scale(interface_image_4, (100, 100)), (800, 300))
                color = GREEN

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

            screen.blit(background_image, (-385, 0))

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

    inGameOverScreen = True
    go_to_interface = False

    play_again_button = pygame.Rect(SCREENWIDTH // 2 - 115, SCREENHEIGHT // 2 + 138, 255, 62)
    goto_interface_button = pygame.Rect(SCREENWIDTH // 2 - 175, SCREENHEIGHT // 2 + 237, 370, 62)

    pygame.display.flip()

    # Checking for events to see if user wants to quit,retry
    while inGameOverScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    car_racing(difficulty, color1_flag, color2_flag)
                    inGameOverScreen = False
                elif event.key == pygame.K_n:
                    go_to_interface = True
                    inGameOverScreen = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_button.collidepoint(event.pos):
                    car_racing(difficulty, color1_flag, color2_flag)
                    inGameOverScreen = False
                elif goto_interface_button.collidepoint(event.pos):
                    go_to_interface = True
                    inGameOverScreen = False

    if go_to_interface:
        interface()


pygame.quit()
