import arcade
import random
import os
import json
from typing import List, Dict

# dimensions of the screen
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# variables for the character animation
CHARACTER_SCALING = 0.4
MOVEMENT_SPEED = 5
FRAME_RATE = 7

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1
Gravity = 2


class State():
    '''
    First class State() to create different game status of the player
    '''
    MAIN_MENU = 0
    PLAYING = 1
    GAME_OVER = 2

# List of different background images that are chosen randomly by the random
# function

background = ["Objects" + os.sep + "sprites" + os.sep + "officebackground.jpg"]
platform = "Objects" + os.sep + "sprites" + os.sep + "platform2.png"
player = "Objects" + os.sep + "sprites" + os.sep + "officeguy.png"
enemy = "Objects" + os.sep + "sprites" + os.sep + "obstacle.png"
# Start screen and game over images
play = "Objects" + os.sep + "sprites" + os.sep + "play.png"
ready = "Objects" + os.sep + "sprites" + os.sep + "presspace.png"
ready_message = "Objects" + os.sep + "sprites" + os.sep + "Readymessage.png"
volume = "Objects" + os.sep + "sprites" + os.sep + "soundup.png"
highscore = "Objects" + os.sep + "sprites" + os.sep + "highscore.png"
gameover = "Objects" + os.sep + "sprites" + os.sep + "gameover2.png"

# Images for the different numbers used in scoring
SCORE = {
    '0': 'Objects' + os.sep + 'sprites' + os.sep + '0.png',
    '1': 'Objects' + os.sep + 'sprites' + os.sep + '1.png',
    '2': 'Objects' + os.sep + 'sprites' + os.sep + '2.png',
    '3': 'Objects' + os.sep + 'sprites' + os.sep + '3.png',
    '4': 'Objects' + os.sep + 'sprites' + os.sep + '4.png',
    '5': 'Objects' + os.sep + 'sprites' + os.sep + '5.png',
    '6': 'Objects' + os.sep + 'sprites' + os.sep + '6.png',
    '7': 'Objects' + os.sep + 'sprites' + os.sep + '7.png',
    '8': 'Objects' + os.sep + 'sprites' + os.sep + '8.png',
    '9': 'Objects' + os.sep + 'sprites' + os.sep + '9.png', }


def bubblesort(numbers: List[int]) -> List[int]:
    n = len(numbers)

    for i in range(n):
        for j in range(n - i - 1):
            if numbers[j] < numbers[j + 1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]

    return numbers

def binary_search(lst: List[int], target: int) -> int:
    start = 0
    end = len(lst) -1

    while start < end:
        mid = (start + end)//2
        
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            end = mid - 1
        else:
            start = mid + 1

    return -1

def load_texture_pair(filename: str) -> "SpriteList":
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename, scale=CHARACTER_SCALING),
        arcade.load_texture(filename, scale=CHARACTER_SCALING, mirrored=True)]


class PlayerCharacter(arcade.Sprite):
    """ Class PlayerCharacter

        Attrs:
            character_face_directio (int): face direction of the character 
            defaulted to right facing
            vel (int): The player's velocity
            dead (bool): Boolean statement used to track the player's state
            gravity_on (bool): Boolean statement to activate gravity
            walk_textures (List[sprites]): List of different walking textures 
            for animations
            jump_texture (sprite): Player character jumping texture
    """

    def __init__(self) -> None:
        """Creates a player character object"""

        # Set up parent class
        super().__init__()

        # Default to face-right
        self._character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self._cur_texture = 0
        self._vel = 0
        self._dead = False
        self._gravity_on = False

        # Track out state
        main_path = ":resources:images/animated_characters/male_person/malePerson"
        # Load textures for idle standing
        self._idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        # Load textures for walking
        self._walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self._walk_textures.append(texture)

        self._jump_texture = load_texture_pair(f"{main_path}_jump.png")

    def update_animation(self, delta_time: float = 1/60) -> None:
        """Updates the animation of the player
        Args: 
            delta_time (float): speed of the animation
        """

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self._character_face_direction == RIGHT_FACING:
            self._character_face_direction = LEFT_FACING
        if self.change_x > 0 and self._character_face_direction == LEFT_FACING:
            self._character_face_direction = RIGHT_FACING
            
        # walking animation
        if self.change_x == 0 and self.change_y == 0:
            self._cur_texture += 1
            if self._cur_texture > 7 * FRAME_RATE:
                self._cur_texture = 0
            self.texture = self._walk_textures[self._cur_texture // FRAME_RATE][self._character_face_direction]

        if self._dead:
            self.angle = 90
            if self.center_y > self.death_height + self.height//2:
                self.center_y -= 4

        if self._vel > 0:
            self.center_y += 2
            self._vel -= 2
            self.texture = self._jump_texture[0]

        if self._vel == 0 and self._gravity_on is True:
            self.center_y -= 2

    # How many pixels per jump
    def jump(self) -> None:
        """get the player to jump"""
        self._vel = 60

    def die(self) -> None:
        """instance method to make the player die"""
        self._dead = True


class Platform(arcade.Sprite):
    """class platform
    Attrs:
        horizontal_speed(int): speed of the platform
        scored(bool): To track whether if the player gained a point
        """    

    def __init__(self, image: "sprite") -> None:
        """creates a platform object

        Args:
            image(sprite): The texture for the platform sprite
        """
        super().__init__(image)
        self._horizontal_speed = -4
        self._scored = False

    @classmethod
    def random_platform_generator(cls) -> "sprites":
        """class method to generate random platform

        Args:
            sprites(sprite): The texture for the platform sprite

        Returns:
            returns a sprite image
        """

        new_platform = cls(platform)
        new_platform.center_y = random.randrange(150, SCREEN_HEIGHT//2, 10)
        new_platform.left = 250
        new_platform.width = random.randrange(180, 250)
        new_platform.height = 25
        return new_platform

    def update(self) -> None:
        """ Update method to update the x position of the platform"""
        self.center_x += self._horizontal_speed


# Main Game class
class Game(arcade.Window):
    """ Main class for the game

    Attrs:
        background: texture for the background image. Defaults to None.
        player_list (List[sprites]): list to store sprites for the player 
        character. Defaults to None.
        platform_sprites (List[sprites]): list to store the platform sprites. 
        Defaults to None.
        enemy_sprites (List[sprites]): list to store sprites for the enemy 
        image. Defauls to None.
        player: variable to store the call to the Player class. 
        Defaults to None.
        score_board (List[sprites]): list to store the sprites to display 
        scores. 
        Defaults to None.
        jump (bool): a boolean to check if the user pressed space bar.
        score (int): a variable to store the score. Defaults to None.
        state: variable used to track the state of the player. Defaults to main 
        menu.
        menus (Dict): dictionary to store different texture for the menu 
        screen.
        double_jump (bool): a boolean statement to check whether the player
        used double jump. Defaults to False.
        sorted_list (List[int]): list to store a sorted list of scores from 
        highest to lowest. Defaults to empty list
        stored_score (bool): boolean statement to check if we stored the score. 
        Defaults to False.
        sorted_score (bool): boolean statement to check if we sorted the list 
        already. Defaults to False.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initializer for the game window, note that we need to call setup() on 
        the game object.

        Args: 
            width(int): the width of the screen
            height(int): the height of the screen
            title(str): the title of the screen
        """
        super().__init__(width, height, title="office guy")
        self._background = None
        self._player_list = None
        self._platform_sprites = None
        self._enemy_sprites = arcade.SpriteList()
        self._player = None
        # Score texture
        self._score_board = None
        self._score_list = None
        # A boolean to check if the user pressed space bar
        self._jump = False
        # initial score
        self._score = None
        # Initial state of the game
        self._state = State.MAIN_MENU
        # The texture for the start and game over screens.
        self._menus = {'start': arcade.load_texture(ready),
                      'ready': arcade.load_texture(ready_message),
                      'gameover': arcade.load_texture(gameover),
                      'play': arcade.load_texture(play),
                      'highscore': arcade.load_texture(highscore)}
        self._double_jump = False
        self._sorted_list = []
        self._stored_score = False
        self._sorted_score = False
        
        # for loop to generate 100 enemy sprites
        for _ in range(100):
            self._sprite1 = arcade.Sprite()
            self._sprite1.texture = arcade.load_texture(file_name=enemy, scale=0.2)
            self._sprite1.left = 400
            self._sprite1.center_y = random.randrange(200, SCREEN_HEIGHT//2+20)
            self._enemy_sprites.append(self._sprite1)

    def setup(self) -> None:
        """Sets up sprites for the game"""

        self._score = 0
        self._score_board = arcade.SpriteList()
        self._score_list = arcade.SpriteList()
        self._background = arcade.load_texture(random.choice(background))
        self._platform_sprites = arcade.SpriteList()
        self._player_list = arcade.SpriteList()
        self._scores_list = []
        self._five_best = []

        start_platform1 = Platform.random_platform_generator()
        self._platform_sprites.append(start_platform1)
        self._player = PlayerCharacter()
        self._player.center_x = 55
        self._player.center_y = SCREEN_HEIGHT//2 + 250
        self._player.scale = 0.8
        self._player_list.append(self._player)

    def draw_enemy_sprites(self, index: int) -> "sprite":
        """recursive function to draw sprites from the enemy sprites list"""

        n = len(self._enemy_sprites)

        if index > n:  # base case
            return True

        elif index < n:
            self._enemy_sprites[index].change_x = -4
            self._enemy_sprites[index].draw()

            if self._enemy_sprites[index].center_x <= 10:
                return self.draw_enemy_sprites(index+1)  # recursive step

    def draw_background(self) -> None:
        """draws the background"""

        # Function that loads the texture for the background
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, 500,
                                      500, self._background, 0)

    def draw_score_board(self) -> None:
        # function that loads the texture to draw the score
        self._score_board.draw()
        self._score_list.draw()

    def on_draw(self) -> None:
        """draw function to draw all necessary sprites on the screen"""
        # Start rendering and draw all the objects
        arcade.start_render()
        # draw background, then pipes on top, then base, then bird.
        self.draw_background()
        self._platform_sprites.draw()
        self._player_list.draw()
        # calling recursive function 
        self.draw_enemy_sprites(0)

        # What to draw if the game state in on menu
        if self._state == State.MAIN_MENU:
            # Show the main menu
            texture = self._menus['start']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 + 50, 
                                          250, 50, texture, 0)
            texture = self._menus['ready']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 + 100,
                                          250, 200, texture, 0)
        elif self._state == State.GAME_OVER:
            # Draw the game over menu if the player lost and the restart play 
            # button
            texture = self._menus['gameover']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 + 25, 
                                          100, 100, texture)
            texture = self._menus['play']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 - 50, 
                                          texture.width, texture.height, 
                                          texture, 0)
            arcade.draw_text(f"Congratulations you are number {self._player_rank + 1}", 
                              10, SCREEN_HEIGHT//2 - 200, arcade.color.BLACK, 25)
            arcade.draw_text("Top Five", 75, 455, arcade.color.YELLOW_ORANGE, 20)
            arcade.draw_text("Current Score", SCREEN_WIDTH - 175, 455,
                              arcade.color.YELLOW_ORANGE, 20 )
            # If statement to compute if there is a new highscore
            self.draw_score_board()

    def on_key_press(self, key, key_modifiers) -> None:
        if key == arcade.key.SPACE and self._state == State.MAIN_MENU: 
            # If game state is back to playing , just change the state and 
            # return
            self._state = State.PLAYING
        if key == arcade.key.SPACE and self._double_jump:
            # If Space bar is pressed, self.jump is set to true and will allow 
            # the player to jump
            self._jump = True

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        # if statement to check whether the user clicks in the required box to 
        # restart game
        if self._state == State.GAME_OVER:
            texture = self._menus['play']
            x_position = self.width//2
            y_position = self.height//2 - 50
            if x_position - texture.width//2 <= x <= x_position + texture.width//2:
                if y_position - texture.height//2 <= y <= y_position + texture.height//2:
                    self.setup()
                    self._state = State.MAIN_MENU
                    self._stored_score = False
                    self._sorted_list = []

    def scoreboard(self) -> None:
        '''
        Function created to calculate the score by using a for loop
        '''
        center = SCREEN_WIDTH - 105
        self._score_board = arcade.SpriteList()

        for num in str(self._score):
            self._score_board.append(arcade.Sprite(SCORE[num], 1, 
                                                  center_x=center,
                                                  center_y=420))
            center += 24

    def store_score(self, score: int) -> None:
        """stores the score when game is over
        Args:
            score(int): the player's score
        """
        with open("score.json", "r") as f:
            data = json.load(f)
        data[f"user {len(data) + 1}"] = score
        with open("score.json", "w") as f:
            json.dump(data, f)

        self._stored_score = True

    def display_score_list(self) -> None:
        """displays all the score from highest to lowest"""
        
        self._score_list = arcade.SpriteList()
        x_position = 100  # x coordinate of best scores on the screen
        y_position = 430  # y coordinate of the best scores on the screen
        self._scores_list = []
        self._five_best = []
        self._player_rank = 0
        # calling the json file to load the dictionary of scores
        with open("score.json", "r") as f:
            data = json.load(f)
        # sort all the scores from highest to lowest
        for values in data.values():
            self._sorted_list.append(values)
            bubblesort(self._sorted_list)
        # remove any repeating scores
        for num in self._sorted_list:
            if num not in self._scores_list:
                self._scores_list.append(num)
        # get the rank of the player by using binary search
        self._player_rank = binary_search(self._scores_list, list(data.values())[-1])
        # only draw the five best scores
        if len(self._scores_list) < 6:
            self._five_best = self._scores_list
        else:
            self._five_best = self._scores_list[:5]
         
        for score in self._five_best:
            if len(str(score)) == 1:
                for num in str(score):
                    self._score_list.append(arcade.Sprite(SCORE[num], 1,
                                           center_x=x_position,
                                           center_y=y_position))
                    y_position -= 50

            if len(str(score)) == 2:
                for num in str(score):
                    self._score_list.append(arcade.Sprite(SCORE[num], 1, 
                                           center_x=x_position, 
                                           center_y=y_position))
                    x_position += 24
                y_position -= 50
                x_position = 100

    def generate_platform(self) -> None:
        """generates random platform"""

        new_platform = None
        for plat in self._platform_sprites:
            if plat.right <= 0:
                plat.kill()
            elif len(self._platform_sprites) == 1 and plat.right <= random.randrange(self.width // 2, self.width // 2 + 15):
                new_platform = Platform.random_platform_generator()

        if new_platform:
            self._platform_sprites.append(new_platform)

    def on_update(self, delta_time: float) -> None:
        """
        This a function to update all the images on screen before being drawn
        """
        self._player_list.update_animation()

        if self._state == State.PLAYING:
            self.generate_platform()
            self._player._gravity_on = True

            if self._jump:
                self._player.jump()
                self._jump = False
                self._player.center_y -= 2
               
            if self._player.center_y <= 0:
                self._state = State.GAME_OVER
                
            if self._player.top > self.height:
                self._player.top = self.height

            if self._player.center_x >= self._platform_sprites[0].center_x and not self._platform_sprites[0]._scored:
                self._score += 1
                self._platform_sprites[0]._scored = True

            hit = arcade.check_for_collision_with_list(self._player, 
                                                       self._enemy_sprites)
            if any(hit):
                self._state = State.GAME_OVER
            # checking when double jump is used up
            if self._player.center_y - self._player.height//2 <= self._platform_sprites[0].center_y + self._platform_sprites[0].height//2 and self._player.center_y >= self._platform_sprites[0].center_y - self._platform_sprites[0].height//2 and self._player.center_x <= self._platform_sprites[0].center_x + self._platform_sprites[0].width//2 and self._player.center_x >= self._platform_sprites[0].center_x - self._platform_sprites[0].width//2:
                self._double_jump = True
            if self._player.center_y > self._platform_sprites[0].center_y + 120:
                self._double_jump = False
            if self._player.center_y < self._platform_sprites[0].center_y - 100:
                self._double_jump = False
            # check if the player collides with platform
            if self._player.center_y - self._player.height//2 <= self._platform_sprites[0].center_y + self._platform_sprites[0].height//2 and self._player.center_y >= self._platform_sprites[0].center_y - self._platform_sprites[0].height//2 and self._player.center_x <= self._platform_sprites[0].center_x + self._platform_sprites[0].width//2 and self._player.center_x >= self._platform_sprites[0].center_x - self._platform_sprites[0].width//2:
                self._player.center_y = self._platform_sprites[0].center_y + self._platform_sprites[0].height//2 + self._player.height//2
            # check if the player hits the platform from under
            if self._player.center_y + self._player.height//2 >= self._platform_sprites[0].center_y - self._platform_sprites[0].height//2 and self._player.center_y <= self._platform_sprites[0].center_y and self._player.center_x > self._platform_sprites[0].center_x - self._platform_sprites[0].width//2 and self._player.center_x < self._platform_sprites[0].center_x + self._platform_sprites[0].width//2:
                self._state = State.GAME_OVER
            # This calls update() method on each object in the SpriteList
            self._player_list.update()
            self._player_list.update_animation()
            self._platform_sprites.update()
            self._enemy_sprites.update()
        # if state is game over the player is updated, the gravity is deactivated and the score board is called
        if self._state == State.GAME_OVER:
            self._player.update()
            self._player._gravity_on = False
            self.scoreboard()
            
            if self._stored_score is False:
                self.store_score(self._score)
                self.display_score_list()
                
                
def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()