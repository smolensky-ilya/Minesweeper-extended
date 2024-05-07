import pygame

# init everything
pygame.init()
screen = pygame.display.set_mode((1200, 800))

# shapes
player = pygame.Rect((300, 250, 50, 50))  # creating the shape


run = True
while run:
    screen.fill((0, 0, 0))  # this is necessary to fill in the screen every time with a colour to update it
    # drawing shapes
    pygame.draw.rect(screen, 'red', player)  # actually drawing the shape

    # getting the pressed key
    key = pygame.key.get_pressed()
    # checking what key was pressed and doing stuff
    if key[pygame.K_a]:  # these are keyboard keys
        player.move_ip(-1, 0)  # these are coordinates
    elif key[pygame.K_d]:
        player.move_ip(1, 0)
    elif key[pygame.K_w]:
        player.move_ip(0, -1)
    elif key[pygame.K_s]:
        player.move_ip(0, 1)


    # checking if the QUIT button was pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # updating the screen to see changes in each loop
    pygame.display.update()

# quitting
pygame.quit()
