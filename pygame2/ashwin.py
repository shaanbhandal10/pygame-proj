# Messi Vs Ronaldo
import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("James Games!")

GREEN = (79, 235, 52)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(0, HEIGHT//2 - 5, WIDTH, 10)

BULLET_HIT_SOUND = pygame.mixer.Sound('arsh/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('arsh/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont("Oswald", 40)
WINNER_FONT = pygame.font.SysFont("Oswald", 50)


FPS = 100
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
soccer_width, soccer_height = 125, 125

ron_hit = pygame.USEREVENT + 1
mess_hit = pygame.USEREVENT + 2

ronaldo = pygame.image.load(
    os.path.join("arsh", "ronaldo.png"))
RONALDO = pygame.transform.rotate(pygame.transform.scale(
    ronaldo, (soccer_width + 25, soccer_height + 25)), 0 )

messi = pygame.image.load(
    os.path.join("arsh", "messi.png"))
MESSI = pygame.transform.rotate(pygame.transform.scale(
    messi, (soccer_width, soccer_height)), 0)

field = pygame.transform.scale(pygame.image.load(os.path.join("arsh", "soccer.png")), (WIDTH, HEIGHT))  

def draw_window(mess, ron, ron_bullets, mess_bullets, mess_health, ron_health):
    WIN.blit(field, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER )

    mess_health_text = HEALTH_FONT.render(
        "Health: " + str(mess_health), 1, BLACK) 
    ron_health_text = HEALTH_FONT.render(
        "Health: " + str(ron_health), 1, BLACK)
    WIN.blit(mess_health_text, (WIDTH - mess_health_text.get_width() - 10, 10))
    WIN.blit(ron_health_text, (10, 10))

    WIN.blit(RONALDO, (ron.x, ron.y))
    WIN.blit(MESSI, (mess.x, mess.y))


    for bullet in mess_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in ron_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def ronaldo_move(keys_pressed, ron):
    if keys_pressed[pygame.K_s] and ron.x - VEL > -50: #LEFT
        ron.x -= VEL
    if keys_pressed[pygame.K_f] and ron.x + VEL + ron.height < 920: #RIGHT
        ron.x += VEL
    if keys_pressed[pygame.K_e] and ron.y - VEL > BORDER.y - 25: #UP
        ron.y -= VEL
    if keys_pressed[pygame.K_d] and ron.y + VEL + ron.width < HEIGHT: #DOWN
        ron.y += VEL

def messi_move(keys_pressed, mess):
    if keys_pressed[pygame.K_LEFT] and mess.x - VEL > -25: #LEFT
        mess.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and mess.x + VEL + mess.height < 925: #RIGHT
        mess.x += VEL
    if keys_pressed[pygame.K_UP] and mess.y - VEL > -30: #UP
        mess.y -= VEL
    if keys_pressed[pygame.K_DOWN] and mess.y + VEL < 325: #DOWN
        mess.y += VEL

def bullets_move(ron_bullets, mess_bullets, ron, mess):
    for bullet in ron_bullets:
        bullet.y -= BULLET_VEL
        if mess.colliderect(bullet):
            pygame.event.post(pygame.event.Event(mess_hit))
            ron_bullets.remove(bullet)
        elif bullet.y < 0:
            ron_bullets.remove(bullet)

    for bullet in mess_bullets:
        bullet.y += BULLET_VEL
        if ron.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ron_hit))
            mess_bullets.remove(bullet)
        elif bullet.y < 0:
            mess_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() /
                        2, HEIGHT/2 - draw_text.get_height()/2)) 
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    mess = pygame.Rect(400, 0, soccer_width, soccer_height)
    ron = pygame.Rect(400, 750, soccer_width, soccer_height)

    mess_bullets = []
    ron_bullets = []

    mess_health = 15
    ron_health = 15

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(ron_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        ron.x + ron.width, ron.y + ron.height//2 - 2, 10, 5)
                    ron_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(mess_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        mess.x, mess.y + mess.height//2 - 2, 10, 5)
                    mess_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            if event.type == mess_hit:
                mess_health -= 1  
                BULLET_HIT_SOUND.play()

            if event.type == ron_hit:
                ron_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text =""
        if mess_health <= 0:
            winner_text = "Ronaldo wins! SUIIIIIIII"

        if ron_health <= 0:
            winner_text = "Messi wins! I have 7 ballon d'ors"
        
        if winner_text != "":
            draw_winner(winner_text)
            break 


        keys_pressed = pygame.key.get_pressed()
        ronaldo_move(keys_pressed, ron)
        messi_move(keys_pressed, mess)

        bullets_move(ron_bullets, mess_bullets, ron, mess)

        draw_window(mess, ron, mess_bullets, ron_bullets,
                     mess_health, ron_health)

    pygame.quit()

if __name__ == "__main__":
    main()