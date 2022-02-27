from PIL import Image, ImageFilter


# CHANGABLE
# Skin file
FILE = "test_skin.png"
# Skin arm size, steve = 4, alex = 3
ARM_SIZE = 3
# Blur background
BLUR = True
# Background color in RGB format
BACKGROUND_COLOR = (67, 97, 110)
# Also use top layer on the render
TOP_LAYER = True

# SEMI-CHANGABLE
CANVAS_SIZE = (1000, 1000)
PIXEL_SIZE = round(CANVAS_SIZE[0] / 20)
BODY_PIXEL_SIZE  = round(CANVAS_SIZE[0] / 35)
TOP_LAYER_OFFSET = PIXEL_SIZE

# DON'T CHANGE
HEAD_FRONT_BOUNDS = (8, 8, 15, 16)
HEAD_FRONT_TOP_BOUNDS = (40, 8, 47, 16)
HEAD_LEFT_BOUNDS = (4, 8, 8, 16)
HEAD_LEFT_TOP_BOUNDS = (35, 8, 40, 16)
NECK_BOUNDS = (20, 18, 28, 20)
BODY_BOUNDS = (20, 20, 28, 32)
ARM_LEFT_BOUNDS = (52 - 5 * ARM_SIZE, 52, 52 - 4 * ARM_SIZE, 64)
ARM_RIGHT_BOUNDS = (40 + ARM_SIZE, 20, 40 + 2 * ARM_SIZE, 32)


def create_size(bounds, pixel=PIXEL_SIZE):
    return (
        (bounds[2] - bounds[0]) * pixel,
        (bounds[3] - bounds[1]) * pixel
    )


def generate():
    skin = Image.open(FILE).convert("RGBA")

    skin_canvas = Image.new('RGBA', CANVAS_SIZE)

    canvas = Image.new('RGBA', CANVAS_SIZE)

    canvas.paste(BACKGROUND_COLOR, (0, 0, CANVAS_SIZE[0], CANVAS_SIZE[1]))


    # HEAD FRONT
    head_front = skin.crop(HEAD_FRONT_BOUNDS)
    head_front_size = create_size(HEAD_FRONT_BOUNDS)
    head_front = head_front.resize(head_front_size, resample=Image.NONE)

    head_front_loc = (
        round(CANVAS_SIZE[0] / 2 - 2 * PIXEL_SIZE),
        200
    )

    skin_canvas.paste(head_front, head_front_loc)

    # HEAD FRONT TOP
    if TOP_LAYER:
        head_front_top = skin.crop(HEAD_FRONT_TOP_BOUNDS)
        head_front_top = head_front_top.resize(head_front_size, resample=Image.NONE)

        head_front_top_loc = (
            round(head_front_loc[0] + TOP_LAYER_OFFSET),
            round(head_front_loc[1] - PIXEL_SIZE)
        )

        skin_canvas.paste(head_front_top, head_front_top_loc, head_front_top)

    # HEAD LEFT
    head_left = skin.crop(HEAD_LEFT_BOUNDS)
    head_left_size = create_size(HEAD_LEFT_BOUNDS)
    head_left = head_left.resize(head_left_size, resample=Image.NONE)

    head_left_overlay = Image.new('RGBA', head_left.size)
    head_left_overlay.paste((0, 0, 0, 65), (0, 0, head_left.size[0], head_left.size[1]))

    head_left.alpha_composite(head_left_overlay)

    head_left_loc = [
        round(head_front_loc[0]) - 3 * PIXEL_SIZE,
        round(head_front_loc[1])
    ]
    skin_canvas.paste(head_left, head_left_loc, head_left)

    # HEAD LEFT TOP
    if TOP_LAYER:
        head_left_top = skin.crop(HEAD_LEFT_TOP_BOUNDS)
        head_left_top = head_left_top.resize(head_left_size, resample=Image.NONE)

        head_left_top_loc = [
            round(head_left_loc[0] + TOP_LAYER_OFFSET),
            round(head_left_loc[1])
        ]

        skin_canvas.paste(head_left_top, head_left_loc, head_left_top)

    # BODY
    body = skin.crop(BODY_BOUNDS)
    body_size = create_size(BODY_BOUNDS, pixel=BODY_PIXEL_SIZE)
    body = body.resize(body_size, resample=Image.NONE)

    body_loc = (
        round(head_front_loc[0] - BODY_PIXEL_SIZE),
        round(head_front_loc[1] + head_front_size[1] + 2 * BODY_PIXEL_SIZE)
    )

    skin_canvas.paste(body, body_loc, body)

    # NECK
    neck = skin.crop(NECK_BOUNDS)
    neck_size = create_size(NECK_BOUNDS, pixel=BODY_PIXEL_SIZE)
    neck.putpixel((0, 0), (0, 0, 0, 0))
    neck.putpixel((7, 0), (0, 0, 0, 0))
    neck = neck.resize(neck_size, resample=Image.NONE)

    neck_loc = (
        round(body_loc[0]),
        round(body_loc[1] - 2 * BODY_PIXEL_SIZE)
    )

    skin_canvas.paste(neck, neck_loc, neck)

    # ARM RIGHT
    arm_right = skin.crop(ARM_RIGHT_BOUNDS)
    arm_right_size = create_size(ARM_RIGHT_BOUNDS, pixel=BODY_PIXEL_SIZE)
    arm_right.putpixel((ARM_SIZE - 1, 0), (0, 0, 0, 0))
    arm_right.putpixel((ARM_SIZE - 2, 0), (0, 0, 0, 0))
    arm_right = arm_right.resize(arm_right_size, resample=Image.NONE)

    arm_right_loc = (
        round(body_loc[0] + body_size[0]),
        round(body_loc[1] - BODY_PIXEL_SIZE)
    )

    skin_canvas.paste(arm_right, arm_right_loc, arm_right)

    # ARM LEFT
    arm_left = skin.crop(ARM_LEFT_BOUNDS)
    arm_left_size = create_size(ARM_LEFT_BOUNDS, pixel=BODY_PIXEL_SIZE)
    arm_left.putpixel((0, 0), (0, 0, 0, 0))
    arm_left.putpixel((1, 0), (0, 0, 0, 0))
    arm_left = arm_left.resize(arm_left_size, resample=Image.NONE)

    arm_left_loc = (
        round(body_loc[0] - ARM_SIZE * BODY_PIXEL_SIZE),
        round(body_loc[1] - BODY_PIXEL_SIZE)
    )

    skin_canvas.paste(arm_left, arm_left_loc, arm_left)


    if BLUR:
        shadow = Image.new("RGBA", skin_canvas.size, color=(0, 0, 0))

        canvas.paste(shadow, (0, 0), skin_canvas)
        for _ in range(250):
            canvas = canvas.filter(ImageFilter.BLUR)

    canvas.paste(skin_canvas, (0, 0), skin_canvas)

    canvas.save("result.png")


if __name__ == "__main__":
    generate()