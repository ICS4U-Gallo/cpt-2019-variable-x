import random
import arcade
import os
import json
from typing import List

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ZOMBIE = 0.5
SPRITE_SCALING_LASER = 0.8

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WIDTH = 800
HEIGHT = 600
SCREEN_TITLE = "Zombie Invasion"
BULLET_SPEED = 5
def merge_sort(numbers: List[int]) -> List[int]:
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
        # if right value less than left value, add right value to sorted, increase right marker
        if left_side[left_marker] > right_side[right_marker]:
            sorted_list.append(left_side[left_marker])
            left_marker += 1
        # if left value less than right value, add left value to sorted, increase left marker
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


def bubblesort(numbers):
    n = len(numbers)

    for i in range(n):
        for j in range(n - i - 1):
            if numbers[j] < numbers[j + 1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]

    return numbers


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Zombie Invasion", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to go next", WIDTH/2, HEIGHT/2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions: \n Left arrow key to move left \n Right arrow key to move right \n Space to shoot \n Your mission is to eliminate all zombies that come your way. You have one life to do this. Good luck.", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=12, anchor_x="center")
        arcade.draw_text("Click to begin", WIDTH/2, HEIGHT/2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        self.window.show_view(game_view)


class HighscoreInput(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        highscore = MyGame().SCORE
        arcade.start_render()
        arcade.draw_text(f"The Zombies have made a breach in our defenses! \n You have fought valiently, achieving a zombie kill count of: {highscore}", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=12, anchor_x="center")
        arcade.draw_text("Click to see other highscores", WIDTH/2, HEIGHT/2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        highscore = MyGame().SCORE
        with open("data.json", "r") as f:
            data = json.load(f)
    
        data[f"highscore {len(data) + 1}"] = highscore

        with open("data.json", 'w') as f:
            json.dump(data, f)
        highscore_view = HighscoreView()
        self.window.show_view(highscore_view)


class HighscoreView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        height_decrease = 120
        sorted_list = []
        arcade.start_render()
        with open("data.json", "r") as f:
            data = json.load(f)

        for values in data.values():
            sorted_list.append(values)
            merge_sort(sorted_list)
        arcade.draw_text(f"Highscores: \n", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        for i in range(5):
            arcade.draw_text(f"{i+1}: {sorted_list[i]} \n", WIDTH/2, HEIGHT/2-height_decrease,
                             arcade.color.BLACK, font_size=18, anchor_x="center")
            height_decrease -= 20
        arcade.draw_text("Click to continue", WIDTH/2, HEIGHT/2-250,
                         arcade.color.WHITE, font_size=20, anchor_x="center")



class MyGame(arcade.View):
    ZOMBIE_COUNT = 50
    SCORE = 0

    def __init__(self):
        super().__init__()
        self.wave = 1
        self.score = 0
        self.hidden_score = 0
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.lives = 1
        self.player_sprite = arcade.Sprite(":resources:/images/animated_characters/male_adventurer/maleAdventurer_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)
        self.setup()

    def setup(self):
        self.zombie_list = arcade.SpriteList()
        for i in range(MyGame.ZOMBIE_COUNT):
            zombie = arcade.Sprite(":resources:/images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING_ZOMBIE)
            zombie.center_x = random.randrange(SCREEN_WIDTH)
            zombie.center_y = random.randrange(600, 800)
            zombie.change_y = -0.5
            self.zombie_list.append(zombie)

    def on_show(self):
        self.window.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()

        self.zombie_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        arcade.draw_text(f"Zombies Eliminated: {self.score}", 10, 20, arcade.color.WHITE, 14)

        arcade.draw_text(f"Lives: {self.lives}", 720, 20, arcade.color.WHITE, 14)

        arcade.draw_text(f"WAVE: {self.wave}", 720, 500, arcade.color.WHITE, 14)           

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:

            bullet = arcade.Sprite(":resources:/images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

            bullet.angle = 90

            bullet.change_y = BULLET_SPEED

            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

            self.bullet_list.append(bullet)

        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -3
        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = 3

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.bullet_list.update()
        self.zombie_list.update()
        self.player_sprite.update()

        for bullet in self.bullet_list:

            hit_list = arcade.check_for_collision_with_list(bullet, self.zombie_list)

            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            for zombie in hit_list:
                zombie.remove_from_sprite_lists()
                self.score += 1
                self.hidden_score += 1


            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        if self.player_sprite.center_x < 20:
            self.player_sprite.center_x = 20

        if self.player_sprite.center_x > SCREEN_WIDTH - 20:
            self.player_sprite.center_x = SCREEN_WIDTH - 20
            
        for zombie in self.zombie_list:       
            if zombie.center_y == 0:
                self.lives -= 1
            if self.player_sprite.collides_with_sprite(zombie):
                self.lives -= 1
        while self.lives > 0:
            if self.hidden_score == MyGame.ZOMBIE_COUNT:
                current_score = self.score
                current_wave = self.wave
                current_x = self.player_sprite.center_x
                current_y = self.player_sprite.center_y
                MyGame.ZOMBIE_COUNT += 15
                self.setup()
                self.hidden_score = 0
                self.score = current_score
                self.wave = current_wave + 1
                self.player_sprite.center_x = current_x
                self.player_sprite.center_y = current_y
            else:
                break
        if self.lives == 0:
            for zombie in self.zombie_list:
                zombie.center_y = 1000
            MyGame.SCORE = self.score
            highscore_input = HighscoreInput()
            self.window.show_view(highscore_input) 
        


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Zombie Invasion")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
