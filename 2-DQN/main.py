# -*- coding: UTF-8 -*-

"""
游戏的主程序，调用DQN和ENV
"""

from game import Env
from DQN import DQN
import pygame

MEMORY_CAPACITY = 100      # 记忆库大小


def update(dqn):
    study = 1
    for episode in range(100):  # 游戏情节
        # 初始化 state（状态）
        state, _ = env.reset()  # state此时是一个数
        # print(state)

        step_count = 0  # 记录走过的步数

        while True:
            # 更新可视化环境

            clock = pygame.time.Clock()  # 设置时钟
            clock.tick(10)  # 每秒执行100次

            tensor_state = dqn.int2tensor(state)
            # RL 大脑根据 state 挑选 action
            action = dqn.choose_action(tensor_state)
            # 探索者在环境中实施这个 action, 并得到环境返回的下一个 state, reward 和 done (是否是踩到炸弹或者找到宝藏)
            state_, reward, done = env.step(action)  # 得到的state_是一个数
            tensor_state_ = dqn.int2tensor(state_)
            dqn.store_transition(tensor_state, action, reward, tensor_state_)
            step_count += 1  # 增加步数

            if step_count > 200:
                break

            # 机器人移动到下一个 state
            state = state_
            print("new state"+ str(state))
            env.person = state

            env.draw_map()
            if dqn.memory_counter > MEMORY_CAPACITY:
                if study == 1:
                    print('2000经验池')
                    study = 0
                dqn.learn(episode)  # 记忆库满了就进行学习
            # 如果踩到炸弹或者找到宝藏, 这回合就结束了
            if not done:
                print('epoch', episode, reward, '游戏未结束')
            elif done:
                print('epoch', episode, reward, '游戏结束')
                print("回合 {} 结束. 总步数 : {}\n".format(episode + 1, step_count))
                break

    # 结束游戏并关闭窗口
    print('game end!')
    pygame.quit()


if __name__ == "__main__":
    # 创建环境 env 和 RL
    pygame.init()  # 初始化pygame
    env = Env()
    mydqn = DQN()
    # 执行update函数
    update(mydqn)
