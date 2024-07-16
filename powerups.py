from abc import ABC, abstractmethod
import pygame

WHITE = (255, 255, 255)


# Define a base class for PowerUp using ABC (Abstract Base Class)
class PowerUp(ABC, pygame.sprite.Sprite):
    """
            Initialize a PowerUp object.

            Args:
                color (tuple): RGB tuple representing the color of the power-up.
                width (int): Width of the power-up.
                height (int): Height of the power-up.
                speed (int): Speed of the power-up.
                image (str): Image path for the power-up.
    """
    def __init__(self, color, width, height, speed, image=None):
        super().__init__()
        if image is None:
            # If no image is provided, create a rectangle with the specified color
            self.image = pygame.Surface([width, height])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
            self.width = width
            self.height = height
            self.color = color
            pygame.draw.rect(self.image, color, [0, 0, width, height])
        else:
            self.image = pygame.image.load(image)
            self.width = width
            self.height = height
            self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.speed = speed

    def moveBackward(self, player_car_speed):
        pixels = self.speed + player_car_speed
        self.rect.y += pixels

    def apply_power_up_1(self, player):
        player.activate_invincibility(duration=300)

    def apply_power_up_2(self, player):
        player.activate_double(duration=300)

    def apply_power_up_3(self, player):
        player.activate_small(duration=300)

    def apply_power_up_4(self, player):
        player.activate_slowdown(duration=300)


class InvincibilityPowerUp(PowerUp):
    def affect_player(self, player):
        player.activate_invincibility(duration=300)

    def affect_traffic(self, traffic):
        pass


class DoublePowerUp(PowerUp):
    def affect_player(self, player):
        player.activate_double(duration=300)

    def affect_traffic(self, traffic):
        pass


class SmallPowerUp(PowerUp):
    def affect_player(self, player):
        player.activate_small(duration=300)

    def affect_traffic(self, traffic):
        pass


class SlowdownPowerUp(PowerUp):
    def affect_player(self, player):
        pass

    def affect_traffic(self, traffic):
        traffic.activate_slowdown(duration=300)
