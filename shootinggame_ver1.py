import pygame
import sys
import random 

# 初期化
pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Simple Game")

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

# クロック
clock = pygame.time.Clock()

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
        bullet[1] -= bullet_speed  # 弾を上に移動

    # 画面外の弾を削除
    bullets = [b for b in bullets if b[1] > 0]

    # 敵の出現
    spawn_timer += 1
    if spawn_timer >= enemy_spawn_delay:
        spawn_timer = 0
        enemy_x = random.randint(0, 400 - enemy_size)
        enemy_y = -enemy_size
        enemies.append([enemy_x, enemy_y])

    # 敵の移動
    for enemy in enemies:
        enemy[1] += enemy_speed

    # 弾と敵の当たり判定
    new_enemies = []
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        hit = False
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)
            if enemy_rect.colliderect(bullet_rect):
                hit = True
                bullets.remove(bullet)
                break
        if not hit:
            new_enemies.append(enemy)
    enemies = new_enemies




    # 描画
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (x, y, player_size, player_size))  # プレイヤー
    for bullet in bullets:
        pygame.draw.rect(screen, BLUE, (bullet[0], bullet[1], bullet_size, bullet_size))  # 弾

     # 敵の描画
    for enemy in enemies:
        pygame.draw.rect(screen, (0, 255, 0), (enemy[0], enemy[1], enemy_size, enemy_size))  # 緑の敵

    pygame.display.flip() #これループ後に入れる(for enemyの上じゃ機能せず)
    clock.tick(30)
# 終了
pygame.quit()
sys.exit()