"""
Neural Network
"""
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    """
    构建神经网络：两个卷积层，两个全连接层
    """
    def __init__(self):
        super(Net, self).__init__()
        self.conv_1 = nn.Conv2d(1, 1, 5, 1, 0)  # 输入单通道1 * 10 * 10
        self.conv_2 = nn.Conv2d(1, 1, 3, 1, 0)  # 输入单通道1 * 6 * 6， 输出 1 * 4 * 4
        self.Linear_1 = nn.Linear(16, 8)
        self.Linear_1.weight.data.normal_(0, 0.1)
        self.Linear_2 = nn.Linear(8, 4)  # 输出4个action
        self.Linear_2.weight.data.normal_(0, 0.1)

    def forward(self, x):
        x = F.relu(self.conv_2(F.relu(self.conv_1(x))))
        x = x.view(x.size(0), -1)  # flatten
        action = self.Linear_2(F.relu(self.Linear_1(x)))
        return action


if __name__ == '__main__':
    net = Net()
    x = torch.ones(1, 1, 10, 10)
    action = net.forward(x)
    print(torch.argmax(action[0]).numpy())  # 找最大值索引


