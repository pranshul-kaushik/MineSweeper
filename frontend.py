import pygame as pg

white =(255,255,255)
black =(0,0,0)
pg.init()
gameDisplay = pg.display.set_mode((1350,700))
pg.display.set_caption("MineSweeper")
gameDisplay.fill(white) 
gameExit =False

scale_x =100
scale_y =100

next_line_x =0
next_line_y =0

while not gameExit:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                gameExit= True
    
    pg.draw.line(gameDisplay ,black ,(next_line_x,0),(next_line_x,700),1)
    pg.draw.line(gameDisplay ,black ,(0,next_line_y),(1350,next_line_y),1)
    print((next_line_x ,next_line_y))
    
    next_line_x=(next_line_x+ scale_x)%1350
    next_line_y=(next_line_y+ scale_y)%700


    pg.display.update()    

pg.quit()
quit()