#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import pygame
from  settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_status import GameStatus
from button import Button
from scoreboard import ScoreBoard
def run_game():
  #初始化游戏并创建一个屏幕对象
  pygame.init()
  ai_settings  =  Settings()
  screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
  pygame.display.set_caption("Alien Invasion")
  #创建一个ship实例
  ship = Ship(ai_settings,screen)
  #创建一个外星人实例
  alien = Alien(ai_settings,screen)
  #创建一个存储外星人的编组
  aliens = Group()
  #创建外星人群
  gf.create_fleet(ai_settings, screen,ship, aliens)
  #创建一个用于存储子弹的编组
  bullets = Group()
  pygame.display.set_caption("Alien Invasion")
  #创建一个用于存储游戏统计信息的实例
  status = GameStatus(ai_settings)
  #create score caculate
  sb = ScoreBoard(ai_settings,screen,status)
  #创建play按钮
  play_button = Button(ai_settings,screen,msg = "play")
  #开始游戏的主循环
  while True:
    #监视键盘和鼠标事件
    gf.check_events(ship,ai_settings,bullets,screen,status,play_button,aliens)
    gf.update_screen(ship, ai_settings, bullets, screen, aliens, status, play_button,sb)
    if status.game_active:
      ship.update()
      # 每次循环时都重绘屏幕
      gf.update_bullets(ai_settings, screen, ship, aliens, bullets,status,sb)
      gf.update_aliens(ai_settings, aliens, ship, screen, status, bullets,sb)

run_game()
