import arcade
WIDTH = 800
HEIGHT = 800
SCREEN_TITLE = "Conclusion"

class ConclusionView(arcade.View):
    
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("THE END", WIDTH/2, 650, color = arcade.color.WHITE, font_size = 30, anchor_x="center")
        arcade.draw_text("You started out as just an office employee.", WIDTH/2, 600, color = arcade.color.WHITE, font_size = 15, anchor_x="center")
        arcade.draw_text("You broke out of the maze of cubicles.", WIDTH/2, 550, color = arcade.color.WHITE, font_size = 15, anchor_x="center")
        arcade.draw_text("You scaled various platforms in order to achieve freedom.", WIDTH/2, 500, color = arcade.color.WHITE, font_size = 15, anchor_x="center")
        arcade.draw_text("And you damn near saved your whole office from a deathly swarm of zombies.", WIDTH/2, 450, color = arcade.color.WHITE, font_size = 15, anchor_x="center")
        arcade.draw_text("You're more than just an office employee now...", WIDTH/2, 400, color = arcade.color.WHITE, font_size = 15, anchor_x="center")
        arcade.draw_text("You're a office manager now!", WIDTH/2, 350, color = arcade.color.WHITE, font_size = 15, anchor_x="center")
        arcade.draw_text("We must thank you for completing all the challenges sent at you!", WIDTH/2, 300, color = arcade.color.WHITE, font_size = 15, anchor_x="center")
        arcade.draw_text("Now it is time to start your first day as a manager.", WIDTH/2, 250, color = arcade.color.WHITE, font_size = 15, anchor_x="center")
        arcade.draw_text("CLICK TO EXIT", WIDTH/2, 100, color = arcade.color.YELLOW, font_size = 15, anchor_x="center")
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.close()


def main():
    """Main function to set up windows"""
    window = arcade.Window(WIDTH, HEIGHT, SCREEN_TITLE)
    conclusion_view = ConclusionView()
    window.show_view(conclusion_view)
    arcade.run()
    # runs the code

if __name__ == "__main__":
    """Starts the file"""
    main()
