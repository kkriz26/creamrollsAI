import os

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


#modify these three commented sections when modifying the layers and their sizes
class linear_qnet(nn.Module):
    #def __init__(self, input_size, hidden_size, output_size):
    def __init__(self, input_size, hidden_size, hidden_size2, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size2)
        self.linear4 = nn.Linear(hidden_size2, output_size)


        '''        self.linear2 = nn.Linear(hidden_size, hidden_size2)
        self.linear3 = nn.Linear(hidden_size2, hidden_size3)
        self.linear4 = nn.Linear(hidden_size3, hidden_size4)
        self.linear5 = nn.Linear(hidden_size4, hidden_size5)
        self.linear6 = nn.Linear(hidden_size5, output_size)'''



    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        x = self.linear4(x)
        #x = self.self.linear5(x)


        return x
    
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        #self.optimizer = optim.SGD(model.parameters(), lr=self.lr, momentum=0.9)
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train(self, state, action, reward, next_step, done):
        state = torch.tensor(state, dtype=torch.float)
        next_step = torch.tensor(next_step, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_step = torch.unsqueeze(next_step, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )
        pred = self.model(state)
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_step[idx]))
            target[idx][torch.argmax(action).item()] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()
    
