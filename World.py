import pygame
from Item import ItemBox, HealthBar
from Character import Character, MainCharacter, EnemyCharacter
from Skills import Explosion
from game_function import game_settings, world_data, level_setup, Monitor
import csv

class World():
    def __init__(self, screen) -> None:
        self.screen = screen
        self.data = []
        self.dragon_balls = []
        self.obj_list = []
        self.img_list = []
        self.TILE_SIZE = self.screen.TILE_SIZE
        self.game_level = 1
        self.ROWS, self.COLS = level_setup(screen)
        self.data = world_data(self.data, screen, self.game_level)
        for x in range(21):
            img = pygame.image.load(f'LevelEditor-main/img/tile/{x}.png')
            img = pygame.transform.scale(img, (self.TILE_SIZE, self.TILE_SIZE))
            self.img_list.append(img)
        self.sky_img = pygame.image.load(f'Background/{self.game_level}/Sky.png').convert_alpha()
        self.top_img = pygame.image.load(f'Background/{self.game_level}/Top.png').convert_alpha()
        self.mid_img = pygame.image.load(f'Background/{self.game_level}/Mid.png').convert_alpha()
        self.bot_img = pygame.image.load(f'Background/{self.game_level}/Bottom.png').convert_alpha()
        self.level_length = len(self.data[0])
    def update_level(self, character_group: pygame, item_group: pygame, decoration_group: pygame, exit_group: pygame) -> None:  
        self.data = []
        self.data = world_data(self.data, self.screen, self.game_level)
        player, health_bar = self.process_data(character_group, item_group, decoration_group, exit_group)
        return player, health_bar
    def process_data(self, character_group: pygame, item_group: pygame, decoration_group: pygame, exit_group: pygame):
        #iterate through each value in level data file
        for y, row in enumerate(self.data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = self.img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * self.TILE_SIZE
                    img_rect.y = y * self.TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obj_list.append(tile_data)
                    elif tile >= 0 and tile <= 10:
                        #Water
                        water = Decoration(img, x * self.TILE_SIZE, y * self.TILE_SIZE, self.screen)
                        decoration_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        #decoration(rock, grass)
                        decoration = Decoration(img, x * self.TILE_SIZE, y * self.TILE_SIZE, self.screen)
                        decoration_group.add(decoration)
                    elif tile == 15:
                        player = MainCharacter('Goku',1, x * self.TILE_SIZE, y * self.TILE_SIZE,1.5, 6, True)
                        health_bar = HealthBar(10, 10, player.health, player.max_health)
                        character_group.add(player)
                    elif tile == 16:      
                        enemy = EnemyCharacter('Nappa',1, x * self.TILE_SIZE, y * self.TILE_SIZE,1.8, 2)
                        character_group.add(enemy)
                    elif tile == 17: #Energy box
                        item_box = ItemBox(self.screen, 'energy', x*self.TILE_SIZE, y * self.TILE_SIZE,1)
                        item_group.add(item_box)
                    elif tile == 18: #Dragon Ball
                        item_box = ItemBox(self.screen, 'ball', x*self.TILE_SIZE, y * self.TILE_SIZE,len(self.dragon_balls)+1)
                        self.dragon_balls.append(item_box)
                        item_group.add(item_box)
                    elif tile == 19: #health box
                        item_box = ItemBox(self.screen, 'health', x*self.TILE_SIZE, y * self.TILE_SIZE,1)
                        item_group.add(item_box)
                    elif tile == 20: #exit
                        exit = Exit(img, x * self.TILE_SIZE, y * self.TILE_SIZE, self.screen)
                        exit_group.add(exit)
        return player, health_bar
        
    def draw(self, screen_scroll):
        for tile in self.obj_list:       
            tile[1][0] += screen_scroll
            self.screen.canvas.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y, screen):
        pygame.sprite.Sprite.__init__(self)
        self.ROWS, self.COLS = level_setup(screen)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + screen.TILE_SIZE // 2, y + (screen.TILE_SIZE - self.image.get_height()))
    def update(self, screen_scroll) -> None:
        self.rect.x += screen_scroll
class Exit(Decoration):
    def __init__(self, img, x, y, screen) -> None:
        pygame.sprite.Sprite.__init__(self)
        super().__init__(img, x, y, screen)
    def update(self, screen_scroll) -> None:
        self.rect.x += screen_scroll