import arcade
import random
import os

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

CHARACTER_SCALING = 0.5

MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 7

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

class State():
    '''
    First class State() to create different game status of the player
    '''
    MAIN_MENU = 0
    PLAYING = 1
    GAME_OVER = 2



# Image of the base floor
# List of different background images that are chosen randomly by the random function
background = ["Objects" + os.sep + "sprites" + os.sep + "officebackground2.jpg"
               ,"Objects" + os.sep + "sprites" + os.sep + "cloudsky.jpg"]
platform = "Objects" + os.sep + "sprites" + os.sep + "platform2.png"

player = "Objects" + os.sep + "sprites" + os.sep + "officeguy.png"

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
    '9': 'Objects' + os.sep + 'sprites' + os.sep + '9.png',}



def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename, scale=CHARACTER_SCALING),
        arcade.load_texture(filename, scale=CHARACTER_SCALING, mirrored=True)
    ]

Gravity = 2

class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.score = 0
        self.vel = 0
        self.dead = False

        # Track out state
     

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        main_path = ":resources:images/animated_characters/male_person/malePerson"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        # main_path = ":resources:images/animated_characters/male_person/malePerson"
        # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        # main_path = ":resources:images/animated_characters/zombie/zombie"
        # main_path = ":resources:images/animated_characters/robot/robot"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        self.jump_texture = load_texture_pair(f"{main_path}_jump.png")

    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        
       
            
        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
        # Walking animation
            self.cur_texture += 1
            if self.cur_texture > 7 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]


        if self.dead:
            self.angle = 90
            if self.center_y > self.death_height + self.height//2:
                self.center_y -= 4
            return

        if self.vel > 0:
            self.center_y += 2
            # self.vel initially set to 0
            self.vel -= 2
            self.texture = self.jump_texture[0]

    
        else:
            self.center_y -= 2

    # How many pixels per jump
    def jump(self):
        self.vel = 60

    def die(self):
        self.dead = True

class Platform(arcade.Sprite):

    def __init__(self, image):
       
        super().__init__(image)
        # speed
        self.horizontal_speed = -3
        self.scored = False

    @classmethod
    def random_platform_generator(cls, sprites, height):

        new_platform = cls(platform)
        new_platform.center_y = random.randrange(100, SCREEN_HEIGHT//2, 10)
        new_platform.left = 250
        new_platform.width = random.randrange(100, 300)
        new_platform.height = 25


        return new_platform

    def update(self):
        self.center_x += self.horizontal_speed

class Game(arcade.Window):

    def __init__(self, width, height):

        """
        Initializer for the game window, note that we need to call setup() on the game object.
        """
        super().__init__(width, height, title= "office guy")
        self.background = None
        self.player_list = None
        self.sprites = None
        self.platform_sprites = None
        self.player = None
        # Background texture

        # Score texture
        self.score_board = None
        #highscore
        self.highscore = None
        self.new_highscore = None
        # A boolean to check if the user pressed space bar
        self.jump = False
        # initial score
        self.score = None
        # Initial state of the game
        self.state = State.MAIN_MENU
        # The texture for the start and game over screens.
        self.menus = {'start': arcade.load_texture(ready),
                      'ready': arcade.load_texture(ready_message),
                      'gameover': arcade.load_texture(gameover),
                      'play': arcade.load_texture(play),
                      'highscore': arcade.load_texture(highscore)}

        self.double_jump = False
        self.score_list = []


    def setup(self):
        self.highscore = None
        self.score = 0
        self.score_board = arcade.SpriteList()
        self.background = arcade.load_texture(random.choice(background))
        self.platform_sprites = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
    
        self.sprites = dict()
        self.sprites['background'] = self.background

        start_platform1 = Platform.random_platform_generator(self.sprites, self.height)
        self.platform_sprites.append(start_platform1)
        self.player = PlayerCharacter()

        self.player.center_x = 55
        self.player.center_y = SCREEN_HEIGHT//2 + 250
        self.player.scale = 0.8


        self.player_list.append(self.player)


    
    def draw_background(self):

        #Function that loads the texture for the background

        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, 500, 500,
                                      self.background, 0)

    def draw_score_board(self):

        #function that loads the texture to draw the score

        self.score_board.draw()

    def on_draw(self):
      

        # Start rendering and draw all the objects
        arcade.start_render()

        # draw background, then pipes on top, then base, then bird.
        self.draw_background()
        self.platform_sprites.draw()
        self.player_list.draw()


        #What to draw if the game state in on menu
        if self.state == State.MAIN_MENU:
            # Show the main menu
            texture = self.menus['start']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 + 50, 250, 50, texture, 0)
            texture = self.menus['ready']
            arcade.draw_texture_rectangle(self.width//2,self.height//2 +100,250,200,texture,0)
     


        elif self.state == State.GAME_OVER:
            # Draw the game over menu if the player lost and the restart play button
            texture = self.menus['gameover']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 + 50, 200, 100, texture, 0)
            texture = self.menus['play']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 - 50, texture.width, texture.height,texture, 0)

            #If statement to compute if there is a new highscore
            if self.new_highscore == True:
                texture = self.menus['highscore']
                arcade.draw_texture_rectangle(self.width // 2, self.height // 2 - 50, 100, 200, texture, 0)

            self.draw_score_board()


    def on_key_press(self, key, modifiers):

        if key == arcade.key.SPACE and self.state == State.MAIN_MENU:
            # If game state is back to playing , just change the state and return
            self.state = State.PLAYING
            
        if key == arcade.key.SPACE and self.double_jump:
            #If Space bar is pressed, self.jump is set to true and will aloow the player to jump
            self.jump = True

      
          
    def on_mouse_press(self, x, y, button, modifiers):
        #Function for the restart button if game is gameover. If the coordinates of the mouse press are within the coordinates of the image it will update the game
        #state and call setup again which is going to draw all the images again.

        if self.state == State.GAME_OVER:
            texture = self.menus['play']
            x_position = self.width//2
            y_position = self.height//2 - 50
            if x_position - texture.width//2 <= x <= x_position + texture.width//2:
                if y_position - texture.height//2 <= y <= y_position + texture.height//2:
                    self.setup()
                    self.state = State.MAIN_MENU


    def scoreboard(self):
        '''
        Function created to calculate the score by using a for loop
        '''

        #This is the initial x coordinate of the score on the screen
        center = 230
        self.score_board = arcade.SpriteList()

        #Down below in the on_update function, the self.score is going to be updated.
        #By using a for each loop the value num is used an index to find the right score image from the list SCORE
        for num in str(self.score):
            self.score_board.append(arcade.Sprite(SCORE[num], 1, center_x= center , center_y=440))
            center += 24



    def on_update(self, delta_time):

        """
        This a function to update all the images on screen before being drawn, (angles, positions....etc)
        """

        self.player_list.update_animation()

        if self.state == State.PLAYING:

            if self.jump:
                self.player.jump()
                self.jump = False
            

            if self.player.center_y <= 0 :
                
                self.state = State.GAME_OVER

            if self.player.top > self.height:
                self.player.top = self.height

            new_platform = None

            for plat in self.platform_sprites:
                if plat.right <= 0:
                    plat.kill()
                elif len(self.platform_sprites) == 1 and plat.right <= random.randrange(self.width // 2, self.width // 2 + 15):
                    new_platform = Platform.random_platform_generator(self.sprites, self.height)
 
            if new_platform:
                self.platform_sprites.append(new_platform)


            if self.player.center_x >= self.platform_sprites[0].center_x and not self.platform_sprites[0].scored:
                self.score += 1
                self.platform_sprites[0].scored = True
                print(self.score)

            hit = arcade.check_for_collision_with_list(self.player, self.platform_sprites)
            if self.player.center_y - self.player.height//2 <= self.platform_sprites[0].center_y + self.platform_sprites[0].height//2  and self.player.center_y >= self.platform_sprites[0].center_y - self.platform_sprites[0].height//2  and self.player.center_x <= self.platform_sprites[0].center_x + self.platform_sprites[0].width//2  and self.player.center_x >= self.platform_sprites[0].center_x - self.platform_sprites[0].width//2:
                self.double_jump = True

            if self.player.center_y > self.platform_sprites[0].center_y + 120:
                self.double_jump = False
            
            if self.player.center_y - self.player.height//2 <= self.platform_sprites[0].center_y + self.platform_sprites[0].height//2  and self.player.center_y >= self.platform_sprites[0].center_y - self.platform_sprites[0].height//2  and self.player.center_x <= self.platform_sprites[0].center_x + self.platform_sprites[0].width//2  and self.player.center_x >= self.platform_sprites[0].center_x - self.platform_sprites[0].width//2 :
                self.player.center_y = self.platform_sprites[0].center_y + self.platform_sprites[0].height//2 + self.player.height//2
                self.player.angle = 0

            if self.player.center_y + self.player.height//2 >= self.platform_sprites[0].center_y - self.platform_sprites[0].height//2 and self.player.center_y <= self.platform_sprites[0].center_y and self.player.center_x > self.platform_sprites[0].center_x - self.platform_sprites[0].width//2 and self.player.center_x < self.platform_sprites[0].center_x + self.platform_sprites[0].width//2:
                self.state = State.GAME_OVER


            # This calls update() method on each object in the SpriteList
            self.player_list.update()
            self.player_list.update_animation()
            self.platform_sprites.update()


    
        if self.state == State.GAME_OVER:
            self.player.update()

            self.scoreboard()

       
       

def main():
    game = Game(SCREEN_WIDTH, SCREEN_WIDTH)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
