# Project ) 오락식 Pand게임 만들기

# [게임 조건]
# 1. 캐릭터는 화면 아래에 위치, 좌우로만 이동가능
# 2. 스페이스를 누르면 무기를 쏘아올림
# 3. 큰 공 1개가 나타나서 바운스
# 4. 무기에 닿으면 공은 작은 크기 2개로 분할, 가장 작은 크기의 공은 사라짐
# 5. 모든 공을 없애면 게임 종료 (성공)
# 6. 캐릭터는 공에 닿으면 게임 종료 (실패)
# 7. 시간 제한 99초 시 게임 종료 (실패)
# 8. FPS는 30으로 고정 (필요시 speed값을 조정)

# [게임 이미지]
# 1. 배경 : 640 * 480 (가로 세로) - background.png
# 2. 무대 : 640 * 50 - stage.png
# 3. 캐릭터 : 33 * 60 - character.png
# 4. 무기 : 20 * 430 - weapon.png
# 5. 공 : 160 * 160, 80 * 80, 40 * 40, 20 * 20 - ballon1.png~ballon4.png 

import pygame
import os

pygame.init()

# screen size
screen_width=640
screen_height=480
screen=pygame.display.set_mode((screen_width,screen_height))

# screen title
pygame.display.set_caption("공 터뜨리기 GAME")

# FPS
clock=pygame.time.Clock()

# 1. 사용자 게임 초기화
current_path=os.path.dirname(__file__)
image_path=os.path.join(current_path,"images")
# background
background=pygame.image.load(os.path.join(image_path,"background.png"))
# stage
stage=pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size=stage.get_rect().size
stage_height=stage_size[1]
# character
character=pygame.image.load(os.path.join(image_path,"character.png"))
character_size=character.get_rect().size
character_width=character_size[0]
character_height=character_size[1]
character_x_pos=(screen_width/2)-(character_width/2)
character_y_pos=screen_height-stage_height-character_height
character_to_x_LEFT=0
character_to_x_RIGHT=0
character_speed=1
# weapon
weapon=pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size=weapon.get_rect().size
weapon_width=weapon_size[0]
weapons=[] # weapon은 동시에 여러 발 발사가능 
weapon_speed=15
# balloon 
ball_images=[
    pygame.image.load(os.path.join(image_path,"balloon1.png")),
    pygame.image.load(os.path.join(image_path,"balloon2.png")),
    pygame.image.load(os.path.join(image_path,"balloon3.png")),
    pygame.image.load(os.path.join(image_path,"balloon4.png"))
]
balls=[]
ball_speed_y=[-18,-15,-12,-9] # balloon크기에 따른 최초 스피드(공이 클수록 스피드가 큼)
balls.append({
    "pos_x":50,
    "pos_y":50,
    "img_idx":0,
    "to_x":3,
    "to_y":-6,
    "init_spd_y":ball_speed_y[0]
})

# 충돌했을 때 사라질 무기, 공 정보 저장 변수
weapon_to_remove=-1
ball_to_remove=-1

# Font 정의
game_font=pygame.font.Font(None,40)
total_time=100
start_ticks=pygame.time.get_ticks()

# Game message
# Time Over(시간 초과, 실패)
# Mission Complete(성공)
# Game Over(캐릭터 공에 맞음, 실패)
game_result="GAME OVER"

running=True
while running:
    dt=clock.tick(30)
    # 2. 이벤트 처리
    for event in pygame.event.get():
        if event.type==pygame.QUIT: 
            running=False 
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                character_to_x_LEFT-=character_speed
            elif event.key==pygame.K_RIGHT:
                character_to_x_RIGHT+=character_speed
            elif event.key==pygame.K_SPACE:
                weapon_x_pos=character_x_pos+character_width/2-weapon_width/2
                weapon_y_pos=character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                character_to_x_LEFT=0
            elif event.key==pygame.K_RIGHT:
                character_to_x_RIGHT=0
    # 3. 게임 캐릭터 위치 정의
    # character
    character_x_pos+=(character_to_x_LEFT+character_to_x_RIGHT)*dt
    if character_x_pos<0: # 양쪽 벽에 닿은 경우
        character_x_pos=0
    elif character_x_pos>screen_width-character_width:
        character_x_pos=screen_width-character_width
    # weapon
    weapons=[[w[0],w[1]-weapon_speed] for w in weapons]
    weapons=[[w[0],w[1]] for w in weapons if w[1]>0] # 천장에 닿지 않은 경우만 저장
    # balloon
    for ball_idx,ball_val in enumerate(balls):
        ball_x_pos=ball_val["pos_x"]
        ball_y_pos=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]

        ball_size=ball_images[ball_img_idx].get_rect().size
        ball_width=ball_size[0]
        ball_height=ball_size[1]

        if ball_x_pos<0 or ball_x_pos>screen_width-ball_width:
            ball_val["to_x"]=ball_val["to_x"]*-1 # 양쪽 벽에 부딪히면 반대방향으로 바뀜
        if ball_y_pos>=screen_height-stage_height-ball_height:
            ball_val["to_y"]=ball_val["init_spd_y"] # 스테이지에 부딪히면 반대방향으로 튕김
        else:
            ball_val["to_y"]+=0.5 # 그 외의 모든 경우는 속도를 줄여 포물선 그림

        ball_val["pos_x"]+=ball_val["to_x"]
        ball_val["pos_y"]+=ball_val["to_y"]
    
    # 4. 충돌 처리
    # collision with character and ball
    # character's rect info update
    character_rect=character.get_rect()
    character_rect.left=character_x_pos
    character_rect.top=character_y_pos

    for ball_idx,ball_val in enumerate(balls):
        ball_x_pos=ball_val["pos_x"]
        ball_y_pos=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]
        # balls's rect info update
        ball_rect=ball_images[ball_img_idx].get_rect()
        ball_rect.left=ball_x_pos
        ball_rect.top=ball_y_pos

        # cheking collision(character & balls)
        if character_rect.colliderect(ball_rect):
            running=False
            break

        for weapon_idx,weapon_val in enumerate(weapons):
            weapon_x_pos=weapon_val[0]
            weapon_y_pos=weapon_val[1]
            # weapons's rect info update
            weapon_rect=weapon.get_rect()
            weapon_rect.left=weapon_x_pos
            weapon_rect.top=weapon_y_pos

            # cheking collision(balls & weapons)
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove=weapon_idx
                ball_to_remove=ball_idx
                if ball_img_idx<3: # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width=ball_rect.size[0]
                    ball_height=ball_rect.size[1]
                    # 나눠진 공 정보
                    small_ball_rect=ball_images[ball_img_idx+1].get_rect()
                    small_ball_width=small_ball_rect.size[0]
                    small_ball_height=small_ball_rect.size[1]
                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x":ball_x_pos+(ball_width/2)-(small_ball_width/2),
                        "pos_y":ball_y_pos+(ball_height/2)-(small_ball_height/2),
                        "img_idx":ball_img_idx+1,
                        "to_x":-3,
                        "to_y":-6,
                        "init_spd_y":ball_speed_y[ball_img_idx+1]
                    })
                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x":ball_x_pos+(ball_width/2)-(small_ball_width/2),
                        "pos_y":ball_y_pos+(ball_height/2)-(small_ball_height/2),
                        "img_idx":ball_img_idx+1,
                        "to_x":3,
                        "to_y":-6,
                        "init_spd_y":ball_speed_y[ball_img_idx+1]
                    })
                break # weapon for문을 빠져나오는 break
        else: # 이중 for문의 break로 인한 버그 수정을 위해 trick으로 이 형식을 사용
            continue # weapon for문과 (if-else 구조)
        break # weapon for문의 break을 거쳐야지만 실행됨

    # 충돌된 공 or 무기 없애기
    if ball_to_remove>-1:
        del balls[ball_to_remove]
        ball_to_remove=-1
    if weapon_to_remove>-1:
        del weapons[weapon_to_remove]
        weapon_to_remove=-1        
        
    # 모든 공을 제거한 경우 게임종료 (성공)
    if len(balls)==0:
        game_result="Mission Complete"
        running=False

    # 5. 화면에 그리기
    screen.blit(background,(0,0))
    for weapon_x_pos,weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_x_pos=val["pos_x"]
        ball_y_pos=val["pos_y"]
        ball_img_idx=val["img_idx"]
        screen.blit(ball_images[ball_img_idx],(ball_x_pos,ball_y_pos))

    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))

    # elapsed_time
    elapsed_time=(pygame.time.get_ticks()-start_ticks)/1000
    timer=game_font.render(f"Time : {int(total_time-elapsed_time)}",True,(255,255,255))
    screen.blit(timer,(10,10))

    if total_time-elapsed_time<=0:
        game_result="Time Over"
        running=False

    pygame.display.update()

# Game result message
msg=game_font.render(game_result,True,(255,255,0)) 
msg_rect=msg.get_rect(center=(int(screen_width/2),int(screen_height/2)))
screen.blit(msg,msg_rect)
pygame.display.update()

pygame.time.delay(2000)

pygame.quit()