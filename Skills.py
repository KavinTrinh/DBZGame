import pygame
from pygame.sprite import Group
from spritesheet import Spritesheet
import json

class Skill(pygame.sprite.Sprite):
    def __init__(self, direction: bool, shooter) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.direction = direction
        self.shooter = shooter
        self.frame_index = 0
        self.frame_list = [] 
        self.update_time = pygame.time.get_ticks()
        self.my_sheet = None
        self.SKILL_COOLDOWN = 100

# class Kameha(Skill):
#     def __init__(self, x, y, direction: bool, shooter) -> None:
#         pygame.sprite.Sprite.__init__(self)
#         super().__init__(direction, shooter)
#         self.my_sheet = Spritesheet('Character/Goku/1/Goku.png')
#         skill_name = 'kamebomb'  # Ensure proper formatting with leading zeros
#         print(f'The skill name is: {skill_name}')
#         img = self.my_sheet.parse_sprite(skill_name)
#         self.image = pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2)))
#         self.image = pygame.transform.flip(self.image, self.direction, False)
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)

#     def update(self) -> None:
#         if self.direction is False:
#             self.rect.x += (1 * self.speed)
#         else:
#             self.rect.x += (-1 * self.speed)

class LongAttackSkill(Skill):
    def __init__(self, name, x, y, direction: bool, width, shooter) -> None:
        pygame.sprite.Sprite.__init__(self)
        super().__init__(direction, shooter)
        self.my_sheet = Spritesheet(f'Character/{shooter.name}/{shooter.level}/{shooter.name}.png')
        self.screen_width = width
        self.damage = -20 if shooter.is_player else -3
        self.name = name
        if name == 'normalbomb':
            self.damage*=2

        for i in range (1, 3):
            skill_name = f'{name}{i:03d}'  # Ensure proper formatting with leading zeros
            # print(f'The skill name is: {skill_name}')
            try:
                img = self.my_sheet.parse_sprite(skill_name)
                img = pygame.transform.scale(img, (int(img.get_width() * 1.5), int(img.get_height() * 1.5)))
                self.frame_list.append(img)
            except Exception as e:
                print(f"Error loading frame {skill_name}: {e}")  # Debug print            
        self.image = self.frame_list[self.frame_index]
        #self.image = pygame.transform.flip(self.image, self.direction, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, characters: pygame, obstacle_list: list, screen_scroll) -> None:
        if self.direction is False:
            self.rect.x += (1 * self.speed) + screen_scroll
        else:
            self.rect.x += (-1 * self.speed) + screen_scroll
        self.image = self.frame_list[self.frame_index]
        self.image = pygame.transform.flip(self.image, self.direction, False)
        if pygame.time.get_ticks() - self.update_time > self.SKILL_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index = (self.frame_index + 1)
            if self.frame_index > len(self.frame_list)-1:
                self.frame_index = len(self.frame_list)-1
        if self.rect.right < 0 or self.rect.left > self.screen_width:
            self.kill()
        #collision with levels 
        # for tile in obstacle_list:
        #     if tile[1].colliderect(self.rect):
        #         self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, name, x, y, scale) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.frame_index = 0
        self.frame_list = []
        if name == 'normalbombexp' or name == 'destructodiscexp':
            self.my_sheet = Spritesheet('Character/Goku/1/Goku.png')
            if name == 'destructodiscexp':
                x = x + 100
                y = y + 20

        for i in range (1, 4):
            exlosion_name = f'{name}{i:03d}'  # Ensure proper formatting with leading zeros
            # print(f'The explosion name is: {exlosion_name}')
            try:
                img = self.my_sheet.parse_sprite(exlosion_name)
                img = pygame.transform.scale(img, (int(img.get_width() * 1.5), int(img.get_height() * 1.5)))
                self.frame_list.append(img)
            except Exception as e:
                print(f"Error loading frame {exlosion_name}: {e}")  # Debug print            
        self.image = self.frame_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    def update(self, screen_scroll)->None:
        #Scroll
        self.rect.x +=  screen_scroll
        EXPLOSION_SPEED = 4
        #update explosion animation
        self.counter+=1
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index+=1
            if self.frame_index >= len(self.frame_list):
                self.kill()
            else:
                self.image = self.frame_list[self.frame_index]
