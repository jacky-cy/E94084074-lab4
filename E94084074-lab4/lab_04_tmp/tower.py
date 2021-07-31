import pygame
import os
import math

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


GRAY=(128,128,128)

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """

        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """
        x0, y0 = self.center                                     #將塔的中心點座標輸入為x0,y0
        x1, y1 = enemy.get_pos()                                 #將敵人的座標輸入為x1,y1
        distance_A_B = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)    #座標點相減平方相加開根號為敵人與塔之距離:distance_A_B
        if(distance_A_B<=self.radius):                           #要是其距離小於self.radius(塔攻擊半徑)
            iscollide=True                                       #則iscollide為True
        else:
            iscollide=False                                      #否則iscollide為False
        
        
        return iscollide                                         #回傳iscollide(True or False)

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        
                                                                                                      # create semi-transparent surface(建立畫布)
        win_surface = pygame.Surface((1024, 600), pygame.SRCALPHA)
        transparency = 128                                                                            # define transparency: 0~255, 0 is fully transparent
                                                                                                      # draw the circle on the transparent surface
        pygame.draw.circle(win_surface,(128,128,128, transparency), self.center, self.radius )

        win.blit(win_surface, (0,0))                                                                  #將圖形顯現出來
        
        
        return None


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = False  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """

        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """
        if (self.cd_count < self.cd_max_count):                     #利用self.cd_count來計算塔的cd時間~
            self.cd_count += 1                                      
        else :
            self.cd_count=0                                         #要是當達到self.cd_max_count時，冷卻結束
        
        
        return True if self.cd_count else False                     #is_cool_down True 時代表在冷卻
                                                                    #is_cool_down False 時代表在冷卻結束
        
        
        
        
        pass

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        
        enemylist=enemy_group.get()                                                       #建立一個敵人列表
        if(self.is_cool_down()==False):                                                   #判斷塔是否在冷卻
            attack=0                                                                      #並賦予攻擊attack=0(因為冷卻結束就可以攻擊一次)
            for i in range(len(enemylist)):                                               #用for迴圈檢查所有敵人
               
                if(self.range_circle.collide(enemylist[i])==True and attack==0):          #要是在塔的範圍內且冷卻結束後尚未攻擊過
                    enemylist[i].get_hurt(self.damage)                                    #則那個敵人扣寫並賦予attack=1表示攻擊過(反之繼續檢查下一個敵人)
                    attack=1
                
                           
        else:
            return None
            
            
                    
            
             
    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        ( x0, y0)= self.rect.center                     #賦予塔的圖片中心(x0,y0)          
        x1=x0-35                                        #塔的圖片寬度是70，所以寬度取加減35表示其範圍
        x2=x0+35                                   
        y1=y0-35                                        #塔的圖片高度是70，所以高度取加減35表示其範圍
        y2=y0+35
        if(x1<= x and x<= x2 and y1<= y and y<=y2 ):    #要是滑鼠游標(x,y)在範圍內，則定義is_clicked為 True 否則為False
            return True
        
        else:
            return False
        
        

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

