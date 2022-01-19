# Spider-Man: Going Home (weird name, but I like it)
# TODO: figure out how to make spider-man move according to his action

import random

import pygame

pygame.init()

BLACK = (0, 0, 0)
BG_COLOR = BLACK
FPS = 15

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "Spider-Man: Going Home"
bg = pygame.image.load("./images/background/sky.png")

bg = pygame.transform.scale(bg, (1920, 1080))

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

buildings = [
    pygame.image.load("./images/background/building1.png"), pygame.image.load("./images/background/building2.png"),
    pygame.image.load("./images/background/building3.png")
]


class Player(pygame.sprite.Sprite):
    """
    attributes:
        images: each frame of the animation
        index: number of the current frame
        image: current image

    methods:
        swing: update self.image to play the animation
    """

    def __init__(self) -> None:
        # Call the superclass constructor
        super().__init__()

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
        3. when swing() returns True, animation will be drawn
        """
        if self.index >= len(self.images):
            # return False if player is not swinging or finish swinging
            # else return True and update the image
            return False
        self.image = self.images[self.index]
        self.index += 1
        return True


class Building(pygame.sprite.Sprite):
    """
    attributes:
        v: velocity of the building
        image: image of the building
        rect.x, rect.y: a random location

    methods:
        update: move the building, change self.image and xy if it is out of the screen
    """

    def __init__(self, image) -> None:
        # call the superclass constructor
        super().__init__()

        self.v = 10
        self.index = -1
        # image
        self.image = image
        self.rect = self.image.get_rect()
        # assign random location
        self.rect.x, self.rect.y = (
            random.randrange(SCREEN_WIDTH),
            random.randrange(600, SCREEN_HEIGHT - 100)
        )

    def update(self):
        """
        buildings keep going down (y increases)
        if buildings are out of screen, then change self.image to a random building
        and appear after 1 - 3 seconds at another random location
        """
        self.rect.y += self.v
        # if the building is out of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.index = random.randrange(len(buildings))
            self.image = buildings[self.index]
            self.rect.x, self.rect.y = (
                random.randrange(SCREEN_WIDTH),
                random.randrange(600, SCREEN_HEIGHT - 100)
            )


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
    player_sprites.add(player)

    # background group
    building_sprites = pygame.sprite.Group()
    # add building sprites in the group
    for building in buildings:
        b = Building(building)
        building_sprites.add(b)

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

        # ----------- CHANGE ENVIRONMENT
        # update the buildings' locations
        building_sprites.update()
        # ----------- DRAW THE ENVIRONMENT
        screen.blit(bg, (0, 0))  # draw background

        # draw sprites
        # draw buildings
        building_sprites.draw(screen)

        # if player is swinging, draw
        if player.swing():
            player_sprites.draw(screen)

        # Update the screen
        pygame.display.flip()

        # ----------- CLOCK TICK
        clock.tick(FPS)


if __name__ == "__main__":
    main()
