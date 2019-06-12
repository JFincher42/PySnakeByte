import arcade


class ArcadeTest(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK_LEATHER_JACKET)

        # Set a center for the circle
        self.center_x, self.center_y = 300, 250

        # Set a speed
        self.speed_x, self.speed_y = 13, 7

    def on_draw(self):
        arcade.start_render()

        arcade.draw_circle_filled(
            self.center_x, self.center_y, 10, arcade.color.WHEAT
        )

    def on_update(self, delta):
        self.center_x += self.speed_x
        self.center_y += self.speed_y

        if self.center_x < 5 or self.center_x > 795:
            self.speed_x = -self.speed_x
        if self.center_y < 5 or self.center_y > 695:
            self.speed_y = -self.speed_y


if __name__ == "__main__":
    arcade_test = ArcadeTest(800, 700, "Test")

    arcade.run()
