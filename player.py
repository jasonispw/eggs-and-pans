import pygame
import random
import os

os.chdir("c:/Users/jason/OneDrive/Bureaublad/python/game")




# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("chath the eggs ")

pygame.mixer.music.load("game_muziek.wav")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

click_sound = pygame.mixer.Sound('click.wav')
click_sound.set_volume(1)

buzz = pygame.mixer.Sound("wrong.mp3")



# Game variables
    #beeld
screen_x = 600
screen_y = 600
screen = pygame.display.set_mode((screen_x, screen_y))
    #player
player_image = pygame.image.load("player.png")
player_rect = player_image.get_rect()
player_x = 250
player_y = 400
player_speed = 7.5
    #ei
clones = []
clone_image = pygame.image.load("image.png")
gravity = 5
clone_timer = 1.75
elapsed_time = 0
clock = pygame.time.Clock()
random_egg = 1

    #eieren
eieren =  0
multiplier = 0
eieren_points = 1
eieren_sise_x = 15
eieren_sise_y = 15
roundet_eieren = round(eieren, 1)
    #balk onder in het beeld
rect_1_x = 0
rect_1_y = screen_y - 100
rect_1_width = screen_x
rect_1_height = 100
rect_1_color = (150, 150, 150)
    #upgrade button 1

upgrade_button = pygame.image.load("upgrade_button.png")
upgrade_rect = upgrade_button.get_rect()
upgrade_rect.x = 490
upgrade_rect.y = screen_y -100
upgrade_cost = 10
upgrade_level = 0
upgrade_level_cost = 0
    #upgrade button 2
upgrade_button_1 = pygame.image.load("upgrade1.png")
upgrade_rect_1 = upgrade_button_1.get_rect()
upgrade_rect_1.x = 270
upgrade_rect_1.y = 500
upgrade_cost_1 = 20
upgrade_level_1 = 0
upgrade_level_cost_1 = 0
max_2 = False

Knop_L = pygame.image.load("knop_L.png")
Knop_R = pygame.image.load("knop_R.png")
Knop_L_rect = Knop_L.get_rect()
Knop_R_rect = Knop_R.get_rect()
Knop_L_rect.x = 5
Knop_L_rect.y = 425
Knop_R_rect.x = 500
Knop_R_rect.y = 425



# Load images
def load_images():
    global player_image, player_rect, clone_image
    player_image = pygame.image.load("player.png")
    player_rect = player_image.get_rect()
    player_rect.x = player_x
    player_rect.y = player_y
    
    

    
    clone_image = pygame.image.load("image.png")



# Draw the game
def draw_game():
    achtergrond_img = pygame.image.load('achtergrond1.png')
    screen.blit(achtergrond_img, (0, 0))
    #balk onderaan
    pygame.draw.rect(screen, rect_1_color, (rect_1_x, rect_1_y, rect_1_width, rect_1_height))
    #de rest
    screen.blit(upgrade_button, upgrade_rect)
    font = pygame.font.Font(None, 30)
    font_1 = pygame.font.Font(None, 25)
    text = font.render(f"eieren: {round(eieren, 1)} ", True, (0, 0, 0))
    text_cost_1 = font_1.render("cost: " + str(upgrade_cost) ,True,  (200, 200, 200))
    text_rect = text.get_rect()
    text_rect = (400, 550)
    if max_2 == True:
        text_cost_2 = font_1.render("    max", True, (200, 200, 200))
    else:
        text_cost_2 = font_1.render("cost:" + str (upgrade_cost_1), True, (200, 200, 200))
    text_rect_1 = text_cost_2.get_rect()
    text_rect_1 = (190, 550)
    screen.blit(text_cost_2, text_rect_1)
    screen.blit(text_cost_1, text_rect)
    screen.blit(text, (eieren_sise_x, eieren_sise_y))
    screen.blit(player_image, player_rect)
    screen.blit(upgrade_button, upgrade_rect)
    screen.blit(upgrade_button_1, upgrade_rect_1)
    screen.blit(Knop_L, (5, 425))
    screen.blit(Knop_R ,(500, 425))
    for clone in clones:
        screen.blit(clone_image, (clone.x, clone.y))

# Handle player movement
def handle_player_movement():
    global player_x, player_y, player_rect, event
    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if Knop_L_rect.collidepoint(mouse_x, mouse_y):
            player_x -= player_speed
        if Knop_R_rect.collidepoint(mouse_x, mouse_y):
            player_x += player_speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if player_x > 0:
            player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if player_x < screen_x - player_rect.width:
            player_x += player_speed
    player_rect.x = player_x
    player_rect.y = player_y


# Spawn new clones
def spawn_clones():
    global elapsed_time, clones, random_egg ,random
    dt = clock.tick(30) / 1000
    elapsed_time += dt
    for clone in clones:
        clone.y += gravity
    if elapsed_time >= clone_timer:
        new_clone = clone_image.copy()
        new_clone_rect = new_clone.get_rect()
        new_clone_rect.x = random.randint(100 , screen_x - 100 - new_clone_rect.width)
        new_clone_rect.y = 0
        clones.append(new_clone_rect)
        elapsed_time = 0

# Handle collisions and update eieren
def handle_collisions():
    global eieren
    if player_rect:
        for clone in clones:
            if player_rect.colliderect(clone):
                sound1 = pygame.mixer.Sound('plop1.wav')
                sound2 = pygame.mixer.Sound('plop2.wav')
                selected_sound = random.choice([sound1, sound2])
                selected_sound.set_volume(0.5)
                selected_sound.play()
                eieren += multiplier
                eieren += eieren_points 
                clones.remove(clone)
    else:
        for clone in clones: screen.blit(clone_image, (clones.x, clones.y))
# upgrade button egg points
def upgrade_button_egg():
    global upgrade_level_cost, upgrade_cost, upgrade_level, multiplier
    #upgrade levels met multiplayer
    if upgrade_level_cost >= 5:
        if upgrade_level_cost >= 11:
            if upgrade_level_cost >= 19:
                if upgrade_level_cost >= 24:
                    if upgrade_level_cost >= 32:
                        if upgrade_level_cost >= 39:
                            if upgrade_level_cost >= 46:
                                if upgrade_level_cost >= 54:
                                    if upgrade_level_cost >= 61:
                                        if upgrade_level_cost >= 68:
                                            upgrade_cost += 190
                                        else:
                                            upgrade_cost += 170
                                    else:
                                        upgrade_cost += 150
                                else:
                                    upgrade_cost += 130
                            else: 
                                upgrade_cost += 110
                        else:
                            upgrade_cost += 90
                    else:
                        upgrade_cost += 70
                else:
                    upgrade_cost += 50
            else:
                upgrade_cost+= 30
        else: 
            upgrade_cost += 15
    else:
        upgrade_cost += 10
    if upgrade_level >= 5:
        if upgrade_level>= 15:
            if upgrade_level >= 30:
                if upgrade_level >= 45:
                    if upgrade_level >= 53:
                        if upgrade_level >= 68:
                            multiplier += 2.2
                        else: multiplier += 2
                    else:
                        multiplier += 1.9
                else:
                    multiplier += 1.8
            else:
                multiplier += 1.6
        else:
            multiplier += 1.5
    else:
        multiplier += 1

# upgrade button egg faling
def upgrade_button_egg_faling():
    global upgrade_cost_1, upgrade_level_cost_1, upgrade_level_1, upgrade_clicked_1, clone_timer, max_2, gravity
    if upgrade_level_cost_1 >= 1:
        if upgrade_level_cost_1 >= 2:
            if upgrade_level_cost_1 >= 3:
                if upgrade_level_cost_1 >= 4:
                    if upgrade_level_cost_1 >= 5:
                        if upgrade_level_cost_1 >= 6:
                            upgrade_clicked_1 = True
                    else:
                        upgrade_cost_1 += 90
                else:
                    upgrade_cost_1 += 75
            else:
                upgrade_cost_1 += 50
        else:
            upgrade_cost_1 += 30
    else:
        upgrade_cost_1 += 15

    if upgrade_level_1 >= 0:
        clone_timer -= 0.10
        gravity += 0.5
        if upgrade_level_1 >= 6:
            max_2 = True
            upgrade_clicked_1 = True
            
# Main game loop
load_images()
running = True
upgrade_clicked = False
upgrade_clicked_1 = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # upgrade eggs
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if upgrade_rect.collidepoint(mouse_x, mouse_y):
                if not upgrade_clicked:
                    if eieren >= upgrade_cost:
                        upgrade_level += 1
                        upgrade_level_cost += 1
                        eieren -= upgrade_cost
                        upgrade_button_egg()
                        upgrade_clicked = False
                    else:
                        buzz.play()
                        
        #upgrade faling eggs
            if upgrade_rect_1.collidepoint(mouse_x, mouse_y):
                if not upgrade_clicked_1:
                    if eieren >= upgrade_cost_1:
                        upgrade_level_1 += 1
                        upgrade_level_cost_1 += 1
                        eieren -= upgrade_cost_1
                        upgrade_button_egg_faling()
                        
                    else:
                        buzz.play()
    handle_player_movement()
    spawn_clones()
    handle_collisions()
    draw_game()
    pygame.display.update()

pygame.quit()
