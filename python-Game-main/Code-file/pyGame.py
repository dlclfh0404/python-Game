import pygame

pygame.init()

# pygame 사용되는 전역변수
WHITE = (255,255,255)
size = [400,300]
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()

# 이미지 호출
airplane = pygame.image.load('images/plane.png')
airplane = pygame.transform.scale(airplane, (60, 45))


def runGame():
    global done, airplane
    x = 20
    y = 24

    while not done:
        clock.tick(10)
        screen.fill(WHITE)


        # 방향키 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y -= 10
                elif event.key == pygame.K_DOWN:
                    y += 10

        screen.blit(airplane, (x, y))
        pygame.display.update()

runGame()
pygame.quit()
