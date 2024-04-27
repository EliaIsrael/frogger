import time
from object import *
from pygame.locals import *

# Sounds
hop = "music/hop.wav"
death = "music/doom.wav"
plunk = "music/plunk.wav"
extra = "music/extra.wav"

"""------------------------------------------------------------------------------------------------------------------
Plays music
"""


def play_music():
    # Load background music
    sound1 = pygame.mixer.Sound("music/music.mp3")  # add sound
    sound1.set_volume(0.2) # lower the volume
    music_channel = pygame.mixer.Channel(0) # create channel
    music_channel.play(sound1, loops=-1)


"""------------------------------------------------------------------------------------------------------------------
Plays sound
"""


def play_sound(sound):
    # Initialize Pygame mixer for sound
    pygame.mixer.init()
    # Load background music
    sound = pygame.mixer.Sound(sound)
    sound.set_volume(1.0)
    music_channel = pygame.mixer.Channel(1)
    music_channel.play(sound)


"""------------------------------------------------------------------------------------------------------------------
Plays celebration sound
"""


def play_celebration(sound):
    # Initialize Pygame mixer for sound
    pygame.mixer.init()
    # Load background music
    sound = pygame.mixer.Sound(sound)
    sound.set_volume(1.0)
    music_channel = pygame.mixer.Channel(2)
    music_channel.play(sound)


"""------------------------------------------------------------------------------------------------------------------
Quits pygame
"""


def cleanup():
    pygame.quit()
    quit()


"""------------------------------------------------------------------------------------------------------------------
Load highest ever score
"""


def load_high_score():
    try:
        with open("text/high_score.txt", "r") as file:
            score = int(file.read())
    except FileNotFoundError:
        # Create the file with initial high score of 0
        score = 0
        with open("text/high_score.txt", "w") as file:
            file.write(str(score))
    return score


class Game:
    def __init__(self):
        self.window_width = 900 # screen width
        self.window_height = 1000# screen height
        self.fps = 40 # fps(speed)
        self.running = True # flag for weather the game is/ should run or not
        self.display_surf = None # game display
        self.clock = None # game clock
        self.grid = 74 # game grid
        self.frog = None # game frog
        self.cars = [] # array of cars
        self.logs = [] # array of logs
        self.lives = 5 # number of lives
        self.houses = [False, False, False, False, False] # array of occupied houses (start none)
        self.score = 0 # users score

        self.restart = True # flag who checks weather it is a brand-new game
        self.muted = False # flag to check weather the music is muted
        self.scoreMulti = 1 # multiplier for the score (gets higher as the game goes on)
        self.highest_score = load_high_score() # highest ever score

    """
------------------------------------------------------------------------------------------------------------------------
    Initializes the game, sets up the display, and adds initial game objects.
"""
    def init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode([self.window_width, self.window_height], pygame.HWSURFACE)
        self.running = True
        self.clock = pygame.time.Clock()

        self.reset()
        # self.frog = Frog(self.window_height/2 - self.grid, self.window_height - 8 * self.grid, self.grid)

        self.add_objects()

    """
------------------------------------------------------------------------------------------------------------------------
    Adds cars and logs to the game based on predefined positions and attributes.
"""
    def add_objects(self):
        for i in range(3):  # LINE 1
            self.cars.append(
                Car(i * 500 + 200, self.window_height - 2.2 * self.grid, self.grid * 2 - 25, self.grid, 1.5))
        for i in range(3):  # LINE 2
            self.cars.append(
                Car(i * 320 + 300, self.window_height - 3.4 * self.grid, self.grid * 2 - 25, self.grid, 2.4))
        for i in range(2):  # LINE 3
            self.cars.append(
                Car(i * 400 + 450, self.window_height - 4.6 * self.grid, self.grid * 2 - 25, self.grid, -3.2))
        for i in range(3):  # LINE 4
            self.cars.append(
                Car(i * 260 + 150, self.window_height - 5.8 * self.grid, self.grid * 2 - 25, self.grid, -2))

        for i in range(2):  # LINE 5
            self.logs.append(Log(i * 380 + 20, self.window_height - 8.2 * self.grid, 240, self.grid, -2))
        for i in range(2):  # LINE 6
            self.logs.append(Log(i * 360 + 50, self.window_height - 9.4 * self.grid, 240, self.grid, 2.4))
        for i in range(2):  # LINE 7
            self.logs.append(Log(i * 600 + 200, self.window_height - 10.6 * self.grid, 240, self.grid, -2.4))
        for i in range(2):  # LINE 8
            self.logs.append(Log(i * 600 + 0, self.window_height - 11.8 * self.grid, 240, self.grid, 4))

    """
------------------------------------------------------------------------------------------------------------------------
    Resets the game state, handles frog's collision with cars and logs,
    updates the score, and resets the frog's position.
"""
    def reset(self):
        if self.frog is not None:
            if not self.house() and not self.restart:
                self.draw()
                self.lives -= 1

                self.display_skull(self.frog.x, self.frog.y)

            else:
                play_celebration(extra)
                self.update_score()

        self.frog = Frog(self.window_height / 2 - self.grid, self.window_height * self.grid,
                         self.grid - 20)  # resets the frog to the bottom of the screen
        self.frog.attach(None)

    """
------------------------------------------------------------------------------------------------------------------------
    Handles game events such as keyboard inputs, mouse clicks, and window close events.
"""
    def event(self, event):
        if event.type == QUIT:
            self.running = False

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.running = False

        if event.type == KEYDOWN and event.key == K_LEFT:
            self.frog.move(-0.8, 0, self.grid)
            play_sound(hop)
        if event.type == KEYDOWN and event.key == K_RIGHT:
            self.frog.move(0.8, 0, self.grid)
            play_sound(hop)
        if event.type == KEYDOWN and event.key == K_UP:
            self.frog.move(0, -1.2, self.grid)
            play_sound(hop)
        if event.type == KEYDOWN and event.key == K_DOWN:
            self.frog.move(0, 1.2, self.grid)
            play_sound(hop)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            self.mute_music(x, y)

        """
------------------------------------------------------------------------------------------------------------------------
    Mutes or unmutes the game music based on the mute button click position.
"""
    def mute_music(self, x, y):
        if self.window_width - 80 <= x <= self.window_width - 20 and self.window_height - 60 <= y <= self.window_height:
            if self.muted:
                pygame.mixer.Channel(0).unpause()
                pygame.mixer.Channel(1).unpause()
            else:
                pygame.mixer.Channel(0).pause()
                pygame.mixer.Channel(1).pause()
            self.muted = not self.muted

    """
------------------------------------------------------------------------------------------------------------------------
    Updates the game state, checks for collisions, updates car and log positions,
    and updates the frog's position and attachment status.
"""
    def update(self):
        if self.lives == 0:
            self.running = self.handle_game_over()  # End game if no lives left
        for car in self.cars:
            car.update(self.window_width)
            if self.frog.intersects(car):
                play_sound(death)
                self.reset()
        for log in self.logs:
            log.update(self.window_width)
        if self.window_height - self.grid * 8 > self.frog.y > self.window_height - self.grid * 13:
            attached = False
            for log in self.logs:
                if self.frog.intersects(log):
                    attached = True
                    self.frog.attach(log)
            if not attached:
                play_celebration(plunk)
                self.reset()
        else:
            self.frog.attach(None)
        self.frog.update(self.window_width, self.window_height)

    """
------------------------------------------------------------------------------------------------------------------------
    Checks if the frog reaches a house and updates the house status.
"""
    def house(self):
        for i in range(len(self.houses)):
            y = self.window_height - 12 * self.grid
            x1 = 2 * i * 92
            x2 = x1 + 92

            if self.frog.y < y and (x1 < self.frog.x < x2):
                if not self.houses[i]:
                    self.houses[i] = True
                    return True

        return False

    """
------------------------------------------------------------------------------------------------------------------------
    Displays the mute/unmute button on the screen based on the mute state.
"""
    def display_mute(self):

        image = pygame.image.load("photos/unmute.png")
        if self.muted:
            image = pygame.image.load("photos/mute.png")
        image = pygame.transform.scale(image, (60, 60))
        self.display_surf.blit(image, (self.window_width - 70, self.window_height - 60))

    """
------------------------------------------------------------------------------------------------------------------------
    Displays the game background image on the screen.
"""
    def display_background(self):
        background_image = pygame.image.load("photos/frogger_background.png")
        background_image = pygame.transform.scale(background_image, (self.window_width, self.window_height))
        # Blit the background image to the screen
        self.display_surf.blit(background_image, (0, 0))

    """
------------------------------------------------------------------------------------------------------------------------
    Draws all cars on the screen.
"""
    def display_cars(self):
        for car in self.cars:
            car.draw(self.display_surf)

    """
------------------------------------------------------------------------------------------------------------------------
    Draws all logs on the screen.
"""
    def display_logs(self):
        for log in self.logs:
            log.draw(self.display_surf)

    """
------------------------------------------------------------------------------------------------------------------------
    Displays the remaining lives (hearts) on the screen.
"""
    def display_hearts(self):
        heart_image = pygame.image.load("photos/heart.png")  # Load heart image
        heart_width, heart_height = heart_image.get_size()  # Get heart image size
        heart_spacing = 10  # Spacing between hearts

        for i in range(self.lives):
            x = heart_spacing + i * (heart_width + heart_spacing)
            y = self.window_height - heart_height  # Position hearts at bottom left
            self.display_surf.blit(heart_image, (x, y))

    """
------------------------------------------------------------------------------------------------------------------------
    Displays the current score text on the screen.
"""
    def display_text(self):
        # Draw score text

        # Load the pixel font
        font_path = "text/pixel.ttf"  # Replace with your font file path
        font = pygame.font.Font(font_path, 100)  # Adjust font size as needed

        score_text = f"{self.score}"  # Format the score string
        score_text_surface = font.render(score_text, True, (57, 255, 20))  # Render text
        text_width, text_height = score_text_surface.get_size()  # Get text dimensions
        x = 10  # Position text at bottom right with padding
        y = self.window_height / 2 + 72 - text_height
        self.display_surf.blit(score_text_surface, (x, y))

    """
------------------------------------------------------------------------------------------------------------------------
       Displays the highest ever score on the screen.
"""

    def display_highest_score(self):

        font_path = "text/pixel.ttf"  # Replace with your font file path
        font = pygame.font.Font(font_path, 60)  # Adjust font size as needed
        if self.score > self.highest_score:
            self.highest_score = self.score
        score_text = f"HI-SCORE: {self.highest_score}"  # Format the score string
        score_text_surface = font.render(score_text, True, (255, 255, 255))  # Render text
        text_width, text_height = score_text_surface.get_size()  # Get text dimensions
        x = self.window_width - text_width  # Position text at bottom right with padding
        y = self.window_height / 2 + 72 - text_height
        self.display_surf.blit(score_text_surface, (x, y))

    """
------------------------------------------------------------------------------------------------------------------------
    Displays a skull image at the specified position for a short duration.
"""
    def display_skull(self, x, y):
        # Load skull image
        skull_image = pygame.image.load("photos/skull.png")

        # Display skull for 3 seconds
        start_time = time.time()  # Get start time using the imported time module
        self.frog = Frog(self.window_height / 2 - self.grid, self.window_height - 1 * self.grid,
                         self.grid - 20)  # resets the frog to the bottom of the screen
        self.display_surf.blit(skull_image, (x, y))

        pygame.display.flip()
        self.update()

        while time.time() - start_time < 1:
            self.display_surf.blit(skull_image, (x, y))

            pygame.display.flip()

    """
------------------------------------------------------------------------------------------------------------------------
    Draws all game elements on the screen.
"""
    def draw(self):

        self.display_background()
        self.display_cars()
        self.display_logs()
        self.display_text()
        self.display_hearts()
        self.display_highest_score()
        self.display_houses(self.houses)
        self.display_mute()
        self.frog.draw(self.display_surf)
        pygame.display.flip()

    """
------------------------------------------------------------------------------------------------------------------------
    Updates the player's score based on captured houses and multipliers.
"""
    def update_score(self):
        all_houses = 0
        for i in range(len(self.houses)):

            if self.houses[i]:
                all_houses += 1
                self.score += 250*self.scoreMulti
                self.update_high_score()
        if all_houses == 5:
            self.score += 2250*self.scoreMulti
            self.houses = [False, False, False, False, False]
            self.scoreMulti *= 3
            self.fps *= 2

    """
------------------------------------------------------------------------------------------------------------------------
    Draws the houses on the screen based on the provided houses list.
    """
    def display_houses(self, houses):
        house_image = pygame.image.load("photos/house.png")
        house_width, house_height = house_image.get_size()

        for i in range(len(houses)):
            if houses[i]:  # Check if the current element is True
                x = 30 + i * (house_width + 125)
                y = self.window_height - house_height - 12 * self.grid
                self.display_surf.blit(house_image, (x, y))

    """
------------------------------------------------------------------------------------------------------------------------
    Handles the game over state by displaying game over text and handling user input.
    """
    def handle_game_over(self):
        font_path = "text/pixel.ttf"
        font = pygame.font.Font(font_path, 100)

        score_text = f"GAME OVER! "

        game_over_text_surface = font.render(score_text, True, (255, 0, 0))
        text_width, text_height = game_over_text_surface.get_size()
        x = self.window_width // 2 - text_width // 2
        y = self.window_height // 2 - text_height // 2 + 25
        self.display_surf.blit(game_over_text_surface, (x, y - 80))

        score_text = f"Again? (y/n) "
        game_over_text_surface2 = font.render(score_text, True, (255, 100, 100))
        self.display_surf.blit(game_over_text_surface2, (x, y))

        pygame.display.flip()

        # Wait for user input (Yes or No)
        while True:
            for event in pygame.event.get():
                pygame.mixer.music.stop()  # Stop the music before quitting
                self.update_high_score()
                if event.type == QUIT:
                    return False  # Exit the game if user exits
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        play_music()
                        self.restart = True
                        self.score = 0
                        self.lives = 5
                        self.fps = 40
                        self.houses = [False, False, False, False, False]
                        self.muted = False
                        self.scoreMulti = 1
                        self.reset()  # Reset the game if user presses 'y'
                        return True  # Continue the game loop
                    elif event.key == K_n:
                        return False  # Exit the game if user presses 'n'

    """
    ------------------------------------------------------------------------------------------------------------------------
        update the highest score after a users session
"""
    def update_high_score(self):
        if self.score >= self.highest_score:
            with open("text/high_score.txt", "w") as file:
                file.write(str(self.score))

    """
------------------------------------------------------------------------------------------------------------------------
    Main game loop that initializes the game, handles events, updates, and draws game elements.
"""
    def execute(self):

        if self.init() == False:
            self.running = False
        play_music()
        while self.running:
            load_high_score()
            self.restart = False
            for event in pygame.event.get():
                self.event(event)
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        cleanup()

    """
------------------------------------------------------------------------------------------------------------------------
Runs the game
"""


if __name__ == "__main__":
    gameApp = Game()
    gameApp.execute()
