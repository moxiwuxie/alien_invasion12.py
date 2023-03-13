#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame
import pygame.font
from pygame.sprite import Group
from ship import Ship
class ScoreBoard():
  """exhxbt score data """
  def __init__(self,ai_settings,screen,status):
    self.screen = screen
    self.screen_rect = screen.get_rect()
    self.ai_settings = ai_settings
    self.status = status
    self.text_color = (30,30,30)
    self.font = pygame.font.SysFont(None,48)
    self.prep_score()
    self.prep_high_score()
    self.prep_level()
    self.prep_ships()
  def prep_score(self):
    """screen jameg score"""
    rounded_score = int(round(self.status.score,-1))
    score_str = "{:,}".format(rounded_score)
    # score_str = str(self.status.score)
    self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)
    self.score_rect = self.score_image.get_rect()
    self.score_rect.right = self.screen_rect.right - 20
    self.score_rect.top = 20
  def show_score(self):
    """screen"""
    self.screen.blit(self.score_image,self.screen_rect)
    self.screen.blit(self.high_score_image,self.high_score_rect)
    self.screen.blit(self.level_image,self.level_rect)
    self.ships.draw(self.screen)
  def prep_high_score(self):
    """let high_score change to screen image"""
    high_score = int(round(self.status.high_score,-1))
    high_score_str = "{:,}".format(high_score)
    self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)
    self.high_score_rect = self.high_score_image.get_rect()
    self.high_score_rect.centerx = self.screen_rect.centerx
    self.high_score_rect.top = self.high_score_rect.top
  def prep_level(self):
    """level"""
    self.level_image = self.font.render(str(self.status.level),True,self.text_color,self.ai_settings.bg_color)
    self.level_rect = self.level_image.get_rect()
    self.level_rect.right = self.score_rect.right
    self.level_rect.top = self.score_rect.bottom+10
  def prep_ships(self):
    """stay ships"""
    self.ships = Group()
    for ship_number in range(self.status.ships_left):
      ship = Ship(self.ai_settings,self.screen)
      ship.rect.x = 10+ship_number * ship.rect.width
      ship.rect.y = 10
      self.ships.add(ship)
