RL_shoot_game 强化学习射击小游戏
--

使用强化学习训练射击类通关小游戏AI  
  
## 游戏介绍  
  
### 开始游戏  
```
python main.py
```    

### 游戏界面  
![screen](./img/screen.png)  
绿色代表终点，紫色代表怪兽， 灰色代表围墙，红色代表玩家  

### 如何攻击  
角色有效攻击范围如图中红色部分所示, 当怪兽位于攻击范围内时,玩家必须**静止2s**,才能完成怪物的击杀  

![attack](./img/attack.png)

### 如何通关  
必须消灭所有怪物后才能通关， 否则只是相当于移动到终点

### 效果展示
![show](./img/show.gif)

### 关于项目文件 
* game.py 里面定义游戏界面
* q_learning.py Qlearning算法核心
* main.py 主函数， 负责游戏情节迭代
游戏结束会自动生成Q表  

###  时间线
- [x] 完成界面搭建 21-07-23   
- [x] 使用强化学习Q-learning算法实现 21-08-01
- [ ] 添加更多强化学习方法，例如DQN
 