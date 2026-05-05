import pygame
import random
import sys
import json
import os
# ===================== SETTINGS =====================
SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
   "sound": True,
   "grid": False,
   "speed": "normal",
   "color": [0, 255, 0]
}
def load_settings():
   if os.path.exists(SETTINGS_FILE):
       try:
           with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
               return json.load(f)
       except:
           pass
   return DEFAULT_SETTINGS.copy()
def save_settings():
   with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
       json.dump(settings, f, indent=2)
settings = load_settings()
# ===================== INIT =====================
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 600, 400
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake PRO")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
big = pygame.font.SysFont("Arial", 40)
GREEN = tuple(settings["color"])
# ===================== SOUND =====================
def safe_sound(path):
   try:
       if os.path.exists(path):
           return pygame.mixer.Sound(path)
   except:
       pass
   return None
def play_music():
   try:
       if settings["sound"]:
           pygame.mixer.music.load("sounds/music.mp3")
           pygame.mixer.music.play(-1)
   except:
       pass
crash_sound = safe_sound("sounds/crash.wav")
# ===================== GAME DATA =====================
snake = [(100,100),(80,100),(60,100)]
direction = (CELL,0)
score = 0
def spawn_food():
   return (random.randrange(0, WIDTH, CELL),
           random.randrange(0, HEIGHT, CELL))
food = spawn_food()
# ===================== SPEED =====================
def get_fps():
   if settings["speed"] == "slow":
       return 6
   if settings["speed"] == "fast":
       return 15
   return 10
# ===================== MENU =====================
def menu():
   while True:
       screen.fill((0,0,0))
       screen.blit(big.render("SNAKE PRO",True,(255,255,255)),(180,80))
       screen.blit(font.render("ENTER - PLAY",True,(255,255,255)),(200,180))
       screen.blit(font.render("S - SETTINGS",True,(255,255,255)),(200,210))
       screen.blit(font.render("L - LEADERBOARD",True,(255,255,255)),(200,240))
       pygame.display.flip()
       for e in pygame.event.get():
           if e.type == pygame.QUIT:
               sys.exit()
           if e.type == pygame.KEYDOWN:
               if e.key == pygame.K_RETURN:
                   return
               if e.key == pygame.K_s:
                   settings_menu()
               if e.key == pygame.K_l:
                   leaderboard()
# ===================== SETTINGS =====================
def settings_menu():
   global GREEN
   colors = [(0,255,0),(255,255,0),(0,255,255),(255,0,0)]
   i = colors.index(tuple(settings["color"])) if tuple(settings["color"]) in colors else 0
   while True:
       screen.fill((20,20,20))
       screen.blit(big.render("SETTINGS",True,(255,255,255)),(180,50))
       lines = [
           f"1 Sound: {settings['sound']}",
           f"2 Grid: {settings['grid']}",
           f"3 Speed: {settings['speed']}",
           "4 Color",
           "S Save & Back"
       ]
       y = 140
       for l in lines:
           screen.blit(font.render(l,True,(255,255,255)),(180,y))
           y += 40
       pygame.display.flip()
       for e in pygame.event.get():
           if e.type == pygame.QUIT:
               sys.exit()
           if e.type == pygame.KEYDOWN:
               if e.key == pygame.K_1:
                   settings["sound"] = not settings["sound"]
                   if settings["sound"]:
                       play_music()
                   else:
                       pygame.mixer.music.stop()
               if e.key == pygame.K_2:
                   settings["grid"] = not settings["grid"]
               if e.key == pygame.K_3:
                   settings["speed"] = "fast" if settings["speed"]=="normal" else "slow" if settings["speed"]=="fast" else "normal"
               if e.key == pygame.K_4:
                   i = (i+1) % len(colors)
                   settings["color"] = list(colors[i])
                   GREEN = tuple(settings["color"])
               if e.key == pygame.K_s:
                   save_settings()
                   return
# ===================== LEADERBOARD =====================
def leaderboard():
   while True:
       screen.fill((0,0,0))
       screen.blit(big.render("TOP 10 (local)",True,(255,255,255)),(180,50))
       screen.blit(font.render("ESC - BACK",True,(150,150,150)),(240,350))
       pygame.display.flip()
       for e in pygame.event.get():
           if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
               return
# ===================== RESTART =====================
def restart():
   global snake, score, direction, food
   snake = [(100,100),(80,100),(60,100)]
   direction = (CELL,0)
   score = 0
   food = spawn_food()
# ===================== START =====================
menu()
play_music()
# ===================== GAME LOOP =====================
while True:
   for e in pygame.event.get():
       if e.type == pygame.QUIT:
           sys.exit()
       if e.type == pygame.KEYDOWN:
           if e.key == pygame.K_UP:
               direction = (0,-CELL)
           if e.key == pygame.K_DOWN:
               direction = (0,CELL)
           if e.key == pygame.K_LEFT:
               direction = (-CELL,0)
           if e.key == pygame.K_RIGHT:
               direction = (CELL,0)
           if e.key == pygame.K_r:
               restart()
   head = (snake[0][0]+direction[0], snake[0][1]+direction[1])
   # collision
   if head in snake or head[0]<0 or head[0]>=WIDTH or head[1]<0 or head[1]>=HEIGHT:
       if crash_sound:
           crash_sound.play()
       pygame.time.delay(500)
       restart()
   snake.insert(0, head)
   if head == food:
       score += 1
       food = spawn_food()
   else:
       snake.pop()
   screen.fill((0,0,0))
   for s in snake:
       pygame.draw.rect(screen, GREEN, (*s,CELL,CELL))
   pygame.draw.rect(screen,(255,0,0),(*food,CELL,CELL))
   screen.blit(font.render(f"Score: {score}",True,(255,255,255)),(10,10))
   if settings["grid"]:
       for x in range(0,WIDTH,CELL):
           pygame.draw.line(screen,(40,40,40),(x,0),(x,HEIGHT))
   pygame.display.flip()
   clock.tick(get_fps())