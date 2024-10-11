import pygame
import json

class Spritesheet:
    def __init__(self, f_loc) -> None:
        self.file_location = f_loc
        self.sprite_sheet = pygame.image.load(f_loc).convert_alpha()
        self.meta_data = self.file_location.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()
        #print(self.data['frames'].keys())

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite.set_colorkey((255, 255, 255))
        sprite.blit(self.sprite_sheet, (0,0), (x,y,w,h))
        return sprite
    
    def parse_sprite(self, name):
        try:
            sprite = self.data['frames'][name]['frame']
        except KeyError:
            # raise KeyError(f"Sprite '{name}' not found in the JSON file. Available sprites are: {list(self.data['frames'].keys())}")
            raise KeyError()
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image
