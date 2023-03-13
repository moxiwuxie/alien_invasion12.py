#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import pygame
import ship
from bullet import Bullet
from alien import Alien
from time import sleep
def check_keydown_events(event,ship,ai_settings,bullets,screen):
  """响应按键"""
  if event.key == pygame.K_RIGHT:
    ship.moving_right = True
  if event.key == pygame.K_LEFT:
    ship.moving_left = True
  elif event.key == pygame.K_SPACE:
    fire_bullet(ship,ai_settings,bullets,screen)
  elif event.key == pygame.K_q:
    sys.exit()
def fire_bullet(ship,ai_settings,bullets,screen):
  """如果没有到达限制，就发射一颗子弹"""
  if len(bullets) < ai_settings.bullets_allowed:
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)
def check_keyup_events(event,ship):
  """响应松开"""
  if event.key == pygame.K_RIGHT:
    ship.moving_right = False
  if event.key == pygame.K_LEFT:
    ship.moving_left = False
def check_events(ship,ai_settings,bullets,screen,status,play_button,aliens):
  """响应按键和鼠标事件"""
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      check_keydown_events(event,ship,ai_settings,bullets,screen)
    elif event.type == pygame.KEYUP:
      check_keyup_events(event,ship)
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x,mouse_y = pygame.mouse.get_pos()
      check_play_button(ai_settings, screen,status,play_button,mouse_x,mouse_y,aliens,bullets,ship,sb)

def check_play_button(ai_settings, screen,status,play_button,mouse_x,mouse_y,aliens,bullets,ship,sb):
  """start game when player click the button"""
  button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
  if button_clicked and not status.game_active:
    ai_settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    status.reset_status()
    status.game_active = True
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen,ship, aliens)
    ship.center_ship()
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()







def update_screen(ship,ai_settings,bullets,screen,aliens,status,play_button,sb):
  screen.fill(ai_settings.bg_color)
  # 在飞船和外星人后面重绘所有子弹
  for bullet in bullets.sprites():
    bullet.draw_bullet()
  ship.blitme()
  # aliens.blitme()
  aliens.draw(screen)
  sb.show_score()
  if not status.game_active:
    play_button.draw_button()
  pygame.display.flip()


def update_bullets(ai_settings, screen,ship, aliens,bullets,status,sb):
  """更新子弹的位置，并删除已消失的子弹"""
  #更新子弹的位置
  bullets.update()
  # 删除已消失的子弹
  for bullet in bullets.copy():
    if bullet.rect.bottom <= 0:
      bullets.remove(bullet)
  # print(len(bullets))
  check_bullet_alien_collisions(ai_settings, screen,ship, aliens,bullets,status,sb)

def check_bullet_alien_collisions(ai_settings, screen,ship, aliens,bullets,status,sb):
  collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
  if collisions:
    for aliens in collisions.values():
      status.score += ai_settings.alien_points * len(aliens)
      sb.prep_score()
      check_high_score(status,sb)
  if len(aliens) == 0:
    bullets.empty()
    ai_settings.increase_speed()
    status.level += 1
    sb.prep_level()
    create_fleet(ai_settings, screen,ship, aliens)
def check_high_score(status,sb):
  """check high_score created"""
  if status.score > status.high_score:
    status.high_score = status.score
    sb.prep_high_score()






def get_number_aliens_x(ai_settings,alien_width):
  """计算每行可容纳多少个外星人"""
  available_space_x = ai_settings.screen_width - 2 * alien_width
  number_aliens_x = int(available_space_x / (2 * alien_width))
  return number_aliens_x

def get_number_rows(ai_settings,alien_height,ship_height):
  """计算屏幕可容纳多少行外星人"""
  available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
  number_rows = int(available_space_y / (2 * alien_height))
  return number_rows





def create_alien(ai_settings,screen,aliens,alien_number,row_number):
  """创建一个外星人并将其放在当前行"""
  alien = Alien(ai_settings, screen)
  alien_width = alien.rect.width
  alien.x = alien_width + 2 * alien_width * alien_number
  alien.rect.x = alien.x
  alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
  aliens.add(alien)


def create_fleet(ai_settings, screen,ship, aliens):
  """创建外星人群"""
  alien= Alien(ai_settings,screen)
  number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
  number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
  # 创建第一行外星人
  for row_number in range(number_rows):
    for alien_number in range(number_aliens_x):
      # 创建一个外星人并将其加入当前行
      create_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
  """有外星人到达边缘时采取相应的措施"""
  for alien in aliens.sprites():
    if alien.check_edges():
      change_fleet_direction(ai_settings,aliens)
      break

def change_fleet_direction(ai_settings,aliens):
  """将郑群外星人下移，并改变他们的方向"""
  for alien in aliens.sprites():
    alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1



def ship_hit(ai_settings,aliens,ship,screen,status,bullets,sb):
  """响应被外星人撞到的飞船"""


  if status.ships_left > 0:
    status.game_active = False
    pygame.mouse.set_visible(True)
    status.ships_left -= 1
    sb.prep_ships()
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen,ship, aliens)
    ship.center_ship()
    sleep(0.5)
  else:
    status.game_active = False




def check_aliens_bottom(ai_settings,aliens,ship,screen,status,bullets,sb):
  """检查是否有外星人到达了屏幕底端"""
  screen_rect = screen.get_rect()
  for alien in aliens.sprites():
    if alien.rect.bottom >= screen_rect.bottom:
      ship_hit(ai_settings,aliens,ship,screen,status,bullets,sb)
      break




def update_aliens(ai_settings,aliens,ship,screen,status,bullets,sb):
  """更新外星人群中所有外星人的位置"""
  check_fleet_edges(ai_settings,aliens)
  aliens.update()
  if pygame.sprite.spritecollideany(ship,aliens):
    # print("Ship hit!!")
    ship_hit(ai_settings,aliens,ship,screen,status,bullets)
  check_aliens_bottom(ai_settings, aliens, ship, screen, status, bullets,sb)




"""
avilable_space_y = ai_settings.screen_height -3 * alien_heght - ship_height
number_rows = available_space_y / (2 * alien_height)




"""

