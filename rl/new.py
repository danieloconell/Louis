import pygame as pg


def rotate(surface, angle, rect, offset):
    """Rotate the surface and add the offset to the new rect.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float)
        rect (pygame.Rect)
        offset (pygame.math.Vector2): This vector is added to the center.
    """
    rotated_image = pg.transform.rotate(surface, -angle)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the old center to adjust the position.
    rect = rotated_image.get_rect(center=rect.center+rotated_offset)
    return rotated_image, rect


pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
BG_COLOR = pg.Color('gray15')
# The original image will never be modified.
IMAGE = pg.Surface((140, 60), pg.SRCALPHA)
IMAGE.fill(pg.Color('dodgerblue3'))
rect = IMAGE.get_rect(center=(200, 250))
offset = pg.math.Vector2(50, 0)
angle = 0

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_d] or keys[pg.K_RIGHT]:
        angle += 1
    elif keys[pg.K_a] or keys[pg.K_LEFT]:
        angle -= 1
    if keys[pg.K_f]:
        rect.x += 2

    # Rotate the image and rect (the rect will just change its size).
    rotated_image, offset_rect = rotate(IMAGE, angle, rect, offset)

    # Draw everything.
    screen.fill(BG_COLOR)
    screen.blit(rotated_image, offset_rect)  # Blit the rotated image.
    pg.draw.circle(screen, (30, 250, 70), rect.center, 3)  # center of orig rect / pivot.
    pg.draw.rect(screen, (30, 250, 70), offset_rect, 1)  # The offset rect.
    pg.display.set_caption('Angle: {}'.format(angle))
    pg.display.flip()
    clock.tick(30)

pg.quit()
