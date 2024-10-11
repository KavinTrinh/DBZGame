import pygame
from spritesheet import Spritesheet
import json
import random
from Skills import LongAttackSkill

class Character(pygame.sprite.Sprite):
    def __init__(self, name, level, x, y, scale, speed, sprite_sheet_path):
        super().__init__()
        self.my_sheet = Spritesheet(sprite_sheet_path)
        self.name = name
        self.level = level
        self.scale = scale
        self.x = x
        self.y = y
        self.speed = speed*level
        self.initial_speed = speed*level
        self.energy = 10*level
        self.skill_cooldown = 12
        self.health = 100
        self.max_health = 100
        self.attack_damage = -0.1*5
        self.vel_y = 0
        self.moving_left = False
        self.moving_right = False
        self.crouch = False
        self.jump = False
        self.got_hit = False
        self.close_attacking = False
        self.long_attackj = False
        self.long_attacku = False
        self.in_air = False
        self.direction = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 
        self.update_time = pygame.time.get_ticks()
        self.GRAVITY = 0.75

        

        #ITEMS
        self.balls = []
        

        self.hit_timer = 0  # Timer for hit action
        self.hit_duration = 200 
        
    def draw(self):
        pass

    

class MainCharacter(Character):
    def __init__(self, name, level, x, y, scale, speed, is_player: bool) -> None:
        pygame.sprite.Sprite.__init__(self)
        
        sprite_sheet_path = f'Character/{name}/{level}/{name}.png'
        super().__init__(name, level, x, y, scale, speed, sprite_sheet_path)
        self.is_player = is_player

        #animation
        self.load_animation()
    
    def level_up(self):
        self.level += 1
        self.speed = self.initial_speed * self.level
        self.energy = 10 * self.level
        self.sprite_sheet_path = f'Character/{self.name}/{self.level}/{self.name}.png'
        self.my_sheet = Spritesheet(self.sprite_sheet_path)

        # Re-load animations
        self.load_animation()

    def load_animation(self):
        with open(f'Character/{self.name}/{self.level}/{self.name}.json', 'r') as file:
            data = json.load(file)
        # Convert JSON data to a string
        data_str = json.dumps(data)

        animation_types = ['stand', 'run', 'jump','attack', 'longattackj', 'hit', 'death', 'longattacku', 'walk']
        self.animation_list = []  # Ensure it's cleared
        
        for animation in animation_types:
            #reset temporary list
            temp_list = []
            #count number of files in the folder
            num_of_frames = data_str.count(animation)
            
            
            for i in range(1, num_of_frames + 1):
                frame_name = f'{animation}{i:03d}'  # Ensure proper formatting with leading zeros
                # print(f'Tên frame name is: {frame_name}')
                try:
                    img = self.my_sheet.parse_sprite(frame_name)
                    img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                    temp_list.append(img)
                except Exception as e:
                    print(f"Error loading frame {frame_name}: {e}")  # Debug print

            if not temp_list:
                print(f"Warning: No frames found for animation {animation}")  # Debug print

            self.animation_list.append(temp_list)
        if not self.animation_list:
            print("Error: Animation list is empty")  # Debug print
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update_action(self, new_action):
        #check if animation is different
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            
    def check_alive(self):
        if self.health <= 0:
            TILE_SIZE = int(800*0.8) / 16
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(6)
            self.rect.y =  self.rect.y + 45
            # self.kill()
    
    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #Update the image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if time has passed
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            if self.action == 4 or self.action == 2:
                self.frame_index = (self.frame_index + 1)
                if self.frame_index > len(self.animation_list[self.action])-1:
                    self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = (self.frame_index + 1) % len(self.animation_list[self.action])
            
    def longattack(self, name, group, width)->None:
        if self.skill_cooldown <= 0 and self.energy > 0:
            if self.is_player:
                self.skill_cooldown = 5
            else:
                self.skill_cooldown = 30
            if self.frame_index == len(self.animation_list[self.action])-2 or self.frame_index == len(self.animation_list[self.action])-1 :
                if not self.direction:
                    # print(f'Create new skill')
                    skill = LongAttackSkill(name, self.rect.centerx + (1 * self.rect.size[0]), self.rect.centery, self.direction, width, self)
                else:
                    # print(f'Create new skill')
                    skill = LongAttackSkill(name, self.rect.centerx + (-0.5 * self.rect.size[0]), self.rect.centery, self.direction,width, self)
                group.add(skill)
                self.energy-=1
                self.update_action(0)#back to idle
            #reduce energy
            
        else:
            self.skill_cooldown -=1
    def update(self, monitor, skills, obstacle_list, screen_scroll, bg_scroll, world_len)->int:
        self.update_animation()
        screen_scroll = self.move(monitor, obstacle_list, bg_scroll, world_len)
        self.check_alive()
        if self.alive:
            if self.got_hit:
                self.being_hit()
            elif self.jump or self.in_air:
                self.update_action(2)#2: Jumping
            elif self.close_attacking:
                self.update_action(3)#3: attacking
            elif self.long_attacku and self.energy>0:
                # print(f'player energy is {player.energy}')
                self.update_action(7)#4: disc
                self.longattack('destructodisc',skills, monitor.get_width())
            elif self.long_attackj and self.energy>0:
                # print(f'player energy is {player.energy}')
                self.update_action(4)#4: Kameha
                self.longattack('normalbomb',skills,  monitor.get_width())
            elif (self.moving_left or self.moving_right) and self.speed > 4:
                self.update_action(1)#1: sprinting
            elif (self.moving_left or self.moving_right) and self.speed < 4:
                self.update_action(8)#8: walking
            else:
                self.update_action(0)#0: standing
        
        return screen_scroll
    
    def draw(self, monitor: pygame) -> None:
        monitor.canvas.blit(pygame.transform.flip(self.image, self.direction, False) ,self.rect)

    def move(self, monitor: pygame, obstacle_list: list, bg_scroll, world_len):
        #movement var
        ROWS = 16
        SCREEN_WIDTH = monitor.get_width()
        SCREEN_HEIGHT = monitor.get_height()
        TILE_SIZE = monitor.TILE_SIZE
        screen_scroll = 0
        dx = 0
        dy = 0
        
        SCROLL_THRESH = 200

        #assigning movement
        if self.moving_left and not self.long_attackj and not self.long_attacku:
            dx = -self.speed
            self.direction = True
        if self.moving_right and not self.long_attackj and not self.long_attacku:
            dx = +self.speed
            self.direction = False
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True
        #Pull down gravity
        dy = self.gravity(dy)

        #check for collision
        for tile in obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check collision vertically
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0
                #Below the ground, ie jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #Falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        #Collision

        #fallen off the screen:
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0
        #Player going off the edges of the screen
        if self.is_player:
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0
        #update character rect:
        self.rect.x += dx
        self.rect.y += dy

        # Scrolling screen
        if self.is_player:
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world_len * TILE_SIZE) - SCREEN_WIDTH)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        return screen_scroll
    
    def gravity(self, dy: float):
        self.vel_y+=self.GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        return dy

    def being_hit(self)->None:
        self.update_action(5)
        self.speed = 0
    
    def reset_action_after_hit(self):
        if pygame.time.get_ticks() - self.hit_timer > self.hit_duration:
            self.speed = self.initial_speed
            self.update_action(0)  # Reset action to standing
            self.hit_timer = 0  # Reset timer
            self.got_hit = False

class EnemyCharacter(MainCharacter):
    def __init__(self, name, level, x, y, scale, speed) -> None:
        pygame.sprite.Sprite.__init__(self)
        super().__init__(name, level, x, y, scale, speed, False)
        self.move_counter = 0
        self.vision = pygame.Rect(0,0, 220, 20)
        self.idling = False
        self.idling_counter = 0
    def idle(self)->None:
        self.idling = True
        self.moving_left = False
        self.moving_right = False
    def ai(self, player: MainCharacter, screen_scroll) -> None:
        if self.alive and player.alive:
            if self.idling == False and random.randint(1,200) == 1:
                self.idle()
                self.long_attackj = False
                self.idling_counter = 50
            #near player
            # if pygame.sprite.collide_rect(self, player) and player.health> 80:
            #     self.idle()
            #     self.close_attacking = True
            # else:
            #     self.close_attacking = False
            if self.vision.colliderect(player.rect) and self.energy > 0:
                #stop running and face:
                self.idle()
                self.long_attackj = True
                self.enemy_cooldown = 50

            if self.idling == False:
                self.long_attackj = False
                TILE_SIZE = random.randint(50, 120)
                if self.direction is False:
                    self.moving_right = True
                else:
                    self.moving_left = True
                self.moving_right = not self.moving_left
                self.move_counter +=1
                #update vision:
                self.vision.center = (self.rect.centerx + (220/2) * (-1 if self.direction else 1), self.rect.centery)
                if self.move_counter > TILE_SIZE:
                    self.moving_right = self.moving_left
                    self.moving_left = not self.moving_left
                    self.move_counter *= -1
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False

        else:
            self.long_attackj = False
            self.close_attacking = False
        #scroll
        self.rect.x += screen_scroll