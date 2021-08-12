import pygame
import sys
import time
monster = [33, 37]
start_position = 97
step = 50
target = 4  # 目标位置
# 107是为了防止在初始位置往下走
wall = [107, 0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 19, 29, 39, 49, 59, 69, 79, 89, 99, 91, 92, 93, 94, 95, 96, 98]
kill_wait_time = 2
is_killed = False


class Env:
    def __init__(self):
        super(Env, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        # self.title("Q-learning shoot game")
        self.size = width, height = 500, 500  # 设置窗口大小
        self.screen = pygame.display.set_mode(self.size)  # 显示窗口
        # clock = pygame.time.Clock()  # 设置时钟
        self.background_color = (255, 255, 255)  # 设置颜色
        self.person = start_position
        self.monster = [33, 37]
        self.draw_map()

    def draw_map(self):
        """
        :param person:当前人的位置
        :param monster: 当前怪兽的位置
        :return:
        """
        # width、height已经给出
        # 长/宽的三分之一，为一个格子的长宽
        # 表示九个格子
        rect = [0] * 110
        self.screen.fill(self.background_color)  # 填充颜色(设置为0，执不执行这行代码都一样)
        for i in range(10):
            for j in range(10):
                curr_rect = 10 * i + j
                if target == curr_rect:
                    # 绿色表示终点
                    rect[curr_rect] = pygame.draw.rect(self.screen, (0, 228, 0), ((j * step, i * step), (step, step)), width=0)
                elif curr_rect in wall:
                    # 灰色表示墙
                    rect[curr_rect] = pygame.draw.rect(self.screen, (192, 192, 192), ((j * step, i * step), (step, step)), width=0)
                elif curr_rect == self.person:
                    # 红色表示人
                    rect[curr_rect] = pygame.draw.rect(self.screen, (192, 0, 0), ((j * step, i * step), (step, step)), width=0)
                elif curr_rect in monster:
                    # 画出怪兽
                    rect[curr_rect] = pygame.draw.rect(self.screen, (138, 43, 226), ((j * step, i * step), (step, step)), width=0)
                else:
                    # 其余填充白色
                    rect[curr_rect] = pygame.draw.rect(self.screen, (255, 228, 181), ((j * step, i * step), (step, step)), width=1)
        pygame.display.update()

    def judge_win(self):
        """
        如果人到达终点， 则胜利
        :return: True or False
        """
        if self.person == target and is_killed == True:
            return True
        else:
            return False

    def reset(self):
        self.person = start_position
        self.monster = [33, 37]
        print(self.person)
        return self.person, self.monster

    def judge_collision(self, temp_person):
        """判断人是否碰撞到墙或怪物"""
        if temp_person in wall or temp_person in monster or temp_person < 0:
            return True
        else:
            return False

    def kill_monster(person, monster, time):
        """
        人静止两秒且怪物在攻击范围内才能杀死怪物
        人的攻击范围是：
        :param person:人当前的位置
        :param monster: 怪兽当前的位置
        :return: 返回怪兽坐标， 如果杀死怪兽了返回[-1, -1]
        """
        if time < kill_wait_time:
            # print("time short")A
            # 攻击时间小于两秒直接返回， 杀不死怪兽
            return monster
        attack_area = [person-1, person-2, person-3, person, person + 1, person+2, person + 3,\
                   person-13, person-12, person - 11, person - 10, person - 9, person - 8, person -7,\
                   person-23, person-22, person - 21, person - 20, person - 19, person - 18, person -17,\
                   person+13, person+12, person + 11, person + 10, person + 9, person + 8, person + 7]
        if monster[0] in attack_area and monster[1] in attack_area:
            print("kill monster!")
            return [-1, -1]
        else:
            return monster

        # 走一步（机器人实施 action）

    def step(self, action):
        # s状态
        s = self.person

        # 移动机器人, 直接更新下一个state
        if action == 0:  # 上
            s_ = s - 10
            is_collision = self.judge_collision(s_)
            if is_collision:
                s_ = s
        elif action == 1:  # 下
            s_ = s + 10
            is_collision = self.judge_collision(s_)
            if is_collision:
                s_ = s

        elif action == 2:  # 右
            s_ = s + 1
            is_collision = self.judge_collision(s_)
            if is_collision:
                s_ = s

        elif action == 3:  # 左
            s_ = s - 1
            is_collision = self.judge_collision(s_)
            if is_collision:
                s_ = s

        # 奖励机制
        if s_ == target:
            # 找到宝藏，奖励为 1
            reward = 1
            done = True
            # 终止
            print("通关，好棒!")
        elif s_ in monster:
            # 踩到炸弹1，奖励为 -1
            reward = -1
            done = True
            print("碰到怪兽")
        else:
            # 其他格子，没有奖励
            reward = 0
            # 非终止
            done = False
        if is_collision:
            # 碰撞返回-0.5奖励
            reward = -0.5
            done = False
            print("碰壁")
        return s_, reward, done

'''
if __name__ == '__main__':
    pygame.init()  # 初始化pygame
    size = width, height = 500, 500  # 设置窗口大小
    screen = pygame.display.set_mode(size)  # 显示窗口
    clock = pygame.time.Clock()  # 设置时钟
    background_color = (255, 255, 255)  # 设置颜色
    person = start_position
    draw_map(person, monster)
    start_time = time.time()
    while True:  # 死循环确保窗口一直显示
        clock.tick(100)  # 每秒执行100次
        time_now = time.time()
        time_ep = time_now- start_time
        # print(time_ep)
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    person -= 10
                    # 判断是否碰撞
                    is_collision = judge_collision(person)
                    if is_collision:
                        person += 10
                    is_kill_monster = kill_monster(person, monster, time_ep)
                    print(time_ep)
                    if is_kill_monster == [-1, -1]:
                        # 怪兽已经杀死
                        is_killed = True
                        monster = [102, 103]
                    is_win = JudgeWin()
                    print(is_win)
                    if is_win is True:
                        person, monster = reset()
                        is_killed = False
                    draw_map(person, monster)
                    start_time = time.time()

                if event.key == pygame.K_DOWN:
                    person += 10
                    is_collision = judge_collision(person)
                    if is_collision:
                        person -= 10
                    print(time_ep)
                    is_kill_monster = kill_monster(person, monster, time_ep)
                    if is_kill_monster == [-1, -1]:
                        # 怪兽已经杀死
                        is_killed = True
                        monster = [102, 103]
                    is_win = JudgeWin()
                    if is_win:
                        person, monster = reset()
                    draw_map(person, monster)
                    start_time = time.time()

                if event.key == pygame.K_LEFT:
                    person -= 1
                    is_collision = judge_collision(person)
                    if is_collision:
                        person += 1
                    is_kill_monster = kill_monster(person, monster, time_ep)
                    if is_kill_monster == [-1, -1]:
                        # 怪兽已经杀死
                        is_killed = True
                        monster = [102, 103]
                    is_win = JudgeWin()
                    if is_win:
                        person, monster = reset()
                    draw_map(person, monster)
                    start_time = time.time()

                if event.key == pygame.K_RIGHT:
                    person += 1
                    is_collision = judge_collision(person)
                    if is_collision:
                        person -= 1
                    is_kill_monster = kill_monster(person, monster, time_ep)
                    if is_kill_monster == [-1, -1]:
                        # 怪兽已经杀死
                        is_killed = True
                        monster = [102, 103]
                    is_win = JudgeWin()
                    if is_win:
                        person, monster = reset()
                    draw_map(person, monster)
                    start_time =time.time()

    pygame.quit()  # 退出pygame

'''