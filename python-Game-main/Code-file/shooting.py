import pygame
import sys
import random
from time import sleep

BLACK = (0, 0, 0)
size = [480, 640]
rockImage = ['resources/rock01.png','resources/rock02.png','resources/rock03.png','resources/rock04.png','resources/rock05.png', \
             'resources/rock06.png','resources/rock07.png','resources/rock08.png','resources/rock09.png','resources/rock10.png', \
             'resources/rock11.png','resources/rock12.png','resources/rock13.png','resources/rock14.png','resources/rock15.png', \
             'resources/rock16.png','resources/rock17.png','resources/rock18.png','resources/rock19.png','resources/rock20.png', \
             'resources/rock21.png','resources/rock22.png','resources/rock23.png','resources/rock24.png','resources/rock25.png', \
             'resources/rock26.png','resources/rock27.png','resources/rock28.png','resources/rock29.png','resources/rock30.png' ]
explosionSound = ['resources/explosion01.wav','resources/explosion02.wav','resources/explosion03.wav','resources/explosion04.wav']

# 운석을 맞춘 갯수
def writeScore(count):
    global gamePad
    font = pygame.font.Font('resources/NanumGothic.ttf', 20)
    text = font.render('파괴한 운석 수 : ' + str(count), True, (255,255,255))
    gamePad.blit(text,(10,0))

# 운석이 화면 아래로 통과한 개수
def writePassed(count):
    global gamePad
    font = pygame.font.Font('resources/NanumGothic.ttf', 20)
    text = font.render('놓친 운석 : ' + str(count), True, (255,0,0))
    gamePad.blit(text, (360,0))

#게임 메시지
def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('resources/NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (size[0]/2, size[1]/2)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

# 전투기 운석 충돌 메시지 출력
def crash():
    global gamePad
    writeMessage('전투기 파괴!')
    
# 게임 오버 메시지 
def gameOver():
    global gamePad
    writeMessage('게임 오버!')

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode(size)
    pygame.display.set_caption('PyShooting') # 게임 이름
    background = pygame.image.load('resources/background.png') # 배경
    fighter = pygame.image.load('resources/fighter.png') # 전투기
    missile = pygame.image.load('resources/missile.png') # 미사일
    explosion = pygame.image.load('resources/explosion.png') # 폭발
    pygame.mixer_music.load('resources/music.wav') # 배경 음악
    pygame.mixer.music.play(-1) # 배경 음악 재생
    missileSound = pygame.mixer.Sound('resources/missile.wav') # 미사일 사운드
    gameOverSound = pygame.mixer.Sound('resources/gameover.wav') # 게임 오버 사운드
    clock = pygame.time.Clock()

def runGame():
    global gamepad, clock, background, fighter, missile, explosion, missileSound
    
    # 전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    
    # 전투기 초기 위치 (x, y)
    x = size[0] * 0.45
    y = size[1] * 0.9
    fighterX = 0
    
    missileXY = [] # 무기 좌표 리스트
    
    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size # 크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))
    
    # 초기 위치 설정
    rockX = random.randrange(0, size[0] - rockWidth)
    rockY = 0
    rockSpeed = 2
    
    # 전투기 미사일에 운석이 맞을때 
    isShot = False
    shotCount = 0
    rockPassed = 0
    
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]: # 게임 프로그램 종료
                pygame.quit()
                sys.exit()
                
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT: # 왼쪽 이동
                    fighterX -= 5
                elif event.key == pygame.K_RIGHT: # 오른쪽 이동
                    fighterX += 5
                elif event.key == pygame.K_SPACE: # 미사일 발사
                    missileSound.play()
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])
                            
            if event.type in [pygame.KEYUP]: # 아무런 키 움직임 없을때 전투기 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                    

                
        drawObject(background, 0, 0) # 배경화면
        
        x += fighterX
        if x < 0:
            x = 0
        elif x > size[0] - fighterWidth:
            x = size[0] - fighterWidth
            
        # 전투기 운석 충돌 체크     
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or  \
            (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()
                 
        drawObject(fighter, x, y) # 비행기 
            
        # 미사일 발사 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY): # 미사일 반복
                bxy[1] -= 10  # 총알이 위로이동 10만큼
                missileXY[i][1] = bxy[1]
                
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1
                
                if bxy[1] <= 0: # 화면을 벗어낫을때
                    try:
                        missileXY.remove(bxy) # 미사일 제거
                    except:
                        pass
                    
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)
                
        writeScore(shotCount)
                
        rockY += rockSpeed # 운석이 떨어짐
          
        # 운석이 지구로 떨어졌을 때        
        if rockY > size[1]:
            # 새로운 운석
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, size[0] - rockWidth)
            rockY = 0
            rockPassed += 1
            
        if rockPassed == 3: # 3개 놓치면 게임 오버
            gameOver()
            
        writePassed(rockPassed)
        
        # 운석을 맞추었을 때
        if isShot:
            # 운석 폭발
            drawObject(explosion, rockX, rockY) 
            destroySound.play()
            
            # 새로운 운석
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, size[0] - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False
            
            # 운석 맞추면 속도 증가
            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10
                            
        drawObject(rock, rockX, rockY)
        
        pygame.display.update()

        clock.tick(60)

    pygame.quit()

initGame()
runGame()

