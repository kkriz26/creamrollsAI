import math
import os
import random
from collections import deque

#import helper
import numpy as np
import torch

import kremroleAI
import model

MAX_MEM = 100_000
BATCH_SIZE = 1000
#LR = 0.0001
LR = 0.0001
def save_ngames(ngames):
    f = open("model/ngames.txt", "w")
    f.write(str(ngames))
    f.close()






class Agent:
    def __init__(self):
        self.n_games = 0
        if os.path.exists("model/ngames.txt"):
            f = int(open("model/ngames.txt", "r").read().strip())
            print("file exists {}".format(f))

            if f > 0:
                self.n_games = f
                print("resuming...")
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEM)
        # 38, 128, 128, 5 worked for large matrix with discretized space (using only one enemy on screen at time), for 10 parameters, 10, 512, 5 or 10, 1024, 5 were successfully used
        #in that case, make sure to modify model file accordingly
        self.model = model.linear_qnet(38, 128, 128, 5)
        if os.path.exists('model/model.pth'):
            self.model.load_state_dict(torch.load('model/model.pth'))
            self.model.eval()
        self.trainer = model.QTrainer(self.model, lr=LR, gamma=self.gamma)
        

    def get_state(self):
        
        player_rect = kremroleAI.player.rect
        hittingXleft, hittingXright, hittingYdown, hittingYup = False, False, False, False
        #print(player_x, player_y)
        if player_rect.left == 0:
            hittingXleft = True
        if player_rect.right == 800:
            hittingXright = True
        if player_rect.top == 0:
            hittingYup = True
        if player_rect.bottom == 600:
            hittingYdown = True

        if player_rect.left < 60:
            AhittingXleft = True
        if player_rect.right > 740:
            AhittingXright = True
        if player_rect.top < 60:
            AhittingYup = True
        if player_rect.bottom > 540:
            AhittingYdown = True
        
        largelist = []
        treadmilllist = []
        enemylist = []
        platypuslist = []

        left, right, top, bottom = False, False, False, False
        topright, downright, secondlayertowall= False, False, False
        for i in range(1,2):
            enemylist.append([0, 0])
            treadmilllist.append([0, 0])
            #discretization of space to bins. 
        onex, twox, threex, fourx, fivex, sixx, sevenx, eightx, oney, twoy, threey, foury, fivey, sixy, seveny, eighty, niney, teny, eleveny = False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False
        ponex, ptwox, pthreex, pfourx, pfivex, psixx, psevenx, peightx, poney, ptwoy, pthreey, pfoury, pfivey, psixy, pseveny, peighty, pniney, pteny, peleveny = False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False
        #print(lowdangerx)
        if player_rect.centerx in range(0, 100):
            ponex = True
        if player_rect.centerx in range(101, 200):
            ptwox = True
        if player_rect.centerx in range(201, 300):
            pthreex = True
        if player_rect.centerx in range(301, 400):
            pfourx = True
        if player_rect.centerx in range(401, 500):
            pfivex = True
        if player_rect.centerx in range(501, 600):
            psixx = True
        if player_rect.centerx in range(601, 700):
            psevenx = True
        if player_rect.centerx in range(701, 800):
            peightx = True

        if player_rect.centery in range(0, 50):
            poney = True
        if player_rect.centery in range(51, 100):
            ptwoy = True
        if player_rect.centery in range(151, 200):
            pthreey = True
        if player_rect.centery in range(201, 250):
            pfoury = True
        if player_rect.centery in range(251, 300):
            pfivey = True
        if player_rect.centery in range(301, 350):
            psixy = True
        if player_rect.centery in range(351, 400):
            pseveny = True
        if player_rect.centery in range(401, 450):
            peighty = True
        if player_rect.centery in range(451, 500):
            pniney = True
        if player_rect.centery in range(501, 550):
            pteny = True
        if player_rect.centery in range(551, 600):
            peleveny = True
        for idx, sprite in enumerate(kremroleAI.enemies):

            if math.sqrt((player_rect.top -sprite.rect.bottom)**2) < 51 and player_rect.top > sprite.rect.bottom and (player_rect.right in range(sprite.rect.left -20, sprite.rect.right) or player_rect.left in range(sprite.rect.left, sprite.rect.right)  ):
                top = True
            
            if math.sqrt((player_rect.right -sprite.rect.left)**2) < 61 and player_rect.right < sprite.rect.left and (sprite.rect.top in range(player_rect.top, player_rect.bottom) or sprite.rect.bottom in range(player_rect.top, player_rect.bottom)):
                if sprite.rect.centery < player_rect.centery:
                    topright = True
                else:
                    downright = True
                right = True
            if  player_rect.right > 740 or player_rect.left < 60 or player_rect.top < 60 or player_rect.bottom > 600:
                secondlayertowall = True
                
            if math.sqrt((player_rect.bottom -sprite.rect.top)**2) < 51 and player_rect.bottom < sprite.rect.top and (player_rect.right in range(sprite.rect.left -20, sprite.rect.right) or player_rect.left in range(sprite.rect.left, sprite.rect.right) ):
                bottom = True
            if math.sqrt((player_rect.left -sprite.rect.right)**2) < 51 and player_rect.left > sprite.rect.right and (sprite.rect.top in range(player_rect.top, player_rect.bottom) or sprite.rect.bottom in range(player_rect.top, player_rect.bottom)):
                left = True

            if sprite.rect.centerx in range(0, 100):
                onex = True
            if sprite.rect.centerx in range(101, 200):
                twox = True
            if sprite.rect.centerx in range(201, 300):
                threex = True
            if sprite.rect.centerx in range(301, 400):
                fourx = True
            if sprite.rect.centerx in range(401, 500):
                fivex = True
            if sprite.rect.centerx in range(501, 600):
                sixx = True
            if sprite.rect.centerx in range(601, 700):
                sevenx = True
            if sprite.rect.centerx in range(701, 800):
                eightx = True

            if sprite.rect.centery in range(0, 50):
                oney = True
            if sprite.rect.centery in range(51, 100):
                twoy = True
            if sprite.rect.centery in range(151, 200):
                threey = True
            if sprite.rect.centery in range(201, 250):
                foury = True
            if sprite.rect.centery in range(251, 300):
                fivey = True
            if sprite.rect.centery in range(301, 350):
                sixy = True
            if sprite.rect.centery in range(351, 400):
                seveny = True
            if sprite.rect.centery in range(401, 450):
                eighty = True
            if sprite.rect.centery in range(451, 500):
                niney = True
            if sprite.rect.centery in range(501, 550):
                teny = True
            if sprite.rect.centery in range(551, 600):
                eleveny = True

        for idx, sprite in enumerate(kremroleAI.treadmills):
            #print(idx)
            #enemylist[idx] = [ sprite.rect.x, sprite.rect.y ]
            distx = math.sqrt((sprite.rect.x - player_x)**2)
            disty = math.sqrt((sprite.rect.y - player_y)**2)
            if sprite.rect.x < player_x and math.sqrt((sprite.rect.y - player_y)**2) < 70 and distx < 70 and sprite.rect.y < player_y:
                lefttopT = True
            elif sprite.rect.x < player_x and math.sqrt((sprite.rect.y - player_y)**2) < 70 and distx < 70 and sprite.rect.y >= player_y:
                leftdownT = True
            elif sprite.rect.x >= player_x and math.sqrt((sprite.rect.y - player_y)**2) < 70 and disty < 100 and sprite.rect.y < player_y:
                righttopT = True
            elif sprite.rect.x >= player_x and math.sqrt((sprite.rect.y - player_y)**2) < 70 and disty < 100 and sprite.rect.y >= player_y:
                rightdownT = True
                
            
        largelist.append(onex)
        largelist.append(twox)
        largelist.append(threex)
        largelist.append(fourx)
        largelist.append(fivex)
        largelist.append(sixx)
        largelist.append(sevenx)
        largelist.append(eightx)
        largelist.append(oney)
        largelist.append(twoy)
        largelist.append(threey)
        largelist.append(foury)
        largelist.append(fivey)
        largelist.append(sixy)
        largelist.append(seveny)
        largelist.append(eighty)
        largelist.append(niney)
        largelist.append(teny)
        largelist.append(eleveny)
        
        largelist.append(ponex)
        largelist.append(ptwox)
        largelist.append(pthreex)
        largelist.append(pfourx)
        largelist.append(pfivex)
        largelist.append(psixx)
        largelist.append(psevenx)
        largelist.append(peightx)
        largelist.append(poney)
        largelist.append(ptwoy)
        largelist.append(pthreey)
        largelist.append(pfoury)
        largelist.append(pfivey)
        largelist.append(psixy)
        largelist.append(pseveny)
        largelist.append(peighty)
        largelist.append(pniney)
        largelist.append(pteny)
        largelist.append(peleveny)
        

        platypuslist.append(hittingXleft)
        platypuslist.append(hittingXright)
        platypuslist.append(hittingYdown)
        platypuslist.append(hittingYup)

        platypuslist.append(top)
        #platypuslist.append(right)
        platypuslist.append(topright)
        platypuslist.append(downright)
        platypuslist.append(secondlayertowall)
        platypuslist.append(left)
        platypuslist.append(bottom)


        #print(platypuslist)
        #print("---")
        #print(enemylist)
        #objectlist = enemylist.copy()
        #objectlist.append([player_x, player_y])
        #state = np.array(objectlist, dtype=int).flatten()

        #----------Here switch between two alternative inputs. either discretization into space bins or seeing only objects nearby player. FOr the first option, training on multiple enemies on a screen is difficult and also smaller matrices have to be used.
        #state = np.array(platypuslist, dtype=int).flatten()
        state = np.array(largelist, dtype=int).flatten()
        print(state)

        return state

    def remember(self, state, action, reward, next_step, done):
        self.memory.append((state, action, reward, next_step, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_steps, dones = zip(*mini_sample)
        self.trainer.train(states, actions, rewards, next_steps, dones)
        
    def train_short_memory(self, state, action, reward, next_step, done):
        self.trainer.train(state, action, reward, next_step, done)
        
    def get_action(self, state):
        self.epsilon = 100 - self.n_games
        final_move = [0,0,0,0,0]

        rndnum = random.randint(0, 200)
        if rndnum < self.epsilon:
            move = random.randint(0,4)
            final_move[move] = 1
          #  print(final_move)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            #print(state0)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
          #  print(final_move)
        return final_move
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    agent = Agent()
    running = kremroleAI.running
    while running:
        state_old = agent.get_state()
        final_move = agent.get_action(state_old)
        kremroleAI.playstep(final_move)
        reward, done, score, record = kremroleAI.reward, kremroleAI.done, kremroleAI.counter, kremroleAI.record
        print(reward, done, score, record)
        state_new = agent.get_state()
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)
        if kremroleAI.running == False and score > record:
            agent.model.save()

        if done:
            print("DONE")
            agent.n_games += 1
            save_ngames(agent.n_games)
            agent.train_long_memory
            if score > record:
                print("Record: %s".format(record))
                record = score
                agent.model.save()
                #print('Game', agent.n_games,'score', score, 'record', record)
                

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            kremroleAI.wipe_score()

            print(agent.n_games)

    
if __name__ == '__main__':
    train()