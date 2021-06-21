from pygame import Surface, Rect, Color
from pygame.font import Font


def wrap_text(text: str, font: Font, width: int) -> list[str]:
    """Wrap `text` by word, to `width`, using the given `font`.

    Returns a `list[str]` of the wrapped lines.
    """

    lines = []
    
    while len(text) > 0:
        idx = 0

        # increment `idx` until we can't fit any more text on this line
        while font.size(text[:idx])[0] < width and idx < len(text):
            idx += 1

        # if we've wrapped, adjust the wrap to the last word
        if idx < len(text):
            idx = text.rfind(" ", 0, idx) + 1

        # store this line and remove it from the original text
        lines.append(text[:idx])
        text = text[idx:]

    return lines


def draw_text(text: str, surface: Surface, rect: Rect, font: Font, color: Color, line_spacing: int = -2, center: bool = True) -> list[str]:
    """Draw the `text` to the given `surface`, within the bounds of the given
    `rect`, in the given `font` and `color`, line-wrapping the `text` by word.

    If the `center` argument is True (the default), this will center the text
    (both horizontally and vertically) inside the bounds. If set to False,
    the text will be drawn directly against the left side of the bounds.

    Returns the lines of text that did not fit within the bounds, or an empty
    list.

    Internally, this uses the ``wrap_text`` function.
    """

    font_height = font.size("Tg")[1]
    if not isinstance(text, list):
        text = wrap_text(text, font, rect.width)

    printable_lines = 0
    for i in range(0, len(text)):
        if ((font_height + line_spacing) * (i + 1)) <= rect.height:
            printable_lines += 1

    y = rect.top
    if center:
        y = (rect.height / 2) - (((font_height + line_spacing) * printable_lines) / 2)

    for line in text[:printable_lines]:
        # render the line
        image = font.render(line, True, color)

        x = rect.left
        if center:
            x = (rect.width / 2) - (image.get_width() / 2)

        # blit the line
        surface.blit(image, (x, y))
        y += font_height + line_spacing

    return text[printable_lines:]
