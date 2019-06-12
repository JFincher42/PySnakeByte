import arcade


def on_draw(delta):
    arcade.start_render()
    if on_draw.center_x < 5 or on_draw.center_x > 795:
        on_draw.speed_x = -on_draw.speed_x
    if on_draw.center_y < 5 or on_draw.center_y > 695:
        on_draw.speed_y = -on_draw.speed_y

    arcade.draw_circle_filled(
        on_draw.center_x, on_draw.center_y, 10, arcade.color.WHEAT
    )

    on_draw.center_x += on_draw.speed_x
    on_draw.center_y += on_draw.speed_y


if __name__ == "__main__":
    arcade.open_window(800, 700, "Test")
    arcade.set_background_color(arcade.color.BLACK_LEATHER_JACKET)

    # Set a center for the circle
    on_draw.center_x, on_draw.center_y = 300, 250

    # Set a speed
    on_draw.speed_x, on_draw.speed_y = 10, 9

    arcade.schedule(on_draw, 1 / 30)
    arcade.run()
