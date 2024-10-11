import pygame
from spritesheet import Spritesheet
from Character import MainCharacter

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, screen, item_type, x, y, number) -> None:
        self.TILE_SIZE = screen.TILE_SIZE
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = None
        self.my_sheet = Spritesheet('Item/Item.png')
        # print(f'The skill name is: {item_type}')
        item_name = f'{item_type}00{number}'
        img = self.my_sheet.parse_sprite(item_name)
        self.image = pygame.transform.scale(img, (int(img.get_width() * 1.5), int(img.get_height() * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + self.TILE_SIZE // 2, y + (self.TILE_SIZE - self.image.get_height()))
		
    def update(self, player: MainCharacter, screen_scroll):
        #scroll
        self.rect.x += screen_scroll
		#check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
                #check what kind of box it was
                if self.item_type == 'health':
                    player.health += 25
                    if player.health > player.max_health:
                        player.health = player.max_health
                elif self.item_type == 'energy':
                    player.energy += 15
                elif self.item_type == 'ball':
                    player.balls.append(self)
                #delete the item box
                self.kill()	    

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
    def draw(self, screen, health):
        #update
        self.health = health
        #calculate health ration
        BLACK = (0,0,0)
        RED = (255,0,0)
        GREEN = (0,255,0)
        ratio = self.health/self.max_health
        pygame.draw.rect(screen.canvas, BLACK, (self.x-2, self.y-2, 154, 24))
        pygame.draw.rect(screen.canvas, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen.canvas, GREEN, (self.x, self.y, 150*ratio, 20))