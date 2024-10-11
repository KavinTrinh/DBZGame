import pygame
from Character import Character, MainCharacter
from Buttons import Button
from Skills import Explosion
import csv

def world_data(world_list: list, screen, game_level) -> list:
    ROWS, COLS = level_setup(screen)
    for row in range(ROWS):
        r = [-1]* COLS
        world_list.append(r)
    with open(f'level{game_level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile, in enumerate(row):
                world_list[x][y] = int(tile)
    return world_list
def level_setup(screen: pygame) -> tuple:
    ROWS = 16
    COLS = 150
    SCREEN_HEIGHT = screen.get_height()
    TILE_SIZE = SCREEN_HEIGHT//ROWS
    return ROWS, COLS

def game_settings() -> tuple:
    pygame.init()
    width = 800
    height = int(width*0.8)
    BG = (144,201,120)
    return width, BG

def draw_bg(monitor: pygame, sky_img, top_img, mid_img, bot_img)->None:
    SCREEN_HEIGHT = monitor.get_height()
    #Load Images
    BG = monitor.background
    monitor.canvas.fill(BG)
    width = sky_img.get_width()
    bg_scroll = monitor.bg_scroll
    for x in range(5):
        monitor.canvas.blit(sky_img, ((x * width) - bg_scroll * 0.5,0))
        monitor.canvas.blit(top_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - top_img.get_height() - 300))
        monitor.canvas.blit(mid_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - mid_img.get_height() - 150))
        monitor.canvas.blit(bot_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - bot_img.get_height()))
    pygame.display.set_caption('Dragon Ball Z')
def complete_level(player: MainCharacter, exits, world) -> None:
    if pygame.sprite.spritecollide(player, exits, False):
        return True
def collision(characters: Character, skills, explosions) -> None:
    # Check for collisions between skills and characters

    for skill in skills:
        for character in characters:
            if character == skill.shooter:
                continue  # Skip collision check with the shooter
            if pygame.sprite.collide_rect(skill, character):
                if character.alive:  
                    character.health += skill.damage
                    # character.being_hit()
                    character.got_hit = True
                    print(character.health)
                    character.hit_timer = pygame.time.get_ticks() 
                    skill.kill()
                    explosion = Explosion(f'{skill.name}exp', character.rect.x, character.rect.y, 0.6)
                    explosions.add(explosion)
                    break
    # Check for collisions between characters
    for attacker in characters:
        if attacker.close_attacking:
            for victim in characters:
                if victim != attacker and victim.alive and pygame.sprite.collide_rect(attacker, victim):
                    victim.health += attacker.attack_damage
                    # victim.being_hit()
                    victim.got_hit = True
                    victim.hit_timer = pygame.time.get_ticks()
                    print(victim.health)
                    break
    # Reset actions for characters whose hit action duration has expired
    for character in characters:
        if character.hit_timer != 0:
            character.reset_action_after_hit()
    
def draw_text(screen: pygame, text, text_color, x, y)-> None:
    font = pygame.font.SysFont('Futura',30)
    img = font.render(text, True, text_color)
    screen.canvas.blit(img, (x,y))

def scale_image(img, scale)-> pygame:
    scaled_image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    return scaled_image

def draw_menu_buttons(screen) -> tuple[bool,bool]:
    start_but_img = pygame.image.load('Menu Buttons/Start/Start.gif').convert_alpha()
    quit_but_img = pygame.image.load('Menu Buttons/Quit/Quit.gif').convert_alpha()
    start_button = Button(screen, screen.get_width() // 2 - 130, screen.get_height() // 2 - 150, start_but_img, 4)
    quit_button = Button(screen, screen.get_width() // 2 - 110, screen.get_height() // 2 + 50, quit_but_img, 4)
    
    start_pressed = start_button.draw()
    quit_pressed = quit_button.draw()
    
    return (start_pressed, quit_pressed)

def draw_restart_button(screen) -> bool:
    restart_but_img = pygame.image.load('Menu Buttons/Restart/Restart.gif').convert_alpha()
    restart_button = Button(screen, screen.get_width() // 2 - 130, screen.get_height() // 2 - 150, restart_but_img, 4)
    restart_pressed = restart_button.draw()
    return restart_pressed

def reset_level(character_group, skill_group, explosion_group, item_group, exits, decoration_group):
    character_group.empty()
    skill_group.empty()
    explosion_group.empty()
    item_group.empty()
    exits.empty()
    decoration_group.empty()

class Monitor():
    def __init__(self, width, BG):
        self.background = BG
        self.width = width
        self.height = int(width*0.8)
        self.bg_scroll = 0
        self.screen_scroll = 0
        self.canvas = pygame.display.set_mode((self.width, self.height))
        self.TILE_SIZE = self.height / 16

    def get_width(self):
        return self.canvas.get_width()

    def get_height(self):
        return self.canvas.get_height()

    def update_bg_scroll(self, scroll_amount):
        self.bg_scroll = scroll_amount

    def update_screen_scroll(self, scroll_amount):
        self.screen_scroll = scroll_amount