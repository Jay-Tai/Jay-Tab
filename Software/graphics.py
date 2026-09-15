from fonts.pt_serif import FONT_DATA, GLYPHS

def fill_screen(fb, color=0):
    fb.clear(color)

def draw_pixel(fb, x, y, color=1):
    fb.pixel(x, y, color)

def draw_line(fb, x0, y0, x1, y1, color=1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    error = dx - dy

    while True:
        fb.pixel(x0, y0, color)

        if x0 == x1 and y0 == y1:
            break

        doubled = error * 2

        if doubled > -dy:
            error -= dy
            x0 += sx

        if doubled < dx:
            error += dx
            y0 += sy

def draw_rect(fb, x, y, width, height, color=1):
    draw_line(fb, x, y, x + width - 1, y, color)
    draw_line(
        fb,
        x,
        y + height - 1,
        x + width - 1,
        y + height - 1,
        color
    )
    draw_line(fb, x, y, x, y + height - 1, color)
    draw_line(
        fb,
        x + width - 1,
        y,
        x + width - 1,
        y + height - 1,
        color
    )

def fill_rect(fb, x, y, width, height, color=1):
    for row in range(y, y + height):
        for column in range(x, x + width):
            fb.pixel(column, row, color)


def draw_image(fb, image, x, y):
    width = image["width"]
    height = image["height"]
    data = image["data"]

    bytes_per_row = (width + 7) // 8
    for image_y in range(height):
        for image_x in range(width):
            byte_index = (
                image_y * bytes_per_row + (image_x // 8)
            )

            bit_index = 7 - (image_x % 8)

            pixel = 1-(
                (data[byte_index] >> bit_index) & 1
            )

            fb.pixel(
                x + image_x,
                y + image_y,
                pixel
            )

def draw_text(fb, text, x, y, font_data, glyphs, color = 1):
    cursor_x = x

    for character in text:
        if character not in GLYPHS:
            continue

        offset, width, height, x_advance, x_offset, y_offset = glyphs[character]

        bytes_per_row = (width + 7) // 8

        for glyph_y in range(height):
            row_start = offset + glyph_y * bytes_per_row

            for glyph_x in range(width):
                byte_index = row_start + (glyph_x // 8)
                bit_index = 7 - (glyph_x % 8)

                pixel = (font_data[byte_index] >> bit_index) & 1

                if pixel:
                    fb.pixel(
                        cursor_x + x_offset + glyph_x,
                        y + y_offset + glyph_y,
                        color
                    )

        cursor_x += x_advance