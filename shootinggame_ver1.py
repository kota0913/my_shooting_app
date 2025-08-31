import pygame
import sys
import random 

# 初期化
pygame.init()  #このコードの意味は？

screen = pygame.display.set_mode((400, 300))
#pygame.display.set_caption("Simple Game")

# 色
RED = (100, 0, 100)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# プレイヤー
x, y = 50, 50 #かっこありでもなしでもよさそう
speed = 5
player_size = 30

# 弾
bullets = []  # 弾を格納するリスト
bullet_speed = 7
bullet_size = 5

# 敵の設定
enemies = []  # 敵のリスト
enemy_size = 30
enemy_speed = 3
enemy_spawn_delay = 30  # 敵が出現する間隔（フレーム数）
spawn_timer = 0  # フレームカウント

# クロック？
clock = pygame.time.Clock() #下行で使う

# ゲーム開始時
player_hp = 100
player_max_hp = 100

def draw_health_bar(surface, x, y, current_hp, max_hp):
    BAR_WIDTH = 100
    BAR_HEIGHT = 10
    # 体力ゲージの背景（赤色）
    pygame.draw.rect(surface, (255, 0, 0), (x, y, BAR_WIDTH, BAR_HEIGHT))
    # 現在の体力に応じた緑ゲージの長さ
    fill_width = int(BAR_WIDTH * (current_hp / max_hp))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, fill_width, BAR_HEIGHT))
    # 枠線
    pygame.draw.rect(surface, (0, 0, 0), (x, y, BAR_WIDTH, BAR_HEIGHT), 1)


# ゲームループ
running = True
while running:
    for event in pygame.event.get():#():#青のイベントはeventでなくてよいが緑はeventでないといけない
        if event.type == pygame.QUIT:
            running = False

        # スペースキーを押したときに弾を発射
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = x + player_size // 2 - bullet_size // 2
                bullet_y = y
                bullets.append([bullet_x, bullet_y])

    # キー入力
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: #pygame.K_LEFTの書き方は決まっている
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # 画面外に出ないように制限
    x = max(0, min(x, 400 - player_size))
    y = max(0, min(y, 300 - player_size))

    # 弾の更新
    for bullet in bullets:
        bullet[1] -= bullet_speed  #bullet[1]はy座標のこと# 弾を上に移動
#リスト-数値は出来ないのでbullet-=bullet・・・はむり
    # 画面外の弾を削除
    bullets = [b for b in bullets if b[1] > 0]

    # 敵の出現
    spawn_timer += 1
    if spawn_timer >= enemy_spawn_delay:
        spawn_timer = 0
        enemy_x = random.randint(0, 400 - enemy_size)
        enemy_y = -enemy_size
        
        #10体に１体程度HPが大きい敵を出現
        if random.randint(1,10)==1:#1/10の確率
            hp=3#強力な敵はHP3
        else:
            hp=1

        enemies.append([enemy_x,enemy_y,hp])



        #enemies.append([enemy_x, enemy_y])#元々あるenemiesのリストに追加

    # 敵の移動
    for enemy in enemies:#enemiesハリスと
        enemy[1] += enemy_speed

    # 弾と敵の当たり判定
    new_enemies = []
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        hit = False
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)
            if enemy_rect.colliderect(bullet_rect):
                bullets.remove(bullet) #弾を消す
                enemy[2]-=1#HPを1減らす
                if enemy[2]<=0:#HPが0以下なら倒す
                    hit=True #TrueとかFalseのつかいかたがいまいち
                break


                
        if not hit:
            new_enemies.append(enemy)
    enemies = new_enemies

    # 敵とプレイヤーが接触したとき
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        player_rect = pygame.Rect(x, y, player_size, player_size)
        if enemy_rect.colliderect(player_rect):
            player_hp -= 10  # 体力を10減らす
            enemies.remove(enemy)  # プレイヤーにぶつかった敵を削除
            if player_hp <= 0:
                running = False  # ゲームオーバー処理
                #ゲームオーバー画面を表示するには？




    # 描画
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (x, y, player_size, player_size))  # プレイヤー
    for bullet in bullets:
        pygame.draw.rect(screen, BLUE, (bullet[0], bullet[1], bullet_size, bullet_size))  # 弾

     # 敵の描画
    for enemy in enemies:
        if enemy[2] > 1:
            color = (255, 0, 0)   # 強い敵は赤
            enemy_size=45 #これだけ設定すると以降の弾全てが大きくなった
        else:
            color = (0, 255, 0)   # 普通の敵は緑
            enemy_size=30
        pygame.draw.rect(screen, color, (enemy[0], enemy[1], enemy_size, enemy_size)) 
    #for enemy in enemies:
    #    pygame.draw.rect(screen, (0, 255, 0), (enemy[0], enemy[1], enemy_size, enemy_size))  # 緑の敵

    # 描画後、画面に体力ゲージを描画
    draw_health_bar(screen, 10, 10, player_hp, player_max_hp)
    pygame.display.flip() #これループ後に入れる(for enemyの上じゃ機能せず)
    clock.tick(30)
# 終了



pygame.quit()
sys.exit()

#bullet[1] -= bullet_speed は
#bullet[1] = bullet[1] - bullet_speed と同じ

#new_bullets = []
#for b in bullets:
#    if b[1] > 0:   # 画面の上端より上に出ていないなら
#        new_bullets.append(b)
#bullets = new_bullets

#間隔もうちょっといじりたい

#プレーヤーにHPをもたせる→ダメージ判定をつけたい
#チャットGPTがある現在では、この追加の作業もそんなに大変ではないことから、より早いスピードで進めることが必要になってきそう
