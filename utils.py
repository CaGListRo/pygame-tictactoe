import pygame as pg


image_path = 'images'
def load_image(image, width):
    img = pg.image.load(image_path  + '/' + image + '.png').convert_alpha()
    old_width = img.get_width()
    fac = width * 100 / old_width
    old_height = img.get_height()
    height = old_height * fac / 100 
    return pg.transform.smoothscale(img, (width, height))
