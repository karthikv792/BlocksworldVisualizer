import os
import pygame
class Instance_Viz:
    def __init__(self):
        self.screen_size = [800,800]
        self.screen = pygame.display.set_mode(self.screen_size, flags=pygame.HIDDEN)
        self.pic_size = (60,60)
        self.offset = 235
        self.blocks = {}
        self.goal_state_block = {}

    def blit_block(self, color, block_pos, goal=False):
        image = ['images/'+i for i in os.listdir('images/') if color in i][0]
        pic = pygame.image.load(image).convert()
        pic = pygame.transform.scale(pic, self.pic_size)
        if not goal:
            self.blocks[color] = block_pos
        self.screen.blit(pic, block_pos)

    def get_state_viz(self,ex_state, goal_state, ind):
        count = 0
        on_blocks = []
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        # Add goal state - currently handles only on predicates
        self.screen.fill((255, 255, 255))
        goal_text_surface = my_font.render('Goal state:', False, (220, 0, 0))
        self.screen.blit(goal_text_surface, (self.screen_size[0]-300,10))
        for predicate in goal_state:
            if 'on ' not in predicate:
                continue
            predicate = predicate.split(' ')
            color, on_color = predicate[1], predicate[2]
            block_pos, on_block_pos = (700-self.pic_size[0]*count-10*count,40), (700-self.pic_size[0]*count-10*count,45+self.pic_size[0])
            self.blit_block(color,block_pos, goal=True)
            self.blit_block(on_color,on_block_pos, goal=True)
            count+=1
        pygame.draw.line(self.screen, (165,42,42), [500, 115+self.pic_size[0]], [790,115+self.pic_size[0]], 10)
        #my font
        text_surface = my_font.render('Holding:', False, (220, 0, 0))
        self.screen.blit(text_surface, (10,10))
        #put table
        pygame.draw.line(self.screen, (165,42,42), [10, 470], [790,470], 10)
        if ind==0:
            curr_state_surface = my_font.render('Initial State', False, (220, 0, 0))
        else:
            print(ind)
            curr_state_surface = my_font.render('State '+str(ind+1), False, (220, 0, 0))
        self.screen.blit(curr_state_surface, (350,490))
        count = 0
        for predicate in sorted(ex_state):
            if 'clear' in predicate or 'handempty' in predicate:
                continue
            if 'ontable' in predicate:
                color = predicate.split(' ')[1]
                block_pos = (self.offset+self.pic_size[0]*count+10*count, 400)
                self.blit_block(color,block_pos)
            elif 'on' in predicate:
                on_blocks.append(predicate.split(' '))
            if 'holding' in predicate:
                color = predicate.split(' ')[1]
                block_pos = (10,40)
                self.blit_block(color,block_pos)
            count+=1
        #Put on block
        for predicate in on_blocks:
            color, on_color = predicate[1], predicate[2]
            block_place = self.blocks[on_color]
            block_pos = (block_place[0], block_place[1]-self.pic_size[0]-5)
            self.blit_block(color,block_pos)

        pygame.display.update()
