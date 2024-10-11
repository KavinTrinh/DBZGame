import pygame
from World import World
from Character import MainCharacter, EnemyCharacter
from Item import ItemBox, HealthBar
from game_function import game_settings, draw_bg, collision, draw_text, scale_image, Monitor, draw_menu_buttons, draw_restart_button, reset_level, complete_level

def pre_game() -> pygame:
    SCREEN_WIDTH, BG = game_settings()
    screen = Monitor(SCREEN_WIDTH, BG)
    return screen
def play_game(screen: pygame) -> None:
    #set framerates
    clock = pygame.time.Clock()
    start_game = False
    #sprites group
    skill_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    exits = pygame.sprite.Group()
    decoration_group = pygame.sprite.Group()




    #Draw
    character_group = pygame.sprite.Group()
    # player = MainCharacter('Goku',1,200,200,2, 5)
    # health_bar = HealthBar(10, 10, player.health, player.max_health)
    # character_group.add(player)
    # acted_goku = EnemyCharacter('Goku',1,500,200,2, 2)
    # nappa = EnemyCharacter('Nappa',1,300,200,2.6, 2)
    # character_group.add(acted_goku)
    # character_group.add(nappa)

    #Main game loop
    world = World(screen)
    player, health_bar = world.process_data(character_group, item_group, decoration_group, exits)
    #load images
        
    end_game = False
    while not end_game:
        clock.tick(59)
 
        if start_game == False:
            #main game menu
            # screen.canvas.fill(screen.background)
            BG = pygame.image.load('Background/Kamehouse.jpg').convert_alpha()
            BG = pygame.transform.scale(BG, (int(BG.get_width() * 0.55), int(BG.get_height() * 0.55)))
            screen.canvas.blit(BG, (10,0))
            start_game, end_game = draw_menu_buttons(screen)
        else:
            draw_bg(screen, world.sky_img, world.top_img, world.mid_img, world.bot_img)
            #draw the world
            health_bar.draw(screen, player.health)  
            draw_text(screen, f'ENERGY: {player.energy}', (255,255,255), 10, 35)
            draw_text(screen, f'DRAGON BALLS: ', (255,255,255), 10, 60)
            for x in range(len(player.balls)):
                scaled_image = scale_image(player.balls[x].image, 0.6)
                screen.canvas.blit(scaled_image, (180 + (x*23), 56))
            # player.update()
            # acted_goku.update()
            # player.draw(screen) 
            # acted_goku.draw(screenddddd
            # print(f'screen_scroll là {screen_scroll}')

            for character in character_group:
                 if not character.is_player:
                    character.ai(player, screen.screen_scroll)
                    _ = character.update(screen, skill_group, world.obj_list, screen.screen_scroll, screen.bg_scroll, world.level_length)
                    character.draw(screen)
            
            screen.screen_scroll = player.update(screen, skill_group, world.obj_list, screen.screen_scroll, screen.bg_scroll, world.level_length)
            player.draw(screen)
            screen.bg_scroll -= screen.screen_scroll
            if complete_level(player, exits, world):
                screen.screen_scroll = 0
                screen.bg_scroll = 0
                reset_level(character_group, skill_group, explosion_group, item_group, exits, decoration_group)
                world.game_level+=1
                balls = player.balls
                player, health_bar = world.update_level(character_group, item_group, decoration_group, exits)
                player.balls = balls
            if not player.alive:
                screen.screen_scroll = 0
                restart_game = draw_restart_button(screen)
                if restart_game:
                    screen.bg_scroll = 0
                    reset_level(character_group, skill_group, explosion_group, item_group, exits, decoration_group)
                    world = World(screen)
                    player, health_bar = world.process_data(character_group, item_group, decoration_group, exits)


            world.draw(screen.screen_scroll)
            #Draw skill_group
            skill_group.update(character_group, world.obj_list,  screen.screen_scroll)
            skill_group.draw(screen.canvas)
            #Draw explosion group
            explosion_group.update(screen.screen_scroll)
            explosion_group.draw(screen.canvas)

            #Draw item boxes
            item_group.update(player, screen.screen_scroll)
            item_group.draw(screen.canvas)
            
            #Draw decorations
            decoration_group.update(screen.screen_scroll)
            decoration_group.draw(screen.canvas)

            #Draw decorations
            exits.update(screen.screen_scroll)
            exits.draw(screen.canvas)

            #Collision
            collision(character_group, skill_group, explosion_group)

            
        
        
        for event in pygame.event.get():
            #quit the game
            if event.type == pygame.QUIT:
                end_game = True
            #presses the keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end_game = True
                if player.alive:
                    if event.key == pygame.K_a:
                        player.moving_left = True
                    if event.key == pygame.K_d:
                        player.moving_right = True
                    if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        player.jump = True
                    if event.key == pygame.K_j:
                        player.close_attacking = True
                    if event.key == pygame.K_k:
                        player.long_attackj = True
                    if event.key == pygame.K_u:
                        player.long_attacku = True

                        
            #Release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.moving_left = False
                if event.key == pygame.K_d:
                    player.moving_right = False
                if event.key == pygame.K_j:
                    player.close_attacking = False
                if event.key == pygame.K_k:
                    player.long_attackj = False
                if event.key == pygame.K_u:
                    player.long_attacku = False
                
        pygame.display.update()
def main():
    screen = pre_game()
    play_game(screen)

if __name__ == "__main__":
    main()