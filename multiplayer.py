import random
from car import Car
from powerups import *
import sys

pygame.mixer.init()
car_crash_sound = pygame.mixer.Sound("music/car_crash.wav")

driving_sound = pygame.mixer.Sound("music/driving.wav")

street_position = 0


def pause_screen(screen):
    paused_image = pygame.image.load("Images/pause.png")
    screen.blit(paused_image, (0, 0))


# Class for creating labels
class Label:
    """
        Class for creating labels.

        Attributes:
        - x (int): X-coordinate of the label.
        - y (int): Y-coordinate of the label.
        - text (str): The text content of the label.
        - font (pygame.font.Font): The font used for the label.
        - font_size (int): The font size of the label.
        - color (tuple): RGB tuple representing the color of the label.
    """
    def __init__(self, x, y, text, font=None, font_size=54, color=(255, 0, 0)):
        if font is None:
            self.font = pygame.font.SysFont("arial black", font_size)
        else:
            self.font = font
        self.text = self.font.render(text, True, color)
        self.position = (x, y)

    def update_text(self, text, color=(255, 0, 0)):
        self.text = self.font.render(text, True, color)

    def draw(self, screen):
        screen.blit(self.text, self.position)


# Function for multiplayer game
def multi_player(color1_flag=None, color2_flag=None):
    """
          Run the multiplayer game.

          Parameters:
          - color1_flag (str, optional): Flag specifying the color of player 1's car. (Red mcqueen default)
          - color2_flag (str, optional): Flag specifying the color of player 2's car. (Blue mcqueen as default)
    """
    pygame.init()
    from interface import interface

    background_image = pygame.image.load("Images/background.png")
    pygame.image.load("Images/crash.png")

    GREEN = (20, 255, 140)
    BLACK = (0, 0, 0)
    GREY = (210, 210, 210)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    RED2 = (220, 50, 100)
    PURPLE = (255, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (100, 100, 255)

    # Color list for cars
    colorList = (RED, RED2, GREEN, PURPLE, YELLOW, CYAN, BLUE, BLACK)

    SCREENWIDTH = 1000
    SCREENHEIGHT = 700

    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Car Racing")

    image_list = ["Images/faisca.png", "Images/faisca2.png", "Images/faisca3.png", "Images/faisca4.png",
                  "Images/truck.png", "Images/dinoco.png", "Images/hicks.png", "Images/crewchief.png",
                  "Images/mater.png", "Images/tractor.png", "Images/truck2.png", ]

    all_sprites_list = pygame.sprite.Group()

    # Initialize player 1 car
    if color1_flag is not None:
        if color1_flag == "red":
            playerCar = Car(RED, 69, 150, image='Images/red_mcqueen.png')
        elif color1_flag == "blue":
            playerCar = Car(BLUE, 69, 150, image='Images/blue_mcqueen.png')
        elif color1_flag == "green":
            playerCar = Car(GREEN, 69, 150, image='Images/green_mcqueen.png')
        elif color1_flag == "yellow":
            playerCar = Car(YELLOW, 69, 150, image='Images/yellow_mcqueen.png')
    else:
        playerCar = Car(color1_flag, 69, 150, image='Images/red_mcqueen.png')

    playerCar.rect.x = 100
    playerCar.rect.y = 450

    # Initialize player 2 car
    if color2_flag is not None:
        if color2_flag == "red":
            playerCar2 = Car(RED, 69, 150, image='Images/red_mcqueen.png')
        elif color2_flag == "blue":
            playerCar2 = Car(BLUE, 69, 150, image='Images/blue_mcqueen.png')
        elif color2_flag == "green":
            playerCar2 = Car(GREEN, 69, 150, image='Images/green_mcqueen.png')
        elif color2_flag == "yellow":
            playerCar2 = Car(YELLOW, 69, 150, image='Images/yellow_mcqueen.png')
    else:
        playerCar2 = Car(color2_flag, 69, 150, image='Images/blue_mcqueen.png')

    playerCar2.rect.x = 300
    playerCar2.rect.y = 450

    # Initialize AI cars
    car1 = Car(PURPLE, 80, 130, 1, image="Images/faisca.png")
    car1.rect.x = 100
    car1.rect.y = -100

    car2 = Car(YELLOW, 80, 130, 2, image="Images/faisca2.png")
    car2.rect.x = 250
    car2.rect.y = -600

    car3 = Car(CYAN, 80, 130, 4, image="Images/faisca3.png")
    car3.rect.x = 400
    car3.rect.y = -300

    car4 = Car(BLUE, 80, 130, 5, image="Images/faisca.png")
    car4.rect.x = 550
    car4.rect.y = -900

    # Initialize power-ups
    invincibility_power_up = InvincibilityPowerUp(YELLOW, 50, 50, 2, image="Images/shield.png")
    double_power_up = DoublePowerUp(GREEN, 50, 50, 2, image="Images/double.png")
    small_power_up = SmallPowerUp(RED, 50, 50, 2, image="Images/size_reduction.png")

    # Add sprites to the sprite group
    all_sprites_list.add(playerCar, playerCar2)
    all_sprites_list.add(car1)
    all_sprites_list.add(car2)
    all_sprites_list.add(car3)
    all_sprites_list.add(car4)

    all_coming_cars = pygame.sprite.Group()
    all_coming_cars.add(car1)
    all_coming_cars.add(car2)
    all_coming_cars.add(car3)
    all_coming_cars.add(car4)

    carryOn = True
    playerCar_speed = 5
    playerCar2_speed = 5

    font = pygame.font.SysFont("arial black", 30)
    text = font.render("Time: ", True, (255, 255, 255), (0, 0, 0))
    pos_text = text.get_rect()
    pos_text.center = (800, 50)

    timer = 0
    time_second = 0

    score_font = pygame.font.SysFont("arial black", 30)
    pygame.font.SysFont("arial black", 70)

    score = 0

    power_up_caught = False
    active_power_up = None

    # Powerup initialization with weights
    power_up_types = [invincibility_power_up, double_power_up, small_power_up]
    weights = [0.1, 0.1, 0.3]
    power_up = random.choices(power_up_types, weights)[0]
    power_up.rect.x = random.randint(100, 400)
    power_up.rect.y = -300
    all_sprites_list.add(power_up)

    interface_image_1 = pygame.image.load("Images/shield.png")
    interface_image_2 = pygame.image.load("Images/size_reduction.png")
    interface_image_3 = pygame.image.load("Images/double.png")
    interface_image_3 = pygame.image.load("Images/double.png")
    interface_image_4 = pygame.image.load("Images/slow_down.png")

    winner = None

    clock = pygame.time.Clock()

    paused = False
    resume_button = pygame.Rect(SCREENWIDTH // 2 - 132, SCREENHEIGHT // 2 - 83, 255, 62)
    exit_button = pygame.Rect(SCREENWIDTH // 2 - 132, SCREENHEIGHT // 2 + 10, 255, 62)
    countdown_font = pygame.font.Font(None, 64)
    driving_sound.play(-1)
    """
        Similar to game.py's code, loop for the game
        Carryon to be true until the player crashes (on the condition they don't have invicibility active)
    """
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
                    """Mentioned previously - counts down from 3 with a live countdown"""
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

            # Player 1 controls
            if keys[pygame.K_LEFT] and playerCar.rect.x > 50:
                if not playerCar2.rect.colliderect(playerCar.rect.move(-5, 0)):
                    playerCar.moveLeft(5)
            if keys[pygame.K_RIGHT] and playerCar.rect.x < 550:
                if not playerCar2.rect.colliderect(playerCar.rect.move(5, 0)):
                    playerCar.moveRight(5)
            if keys[pygame.K_UP] and playerCar.rect.y > 0:
                if not playerCar2.rect.colliderect(playerCar.rect.move(0, -playerCar_speed)):
                    playerCar.moveForward(playerCar_speed)
            if keys[pygame.K_DOWN] and playerCar.rect.y < SCREENHEIGHT - playerCar.rect.height:
                if not playerCar2.rect.colliderect(playerCar.rect.move(0, playerCar_speed)):
                    playerCar.moveBackward(playerCar_speed)

            # Player 2 controls
            if keys[pygame.K_a] and playerCar2.rect.x > 50:
                if not playerCar.rect.colliderect(playerCar2.rect.move(-5, 0)):
                    playerCar2.moveLeft(5)
            if keys[pygame.K_d] and playerCar2.rect.x < 550:
                if not playerCar.rect.colliderect(playerCar2.rect.move(5, 0)):
                    playerCar2.moveRight(5)
            if keys[pygame.K_w] and playerCar2.rect.y > 0:
                if not playerCar.rect.colliderect(playerCar2.rect.move(0, -playerCar2_speed)):
                    playerCar2.moveForward(playerCar2_speed)
            if keys[pygame.K_s] and playerCar2.rect.y < SCREENHEIGHT - playerCar2.rect.height:
                if not playerCar.rect.colliderect(playerCar2.rect.move(0, playerCar2_speed)):
                    playerCar2.moveBackward(playerCar2_speed)

            if playerCar.small:
                playerCar.resize(69 / 2, 150 / 2)
            else:
                playerCar.resize(69, 150)

            if playerCar.slowdown:
                playerCar_speed = 1
            else:
                playerCar_speed = 5

            if playerCar2.small:
                playerCar2.resize(69 / 2, 150 / 2)
            else:
                playerCar2.resize(69, 150)

            if playerCar2.slowdown:
                playerCar2_speed = 1
            else:
                playerCar2_speed = 5

            all_sprites_list.update()
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

            # Draw the lines with the updated position
            for x in line_positions:
                for i, y in enumerate(line_y_positions):
                    y_pos = (y + street_position) % 700

                    # Draw lines above and below the screen to create a continuous effect
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
                    if power_up == double_power_up and active_power_up == double_power_up:
                        score += 200
                    else:
                        score += 100
                    car.repaint(random.choice(colorList))
                    car.changeSpeed(random.randint(1, 5))
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
                        #power_up_types = [invincibility_power_up, double_power_up, small_power_up]
                        #weights = [0.2, 0.5, 0.4]
                        #power_up = random.choices(power_up_types, weights)[0]
                        power_up.rect.x = random.randint(100, 400)
                        power_up.rect.y = -300
                        #all_sprites_list.add(power_up)

            #Checks both cars to see if they have collided with a powerup and applies the appropriate powerup to the appropriate car

            if pygame.sprite.collide_rect(playerCar, power_up):
                if not power_up_caught:
                    active_power_up = power_up
                    power_up_caught = True
                    if power_up == invincibility_power_up:
                        power_up.apply_power_up_1(playerCar)
                    elif power_up == double_power_up:
                        power_up.apply_power_up_2(playerCar)
                    elif power_up == small_power_up:
                        power_up.apply_power_up_3(playerCar)
                    all_sprites_list.remove(power_up)

            if pygame.sprite.collide_rect(playerCar2, power_up):
                if not power_up_caught:
                    active_power_up = power_up
                    power_up_caught = True
                    if power_up == invincibility_power_up:
                        power_up.apply_power_up_1(playerCar2)
                    elif power_up == double_power_up:
                        power_up.apply_power_up_2(playerCar2)
                    elif power_up == small_power_up:
                        power_up.apply_power_up_3(playerCar2)
                    all_sprites_list.remove(power_up)

            if power_up_caught and random.random() < 0.003:
                power_up_types = [invincibility_power_up, double_power_up, small_power_up]
                weights = [0.1, 0.1, 0.3]
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

            playerCar2.update_invincibility()
            playerCar2.update_double()
            playerCar2.update_small()
            playerCar2.update_slowdown()

            # Win Condition
            """Checks if any cars are collided with one another - player 1 and player 2. 
            If either are the other winner is determined (Player 1 collided > Player 2 is the winner) 
            Then a screen displaying the winner is shown along with the score."""
            for car in all_coming_cars:
                if not playerCar.invincible and pygame.sprite.collide_mask(playerCar, car) is not None:
                    carryOn = False
                    car_crash_sound.play()
                    winner = "Player 2"
                    pygame.draw.rect(screen, BLACK, [60, 0, 400, 500])

                if not playerCar2.invincible and pygame.sprite.collide_mask(playerCar2, car) is not None:
                    carryOn = False
                    car_crash_sound.play()
                    winner = "Player 1"
                    pygame.draw.rect(screen, BLACK, [60, 0, 400, 500])

            score_text = score_font.render(f"Score: {score}", True, (255, 255, 255), (0, 0, 0))
            score_rect = score_text.get_rect(center=(800, 100))
            screen.blit(score_text, score_rect)

            # Powerups for both cars
            #Powerups applied here - if the user is invicible,small,doubled,slowed, this segment will change their appearance (sizes,colors and so on) - does this for both cars
            T = [0, 0]
            if playerCar.invincible:
                screen.blit(pygame.transform.scale(interface_image_1, (100, 100)), (730, 160))
                color = BLUE
                T.append(time_second)
            elif playerCar.small:
                screen.blit(pygame.transform.scale(interface_image_2, (100, 100)), (730, 160))
                color = RED
                T.append(time_second)
                playerCar.rect.width = 69 // 2
                playerCar.rect.height = 150 // 2
            elif playerCar.double:
                screen.blit(pygame.transform.scale(interface_image_3, (100, 100)), (730, 160))
                color = YELLOW
                T.append(time_second)
            elif playerCar.slowdown:
                screen.blit(pygame.transform.scale(interface_image_4, (100, 100)), (730, 160))
                color = GREEN
                T.append(time_second)
            else:
                T = [0, 0]
                color = RED

            if playerCar2.invincible:
                screen.blit(pygame.transform.scale(interface_image_1, (100, 100)), (730, 500))
                color2 = BLUE
                T.append(time_second)
            elif playerCar2.small:
                screen.blit(pygame.transform.scale(interface_image_2, (100, 100)), (730, 500))
                color2 = RED
                T.append(time_second)
                playerCar2.rect.width = 69 // 2
                playerCar2.rect.height = 150 // 2

            elif playerCar2.double:
                screen.blit(pygame.transform.scale(interface_image_3, (100, 100)), (730, 500))
                color2 = YELLOW
                T.append(time_second)

            elif playerCar2.slowdown:
                screen.blit(pygame.transform.scale(interface_image_4, (100, 100)), (730, 500))
                color2 = GREEN
                T.append(time_second)
            else:
                color2 = RED
                playerCar2.rect.width = 69
                playerCar2.rect.height = 150

            player1_text = Label(700, 100, "Player 1", font=None, font_size=54, color=RED)
            player1_text.draw(screen)

            player2_text = Label(700, 420, "Player 2", font=None, font_size=54, color=BLUE)
            player2_text.draw(screen)

            all_sprites_list.draw(screen)
            screen.blit(text, pos_text)

            all_sprites_list.update()

            if playerCar.invincible or playerCar.small or playerCar.double or playerCar.slowdown:
                pygame.draw.rect(screen, color, playerCar.rect, width=4)
            if playerCar2.invincible or playerCar2.small or playerCar2.double or playerCar2.slowdown:
                pygame.draw.rect(screen, color2, playerCar2.rect, width=4)

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
    pygame.display.flip()

    if winner:
        winner_text = font.render(f"Winner: {winner}", True, WHITE)
        winner_rect = winner_text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 - 130))
        screen.blit(winner_text, winner_rect)

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
                    multi_player(color1_flag, color2_flag)
                    inGameOverScreen = False
                elif event.key == pygame.K_n:
                    go_to_interface = True
                    inGameOverScreen = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_button.collidepoint(event.pos):
                    multi_player(color1_flag, color2_flag)
                    inGameOverScreen = False
                elif goto_interface_button.collidepoint(event.pos):
                    go_to_interface = True
                    inGameOverScreen = False

    if go_to_interface:
        interface()

    pygame.quit()
