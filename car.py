import pygame

WHITE = (255, 255, 255)

# Define a class for the car using pygame sprite
class Car(pygame.sprite.Sprite):
    """
              Initialize the car object.

              Args:
                  color (tuple): RGB tuple representing the color of the car.
                  width (int): Width of the car.
                  height (int): Height of the car.
                  speed (int): Initial speed of the car.
                  image (str): Path to the image file for the car (default is "crash.png").
    """
    def __init__(self, color, width, height, speed=0, image="crash.png"):
        super().__init__()

        # Initialize power-up states
        self.invincible = False
        self.small = False
        self.double = False
        self.slowdown = False

        self.original_width = width
        self.original_height = height
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

        # Load and store the original image
        if image is not None:
            self.original_image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (width, height))
        else:
            # If no image is provided, create a rectangle with the specified color
            self.image = pygame.Surface([width, height])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
            pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()
        self.speed = speed
        self.color = color

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveForward(self, speed):
        self.rect.y -= speed

    def moveBackward(self, player_car_speed):
        pixels = self.speed + player_car_speed
        self.rect.y += pixels

    def changeSpeed(self, new_speed):
        self.speed = new_speed

    def repaint(self, color):
        self.color = color

    def resize(self, width, height):

        """
                Resize the car to the specified width and height.

                Args:
                    width (int): The new width of the car.
                    height (int): The new height of the car.
        """
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.original_image, (width, height))

        # Update the rect size and preserve the current position
        current_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = current_center

    def reimage(self, image_path):
        """
        Replace the car's image with a new image, updating the original image as well.
        """
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))

    def activate_invincibility(self, duration):
        self.invincible = True
        self.invincibility_duration = duration

    def update_invincibility(self):
        #Manages invisibility powerup duration and removes it once it has expired
        if self.invincible:
            self.invincibility_duration -= 1
            if self.invincibility_duration <= 0:
                self.invincible = False
                self.invincibility_duration = 300

    def activate_double(self, duration):

        """
               Activate double points power-up for the specified duration.

               Args:
                   duration (int): The duration (seconds) for which the double power-up will be active.
        """
        self.double = True
        self.double_duration = duration

    def update_double(self):
        #Manage the double power-up duration (seconds) and deactivate if it expires.
        if self.double:
            self.double_duration -= 1
            if self.double_duration <= 0:
                self.double = False
                self.double_duration = 300

    def activate_small(self, duration):
        self.small = True
        self.small_duration = duration

    def update_small(self):
        if self.small:
            self.small_duration -= 1
            if self.small_duration <= 0:
                self.small = False
                self.small_duration = 300

    def activate_slowdown(self, duration):
        self.slowdown = True
        self.slowdown_duration = duration

    def update_slowdown(self):
        if self.slowdown:
            self.slowdown_duration -= 1
            if self.slowdown_duration <= 0:
                self.slowdown = False
                self.slowdown_duration = 300

    def adjust_enemy_speed(self, speed_change):
        """
        Adjust the speed of the enemy cars.

        Args:
            speed_change (float): The amount to adjust the speed of the enemy cars.
        """
        self.speed += speed_change
        if self.speed < 0.001:
            self.speed = 0.001
