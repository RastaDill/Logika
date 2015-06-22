#!/usr/bin/env python
#  basic.py
#  
#  Copyright (C) 2015 Voznesensky (WeedMan) Michael <weedman@opmbx.org>
#  
#  This file is path of Logika
#  
#  Logika is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  Logika is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with Logika; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

#Basic classes game Logika
import os
import sys
import random
import pygame
from pygame.locals import *

pygame.init()

######Classes Game######
class Sprite(pygame.sprite.Sprite):
	"""Base class creating sprites"""
	def __init__(self, name_image, x_pos, y_pos):
		super(Sprite, self).__init__()
		self.state = None #specifies the state of the object OR writes a special variable
		self.image = pygame.image.load(name_image).convert_alpha() #load and conver image
		self.rect = self.image.get_rect() #method pygame to work with the image
		self.rect.x = x_pos
		self.rect.y = y_pos #coordinates image
	
	def check_mouse(self, m_pos, change_state = True):
		"""Check position mouse on sprite or not"""
		if (self.rect.left < m_pos[0] < self.rect.right) \
			and (self.rect.top < m_pos[1] < self.rect.bottom) \
			and self.state != False:
			if change_state:
				self.state = 4 #True
			return True
		return False
	
	def update(self, screen):
		"""Render sprite on the screen"""
		screen.blit(self.image, self.rect)
	
	def restart_state(self):
		"""Sets the initial state of the state parameter"""
		self.state = None
	
	def switch_state(self):
		"""Changes the state of the object and makes it move"""
		if self.state or self.state == None:
			self.state = False
		else:
			self.state = True

class Candy(Sprite):
	"""Class for candy (here goes the download only audio)"""
	
	s_candy = os.path.join("sound", "candy.ogg")
	
	def __init__(self, name_image, x_pos, y_pos):
		super(Candy, self).__init__(name_image = name_image,
									 x_pos = x_pos,
									 y_pos = y_pos)
		
		self.sound_candy = pygame.mixer.Sound(Candy.s_candy)
	
	def play_sound_candy(self):
		"""Run sound"""
		self.sound_candy.play()
	
class Tumbler(Sprite):
	"""Class administrate tumbler on/off"""
	
	s_on = os.path.join("sound", "tumbler_on.ogg")
	s_off = os.path.join("sound", "tumbler_off.ogg")
	
	def __init__(self, name_image, name_image_next, x_pos, y_pos):
		super(Tumbler, self).__init__(name_image = name_image,
									   x_pos = x_pos,
									   y_pos = y_pos)
		
		self.image_next = pygame.image.load(name_image_next).convert_alpha()
		self.count_frame = 0 #counts the number of frames
		self.sound_on = pygame.mixer.Sound(Tumbler.s_on)
		self.sound_off = pygame.mixer.Sound(Tumbler.s_off)
	
	def check_work(self, end_game):
		"""Returns the tumbler switch from ON state to OFF"""
		#state change at the check_mouse()
		if self.state:
			self.count_frame += 1
			if end_game == None and self.count_frame >= 15:
				self.state = None
				self.count_frame = 0
	
	def update(self, screen):
		if self.state == None:
			screen.blit(self.image, self.rect)
		else:
			screen.blit(self.image_next, self.rect)
	
	def play_sound_on(self):
		self.sound_on.play()
	
	def play_sound_off(self):
		self.sound_off.play()

class Door(Tumbler):
	"""This class is responsible for rendering and move doors"""
	
	s_open = os.path.join("sound", "door_open.ogg")
	s_close = os.path.join("sound", "door_close.ogg")
	
	def __init__(self, name_image, name_image_next, x_pos, y_pos):
		super(Door, self).__init__(name_image = name_image,
									name_image_next = name_image_next,
									x_pos = x_pos,
									y_pos = y_pos)
		self.state = False
		self.delay = 0 #delay after unlocking or before closing
		self.sound_open = pygame.mixer.Sound(Door.s_open)
		self.sound_close = pygame.mixer.Sound(Door.s_close)
		self.play = True #required for a single run of the sound (without a re-start after each function call)
	
	def update(self, screen):
		if self.state and self.count_frame < 35:
			if self.delay < 60:
				self.delay += 1
			else:
				if self.play:
					self.sound_open.play()
					self.play = False
				self.count_frame += 0.5 #open door
		elif not self.state and self.count_frame > 0:
			if self.delay > 30:
				self.delay -= 1
			else:
				if not self.play:
					self.sound_close.play()
					self.play = True
					self.delay = 0
				self.count_frame -= 1 #close door
			
		screen.blit(self.image, [self.rect.x, self.rect.y-self.count_frame]) #first path door
		screen.blit(self.image_next, [self.rect.x, self.rect.y+12+self.count_frame]) #second path door

class Button(Sprite):
	"""All buttons in game"""
	
	s_down = os.path.join("sound", "button_down.ogg")
	s_up = os.path.join("sound", "button_up.ogg")
	
	def __init__(self, name_image, name_image_next, x_pos, y_pos):
		super(Button, self).__init__(name_image = name_image,
										  x_pos = x_pos,
										  y_pos = y_pos)
		
		self.image_previous = self.image
		self.image_next = pygame.image.load(name_image_next).convert_alpha()
		self.sound_down = pygame.mixer.Sound(Button.s_down)
		self.sound_up = pygame.mixer.Sound(Button.s_up)
	
	def change_image_d(self):
		"""This method is designed for events press DOWN"""
		self.sound_up.stop()
		if not self.state:
			self.state = True
		self.sound_down.play()
		self.image = self.image_next
	
	def change_image_u(self):
		"""This method is designed for events press UP"""
		self.sound_down.stop()
		if self.state:
			#self.state = 4 then run mouse event
			if self.state != 4:
				self.state = None
			self.sound_up.play()
		self.image = self.image_previous

class Result(Sprite):
	"""This class displays the sprites on them for the next result output"""
	def __init__(self, name_gamma, name_omega, name_miniscreen, x_pos, y_pos):
		super(Result, self).__init__(name_image = name_gamma,
									   x_pos = x_pos,
									   y_pos = y_pos)
		
		self.image_omega = pygame.image.load(name_omega).convert_alpha()
		self.image_miniscreen = pygame.image.load(name_miniscreen).convert_alpha()
	
	def update(self, screen):
		screen.blit(self.image, self.rect)
		screen.blit(self.image_omega, [self.rect.x + 52, self.rect.y])
		screen.blit(self.image_miniscreen, [self.rect.x + 23, self.rect.y]) #self.rect.x=400
		screen.blit(self.image_miniscreen, [self.rect.x + 78, self.rect.y])
		
class Block(Sprite):
	"""Creating block
	the states and their meaning:
	0 - block is locked
	1 - first position
	2 - position on drop point (__new_position)
	3 - show block on the screen
	4 - move object mouse
	5 - downtime (moment create object)"""
	
	block_image = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png"] #list name image blocks
	
	s_take = os.path.join("sound", "block_take.ogg")
	s_drop = os.path.join("sound", "block_drop.ogg")
	s_slide = os.path.join("sound", "block_slide.ogg")
	
	def __init__(self, name_image, x_pos, y_pos, id_number, x_out = 710):
		super(Block, self).__init__(name_image = name_image,
									 x_pos = x_out,
									 y_pos = y_pos)
		self.path = name_image
		self.state = 5 #state create block (pisiton out in the screen)
		self.ind_pos = None #writes index position on drop point
		self.id_number = id_number #id blocks
		self.x = x_pos
		self.y = y_pos #additional entry coordinate
		self.sound_take = pygame.mixer.Sound(Block.s_take)
		self.sound_drop = pygame.mixer.Sound(Block.s_drop)
		self.sound_slide = pygame.mixer.Sound(Block.s_slide)
	
	def update(self, m_pos):
		"""Change the coordinates when moving the block with the mouse, or return to the default position"""
		if self.state == 4:
			self.rect.x = m_pos[0]-self.rect.width/2
			self.rect.y = m_pos[1]-self.rect.height/2
		elif self.state == 1:
			self.rect.x = self.x
			self.rect.y = self.y
		elif self.state == 3:
			self.rect.x -= 4
			if self.rect.x <= self.x:
				self.state = 1
	
	def check_point(self, drop_list, line):
		"""Check position block on drop point or not"""
		if self.state == 4:
			count_cross = 0 #count crossing block on drop point
			for j in range(len(drop_list[line])):
				if pygame.sprite.collide_rect(drop_list[line][j], self) and count_cross < 2:
					count_cross += 1
					if drop_list[line][j].state == None:
						self.__new_position(drop_list, line, j) #new block position
						break
				
			if count_cross == 0:
				#return block first position
				if self.ind_pos != None:
					drop_list[line][self.ind_pos].state = None
					self.ind_pos = None
				self.state = 1
			else:
				#return block previously position
				if self.ind_pos != None:
					self.__new_position(drop_list, line, self.ind_pos)
				else:
					self.state = 1
			
			self.play_sound_drop()
	
	def __new_position(self, drop_list, line, j):
		"""The coordinates of the block on the drop point"""
		if self.ind_pos != None: #clear previously position
			drop_list[line][self.ind_pos].state = None
		
		self.state = 2
		self.rect.x = drop_list[line][j].rect.x+4
		self.rect.y = drop_list[line][j].rect.y
		
		self.ind_pos = j #write index point in block
		drop_list[line][j].state = self.id_number #write id block in state point
	
	def change_state(self):
		"""The state change for that would block appeared from off screen"""
		if self.state == 5:
			self.sound_slide.play()
			self.state = 3
	
	def play_sound_take(self):
		self.sound_take.play()
	
	def play_sound_drop(self):
		self.sound_drop.play()

class Brain(object):
	"""The class handles the rules (logic) of the game"""
	
	s_refusal = os.path.join("sound", "refusal.ogg")
	s_unlock = os.path.join("sound", "unlock.ogg")
	s_lock = os.path.join("sound", "lock.ogg")
	
	def __init__(self, y_drop, block_list, old_block_list, drop_list, tumbler_list, game):
		self.font = pygame.font.Font(os.path.join("font", "DejaVuSansMono.ttf"), 16) #font for balance
		self.font_state = pygame.font.Font(os.path.join("font", "DejaVuSansMono.ttf"), 25) #font for state
		self.balance_gamma = self.font.render("", True, [24, 240, 24]) #enter text on screen about number bulls (gamma)
		self.balance_omega = self.font.render("", True, [24, 240, 24]) #enter text on screen about number cows (omega)
		self.text_state = self.font_state.render("-------", True, [255, 255, 0]) #enter text on screen YOU WIN or YOU LOSE
		self.balance_list = [] #list all number bulls and cows
		
		self.y = y_drop #this y coordinate drop point
		
		self.xy_state = [393, 19]
		self.count_return = 0 #count time for return text
		self.text_return = False #if true then text_state = "--------"
		
		self.__survive = False #mode survival
		self.count_frame = 0 #count frame
		self.seconds = 0 #count seconds
		self.minutes = 3 #count minutes
		self.time_end = False #check end time
		
		self.game = game #the reference to the outer class Game
		
		#load sound
		self.sound_refusal = pygame.mixer.Sound(Brain.s_refusal)
		self.sound_unlock = pygame.mixer.Sound(Brain.s_unlock)
		self.sound_lock = pygame.mixer.Sound(Brain.s_lock)
		
		#basic list
		self.block_list = block_list
		self.old_block_list = old_block_list
		self.drop_list = drop_list
		self.tumbler_list = tumbler_list
	
	def run_survival(self, check_run):
		"""Run mode survival"""
		if check_run:
			self.__survive = True
		else:
			self.__survive = False
	
	def check_block_line(self, line, secret_comb, door):
		"""Check the line on blocks"""
		if self.time_end:
			#run then minutes = 0 and seconds = 0
			self.sound_lock.play()
			return line, True, False
		else:
			winning = None #the transition to the next attempt
			block_line = [] #our blocks on the current line
			
			#on current tumbler (state = False)
			self.tumbler_list[line].play_sound_on()
			self.tumbler_list[line].switch_state()
			
			#append id blocks in block_line
			for j in range(len(self.drop_list[line])):
				if self.drop_list[line][j].state != None:
					block_line.append(self.drop_list[line][j].state)
			
			#check on the filling line OR filling all chance_box in chance
			#and check the option to give a new chance
			if len(block_line) == len(self.drop_list[line]):
				winning = self.__check_rule(secret_comb, block_line)
			
			if winning == None:
				#off current tumbler
				self.tumbler_list[line].play_sound_off()
				self.tumbler_list[line].switch_state()
				return line, None, winning
			elif winning:
				self.__lock_block()
				door.switch_state()
				self.__game_text_state("unlock", [0, 255, 0], [400, 19])
				self.sound_unlock.play()
				return line, True, winning
			else:
				if line + 1 == len(self.drop_list): #len(drop_list) == chance
					self.__lock_block()
					self.__game_text_state("lock", [255, 0, 0], [414, 19])
					self.sound_lock.play()
					return line, True, winning
				else:
					self.__lock_block(True)
					self.__game_text_state("refusal", [255, 255, 0])
					self.sound_refusal.play()
					return line + 1, False, winning
	
	def __lock_block(self, create_new = False):
		"""Lock blocks and create new if needed"""
		for block in self.block_list:
			if not create_new:
				block.state = 0 #lock all block
			else:
				if block.ind_pos != None:
					block.state = 0 #lock and the creation of new blocks which stood on the position
					new_block = Block(block.path, block.x, block.y, block.id_number)
					self.old_block_list.add(block)
					self.block_list.remove(block)
					self.block_list.add(new_block)
	
	def __game_text_state(self, text, color, xy_state = [393, 19]):
		"""Setting the state text"""
		if not self.__survive:
			self.xy_state = xy_state
			self.text_state = self.font_state.render(text, True, color)
			if text == "refusal":
				self.text_return = True
		elif text != "refusal": self.time_end = True
	
	def __check_rule(self, secret_comb, block_line):
		"""Check rule game"""
		b = 0 #bull (gamma)
		c = 0 #cow (omega)
		for i in range(len(secret_comb)):
			try:
				box = secret_comb.index(block_line[i])
			except ValueError:
				box = None
			
			if box == i:
				b += 1
			elif box != None:
				c += 1
		
		self.balance_gamma = self.font.render(str(b), True, [24, 240, 24])
		self.balance_omega = self.font.render(str(c), True, [24, 240, 24])
		self.balance_list.append(self.balance_gamma)
		self.balance_list.append(self.balance_omega)
		
		if b == 4:
			return True
		else: return False
	
	def __check_refusal(self):
		"""Retun first state text after output refusal"""
		if self.text_return:
			self.count_return += 1
			if self. count_return == 120:
				self.text_state = self.font_state.render("-------", True, [255, 255, 0])
				self.text_return = False
				self.count_return  = 0
	
	def __time(self):
		"""Calculated and displayed time"""
		if (self.minutes > 0 or self.seconds > 0) and not self.time_end:
			self.count_frame += 1 #60 fps (self.clock.tick(60))
			if self.count_frame > 60:
				self.count_frame = 0
				self.seconds -= 1
				if self.seconds < 0:
					self.seconds += 60
					self.minutes -= 1
		else:
			self.time_end = True
			self.game.run_rule_brain()
		
		#check position
		if self.seconds < 10:
			self.xy_state = [422, 19]
		else:
			self.xy_state = [414, 19]
		
		self.text_state = self.font_state.render((str(self.minutes) + ":" + str(self.seconds)), True, [255, 255, 0])
	
	def update(self, screen):
		"""Print on screen bulls, cows and text state"""
		for i in range(0, len(self.balance_list), 2):
			screen.blit(self.balance_list[i], [430, (self.y*i*0.5)+91]) #the x coordinate almost is the same as the sprite miniscreen
			screen.blit(self.balance_list[i+1], [485, (self.y*i*0.5)+91])
		
		if not self.__survive:
			self.__check_refusal()
		else:
			self.__time()
		
		screen.blit(self.text_state, self.xy_state)
	
	def brain_restart(self):
		"""Reset list balance_list and return the starting coordinates and parameter text_state"""
		self.seconds = 0
		self.minutes = 3
		self.time_end = False
	
		del self.balance_list[:]
		self.xy_state = [393, 19]
		self.text_state = self.font_state.render("-------", True, [255, 255, 0])
######Classes Game######

######Classes Menu######
class MainMenu(pygame.sprite.LayeredUpdates):
	"""The group which will contain all the objects main menu"""
	
	s_transition_up = os.path.join("sound", "transition_up.ogg")
	s_transition_down = os.path.join("sound", "transition_down.ogg")
	
	def __init__(self):
		super (MainMenu, self).__init__()
		self.count_y = 0
		self.step = 0
		self.state = False
		
		self.sound_transition_u = pygame.mixer.Sound(MainMenu.s_transition_up)
		self.sound_transition_d = pygame.mixer.Sound(MainMenu.s_transition_down)
	
	def switch_state(self):
		"""The state of the object is responsible for moving"""
		if self.state:
			self.sound_transition_u.play()
			self.state = False
		else:
			self.sound_transition_d.play()
			self.state = True
	
	def move(self):
		"""Moving menu"""
		if self.state:
			if self.count_y > -480:
				self.step = -10 #menu up
				self.__change_y()
				return False
			else: return True
		elif not self.state:
			if self.count_y < 0:
				self.step = 10 #menu down
				self.__change_y()
				return False
			else: return False
	
	def __change_y(self):
		"""Change coordinate y for moving"""
		self.count_y += self.step
		for obj in self:
			obj.rect.y += self.step

class TextMenu(pygame.sprite.Sprite):
	"""Text main menu"""
	var_text = {0 : "New Game",
				1 : "Rules",
				2 : "Survival",
				3 : "  Exit",
				4 : "Credits"}
	
	def __init__(self, x_pos, y_pos):
		super(TextMenu, self).__init__()
		self.__current_text = 0 #current text on the screen
		self.color = [0, 255, 0]
		
		self.font = pygame.font.Font(os.path.join("font", "DejaVuSansMono.ttf"), 30)
		self.image = self.font.render(TextMenu.var_text[self.__current_text], True, self.color) #output text on screen
		self.rect = self.image.get_rect()
		self.rect.x = x_pos
		self.rect.y = y_pos
		self.x = x_pos #copy
		self.y = y_pos
	
	def left_text(self):
		"""Moving current text left"""
		self.__current_text -= 1
		self.__change_text()
	
	def right_text(self):
		"""Moving current text right"""
		self.__current_text += 1
		self.__change_text()
	
	def __change_text(self):
		"""Change text"""
		if self.__current_text == len(TextMenu.var_text):
			self.__current_text = 0
		elif self.__current_text < 0:
			self.__current_text = len(TextMenu.var_text)-1
		
		self.__render()
	
	def new_optional(self):
		"""Add option Resume"""
		self.__current_text = 5
		if self.__current_text not in TextMenu.var_text:
			TextMenu.var_text[self.__current_text] = " Resume"
		self.__render()
	
	def delete_optional(self):
		"""Delete option Resume"""
		self.__current_text = 5
		if self.__current_text in TextMenu.var_text:
			del TextMenu.var_text[self.__current_text]
		self.__current_text = 0
		self.__render()
	
	def __render(self):
		"""Setting text for render"""
		if self.__current_text == 4:
			self.rect.x += 9
		elif self.__current_text == 1:
			self.rect.x += 27
		else: self.rect.x = self.x
		self.image = self.font.render(TextMenu.var_text[self.__current_text], True, self.color)
		
	@property
	def current_text(self):
		return self.__current_text

class Description(Sprite):
	"""Class for special sprites (contains description)"""
	def __init__(self, name_image, x_pos, y_pos, screen_size):
		super(Description, self).__init__(name_image = name_image,
										   x_pos = x_pos,
										   y_pos = y_pos)
		self.state = False
		self.count_x = -1
		self.count_y = -1
		self.screen_size = screen_size
	
	def update(self, screen):
		self.__check_move()
		screen.blit(self.image, [self.rect.x + self.count_x, self.rect.y + self.count_y])
		
	def __check_move(self):
		"""Checks on which axis to move, relative to the initial location of the object behind the screen"""
		if self.rect.x > self.screen_size[0]:
			#move to x
			self.count_x = self.__moving(self.count_x, self.screen_size[0])
		else:
			#move to y
			self.count_y = self.__moving(self.count_y, self.screen_size[1])
	
	def __moving(self, count, size):
		"""Changing the offset parameter"""
		if self.state and count > -size:
			count -= 10
		elif not self.state and count < 0:
			count += 10
		return count
	
	def end_motion(self):
		"""Check end motion"""
		if self.state:
			return True
		if not self.state:
			if self.count_x >= 0 or self.count_y >= 0:
				return False
			else:
				return True

class Bolt(Sprite):
	"""Class for rotate bolt"""
	
	s_clockwise = os.path.join("sound", "bolt_clockwise.ogg")
	s_counterclockwise = os.path.join("sound", "bolt_counterclockwise.ogg")
	
	def __init__(self, name_image, xy_pos):
		super(Bolt, self).__init__(name_image = name_image,
									x_pos = xy_pos[0],
									y_pos = xy_pos[1])
		
		self.state = False
		
		self.org_image = self.image #the original surface to rotate the image
		self.angle = random.randrange(360)
		self.count_step = 0
		
		self.image = pygame.transform.rotate(self.org_image, self.angle)
		
		self.sound_clockwise = pygame.mixer.Sound(Bolt.s_clockwise)
		self.sound_counterclockwise = pygame.mixer.Sound(Bolt.s_counterclockwise)
	
	def rotate(self, direction):
		"""Roate bolt"""
		if direction:
			#rotate clockwise
			if self.count_step < 360:
				self.count_step += 4
				self.image = pygame.transform.rotate(self.org_image, self.angle + self.count_step)
				if not self.state:
					self.sound_clockwise.play()
					self.switch_state()
		else:
			#rotate counterclockwise
			if self.count_step > 0:
				self.count_step -= 4
				self.image = pygame.transform.rotate(self.org_image, self.angle + self.count_step)
				if self.state:
					self.sound_counterclockwise.play()
					self.switch_state()
######Classes Menu######

if __name__ == '__main__':
	print "You run module: basic"
