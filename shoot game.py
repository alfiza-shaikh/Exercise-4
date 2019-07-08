import pygame
import random
pygame.init()
clock=pygame.time.Clock()
screenwidth=850
screenlength=480
win = pygame.display.set_mode((screenwidth,screenlength))
pygame.display.set_caption("Shooting game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

walkRightEnemy = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png')]
walkLeftEnemy = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png')]
music=pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

font=pygame.font.SysFont('comicsans',100,True)
win.blit(bg,(0,0))
win.blit(walkLeft[0],(2*screenwidth / 3,400))
win.blit(walkRightEnemy[5],(screenwidth / 3,405))
text1=font.render('Shooting Game', 1, (0,128,0))
win.blit(text1, (screenwidth / 2 - (text1.get_width() / 2), screenlength//3))
pygame.display.update()
i=0
while i < 400:
    pygame.time.delay(10)
    i += 1
win.blit(bg,(0,0))
font2=pygame.font.SysFont('comicsans',40,True)
help1=font2.render('LEFT ARROW KEY : TO MOVE LEFT' ,1, (0,128,0))
help2=font2.render('RIGHT ARROW KEY : TO MOVE RIGHT',1, (0,128,0))
help3=font2.render('UP ARROW KEY : TO JUMP',1, (0,128,0))
help4=font2.render('SPACE BAR  : TO SHOOT',1, (0,128,0))
win.blit(help1, (100,screenlength//3 ))
win.blit(help2, (100, screenlength//3+30))
win.blit(help3, (100, screenlength//3+60))
win.blit(help4, (100,screenlength//3+90))
pygame.display.update()
i=0
while i < 600:
    pygame.time.delay(10)
    i += 1



class human :
    def __init__(self,x,y,width,height,vel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=vel
        self.right=False
        self.left=False
        self.standing=True
        self.isJump=False
        self.walkCount=0
        self.jumpCount=10
        self.hitbox=(self.x +17,self.y+11,29,52)
        self.health=10
    def draw(self,win):
        if self.walkCount+1>=27:
            self.walkCount=0
        if self.left :
            win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
            self.walkCount+=1
        elif self.right:
            win.blit(walkRight[self.walkCount//3],(self.x,self.y))
            self.walkCount+=1
        else:
            win.blit(char,(self.x,self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        pygame.display.update()

    def hit(self):
        self.isJump=False
        self.jumpCount=10
        if self.x< (screenwidth-50-64):
            self.x+=50
        else:
            self.x -= 50

        self.y=410
        self.walkCount=0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (screenwidth/2 - (text.get_width() / 2), 2*screenlength//3))
        pygame.display.update()
        i=0
        while i < 50:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()



class shoot:
    def __init__(self,x,y,colour,facing):
        self.x=x
        self.y = y
        self.colour=colour
        self.facing=facing
        self.radius=4
        self.vel=10*facing
    def drawBullet(self,win):
        pygame.draw.circle(win, self.colour, (self.x,self.y), self.radius)

class enemy:
    def __init__(self,x,y,width,height,start,end):
        self.x=x
        self.y=y
        self.vel=3
        self.width=width
        self.height=height
        self.path=[start,end]
        self.walkCount=0
        self.hitbox = (self.x + 17,self.y+11, 29, 52)
        self.health=10
        self.visible=True
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount+1>=27:
                self.walkCount=0
            if self.vel>0:
                win.blit(walkRightEnemy[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(walkLeftEnemy[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            if self.vel > 0:
                self.hitbox = (self.x + 17, self.y, 29, 52)
            else:
                self.hitbox = (self.x + 30, self.y, 29, 52)

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0),(self.hitbox[0],self.hitbox[1] -20,50-(5*(10-self.health)),10))

    def move(self):
        if self.vel>0:
            if self.x < self.path[1]+self.vel:
                self.x+=self.vel
            else:
                self.vel*=-1
                self.x+=self.vel
                self.walkCount=0
        else:
            if self.x > self.path[0] + self.vel:
                self.x += self.vel
            else:
                self.vel *= -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):
        if self.health>0:
            self.health-=1
        else:
            self.visible=False

    def restart(self):
        i = 0
        while i < 20:
            pygame.time.delay(10)
            i += 1
        self.x=random.randrange(0,screenwidth-64)
        self.start = random.randrange(0,screenwidth-64)
        self.visible = True
        self.walkCount = 0
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 10

def gameOver():
    font1 = pygame.font.SysFont('comicsans', 100)
    text = font1.render('GAME OVER ', 1, (255, 0, 0))
    win.blit(text, (screenwidth / 2 - (text.get_width() / 2), 2 * screenlength // 3))
    pygame.display.update()
    i = 0
    while i < 300:
        pygame.time.delay(10)
        i += 1



def redrawGameWindow():
    win.blit(bg,(0,0))
    text=font.render('SCORE :'+str(score),1,(0,0,0))
    win.blit(text,(380,10))
    man.draw(win)
    for bullet in bullets:
        bullet.drawBullet(win)
    goblin1.draw(win)
    goblin2.draw(win)

    pygame.display.update()

man=human(50,400,64,64,5)
goblin1=enemy(100,405,64,64,0,screenwidth-64)
goblin2=enemy(400,405,64,64,0,screenwidth-64)
font=pygame.font.SysFont('comicsans',30,True)
run=True
score=0
bullets=[]
while run:
    clock.tick(27)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False


    for bullet in bullets:
        if bullet.y-bullet.radius<goblin1.hitbox[1]+goblin1.hitbox[3] and bullet.y+bullet.radius>goblin1.hitbox[1] and bullet.x + bullet.radius>goblin1.hitbox[0] and bullet.x-bullet.radius<goblin1.hitbox[0] + goblin1.hitbox[2]:
            goblin1.hit()
            score+=1

        if  bullet.y-bullet.radius<goblin2.hitbox[1]+goblin2.hitbox[3] and bullet.y+bullet.radius>goblin2.hitbox[1] and bullet.x + bullet.radius>goblin2.hitbox[0] and bullet.x-bullet.radius<goblin2.hitbox[0] + goblin2.hitbox[2] :
            goblin2.hit()
            score += 1
        if (bullet.y-bullet.radius<goblin1.hitbox[1]+goblin1.hitbox[3] and bullet.y+bullet.radius>goblin1.hitbox[1] and bullet.x + bullet.radius>goblin1.hitbox[0] and bullet.x-bullet.radius<goblin1.hitbox[0] + goblin1.hitbox[2] ) or ( bullet.y-bullet.radius<goblin2.hitbox[1]+goblin2.hitbox[3] and bullet.y+bullet.radius>goblin2.hitbox[1] and bullet.x + bullet.radius>goblin2.hitbox[0] and bullet.x-bullet.radius<goblin2.hitbox[0] + goblin2.hitbox[2] ):
             bullets.pop(bullets.index(bullet))
        if bullet.x <screenwidth and bullet.x > 0 :
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))


    if goblin1.visible == True:
        if man.hitbox[1] < goblin1.hitbox[1] + goblin1.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin1.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin1.hitbox[0] and man.hitbox[0] < goblin1.hitbox[0] + goblin1.hitbox[2]:
                score -= 5
                if score< 0:
                    gameOver()
                    run=False
                else :
                    man.hit()
    else :
        goblin1.restart()


    if goblin2.visible == True:
        if man.hitbox[1] < goblin2.hitbox[1] + goblin2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin2.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin2.hitbox[0] and man.hitbox[0] < goblin2.hitbox[0] + goblin2.hitbox[2]:
                score -= 5
                if score< 0:
                    gameOver()
                    run=False
                else :
                    man.hit()
    else :
        goblin2.restart()





    if keys[pygame.K_SPACE]:
        if man.left:
            facing=-1
        else:
            facing=1
        if len(bullets)<30:
            bullets.append(shoot(round(man.x + man.width //2), round(man.y + man.height//2), (0,0,0), facing))

    elif keys[pygame.K_LEFT] and man.x>0:
        man.x-=man.vel
        man.left=True
        man.right=False
        man.standing = False
    elif keys[pygame.K_RIGHT]and man.x<screenwidth-man.width:
        man.x+=man.vel
        man.left = False
        man.right = True
        man.standing = False
    else :
        man.standing=True
        man.walkCount=0
    if not(man.isJump):
        if(keys[pygame.K_UP]):
            man.isJump=True
            man.right=False
            man.left = False
    else:
        if man.jumpCount>=-10:
            neg=1
            if man.jumpCount<0:
                neg=-1
            man.y-=(man.jumpCount**2)*0.5*neg
            man.jumpCount-=1
        else :
            man.isJump=False
            man.jumpCount=10
    redrawGameWindow()

pygame.quit()