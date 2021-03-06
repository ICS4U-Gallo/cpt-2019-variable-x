# Zombie Invasion - Chapter 4 - Lucas
import random
import arcade
import json
from typing import List
import math
from conclusion import *

# Set up variables
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ZOMBIE = 0.5
SPRITE_SCALING_LASER = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WIDTH = 800
HEIGHT = 600
SCREEN_TITLE = "Zombie Invasion - Chapter 4"
BULLET_SPEED = 7


def merge_sort(numbers: List[int]) -> List[int]:
    """merge sort for highscore, changed to go from highest to lowest
    Args:
        The list to be sorted
    Returns:
        The sorted list.
    """
    # base case
    if len(numbers) == 1:
        return numbers

    midpoint = len(numbers)//2

    # two recursive steps
    # mergesort left
    left_side = merge_sort(numbers[:midpoint])
    # mergesort right
    right_side = merge_sort(numbers[midpoint:])
    # merge the two together
    sorted_list = []

    # loop through both lists with two markers
    left_marker = 0
    right_marker = 0
    while left_marker < len(left_side) and right_marker < len(right_side):
        # if right value less than left value, add left value to sorted,
        # increase left marker
        if left_side[left_marker] > right_side[right_marker]:
            sorted_list.append(left_side[left_marker])
            left_marker += 1
        # if left value less than right value, add right value to sorted,
        # increase right marker
        else:
            sorted_list.append(right_side[right_marker])
            right_marker += 1
    # create a while loop to gather the rest of the values from either list
    while right_marker < len(right_side):
        sorted_list.append(right_side[right_marker])
        right_marker += 1
    while left_marker < len(left_side):
        sorted_list.append(left_side[left_marker])
        left_marker += 1
    # return the sorted list
    return sorted_list


def binarySearch(numbers, l, length, x):
    """Binary search to find your score in the list
    Args:
        numbers: List
        1: sets up starting point
        length: length of the list
        x: target point
    Return:
        Index of x
    """
    # Check base case, if the length is greater than or equal to 1, start the
    # code.
    if length >= l:
        mid = l + (length - l)//2
        # If x is the mid number, then return it
        if numbers[mid] == x:
            return mid
        # If element is larger than mid, then it is in the left
        # This is because we go highest to lowest using the sorting
        # for highscore
        elif numbers[mid] < x:
            return binarySearch(numbers, l, mid-1, x)
        # Otherwise x can only be left in the right quadrant
        else:
            return binarySearch(numbers, mid+1, length, x)
    else:
        # X is not even in the list, return -1
        return -1


class Player(arcade.Sprite):
    """Player class, has all the important details for the player which later
        are inherited. Not encapsulated since these values are changed often
        and inherited."""
    def __init__(self):
        self.player_sprite = arcade.Sprite(":resources:/images/animated_characters/male_person/malePerson_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = WIDTH / 2
        self.player_sprite.center_y = 70
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        self.player_speed = 3


class Boss(arcade.Sprite):
    """Boss Zombie class, has more features than regular zombies"""
    HEALTH = 300

    def follow_player(self, player_sprite):
        """Moves the zombies towards the player sprite.
        Args:
            player_sprite
        Returns:
            the code to position the zombie towards the player.
        """
        # Created so their movement is not linear
        # Their movement doesn't remain static, updates constantly depending on
        # player position.
        self.center_x += self.change_x
        self.center_y += self.change_y
        # The zombie movement is random, but there is a 1 in 50 chance they lock on
        # to the player. The same is done for the zombie class further down.
        if random.randrange(50) == 0:
            # sets up the start positions.
            start_x = self.center_x
            start_y = self.center_y
            # Get the destination location the player
            destination_x = player_sprite.center_x
            destination_y = player_sprite.center_y
            # Find the difference between the desination of x/y and the start of x/
            # y
            x_difference = destination_x - start_x
            y_difference = destination_y - start_y
            angle = math.atan2(y_difference, x_difference)
            # Using the angle, calculate the velocity needed off of a base movement
            # speed
            self.change_x = math.cos(angle) * 1.5
            self.change_y = math.sin(angle) * 1.5


class MenuView(arcade.View):
    """Main menu/title screen"""
    def on_show(self):
        """Shows itself"""
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """Draws all the text"""
        arcade.start_render()
        arcade.draw_text("Zombie Invasion", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to go next", WIDTH/2, HEIGHT/2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Goes to next view on mouse click"""
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    """Shows instructions"""
    def on_show(self):
        """Shows itself"""
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """Draws all the text and instructions"""
        # starts rendering and drawing all the text
        arcade.start_render()
        arcade.draw_text("Instructions: \n A key to move left \n D key to move right \n S key to move down \n W key to move forward \n Use mouse to aim and shoot \n Your mission is to eliminate all zombies that come your way. \n Collect as many coins as you'd like. \n You have one life to do this. Good luck.", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("Click to begin", WIDTH/2, HEIGHT/2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Goes to next view on mouse click"""
        game_view = MyGame()
        self.window.show_view(game_view)


class HighscoreInput(arcade.View):
    """Inputs highscores into the data.json file"""
    def on_show(self):
        """Shows itself"""
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """Draws all the text"""
        highscore = MyGame().SCORE
        wave_check = MyGame().WAVE_REACHED
        arcade.start_render()
        # Variables to see what wave and score you had
        # Checks if you made it to wave 7
        if wave_check == 8:
            arcade.draw_text("YOUVE WON", WIDTH/2, 400, color = arcade.color.WHITE, font_size = 30, anchor_x="center")
            arcade.draw_text(f"You beat the odds and defeated wave 7, reaching a score of: {highscore}", WIDTH/2, HEIGHT/2,
                            arcade.color.BLACK, font_size=15, anchor_x="center")
        # Gives a different message if you didnt make it.
        else:
            arcade.draw_text("GAME OVER", WIDTH/2, 400, color = arcade.color.WHITE, font_size = 30, anchor_x="center")
            arcade.draw_text(f"The zombies have forced you to run! \n Even so, you fought to the bone, achieving a score of: {highscore}", WIDTH/2, HEIGHT/2,
                            arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("Click to see other highscores", WIDTH/2, HEIGHT/2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """On mouse click, inputs highscore and goes to next view
        Args:
            x, y position of the mosue
            button click
            various modifiers
        Returns:
            the next slide
        """
        highscore = MyGame().SCORE
        # highscore is the score class variable from main game class.
        with open("data.json", "r") as f:
            data = json.load(f)
        # Opens the data.json file
        data[f"highscore {len(data) + 1}"] = highscore
        # Writes to it as a dictionary, with your score being the value
        # and highscore plus whatever interval as the key
        with open("data.json", 'w') as f:
            json.dump(data, f)
            # dumps the data
        print("inputted")
        # testing to make sure it is inputted
        highscore_view = HighscoreView()
        self.window.show_view(highscore_view)
        # goes to next view


class HighscoreView(arcade.View):
    """The highscore view function, shows top 5 highscores"""
    @classmethod
    def on_show(cls):
        arcade.set_background_color(arcade.color.AMAZON)

    @classmethod
    def on_draw(cls):
        # Height decrease keeps a static variable set so later we can space out
        # the amount of a gap between highscores
        height_decrease = 120
        sorted_list = []
        # empty list
        arcade.start_render()
        with open("data.json", "r") as f:
            data = json.load(f)
        # open data.json
        for values in data.values():
            sorted_list.append(values)
            sorted_list2 = merge_sort(sorted_list)
        # merge sort the list from highest to lowest
        arcade.draw_text(f"Highscores: \n", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=22, anchor_x="center")
        for i in reversed(range(5)):
            arcade.draw_text(f"{i+1}: {sorted_list2[i]} \n", WIDTH/2, HEIGHT/2-height_decrease,
                             arcade.color.BLACK, font_size=18, anchor_x="center")
            height_decrease -= 20
        # reverse the range so it is displayed highest to lowest, only showing
        # top 5.
        yourscore = MyGame.SCORE
        yourposition = binarySearch(sorted_list2, 0, len(sorted_list2), yourscore)
        if yourposition != -1:
            arcade.draw_text(f"You placed number {yourposition + 1} on the highscore charts!", WIDTH/2, 300, arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("Click to continue", WIDTH/2, HEIGHT/2-250,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        # if yourposition is not equal to negative 1, the binary search worked
        # Shows your position on the chart using binary search to find your
        # score from the merge sorted list
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Changes view when clicked, same args and returns as other on_mouse_press functions"""
        self.window.close()   
        window = arcade.Window(800, 800, "Conclusion")
        conclusion_view = ConclusionView()
        window.show_view(conclusion_view)
        arcade.run()

class Zombie(arcade.Sprite):
    """
    Zombie class to create their movement
    """
    # Health so they are not so easy to eliminate.
    HEALTH = 150

    def follow_player(self, player_sprite):
        """Moves the zombies towards the player sprite.
        Args:
            player_sprite
        Returns:
            the code to position the zombie towards the player.
        """
        # Created so their movement is not linear
        # Their movement doesn't remain static, updates constantly depending on
        # player position.
        self.center_x += self.change_x
        self.center_y += self.change_y
        if random.randrange(50) == 0:
            # sets up the start positions.
            start_x = self.center_x
            start_y = self.center_y
            # Get the destination location the player
            destination_x = player_sprite.center_x
            destination_y = player_sprite.center_y
            # Find the difference between the desination of x/y and the start of x/
            # y
            x_difference = destination_x - start_x
            y_difference = destination_y - start_y
            angle = math.atan2(y_difference, x_difference)
            # Using the angle, calculate the velocity needed off of a base movement
            # speed
            self.change_x = math.cos(angle) * 1.5
            self.change_y = math.sin(angle) * 1.5


class MyGame(arcade.View, Player):
    """Main game class, creates everything"""
    # Class variables needed to be accessed or changed by other iteration
    # within the class
    # Accessed by things outside the class.
    # Inherits the player class to use it's attributes to make the player
    BOSS_ZOMBIE_COUNT = 1
    ZOMBIE_COUNT = 5
    SCORE = 0
    WAVE_REACHED = 0

    def __init__(self):
        """Initializes game"""
        Player.__init__(self)
        super().__init__()
        # Encapsulate everything here since it is important these items are not
        # changed.
        self._wave = 1
        self._score = 0
        self._hidden_score = 0
        self._bullet_list = arcade.SpriteList()
        self._lives = 1
        self.setup()

    def setup(self):
        """Sets up the zombies"""
        # zombie sprite list
        self.zombie_list = arcade.SpriteList()
        self.bosszombie_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        for i in range(MyGame.ZOMBIE_COUNT):
            zombie = Zombie(":resources:/images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING_ZOMBIE)
            zombie_placed = False
            # Loop to keep checking their positioning
            while not zombie_placed:
                # Position the zombie randomly
                zombie.center_x = random.randrange(800)
                zombie.center_y = random.randrange(600, 700)
                # See if the zombie is hitting another zombie
                zombie_hit_list = arcade.check_for_collision_with_list(zombie, self.zombie_list)
                # See if the zombie is hitting the player
                player_hit_list = arcade.check_for_collision_with_list(zombie, self.player_list)
                # See if the zombie is hitting the boss zombies
                bosszombie_hit_list = arcade.check_for_collision_with_list(zombie, self.bosszombie_list)
                # See if zombie is hitting a coin
                coin_hit_list = arcade.check_for_collision_with_list(zombie, self.coin_list)
                if len(zombie_hit_list) == 0 and len(player_hit_list) == 0 and len(bosszombie_hit_list) == 0 and len(coin_hit_list) == 0:
                    # If it is not hitting anything
                    # It will be placed.
                    zombie_placed = True
            # append to the list
            self.zombie_list.append(zombie)
        # for loop for the boss zombies
        for i in range(MyGame.BOSS_ZOMBIE_COUNT):
            bosszombie = Boss(":resources:/images/animated_characters/zombie/zombie_idle.png", 0.6)
            bosszombie_placed = False
            # Loop to keep checking their positioning
            while not bosszombie_placed:
                # Position the zombie randomly
                bosszombie.center_x = random.randrange(800)
                bosszombie.center_y = random.randrange(600, 700)
                # See if the zombie is hitting another zombie
                zombie_hit_list = arcade.check_for_collision_with_list(bosszombie, self.zombie_list)
                # See if the zombie is hitting the player
                player_hit_list = arcade.check_for_collision_with_list(bosszombie, self.player_list)
                # Check to see if colliding with another boss zombie
                bosszombie_hit_list = arcade.check_for_collision_with_list(bosszombie, self.bosszombie_list)
                # Check to see if hitting a coin
                coin_hit_list = arcade.check_for_collision_with_list(bosszombie, self.coin_list)
                if len(zombie_hit_list) == 0 and len(player_hit_list) == 0 and len(bosszombie_hit_list) == 0 and len(coin_hit_list) == 0:
                    # If it his hitting nothing it will be placed.
                    bosszombie_placed = True
            # Append to list
            self.bosszombie_list.append(bosszombie)
        for i in range(25):
            coin = arcade.Sprite(":resources:/images/items/coinGold.png", 0.25)
            coin_placed = False
            # Loop to keep checking their positioning
            while not coin_placed:
                # Position the coin randomly
                coin.center_x = random.randrange(800)
                coin.center_y = random.randrange(600)
                # See if the coin is hitting a zombie
                zombie_hit_list = arcade.check_for_collision_with_list(coin, self.zombie_list)
                # See if the coin is hitting the player
                player_hit_list = arcade.check_for_collision_with_list(coin, self.player_list)
                # Check to see if colliding with boss zombie
                bosszombie_hit_list = arcade.check_for_collision_with_list(coin, self.bosszombie_list)
                # Check to see if colloding with another coin
                coin_hit_list = arcade.check_for_collision_with_list(coin, self.coin_list)
                if len(zombie_hit_list) == 0 and len(player_hit_list) == 0 and len(bosszombie_hit_list) == 0 and len(coin_hit_list) == 0:
                    # If it is not hitting anything it will be placed.
                    coin_placed = True
            # Append to list
            self.coin_list.append(coin)


    def on_show(self):
        """Shows the view"""
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """Draws everything."""
        arcade.start_render()
        self.player_list.draw()
        self.zombie_list.draw()
        self._bullet_list.draw()
        self.bosszombie_list.draw()
        self.coin_list.draw()
        # Text counters of everything the user needs to be informed of.
        arcade.draw_text(f"Score: {self._score}", 10, 20, arcade.color.WHITE, 14)

        arcade.draw_text(f"Lives: {self._lives}", 720, 20, arcade.color.WHITE, 14)

        arcade.draw_text(f"WAVE: {self._wave}/7", 720, 500, arcade.color.WHITE, 14)

        for bosszombie in self.bosszombie_list:
            arcade.draw_text(f"Health: {bosszombie.HEALTH}", bosszombie.center_x, bosszombie.top, arcade.color.RED, 12)

        for zombie in self.zombie_list:
            arcade.draw_text(f"Health: {zombie.HEALTH}", zombie.center_x, zombie.top, arcade.color.WHITE, 10)

    def on_key_press(self, key, modifiers):
        """Player movement on key press."""
        # Move left to right
        if key == arcade.key.W:
            self.player_sprite.change_y = self.player_speed
        elif key == arcade.key.S:
            self.player_sprite.change_y = -self.player_speed

        # Move up and down
        elif key == arcade.key.A:
            self.player_sprite.change_x = -self.player_speed
        elif key == arcade.key.D:
            self.player_sprite.change_x = self.player_speed

    def on_mouse_press(self, x, y, button, modifiers):
        """Defines what happens when mouse is pressed"""
        # sets up the bullets.
        bullet = arcade.Sprite(":resources:/images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        # start point is the player's center_x and center_y
        # bullets come out from the player
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get the destination for x and y from the function variables
        # uses the mouse x and y location for this.
        destination_x = x
        destination_y = y
        # Calculates the difference between start
        # and destination
        # Uses math tan function for the two
        # differences
        x_difference = destination_x - start_x
        y_difference = destination_y - start_y
        angle = math.atan2(y_difference, x_difference)
        # Angle the bullet so it doesn't just randomly rotate
        bullet.angle = math.degrees(angle)
        # Using the angle and our speed we calculate the velocity of the bullet
        # in order to get the change_x and y
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED
        bullet.center_x = self.player_sprite.center_x
        bullet.bottom = self.player_sprite.center_y
        # add to the bullet list
        self._bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        """Called when a key is released.
            Makes it so that you cant keep sliding in a direction"""

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Updates everything"""
        self._bullet_list.update()
        self.zombie_list.update()
        self.player_list.update()
        self.bosszombie_list.update()
        self.coin_list.update()
        # Calls the follow player code to trace your character
        for zombie in self.zombie_list:
            zombie.follow_player(self.player_sprite)
        for bosszombie in self.bosszombie_list:
            bosszombie.follow_player(self.player_sprite)
        # make sure you can't go past the screen
        if self.player_sprite.center_x < 20:
            self.player_sprite.center_x = 20
        if self.player_sprite.center_x > SCREEN_WIDTH - 20:
            self.player_sprite.center_x = SCREEN_WIDTH - 20
        if self.player_sprite.center_y < 35:
            self.player_sprite.center_y = 35
        if self.player_sprite.center_y > SCREEN_HEIGHT - 35:
            self.player_sprite.center_y = SCREEN_HEIGHT - 35
        # makes sure the regular zombies cannot go below the screen limits
        for zombie in self.zombie_list:
            if zombie.center_x < 20:
                zombie.center_x = 20
            if zombie.center_x > SCREEN_WIDTH - 20:
                zombie.center_x = SCREEN_WIDTH - 20
            if zombie.center_y < 35:
                zombie.center_y = 35
            if zombie.center_y > SCREEN_HEIGHT - 35:
                zombie.center_y = SCREEN_HEIGHT - 35
        # makes sure the boss zombies cannot go below the screen limits
        for bosszombie in self.bosszombie_list:
            if bosszombie.center_x < 20:
                bosszombie.center_x = 20
            if bosszombie.center_x > SCREEN_WIDTH - 20:
                bosszombie.center_x = SCREEN_WIDTH - 20
            if bosszombie.center_y < 35:
                bosszombie.center_y = 35
            if bosszombie.center_y > SCREEN_HEIGHT - 35:
                bosszombie.center_y = SCREEN_HEIGHT - 35
        # setting up bullets
        for bullet in self._bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.zombie_list)
            boss_hit_list = arcade.check_for_collision_with_list(bullet, self.bosszombie_list)
        # If something is hit, the bullet is removed
        # Since the list is greater than 0, things
        # can be removed.
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            if len(boss_hit_list) > 0:
                bullet.remove_from_sprite_lists()
        # For each zombie in the hit list, they get removed
        # Adds to your score, hidden score to keep track
            for bosszombie in boss_hit_list:
                if bosszombie.HEALTH == 50:
                    bosszombie.remove_from_sprite_lists()
                    self._score += 300
                    self._hidden_score += 1
                    # If you beat the zombie, you gain more score points
                else:
                    bosszombie.HEALTH -= 50
                    # bullets have the same effect, just take longer to kill them

            for zombie in hit_list:
                if zombie.HEALTH == 50:
                    zombie.remove_from_sprite_lists()
                    self._score += 100
                    self._hidden_score += 1
                else:
                    zombie.HEALTH -= 50
        # If the bottom of the bullet goes past the screen height
        # remove it from the lists
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()
        # If the zombie touches the character, remove a life.
        for zombie in self.zombie_list:
            if self.player_sprite.collides_with_sprite(zombie):
                self._lives -= 1
        for bosszombie in self.bosszombie_list:
            if self.player_sprite.collides_with_sprite(bosszombie):
                self._lives -= 1
        # If you touch a coin you get the same amount as a zombie.
        for coin in self.coin_list:
            if self.player_sprite.collides_with_sprite(coin):
                self._score += 100
                coin.remove_from_sprite_lists()
        # Core of the game, calls the setup function to repeat
        # the creation of zombies as long as you have above 0
        # lives. Adds an amount of zombies everytime in order
        # to create more zombies on the setup() call.
        while self._lives > 0:
            if self._hidden_score == MyGame.ZOMBIE_COUNT + MyGame.BOSS_ZOMBIE_COUNT:
                # if the hidden_score is equal to the zombie count,
                # the process begins.
                current_score = self._score
                MyGame.ZOMBIE_COUNT += 3
                MyGame.BOSS_ZOMBIE_COUNT += 1
                print(MyGame.BOSS_ZOMBIE_COUNT)
                print(MyGame.ZOMBIE_COUNT)
                self.setup()
                self._hidden_score = 0
                self._score = current_score
                self._wave += 1
                # Add more waves, keep track of score. Reset hidden score.
                # Hidden score is used to keep track of how many zombies youve
                # killed after the zombie count is updated. The regular score
                # keeps going, while hidden score gets reset in order to
                # continue counting up until the zombie count is hit.
            else:
                break

        if self._lives == 0:
            # if you have no lives left, transition to the highscore view.
            MyGame.SCORE = self._score
            highscore_input = HighscoreInput()
            self.window.show_view(highscore_input)
        if self._wave == 8:
            MyGame.SCORE = self._score
            MyGame.WAVE_REACHED = self._wave
            highscore_input = HighscoreInput()
            self.window.show_view(highscore_input)


def main():
    """Main function to set up windows"""
    window = arcade.Window(WIDTH, HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()
    # runs the code

if __name__ == "__main__":
    """Starts the file"""
    main()
