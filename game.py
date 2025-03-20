import pygame
import sys
import random
import time
import json
import os
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Game - Mobile Friendly")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
SAND = (245, 222, 179)
GRAY = (128, 128, 128)

# Player properties
player_width = 48
player_height = 72
player_width_goku = 72
player_x = 100
player_y = SCREEN_HEIGHT - player_height - 50
player_vel_x = 0
player_vel_y = 0
jump_power = -18
gravity = 0.8
is_jumping = False
player_level = 0
total_coins = 0
total_diamonds = 0

# Dodge mechanics
dodge_active = False
dodge_start_time = 0
dodge_cooldown = 60  # 1 minute cooldown
dodge_duration = 10  # 10 seconds duration
last_dodge_time = -dodge_cooldown
dodge_animation_time = 0

camera_x = 0

# Rewards
COIN_REWARDS = [500, 1000, 5000, 10000]
LEVEL_INCREASE = [10, 30, 50, 100]
DIAMOND_REWARD = 500

# Skins (all included)
skins = {
    "Mario": {"image": pygame.image.load(r"C:\Users\deepak mehra\Downloads\mario.png"), "unlocked": True, "equipped": True},
    "Luigi": {"image": pygame.image.load(r"C:\Users\deepak mehra\Downloads\luigi.png"), "unlocked": False, "equipped": False, "cost": 1000},
    "Peach": {"image": pygame.image.load(r"C:\Users\deepak mehra\Downloads\peach.png"), "unlocked": False, "equipped": False, "cost": 5000},
    "Mushroom": {"image": pygame.image.load(r"C:\Users\deepak mehra\Downloads\mushroom1.png"), "unlocked": False, "equipped": False, "cost": 10000},
    "Steve": {"image": pygame.image.load(r"C:\Users\deepak mehra\Downloads\steve.png"), "unlocked": False, "equipped": False, "cost": 50000},
    "Goku": {"image": pygame.image.load(r"C:\Users\deepak mehra\Downloads\goku.png"), "unlocked": False, "equipped": False, "cost": 1000, "special_image": pygame.image.load(r"C:\Users\deepak mehra\Downloads\muigoku2.png")},
    "Serious Saitama": {"image": pygame.image.load(r"C:\Users\deepak mehra\Downloads\serious saitama.png"), "unlocked": False, "equipped": False, "cost": 1500, "special_image": pygame.image.load(r"C:\Users\deepak mehra\Downloads\serious saitama.png")},
}

for skin_name, skin in skins.items():
    if skin_name in ["Goku", "Serious Saitama"]:
        skin["image"] = pygame.transform.scale(skin["image"], (player_width_goku, player_height))
        if "special_image" in skin:
            skin["special_image"] = pygame.transform.scale(skin["special_image"], (player_width_goku, player_height))
    else:
        skin["image"] = pygame.transform.scale(skin["image"], (player_width, player_height))

# Levels (unchanged)
levels = [
    {"world_width": 2000, "platforms": [pygame.Rect(0, SCREEN_HEIGHT - 50, 2000, 50), pygame.Rect(300, 400, 200, 20), pygame.Rect(700, 350, 200, 20), pygame.Rect(1200, 300, 200, 20)], "pipes": [pygame.Rect(500, SCREEN_HEIGHT - 100, 50, 50), pygame.Rect(900, SCREEN_HEIGHT - 150, 50, 100)], "monsters": [{"x": 600, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -2, "width": 48, "height": 48}, {"x": 1000, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -2, "width": 48, "height": 48}], "flag": pygame.Rect(1950, SCREEN_HEIGHT - 100, 20, 50), "coins": [pygame.Rect(350, 350, 20, 20), pygame.Rect(750, 300, 20, 20), pygame.Rect(1250, 250, 20, 20)], "bg_color": WHITE},
    {"world_width": 3000, "platforms": [pygame.Rect(0, SCREEN_HEIGHT - 50, 3000, 50), pygame.Rect(300, 450, 150, 20), pygame.Rect(600, 400, 200, 20), pygame.Rect(1000, 350, 200, 20), pygame.Rect(1500, 300, 200, 20), pygame.Rect(2000, 250, 200, 20)], "pipes": [pygame.Rect(400, SCREEN_HEIGHT - 150, 50, 100), pygame.Rect(800, SCREEN_HEIGHT - 200, 50, 150), pygame.Rect(1300, SCREEN_HEIGHT - 100, 50, 50), pygame.Rect(1800, SCREEN_HEIGHT - 150, 50, 100)], "monsters": [{"x": 500, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -3, "width": 48, "height": 48}, {"x": 900, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -3, "width": 48, "height": 48}, {"x": 1400, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -3, "width": 48, "height": 48}, {"x": 1900, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -3, "width": 48, "height": 48}], "flag": pygame.Rect(2950, SCREEN_HEIGHT - 100, 20, 50), "coins": [pygame.Rect(350, 400, 20, 20), pygame.Rect(650, 350, 20, 20), pygame.Rect(1050, 300, 20, 20), pygame.Rect(1550, 250, 20, 20), pygame.Rect(2050, 200, 20, 20)], "bg_color": WHITE},
    {"world_width": 4000, "platforms": [pygame.Rect(0, SCREEN_HEIGHT - 50, 4000, 50), pygame.Rect(300, 450, 100, 20), pygame.Rect(600, 400, 150, 20), pygame.Rect(900, 350, 200, 20), pygame.Rect(1300, 300, 150, 20), pygame.Rect(1700, 250, 200, 20), pygame.Rect(2200, 200, 150, 20), pygame.Rect(2700, 150, 200, 20)], "pipes": [pygame.Rect(400, SCREEN_HEIGHT - 200, 50, 150), pygame.Rect(800, SCREEN_HEIGHT - 250, 50, 200), pygame.Rect(1200, SCREEN_HEIGHT - 150, 50, 100), pygame.Rect(1600, SCREEN_HEIGHT - 200, 50, 150), pygame.Rect(2000, SCREEN_HEIGHT - 250, 50, 200), pygame.Rect(2500, SCREEN_HEIGHT - 150, 50, 100)], "monsters": [{"x": 500, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -4, "width": 48, "height": 48}, {"x": 800, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -4, "width": 48, "height": 48}, {"x": 1100, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -4, "width": 48, "height": 48}, {"x": 1500, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -4, "width": 48, "height": 48}, {"x": 2000, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -4, "width": 48, "height": 48}, {"x": 2500, "y": SCREEN_HEIGHT - 50 - 48, "vel_x": -4, "width": 48, "height": 48}], "flag": pygame.Rect(3950, SCREEN_HEIGHT - 100, 20, 50), "coins": [pygame.Rect(350, 400, 20, 20), pygame.Rect(650, 350, 20, 20), pygame.Rect(950, 300, 20, 20), pygame.Rect(1350, 250, 20, 20), pygame.Rect(1750, 200, 20, 20), pygame.Rect(2250, 150, 20, 20), pygame.Rect(2750, 100, 20, 20)], "bg_color": WHITE},
    {"world_width": 6000, "platforms": [pygame.Rect(0, SCREEN_HEIGHT - 50, 6000, 50), pygame.Rect(500, 450, 200, 20), pygame.Rect(1000, 400, 250, 20), pygame.Rect(1500, 350, 200, 20), pygame.Rect(2000, 300, 250, 20), pygame.Rect(2500, 250, 200, 20), pygame.Rect(3000, 200, 250, 20), pygame.Rect(3500, 250, 200, 20), pygame.Rect(4000, 300, 250, 20), pygame.Rect(4500, 350, 200, 20)], "pipes": [pygame.Rect(600, SCREEN_HEIGHT - 200, 50, 150), pygame.Rect(1200, SCREEN_HEIGHT - 250, 50, 200), pygame.Rect(1800, SCREEN_HEIGHT - 150, 50, 100), pygame.Rect(2400, SCREEN_HEIGHT - 200, 50, 150), pygame.Rect(3000, SCREEN_HEIGHT - 250, 50, 200), pygame.Rect(3600, SCREEN_HEIGHT - 150, 50, 100), pygame.Rect(4200, SCREEN_HEIGHT - 200, 50, 150)], "monsters": [], "boss": {"x": 1000, "y": SCREEN_HEIGHT - 200, "width": 200, "height": 200, "vel_x": -5, "bullet_timer": 0}, "bullets": [], "flag": pygame.Rect(5950, SCREEN_HEIGHT - 100, 20, 50), "coins": [pygame.Rect(550, 400, 20, 20), pygame.Rect(1050, 350, 20, 20), pygame.Rect(1550, 300, 20, 20), pygame.Rect(2050, 250, 20, 20), pygame.Rect(2550, 200, 20, 20), pygame.Rect(3050, 150, 20, 20), pygame.Rect(3550, 200, 20, 20), pygame.Rect(4050, 250, 20, 20), pygame.Rect(4550, 300, 20, 20)], "bg_color": SAND},
]

# Game states
START_SCREEN = 0
PLAYING = 1
DEAD = 2
WIN = 3
SKINS_MENU = 4
game_state = START_SCREEN
current_level = 0

font = pygame.font.SysFont(None, 36)
SAVE_FILE = "game_save.json"

# Virtual buttons for mobile
BUTTON_SIZE = 80
left_button = pygame.Rect(20, SCREEN_HEIGHT - 100, BUTTON_SIZE, BUTTON_SIZE)
right_button = pygame.Rect(120, SCREEN_HEIGHT - 100, BUTTON_SIZE, BUTTON_SIZE)
jump_button = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100, BUTTON_SIZE, BUTTON_SIZE)
dodge_button = pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, BUTTON_SIZE, BUTTON_SIZE)

def save_game():
    global total_coins, total_diamonds, player_level, skins
    data = {"total_coins": total_coins, "total_diamonds": total_diamonds, "player_level": player_level, "skins": {skin: {"unlocked": info["unlocked"], "equipped": info["equipped"]} for skin, info in skins.items()}}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game():
    global total_coins, total_diamonds, player_level, skins
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            total_coins = data["total_coins"]
            total_diamonds = data["total_diamonds"]
            player_level = data["player_level"]
            for skin, info in data["skins"].items():
                skins[skin]["unlocked"] = info["unlocked"]
                skins[skin]["equipped"] = info["equipped"]

def reset_game(level):
    global player_x, player_y, player_vel_x, player_vel_y, is_jumping, camera_x, game_state, current_level, dodge_active, dodge_animation_time
    player_x = 100
    player_y = SCREEN_HEIGHT - player_height - 50
    player_vel_x = 0
    player_vel_y = 0
    is_jumping = False
    camera_x = 0
    dodge_active = False
    dodge_animation_time = 0
    game_state = PLAYING
    current_level = level
    for monster in levels[current_level]["monsters"]:
        monster["x"] = random.randint(600, levels[current_level]["world_width"] - 100)
    if "boss" in levels[current_level]:
        levels[current_level]["boss"]["x"] = 1000
        levels[current_level]["bullets"] = []

def draw_character(x, y, skin_name, preview=False):
    camera_offset = camera_x if not preview else 0
    if skin_name in ["Goku", "Serious Saitama"] and dodge_active:
        skin_image = skins[skin_name]["special_image"]
        width = player_width_goku
        dodge_offset_x = math.sin(dodge_animation_time * 15) * 8
        dodge_offset_y = abs(math.cos(dodge_animation_time * 10)) * 5
        rotation = math.sin(dodge_animation_time * 20) * 10
        rotated_image = pygame.transform.rotate(skin_image, rotation)
        rect = rotated_image.get_rect(center=(x + dodge_offset_x - camera_offset + width // 2, y - dodge_offset_y + player_height // 2))
        screen.blit(rotated_image, rect.topleft)
    else:
        skin_image = skins[skin_name]["image"]
        width = player_width_goku if skin_name in ["Goku", "Serious Saitama"] else player_width
        screen.blit(skin_image, (x - camera_offset, y))
    return width

def draw_goomba(monster):
    x, y = monster["x"] - camera_x, monster["y"]
    pygame.draw.rect(screen, (139, 69, 19), (x + 6, y, 36, 24))
    pygame.draw.rect(screen, BLACK, (x, y + 24, 48, 12))
    pygame.draw.rect(screen, WHITE, (x + 12, y + 6, 6, 6))
    pygame.draw.rect(screen, WHITE, (x + 30, y + 6, 6, 6))
    pygame.draw.rect(screen, BLACK, (x + 15, y + 9, 3, 3))
    pygame.draw.rect(screen, BLACK, (x + 33, y + 9, 3, 3))

def draw_boss(boss):
    x, y = boss["x"] - camera_x, boss["y"]
    pygame.draw.rect(screen, RED, (x, y, boss["width"], boss["height"]))
    pygame.draw.circle(screen, BLACK, (x + 50, y + 50), 20)
    pygame.draw.circle(screen, BLACK, (x + 150, y + 50), 20)

def draw_bullets(bullets):
    for bullet in bullets[:]:
        bullet["x"] -= bullet["vel_x"]
        pygame.draw.circle(screen, BLACK, (int(bullet["x"] - camera_x), int(bullet["y"])), 10)
        if bullet["x"] < 0:
            bullets.remove(bullet)

def draw_progress_bar():
    bar_width = SCREEN_WIDTH - 40
    pygame.draw.rect(screen, BLACK, (20, 20, bar_width, 20), 2)
    player_pos = (player_x / levels[current_level]["world_width"]) * bar_width + 20
    pygame.draw.circle(screen, RED, (int(player_pos), 30), 5)
    pygame.draw.circle(screen, YELLOW, (bar_width + 20, 30), 5)

def jumpscare():
    screen.fill(RED)
    scare_text = font.render("BOO!", True, BLACK)
    screen.blit(scare_text, (SCREEN_WIDTH // 2 - scare_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    time.sleep(0.5)

def draw_buttons():
    pygame.draw.rect(screen, GRAY, left_button)
    pygame.draw.rect(screen, GRAY, right_button)
    pygame.draw.rect(screen, BLUE, jump_button)
    pygame.draw.rect(screen, GREEN, dodge_button)
    screen.blit(font.render("<", True, BLACK), (left_button.centerx - 10, left_button.centery - 10))
    screen.blit(font.render(">", True, BLACK), (right_button.centerx - 10, right_button.centery - 10))
    screen.blit(font.render("J", True, BLACK), (jump_button.centerx - 10, jump_button.centery - 10))
    screen.blit(font.render("D", True, BLACK), (dodge_button.centerx - 10, dodge_button.centery - 10))

load_game()

clock = pygame.time.Clock()
running = True
preview_skin = None
touching_left = False
touching_right = False

while running:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if game_state == START_SCREEN:
                if pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 40).collidepoint(pos):
                    reset_game(0)
                elif pygame.Rect(SCREEN_WIDTH // 2 - 100, 290, 200, 40).collidepoint(pos):
                    reset_game(1)
                elif pygame.Rect(SCREEN_WIDTH // 2 - 100, 330, 200, 40).collidepoint(pos):
                    reset_game(2)
                elif pygame.Rect(SCREEN_WIDTH // 2 - 150, 370, 300, 40).collidepoint(pos) and player_level >= 500:
                    reset_game(3)
                elif pygame.Rect(SCREEN_WIDTH // 2 - 50, 410, 100, 40).collidepoint(pos):
                    game_state = SKINS_MENU
            elif game_state == SKINS_MENU:
                if pygame.Rect(50, 150, 200, 40).collidepoint(pos) and skins["Mario"]["unlocked"]:
                    for s in skins:
                        skins[s]["equipped"] = False
                    skins["Mario"]["equipped"] = True
                    preview_skin = None
                elif pygame.Rect(50, 210, 200, 40).collidepoint(pos):
                    if skins["Luigi"]["unlocked"]:
                        for s in skins:
                            skins[s]["equipped"] = False
                        skins["Luigi"]["equipped"] = True
                        preview_skin = None
                    elif total_coins >= skins["Luigi"]["cost"]:
                        skins["Luigi"]["unlocked"] = True
                        total_coins -= skins["Luigi"]["cost"]
                        preview_skin = "Luigi"
                elif pygame.Rect(50, 270, 200, 40).collidepoint(pos):
                    if skins["Peach"]["unlocked"]:
                        for s in skins:
                            skins[s]["equipped"] = False
                        skins["Peach"]["equipped"] = True
                        preview_skin = None
                    elif total_coins >= skins["Peach"]["cost"]:
                        skins["Peach"]["unlocked"] = True
                        total_coins -= skins["Peach"]["cost"]
                        preview_skin = "Peach"
                elif pygame.Rect(50, 330, 200, 40).collidepoint(pos):
                    if skins["Mushroom"]["unlocked"]:
                        for s in skins:
                            skins[s]["equipped"] = False
                        skins["Mushroom"]["equipped"] = True
                        preview_skin = None
                    elif total_coins >= skins["Mushroom"]["cost"]:
                        skins["Mushroom"]["unlocked"] = True
                        total_coins -= skins["Mushroom"]["cost"]
                        preview_skin = "Mushroom"
                elif pygame.Rect(50, 390, 200, 40).collidepoint(pos):
                    if skins["Steve"]["unlocked"]:
                        for s in skins:
                            skins[s]["equipped"] = False
                        skins["Steve"]["equipped"] = True
                        preview_skin = None
                    elif total_coins >= skins["Steve"]["cost"]:
                        skins["Steve"]["unlocked"] = True
                        total_coins -= skins["Steve"]["cost"]
                        preview_skin = "Steve"
                elif pygame.Rect(50, 450, 200, 40).collidepoint(pos):
                    if skins["Goku"]["unlocked"]:
                        for s in skins:
                            skins[s]["equipped"] = False
                        skins["Goku"]["equipped"] = True
                        preview_skin = None
                    elif total_diamonds >= skins["Goku"]["cost"]:
                        skins["Goku"]["unlocked"] = True
                        total_diamonds -= skins["Goku"]["cost"]
                        preview_skin = "Goku"
                elif pygame.Rect(50, 510, 200, 40).collidepoint(pos):
                    if skins["Serious Saitama"]["unlocked"]:
                        for s in skins:
                            skins[s]["equipped"] = False
                        skins["Serious Saitama"]["equipped"] = True
                        preview_skin = None
                    elif total_diamonds >= skins["Serious Saitama"]["cost"]:
                        skins["Serious Saitama"]["unlocked"] = True
                        total_diamonds -= skins["Serious Saitama"]["cost"]
                        preview_skin = "Serious Saitama"
                elif pygame.Rect(SCREEN_WIDTH // 2 - 100, 550, 200, 40).collidepoint(pos):
                    game_state = START_SCREEN
                    preview_skin = None
            elif game_state == PLAYING:
                if left_button.collidepoint(pos):
                    touching_left = True
                elif right_button.collidepoint(pos):
                    touching_right = True
                elif jump_button.collidepoint(pos) and not is_jumping:
                    player_vel_y = jump_power
                    is_jumping = True
                elif dodge_button.collidepoint(pos) and (skins["Goku"]["equipped"] or skins["Serious Saitama"]["equipped"]) and current_time - last_dodge_time >= dodge_cooldown:
                    dodge_active = True
                    dodge_start_time = current_time
                    last_dodge_time = current_time
                    dodge_animation_time = 0
            elif game_state == DEAD and pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 300, 40).collidepoint(pos):
                reset_game(current_level)
            elif game_state == WIN and pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 300, 40).collidepoint(pos):
                total_coins += COIN_REWARDS[current_level]
                player_level += LEVEL_INCREASE[current_level]
                if current_level == 3:
                    total_diamonds += DIAMOND_REWARD
                reset_game(current_level)
        if event.type == pygame.MOUSEBUTTONUP:
            touching_left = False
            touching_right = False

    if game_state == START_SCREEN:
        screen.fill(BLACK)
        screen.blit(font.render("MarioCraft", True, WHITE), (SCREEN_WIDTH // 2 - 50, 100))
        screen.blit(font.render(f"Coins: {total_coins}", True, YELLOW), (SCREEN_WIDTH // 2 - 50, 150))
        screen.blit(font.render(f"Diamonds: {total_diamonds}", True, (0, 191, 255)), (SCREEN_WIDTH // 2 - 50, 180))
        screen.blit(font.render(f"Level: {player_level}", True, WHITE), (SCREEN_WIDTH // 2 - 50, 210))
        screen.blit(font.render("Tap for Level 1 (Easy)", True, WHITE), (SCREEN_WIDTH // 2 - 100, 250))
        screen.blit(font.render("Tap for Level 2 (Medium)", True, WHITE), (SCREEN_WIDTH // 2 - 100, 290))
        screen.blit(font.render("Tap for Level 3 (Hard)", True, WHITE), (SCREEN_WIDTH // 2 - 100, 330))
        screen.blit(font.render("Tap for Level 4 (Hell) [500+]", True, WHITE if player_level >= 500 else GRAY), (SCREEN_WIDTH // 2 - 150, 370))
        screen.blit(font.render("Tap for Skins", True, WHITE), (SCREEN_WIDTH // 2 - 50, 410))

    elif game_state == SKINS_MENU:
        screen.fill(BLACK)
        screen.blit(font.render("Skins Menu", True, WHITE), (SCREEN_WIDTH // 2 - 50, 50))
        screen.blit(font.render(f"Coins: {total_coins}", True, YELLOW), (SCREEN_WIDTH // 2 - 50, 100))
        screen.blit(font.render(f"Diamonds: {total_diamonds}", True, (0, 191, 255)), (SCREEN_WIDTH // 2 - 50, 130))
        screen.blit(font.render("Tap to return", True, WHITE), (SCREEN_WIDTH // 2 - 100, 550))
        screen.blit(font.render(f"Mario ({'Equipped' if skins['Mario']['equipped'] else 'Unequipped'})", True, WHITE), (50, 150))
        screen.blit(font.render(f"Luigi ({'Equipped' if skins['Luigi']['equipped'] else 'Unequipped'})", True, WHITE), (50, 210))
        screen.blit(font.render(f"Cost: {skins['Luigi']['cost']} Coins" if not skins["Luigi"]["unlocked"] else "", True, YELLOW), (50, 180))
        screen.blit(font.render(f"Peach ({'Equipped' if skins['Peach']['equipped'] else 'Unequipped'})", True, WHITE), (50, 270))
        screen.blit(font.render(f"Cost: {skins['Peach']['cost']} Coins" if not skins["Peach"]["unlocked"] else "", True, YELLOW), (50, 240))
        screen.blit(font.render(f"Mushroom ({'Equipped' if skins['Mushroom']['equipped'] else 'Unequipped'})", True, WHITE), (50, 330))
        screen.blit(font.render(f"Cost: {skins['Mushroom']['cost']} Coins" if not skins["Mushroom"]["unlocked"] else "", True, YELLOW), (50, 300))
        screen.blit(font.render(f"Steve ({'Equipped' if skins['Steve']['equipped'] else 'Unequipped'})", True, WHITE), (50, 390))
        screen.blit(font.render(f"Cost: {skins['Steve']['cost']} Coins" if not skins["Steve"]["unlocked"] else "", True, YELLOW), (50, 360))
        screen.blit(font.render(f"Goku ({'Equipped' if skins['Goku']['equipped'] else 'Unequipped'})", True, WHITE), (50, 450))
        screen.blit(font.render(f"Cost: {skins['Goku']['cost']} Diamonds" if not skins["Goku"]["unlocked"] else "", True, (0, 191, 255)), (50, 420))
        screen.blit(font.render(f"S. Saitama ({'Equipped' if skins['Serious Saitama']['equipped'] else 'Unequipped'})", True, WHITE), (50, 510))
        screen.blit(font.render(f"Cost: {skins['Serious Saitama']['cost']} Diamonds" if not skins["Serious Saitama"]["unlocked"] else "", True, (0, 191, 255)), (50, 480))
        screen.blit(skins["Mario"]["image"], (300, 150))
        screen.blit(skins["Luigi"]["image"], (300, 210))
        screen.blit(skins["Peach"]["image"], (300, 270))
        screen.blit(skins["Mushroom"]["image"], (300, 330))
        screen.blit(skins["Steve"]["image"], (300, 390))
        screen.blit(skins["Goku"]["image"], (300, 450))
        screen.blit(skins["Serious Saitama"]["image"], (300, 510))
        if preview_skin:
            width = player_width_goku if preview_skin in ["Goku", "Serious Saitama"] else player_width
            preview_image = skins[preview_skin]["image"] if preview_skin not in ["Goku", "Serious Saitama"] or not dodge_active else skins[preview_skin]["special_image"]
            screen.blit(preview_image, (SCREEN_WIDTH - 100 - width // 2, SCREEN_HEIGHT // 2 - player_height // 2))
            preview_text = font.render(f"Preview: {preview_skin}", True, WHITE)
            screen.blit(preview_text, (SCREEN_WIDTH - 150 - preview_text.get_width(), SCREEN_HEIGHT // 2 - 50))

    elif game_state == PLAYING:
        if dodge_active:
            if current_time - dodge_start_time >= dodge_duration:
                dodge_active = False
            else:
                dodge_animation_time += 1 / 60

        if touching_left:
            player_vel_x = -5
        elif touching_right:
            player_vel_x = 5
        else:
            player_vel_x = 0

        player_x += player_vel_x
        player_y += player_vel_y
        player_vel_y += gravity

        if player_x - camera_x > SCREEN_WIDTH * 0.7:
            camera_x = player_x - SCREEN_WIDTH * 0.7
        if camera_x < 0:
            camera_x = 0
        if camera_x > levels[current_level]["world_width"] - SCREEN_WIDTH:
            camera_x = levels[current_level]["world_width"] - SCREEN_WIDTH

        equipped_skin = next((skin for skin, data in skins.items() if data["equipped"]), "Mario")
        current_width = draw_character(player_x, player_y, equipped_skin)
        player_rect = pygame.Rect(player_x, player_y, current_width, player_height)

        for platform in levels[current_level]["platforms"]:
            if player_rect.colliderect(platform):
                if player_vel_y > 0:
                    player_y = platform.top - player_height
                    player_vel_y = 0
                    is_jumping = False
                elif player_vel_y < 0:
                    player_y = platform.bottom
                    player_vel_y = 0

        for pipe in levels[current_level]["pipes"]:
            if player_rect.colliderect(pipe):
                if player_vel_x > 0:
                    player_x = pipe.left - current_width
                elif player_vel_x < 0:
                    player_x = pipe.right

        for coin in levels[current_level]["coins"][:]:
            if player_rect.colliderect(coin):
                levels[current_level]["coins"].remove(coin)
                total_coins += 50

        for monster in levels[current_level]["monsters"]:
            monster["x"] += monster["vel_x"]
            if monster["x"] < 0 or monster["x"] > levels[current_level]["world_width"] - monster["width"]:
                monster["vel_x"] *= -1
            monster_rect = pygame.Rect(monster["x"], monster["y"], monster["width"], monster["height"])
            if player_rect.colliderect(monster_rect) and not dodge_active:
                jumpscare()
                game_state = DEAD

        if "boss" in levels[current_level]:
            boss = levels[current_level]["boss"]
            boss["x"] += boss["vel_x"]
            if boss["x"] < player_x - 500 or boss["x"] > player_x + 500:
                boss["vel_x"] *= -1
            boss_rect = pygame.Rect(boss["x"], boss["y"], boss["width"], boss["height"])
            if player_rect.colliderect(boss_rect) and not dodge_active:
                jumpscare()
                game_state = DEAD
            boss["bullet_timer"] += 1
            if boss["bullet_timer"] >= 60:
                levels[current_level]["bullets"].append({"x": boss["x"], "y": boss["y"] + boss["height"] // 2, "vel_x": -10})
                boss["bullet_timer"] = 0
            for bullet in levels[current_level]["bullets"][:]:
                bullet_rect = pygame.Rect(bullet["x"], bullet["y"] - 5, 20, 20)
                if player_rect.colliderect(bullet_rect) and not dodge_active:
                    jumpscare()
                    game_state = DEAD

        if player_rect.colliderect(levels[current_level]["flag"]):
            game_state = WIN

        if player_x < 0:
            player_x = 0
        if player_y > SCREEN_HEIGHT - player_height:
            player_y = SCREEN_HEIGHT - player_height
            player_vel_y = 0
            is_jumping = False

        screen.fill(levels[current_level]["bg_color"])
        for platform in levels[current_level]["platforms"]:
            pygame.draw.rect(screen, BLUE, (platform.x - camera_x, platform.y, platform.width, platform.height))
        for pipe in levels[current_level]["pipes"]:
            pygame.draw.rect(screen, GREEN, (pipe.x - camera_x, pipe.y, pipe.width, pipe.height))
        for coin in levels[current_level]["coins"]:
            pygame.draw.rect(screen, YELLOW, (coin.x - camera_x, coin.y, coin.width, coin.height))
        for monster in levels[current_level]["monsters"]:
            draw_goomba(monster)
        if "boss" in levels[current_level]:
            draw_boss(levels[current_level]["boss"])
            draw_bullets(levels[current_level]["bullets"])
        draw_character(player_x, player_y, equipped_skin)
        pygame.draw.rect(screen, YELLOW, (levels[current_level]["flag"].x - camera_x, levels[current_level]["flag"].y, 20, 50))
        draw_progress_bar()
        draw_buttons()
        if equipped_skin in ["Goku", "Serious Saitama"]:
            cooldown_remaining = max(0, dodge_cooldown - (current_time - last_dodge_time))
            screen.blit(font.render(f"Dodge: {int(cooldown_remaining)}s", True, WHITE if cooldown_remaining == 0 else GRAY), (10, 50))

    elif game_state == DEAD:
        screen.fill(BLACK)
        screen.blit(font.render("You Died! Tap to Restart", True, RED), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    elif game_state == WIN:
        screen.fill(GREEN)
        screen.blit(font.render(f"Level {current_level + 1} Complete! Tap to Restart", True, BLACK), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

save_game()
pygame.quit()
sys.exit()