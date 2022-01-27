# Spider-Man: Going Home (weird name that has no connection to the gameplay, but I like it)

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

# Images
# game
bg = pygame.image.load("./images/background/sky.png")
bg = pygame.transform.scale(bg, (1920, 1080))
buildings = pygame.image.load("./images/background/bg buildings.png")
over = pygame.image.load("./images/game over.png")
gravity = pygame.image.load("./images/gravity.png")

# a bunch of enemy images
GOBLIN = pygame.image.load("./images/green goblin/green goblin.png")
BOMB = pygame.image.load("./images/green goblin/bomb.png")
HIT = pygame.image.load("./images/green goblin/bomb_hit.png")
EXPLODE = pygame.image.load("./images/green goblin/explode.png")

# Spider-Man's images
# I drew each frame in Photoshop first
# then edit the position of them in Premiere Pro so that it looks smoother
# lastly export each frame to images folder
# there are psd files I drew in ./psd files/hand/
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
shoot = pygame.image.load("./images/hand/shooting.png")
WEB = pygame.image.load("./images/web.png")

# hp
hearts = [
    pygame.image.load("./images/heart/heart1.png"), pygame.image.load("./images/heart/heart2.png"),
    pygame.image.load("./images/heart/heart3.png"), pygame.image.load("./images/heart/heart4.png")
]
for i in range(len(hearts)):
    hearts[i] = pygame.transform.scale(hearts[i], (100, 100))


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

    methods:
        change_vel: change buildings' velocities
        update: move the building, change self.image and xy if it is out of the screen
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


class Goblin(pygame.sprite.Sprite):
    """the green goblin
    attributes:
        start: the time when a bomb is shot
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

    def shoot_bomb(self):
        # create a Bomb
        bomb = Bomb(self.rect.centerx, self.rect.centery)
        return bomb


class Bomb(pygame.sprite.Sprite):
    """green goblin's bomb
    attributes:
        hit: if the bomb is hit
        size: size of the bomb
        width: width of  the sprite
        height: height of the sprite
    methods:
        update: update location and change image if needed
    """

    def __init__(self, x, y) -> None:
        # call superclass constructor
        super().__init__()

        self.hit = False
        self.size = 300
        # load image
        self.image = pygame.transform.scale(BOMB, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.width, self.height = self.rect.width, self.rect.height

    def update(self) -> None:
        # if the bomb explode
        if self.size >= 2000:
            self.image = EXPLODE
        elif self.hit:
            self.rect.y += 500
        else:
            self.size += 50
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.rect.x -= 60
            self.rect.y -= 60

        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()


class Hand(pygame.sprite.Sprite):
    """shooting hand
    attributes:
        shooting: True when player is press S key
        start: the time when player press S key
    methods:
        shoot: tell the loop is player is shooting
    """

    def __init__(self):
        # call super class constructor
        super().__init__()

        # other attributes
        self.image = shoot
        self.rect = self.image.get_rect()
        self.shooting = False
        self.make_web = False
        self.start = None

    def shoot(self) -> bool:
        now = pygame.time.get_ticks()
        if now - self.start >= 100:
            self.shooting = False
            self.make_web = True
            return False
        else:
            self.make_web = False

        if self.shooting:
            return True
        return True


class Web(pygame.sprite.Sprite):
    """Spider-Man's web
    attributes:
        x_vel: velocity on x-axis
        y_vel: velocity on y-axis
    methods:
        update: move the web, if it is out of screen, kill it
    """

    def __init__(self):
        # call super class constructor
        super().__init__()

        # other attributes
        self.image = WEB
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 1300, 550
        self.x_vel = -100
        self.y_vel = -100

    def update(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        if self.rect.top <= -300:
            self.kill()


def main() -> None:
    """Driver of the Python script"""
    # Create the screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)

    # Create some local variables that describe the environment
    done = False
    clock = pygame.time.Clock()

    # game status
    status = "ongoing"
    hp = 3

    # sprite groups
    # player sprite group
    player_sprites = pygame.sprite.Group()
    # create player and add to group
    player = Player()
    player.start = pygame.time.get_ticks()
    player_sprites.add(player)

    # hand groups
    hand_sprites = pygame.sprite.Group()
    hand = Hand()
    hand.start = pygame.time.get_ticks()
    hand_sprites.add(hand)

    # enemy sprite group
    enemy_sprites = pygame.sprite.Group()
    goblin = Goblin(random.randrange(-30, 30), random.randrange(-30, 30))
    enemy_sprites.add(goblin)

    # bomb sprite group
    bomb_sprites = pygame.sprite.Group()

    # background group
    building_sprites = pygame.sprite.Group()
    # add building sprites in the group
    building = Building(buildings)
    building_sprites.add(building)

    # web sprite group
    web_sprites = pygame.sprite.Group()

    # ----------- MAIN LOOP
    while not done:
        # ----------- EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # Listen for the space bar on keyboard
        # set player to first image
        if pygame.key.get_pressed()[pygame.K_SPACE] and status != "end":
            player.index = 0
            player.start = pygame.time.get_ticks()

        # listen for s key on keyboard
        if pygame.key.get_pressed()[pygame.K_s] and status != "end":
            # change hand.shooting and set start time
            hand.shooting = True
            hand.start = pygame.time.get_ticks()
            # shoot web
            if hand.make_web:
                web = Web()
                web_sprites.add(web)

        # ----------- CHANGE ENVIRONMENT
        if status == "ongoing":
            # update sprites
            building_sprites.update(player.status)
            enemy_sprites.update()
            bomb_sprites.update()
            web_sprites.update()

            # goblin shoot bomb
            now = pygame.time.get_ticks()
            if now - goblin.start >= BOMB_WAIT:
                bomb = goblin.shoot_bomb()
                bomb_sprites.add(bomb)
                goblin.start = pygame.time.get_ticks()

        # if the bomb explode
        for bomb in bomb_sprites:
            if bomb.image == EXPLODE:
                hp -= 1
                break
        if hp == 0:
            status = "end"
        # if spider-man hits the ground
        if building.rect.bottom <= SCREEN_HEIGHT:
            status = "fall"

        # bomb hit
        for bomb in bomb_sprites:
            webs_hit = pygame.sprite.spritecollide(bomb, web_sprites, True)
            if webs_hit:
                bomb.hit = True
                bomb.image = HIT

        # ----------- DRAW THE ENVIRONMENT
        screen.blit(bg, (0, 0))  # draw background

        # draw sprites
        # draw buildings
        building_sprites.draw(screen)
        # draw enemies
        enemy_sprites.draw(screen)

        # draw bombs
        bomb_sprites.draw(screen)

        # if player is swinging, draw
        if player.swing():
            player_sprites.draw(screen)

        # if game has ended, draw
        if status == "end":
            screen.blit(over, (0, 0))

        if status == "fall":
            screen.blit(gravity, (0, 0))

        # if spider-man is shooting webs
        if hand.shoot():
            hand_sprites.draw(screen)
            web_sprites.draw(screen)

        if hp == 3:
            screen.blit(hearts[0], (1800, 20))
        elif hp == 2:
            screen.blit(hearts[1], (1800, 20))
        elif hp == 1:
            screen.blit(hearts[2], (1800, 20))
        else:
            screen.blit(hearts[3], (1800, 20))
        # Update the screen
        pygame.display.flip()

        # ----------- CLOCK TICK
        clock.tick(FPS)


if __name__ == "__main__":
    main()
