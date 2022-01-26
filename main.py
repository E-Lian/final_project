# Spider-Man: Going Home (weird name, but I like it)

import random

import pygame

pygame.init()

FPS = 15
WAIT = 10
BOMB_WAIT = 5000

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "Spider-Man: Going Home"

# the background
bg = pygame.image.load("./images/background/sky.png")
bg = pygame.transform.scale(bg, (1920, 1080))

# a bunch of enemy images
GOBLIN = pygame.image.load("./images/green goblin/green goblin.png")
BOMB = pygame.image.load("./images/green goblin/bomb.png")
HIT = pygame.image.load("./images/green goblin/bomb_hit.png")

# I drew each frame in Photoshop first
# then edit the position of them in Premiere Pro so that it looks smoother
# lastly export each frame to images folder
# there are some files I drew in ./psd files/hand/
# also there is a gif of the animation
images = [
    pygame.image.load("./images/hand/hand1.png"), pygame.image.load("./images/hand/hand2.png"),
    pygame.image.load("./images/hand/hand3.png"),
    pygame.image.load("./images/hand/hand4.png"), pygame.image.load("./images/hand/hand5.png"),
    pygame.image.load("./images/hand/hand6.png"),
    pygame.image.load("./images/hand/hand7.png"), pygame.image.load("./images/hand/hand8.png"),
    pygame.image.load("./images/hand/hand9.png"),
    pygame.image.load("./images/hand/hand10.png"), pygame.image.load("./images/hand/hand11.png"),
    pygame.image.load("./images/hand/hand12.png"),
    pygame.image.load("./images/hand/hand13.png"), pygame.image.load("./images/hand/hand14.png"),
    pygame.image.load("./images/hand/hand15.png")
]

buildings = pygame.image.load("./images/background/bg buildings.png")


class Player(pygame.sprite.Sprite):
    """
    attributes:
        status: current status of the player
        start: the time player starts swinging
        images: each frame of the animation
        index: number of the current frame
        image: current image

    methods:
        swing: update self.image to play the animation
        TODO: shooting webs to bombs - draw webs, make it move, and change the bomb's image
    """

    def __init__(self) -> None:
        # Call the superclass constructor
        super().__init__()

        self.status = "falling"
        self.start = None
        # Create the image of the block
        self.images = images
        self.index = -1
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def swing(self) -> bool:
        """
        1.  when space bar is pressed,
            self.image will set to the 1st frame of the animation (see the event listener in main loop)
        2.  swing() will tell the loop if player is swinging,
            if not, swing() will return False,
            otherwise return True and update frame
        3. when swing() returns True, frame will be updated and animation will be drawn
        """
        if self.index >= len(self.images):
            # return False if player is not swinging or finish swinging
            # else return True and update the image
            self.status = "falling"
            return False
        self.image = self.images[self.index]
        self.index += 1
        now = pygame.time.get_ticks()
        if now - self.start >= WAIT:
            self.status = "swinging"
        return True


class Building(pygame.sprite.Sprite):
    """
    attributes:
        v: velocity of the building
        image: image of the building
        rect.x, rect.y: a random location

    methods:
        change_vel: change buildings' velocities
        update: move the building, change self.image and xy if it is out of the screen
    TODO: need to adjust the picture
    """

    def __init__(self, image) -> None:
        # call the superclass constructor
        super().__init__()

        self.v = 0
        # image
        self.image = image
        self.rect = self.image.get_rect()
        # assign random location
        self.rect.x, self.rect.y = 0, 0

    def change_vel(self, status: str):
        """change velocity as player press key bars"""
        if status == "falling":
            self.v = -10
        elif status == "swinging":
            self.v = 20

    def update(self, player: str):
        """
        buildings keep going down (y increases)

        attribute:
            player: a string that represents player's status for change_vel()
        """
        self.change_vel(player)
        self.rect.y += self.v
        # if the building is out of the screen
        # if self.rect.top > SCREEN_HEIGHT:
        #     self.rect.x, self.rect.y = (
        #         random.randrange(SCREEN_WIDTH),
        #         random.randrange(SCREEN_HEIGHT - self.rect.height, SCREEN_HEIGHT - 100)
        #     )


class Goblin(pygame.sprite.Sprite):
    """the green goblin
    attributes:
        x_vel: velocity in x-axis
        y_vel: velocity in y-axis
        image: image of the green goblin

    methods:
        update: update location and shoot bomb
        shoot_bomb: shoot a bomb
    """

    def __init__(self, x_vel, y_vel) -> None:
        # call the superclass constructor
        super().__init__()

        self.start = pygame.time.get_ticks()
        self.x_vel = x_vel
        self.y_vel = y_vel
        # load image
        self.image = pygame.transform.scale(GOBLIN, (700, 700))
        self.rect = self.image.get_rect()

    def shoot_bomb(self):
        # create a Bomb
        bomb = Bomb(self.rect.centerx, self.rect.centery)
        return bomb

    def update(self) -> None:
        # Update the x-coordinate
        self.rect.x += self.x_vel
        # If goblin is too far to the left
        if self.rect.x < 0:
            # Keep the object inside the canvas
            self.rect.x = 0
            # Set the velocity to the negative
            self.x_vel = -self.x_vel
        # If goblin is too far to the right
        if self.rect.x + self.rect.width > SCREEN_WIDTH:
            # Keep the object inside the canvas
            self.rect.x = SCREEN_WIDTH - self.rect.width
            # Set the velocity to the negative
            self.x_vel = -self.x_vel
        # If goblin is too far to the bottom
        if self.rect.y + self.rect.height > SCREEN_HEIGHT:
            # Keep the object inside the canvas
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            # Set the velocity to the negative
            self.y_vel = -self.y_vel
        # If goblin is too far to the bottom
        if self.rect.y < 0:
            # Keep the object inside the canvas
            self.rect.y = 0
            # Set the velocity to the negative
            self.y_vel = -self.y_vel

        # Update the y-coordinate
        self.rect.y += self.y_vel


class Bomb(pygame.sprite.Sprite):
    """green goblin's bomb
    attributes:
        width: width of  the sprite
        height: height of the sprite
    methods:
        update: update location and change image if needed
    TODO: make the bomb explosible
    """

    def __init__(self, x, y) -> None:
        # call superclass constructor
        super().__init__()

        self.hit = False
        self.size = 500
        # load image
        self.image = pygame.transform.scale(BOMB, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.width, self.height = self.rect.width, self.rect.height

    def update(self) -> None:
        self.size += 50
        self.image = pygame.transform.scale(self.image, (self.size, self.size))


def main() -> None:
    """Driver of the Python script"""
    # Create the screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)

    # Create some local variables that describe the environment
    done = False
    clock = pygame.time.Clock()

    # sprite group
    player_sprites = pygame.sprite.Group()
    # create player and add to group
    player = Player()
    player.start = pygame.time.get_ticks()
    player_sprites.add(player)

    # enemy sprite group
    enemy_sprites = pygame.sprite.Group()
    goblin = Goblin(random.randrange(-30, 30), random.randrange(-30, 30))
    enemy_sprites.add(goblin)

    # background group
    building_sprites = pygame.sprite.Group()
    # add building sprites in the group
    building_sprites.add(Building(buildings))

    # ----------- MAIN LOOP
    while not done:
        # ----------- EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # Listen for the space bar on keyboard
        # set player to first image
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player.index = 0
            player.start = pygame.time.get_ticks()

        # ----------- CHANGE ENVIRONMENT
        # update sprites
        building_sprites.update(player.status)
        enemy_sprites.update()
        # shoot bomb
        now = pygame.time.get_ticks()
        if now - goblin.start >= BOMB_WAIT:
            bomb = goblin.shoot_bomb()
            enemy_sprites.add(bomb)
            goblin.start = pygame.time.get_ticks()
        # ----------- DRAW THE ENVIRONMENT
        screen.blit(bg, (0, 0))  # draw background

        # draw sprites
        # draw buildings
        building_sprites.draw(screen)
        # draw enemies
        enemy_sprites.draw(screen)

        # if player is swinging, draw
        if player.swing():
            player_sprites.draw(screen)

        # Update the screen
        pygame.display.flip()

        # ----------- CLOCK TICK
        clock.tick(FPS)


if __name__ == "__main__":
    main()
