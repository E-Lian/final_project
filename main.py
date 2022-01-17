# 1.play the hand animation

import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BGCOLOUR = BLACK
FPS = 30

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "Spider-Man: Going Home"

images = [
    "./images/hand1.png", "./images/hand2.png", "./images/hand3.png", "./images/hand4.png", "./images/hand5.png",
    "./images/hand6.png", "./images/hand7.png", "./images/hand8.png", "./images/hand9.png", "./images/hand10.png",
    "./images/hand11.png", "./images/hand12.png", "./images/hand13.png", "./images/hand14.png", "./images/hand15.png"
]


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        # Call the superclass constructor
        super().__init__()

        # Create the image of the block
        self.images = images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.index += 1


def main() -> None:
    """Driver of the Python script"""
    # Create the screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)

    # Create some local variables that describe the environment
    done = False
    clock = pygame.time.Clock()

    # sprite group
    all_sprites = pygame.sprite.Group()
    # create player and add to group
    player = Player()
    all_sprites.add(player)

    # ----------- MAIN LOOP
    while not done:
        # ----------- EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ----------- CHANGE ENVIRONMENT
        # update
        all_sprites.update()
        # ----------- DRAW THE ENVIRONMENT
        screen.fill(BGCOLOUR)  # fill with bgcolor

        # draw sprites
        all_sprites.draw(screen)

        # Update the screen
        pygame.display.flip()

        # ----------- CLOCK TICK
        clock.tick(FPS)


if __name__ == "__main__":
    main()
