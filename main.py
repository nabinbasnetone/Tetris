import pygame
import sys
import block
import random

pygame.init()

width, height = 320, 480
silver =  192, 192, 192
bs = 20 #Block Size
block_start_pos_x = 160
block_start_pos_y = 0

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
map = [[0 for _ in range(width//bs)] for _ in range(height//bs)]
map[-1] = [1]*width*bs
for row in map:
    row[0] = 1
    row[-1] = 1
woodcolor = 213, 176, 124
blocks = [block.L, block.aL, block.s, block.z, block.az, block.b, block.c]
keys = pygame.key.get_pressed()

def drawframe():
    pygame.draw.rect(screen, woodcolor, (0,0,bs,height))
    pygame.draw.rect(screen, woodcolor, (0,0,width,bs))
    pygame.draw.rect(screen, woodcolor, (0,460,width,bs))
    pygame.draw.rect(screen, woodcolor, (300,0,bs,height))
    
def drawmap(map):
    for c1, y in enumerate(map):
        for c2, x in enumerate(y):
            if x == 1:
                pygame.draw.rect(screen, silver, ( c2*bs,  c1*bs, bs, bs)) #main body
                pygame.draw.rect(screen, (30, 30, 40), (c2*bs, c1*bs, bs, bs), 1) #for boarder

def updatemap(block, map, cp_x, cp_y):
    for c1, y in enumerate(block):
        for c2, x in enumerate(y):
            if x == 1:
                map[cp_y+c1][cp_x+c2] = 1

def check(map, block, cp_x, cp_y):
    offset = 1
    for c1, y in enumerate(block):
        for c2, x in enumerate(y):
            if x == 1:
                if map[cp_y+c1 + offset][cp_x+c2] == 1:
                    return False
    return True

def checkboarderleft(map, block, cp_x, cp_y):         
    offset = 1
    for c1, y in enumerate(block):
        for c2, x in enumerate(y):
            if x == 1:
                if map[cp_y+c1][cp_x+c2 - offset] == 1:
                    return False
    return True

def checkboarderright(map, block, cp_x, cp_y):         
    offset = 1
    for c1, y in enumerate(block):
        for c2, x in enumerate(y):
            if x == 1:
                if map[cp_y+c1][cp_x+c2 + offset] == 1:
                    return False
    return True

def checkvalidrot(map, cp_x, cp_y, pos): 
    live_block = choosen_blocks[pos]
    for c1, y in enumerate(live_block):
        for c2, x in enumerate(y):
            if x == 1:
                if map[cp_y+c1][cp_x+c2] == 1:
                    return False
    return True

def scoremapupdate(map, score):
    for pos, row in enumerate(map[:-1]):
        check = 1
        for column_ele in row:
            check &= column_ele
        if check == 1:
            score += 1
            del map[pos]
            map.insert(0, [0]*(width//bs))
            for row in map:
                row[0] = 1
                row[-1] = 1
                break
    return score

def gameovercheck(map, score):
    check = 0
    for element in map[1][1:-1]:
        check |= element
    if check == 1:
        run = True
        while run:
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    run = False
            clock.tick(45)
            screen.fill((30, 30, 40))
            text = font.render(f"Your Score is: {score}", True, silver)
            screen.blit(text, (100,240))
            drawframe()
            pygame.display.flip()
        pygame.quit()
        sys.exit()


run = True
choosen_num = random.randrange(len((blocks)))
choosen_blocks = blocks[choosen_num]
pos = 0 
live_block = choosen_blocks[pos]
score = 0
while run:
    clock.tick(45)
    screen.fill((30, 30, 40))
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if checkboarderleft(map, live_block, block_start_pos_x//bs, block_start_pos_y//bs):
                    block_start_pos_x -= 20
            elif event.key == pygame.K_RIGHT:
                if checkboarderright(map, live_block, block_start_pos_x//bs, block_start_pos_y//bs):
                    block_start_pos_x += 20
            elif event.key == pygame.K_SPACE:
                possible_pos = block.block_dict[choosen_num]
                prev_pos = pos
                if pos < possible_pos:
                        pos += 1
                else:
                    pos = 0
                if  checkvalidrot(map, block_start_pos_x//bs, block_start_pos_y//bs, pos):
                    live_block = choosen_blocks[pos]
                else:
                    pos = prev_pos
                    live_block = choosen_blocks[pos]
        
    if check(map, live_block, block_start_pos_x//bs, block_start_pos_y//bs):
        for c1, y in enumerate(live_block):
                for c2, x in enumerate(y):
                    if x == 1:
                        pygame.draw.rect(screen, silver, (block_start_pos_x + c2*bs, block_start_pos_y + c1*bs, bs, bs)) #main body
                        pygame.draw.rect(screen, (30, 30, 40), (block_start_pos_x + c2*bs, block_start_pos_y + c1*bs, bs, bs), 1) #for boarder
    
        block_start_pos_y += 2
    else:
        cp_x = block_start_pos_x//bs
        cp_y = block_start_pos_y//bs
        updatemap(live_block, map, cp_x,cp_y)
        block_start_pos_y = 0
        block_start_pos_x = 160
        choosen_num = random.randrange(len((blocks)))
        choosen_blocks = blocks[choosen_num]
        pos = 0
        live_block = choosen_blocks[pos]
    
    score = scoremapupdate(map, score)
    text = font.render(f"Score: {score}", True, (0, 0, 0))

    
    drawmap(map)
    drawframe()
    screen.blit(text, (120, 4))
    gameovercheck(map, score)
    pygame.display.flip()
pygame.quit()
sys.exit()