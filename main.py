# 1.play the hand animation

import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BGCOLOUR = BLACK
FPS = 15

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "Spider-Man: Going Home"
bg = pygame.image.load("./images/background/sky.png")


# I drew each image in Photoshop first
# then edit the position of them in Premiere Pro and export each frame to images folder
# there are psd and png files of the images I drew in ./some files/hand/
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


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        # Call the superclass constructor
        super().__init__()

        # Create the image of the block
        self.images = images
        self.index = -1
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def swing(self) -> bool:
        if self.index >= len(self.images):
            # return False if player is not swinging
            # else return True and update the image
            return False
        self.image = self.images[self.index]
        self.index += 1
        return True


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

        # ----------- DRAW THE ENVIRONMENT
        screen.blit(bg, (0, 0))  # fill with bgcolor

        # draw sprites
        # if player is swinging, draw
        if player.swing():
            player_sprites.draw(screen)

        # Update the screen
        pygame.display.flip()

        # ----------- CLOCK TICK
        clock.tick(FPS)


if __name__ == "__main__":
    main()
