import pygame
import sys
from game import car_racing
from multiplayer import multi_player
from gamemode import special_game_mode

pygame.init()
res = (1000, 720)
screen = pygame.display.set_mode(res)

pygame.mixer.music.load("music/music.mp3")
pygame.mixer.music.play(-1)  # -1 = infinite loop
pygame.mixer.music.set_volume(0.01)  # Set initial volume (low)


def interface(color1_flag=None, color2_flag=None):
    """
        Display the main menu interface and handle user input.

        Parameters:
        - color1_flag (optional, str): Flag indicating the color selected for player 1.
        - color2_flag (optional, str): Flag indicating the color selected for player 2.
    """

    interface_image = pygame.image.load("Images/M_menu.png")
    interface_image = pygame.transform.scale(interface_image, (1000, 720))

    button_G = pygame.Rect(174, 274, 250, 62)
    button_C = pygame.Rect(174, 440, 250, 62)
    button_S = pygame.Rect(174, 358, 250, 62)
    button_Q = pygame.Rect(215, 585, 170, 62)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if button_Q.collidepoint((mx, my)):
                    pygame.quit()
                    sys.exit()
                if button_G.collidepoint((mx, my)):
                    game(color1_flag, color2_flag)
                if button_S.collidepoint((mx, my)):
                    settings()
                if button_C.collidepoint((mx, my)):
                    credits_()

        screen.blit(interface_image, (0, 0))
        pygame.display.update()


def settings():
    """
        Display the settings menu interface and handle user input.
        Images,buttons,sliders,colors are specified and managed
    """
    interface_image = pygame.image.load("Images/Setting.jpg")
    interface_image = pygame.transform.scale(interface_image, (1000, 720))

    apply_button_rect = pygame.Rect(336, 545, 479 - 336, 600 - 545)
    back_button_rect = pygame.Rect(507, 546, 650 - 507, 597 - 546)

    slider_height = 30
    slider_x1, slider_y1 = 400, 250  # Top-left corner of the sound slider
    slider_x2, slider_y2 = 757, 278  # Bottom-right corner of the sound slider
    slider_value = int(pygame.mixer.music.get_volume() * 100)  # Get initial value from music volume
    slider_width = int((slider_x2 - slider_x1) * slider_value / 100)  # Calculate the width based on the percentage
    slider_rect = pygame.Rect(slider_x1, slider_y1, slider_width, slider_height)
    slider_color = (255, 0, 0)
    slider_dragging = False

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)

    color_red = pygame.Rect(400, 340, 50, 50)
    color_green = pygame.Rect(460, 340, 50, 50)
    color_blue = pygame.Rect(520, 340, 50, 50)
    color_yellow = pygame.Rect(580, 340, 50, 50)
    selected_color = None
    color_flag = None

    # Players buttons
    player1_button_rect = pygame.Rect(155, 412, 352, 58)
    player2_button_rect = pygame.Rect(520, 412, 352, 58)
    player1_color = None
    player2_color = None
    color1_flag = None
    color2_flag = None

    # position for the "Music Volume" text
    text_position = (323, 251)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if back_button_rect.collidepoint((mx, my)):
                    interface()

                # Check if the mouse click is inside the slider box
                if slider_x1 <= mx <= slider_x2 and slider_y1 <= my <= slider_y2:
                    slider_dragging = True
                    mx = max(slider_x1, min(slider_x2, mx))
                    slider_value = int(((mx - slider_x1) / (slider_x2 - slider_x1)) * 100)
                    slider_value = max(0, min(100, slider_value))

                    # Calculate the width based on the percentage
                    slider_width = int((slider_x2 - slider_x1) * slider_value / 100)
                    slider_rect.width = max(0, min(slider_x2 - slider_x1, slider_width))

                    # Set the music volume based on the slider value
                    pygame.mixer.music.set_volume(slider_value / 100)

                # box to select car color
                if color_red.collidepoint((mx, my)):
                    selected_color = red
                    color_flag = "red"
                elif color_green.collidepoint((mx, my)):
                    selected_color = green
                    color_flag = "green"
                elif color_blue.collidepoint((mx, my)):
                    selected_color = blue
                    color_flag = "blue"
                elif color_yellow.collidepoint((mx, my)):
                    selected_color = yellow
                    color_flag = "yellow"

                if player1_button_rect.collidepoint((mx, my)):
                    player1_color = selected_color
                    color1_flag = color_flag
                    color_flag = None
                elif player2_button_rect.collidepoint((mx, my)):
                    player2_color = selected_color
                    color2_flag = color_flag
                    color_flag = None

                if slider_rect.collidepoint((mx, my)):
                    slider_dragging = True
                elif back_button_rect.collidepoint((mx, my)):
                    interface(color1_flag, color2_flag)
                elif apply_button_rect.collidepoint((mx, my)):
                    interface(color1_flag, color2_flag)

            elif ev.type == pygame.MOUSEBUTTONUP:
                slider_dragging = False
            elif ev.type == pygame.MOUSEMOTION and slider_dragging:
                mx, my = pygame.mouse.get_pos()
                mx = max(slider_x1, min(slider_x2, mx))
                slider_value = int(((mx - slider_x1) / (slider_x2 - slider_x1)) * 100)
                slider_value = max(0, min(100, slider_value))

                # Calculate the width based on the percentage
                slider_width = int((slider_x2 - slider_x1) * slider_value / 100)
                slider_rect.width = max(0, min(slider_x2 - slider_x1, slider_width))

                # Set the music volume based on the slider value
                pygame.mixer.music.set_volume(slider_value / 100)

        screen.blit(interface_image, (0, 0))

        pygame.draw.rect(screen, slider_color, slider_rect)

        # Draw the colors
        pygame.draw.rect(screen, red, color_red)
        pygame.draw.rect(screen, green, color_green)
        pygame.draw.rect(screen, blue, color_blue)
        pygame.draw.rect(screen, yellow, color_yellow)

        if player1_color is not None:
            pygame.draw.rect(screen, player1_color, [player1_button_rect.x + 295, player1_button_rect.y + 5, 50, 45])
        if player2_color is not None:
            pygame.draw.rect(screen, player2_color, [player2_button_rect.x + 295, player2_button_rect.y + 5, 50, 45])

        font = pygame.font.SysFont("arial black", 24)
        text = font.render(f"{slider_value}%", True, (255, 255, 255))
        screen.blit(text, text_position)

        pygame.display.update()


def credits_():
    interface_image = pygame.image.load("Images/Credits.jpg")
    interface_image = pygame.transform.scale(interface_image, (1000, 720))

    button_B = pygame.Rect(426, 548, 147, 50)
    button_I = pygame.Rect(573, 598, 50, 50)

    font = pygame.font.SysFont("arial black", 36)

    names = [
        "Ashool Lakhani",
        "Fransisco Olivera",
        "Tara Kouros",
    ]

    text_color = (255, 255, 255)
    text_start_y = 275
    text_spacing = 55

    screen.blit(interface_image, (0, 0))

    for i, name in enumerate(names):
        text = font.render(name, True, text_color)
        text_rect = text.get_rect(center=(screen.get_width() // 2, text_start_y + i * text_spacing))
        screen.blit(text, text_rect)

    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if button_B.collidepoint((mx, my)):
                    return

        pygame.display.update()


def how_to_play(flag, color1_flag=None, color2_flag=None):
    """
       Displays the instructions for how to play and also handles input.

       Parameters:
       - flag (int): Flag indicating the game mode (1 or 2).
       - color1_flag (optional, str): Flag indicating the color selected for player 1.
       - color2_flag (optional, str): Flag indicating the color selected for player 2.
    """

    interface_image = pygame.image.load("Images/power_up_rework.png")
    interface_image = pygame.transform.scale(interface_image, (1000, 720))

    button_B = pygame.Rect(15, 15, 50, 50)
    button_I = pygame.Rect(830, 550, 100, 100)
    back_button_rect = pygame.Rect(13, 19, 65 - 13, 72 - 19)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if button_I.collidepoint((mx, my)):
                    if flag == 1:
                        select_gamemode(color1_flag, color2_flag)
                    elif flag == 2:
                        multi_player(color1_flag, color2_flag)
                if back_button_rect.collidepoint((mx, my)):
                    game()

        screen.blit(interface_image, (0, 0))

        pygame.display.update()


def info():
    interface_image = pygame.image.load("Images/C_menu_01.png")
    interface_image = pygame.transform.scale(interface_image, (1000, 720))

    button_B = pygame.Rect(15, 15, 50, 50)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if button_B.collidepoint((mx, my)):
                    interface()

        screen.blit(interface_image, (0, 0))
        pygame.display.update()


def game(color1_flag=None, color2_flag=None):
    interface_image = pygame.image.load("Images/G_menu_01.png")
    interface_image = pygame.transform.scale(interface_image, (1000, 720))

    button_S = pygame.Rect(267, 282, 466, 91)
    button_M = pygame.Rect(267, 413, 466, 91)

    button_B = pygame.Rect(15, 15, 50, 50)
    button_I = pygame.Rect(936, 15, 50, 50)

    print(f"color1_flag: {color1_flag}")
    print(f"color2_flag: {color2_flag}")

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if button_M.collidepoint((mx, my)):
                    how_to_play(2, color1_flag, color2_flag)

                if button_S.collidepoint((mx, my)):
                    how_to_play(1, color1_flag, color2_flag)

                if button_I.collidepoint((mx, my)):
                    info()

                if button_B.collidepoint((mx, my)):
                    interface()

        screen.blit(interface_image, (0, 0))

        pygame.display.update()


def select_difficulty(color1_flag=None, color2_flag=None):
    """
        Display the difficulty selection menu interface and inputs.
        3 Diffucultly levels -  easiest > hardest.
    """
    interface_image = pygame.image.load("Images/Difficulty.jpg")
    interface_image = pygame.transform.scale(interface_image, (1000, 720))

    easy_button_rect = pygame.Rect(74, 336, 225, 84)
    normal_button_rect = pygame.Rect(385, 336, 223, 85)
    hard_button_rect = pygame.Rect(693, 338, 226, 83)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if easy_button_rect.collidepoint((mx, my)):
                    print("Easy")
                    car_racing(1, color1_flag, color2_flag)

                elif normal_button_rect.collidepoint((mx, my)):
                    print("Normal")
                    car_racing(2, color1_flag, color2_flag)

                elif hard_button_rect.collidepoint((mx, my)):
                    print("Hard")
                    car_racing(3, color1_flag, color2_flag)

        screen.blit(interface_image, (0, 0))

        pygame.display.update()


def select_gamemode(color1_flag=None, color2_flag=None):
    interface_image = pygame.image.load("Images/Gamemode.jpg")
    interface_image = pygame.transform.scale(interface_image, (1000, 720))

    normal_button_rect = pygame.Rect(125, 335, 264, 100)
    special_button_rect = pygame.Rect(612, 338, 262, 96)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if normal_button_rect.collidepoint((mx, my)):
                    select_difficulty(color1_flag, color2_flag)
                if special_button_rect.collidepoint((mx, my)):
                    special_game_mode(color1_flag, color2_flag)

        screen.blit(interface_image, (0, 0))

        pygame.display.update()
