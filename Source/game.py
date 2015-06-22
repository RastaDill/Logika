#!/usr/bin/env python
#  game.py
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

#Create all object in game logika
import basic
import os
import sys
import random
import pygame
from pygame.locals import *

class Game (object):
	"""The class responsible for running the game, creating objects"""
	
	s_main_theme = os.path.join("sound", "main_theme.ogg")
	
	pygame.mixer.music.load(s_main_theme)
	pygame.mixer.music.play(-1)
	
	def __init__(self):
		pygame.init() #initialization pygame
		
		icon = pygame.image.load(os.path.join("image", "icon.png"))
		pygame.display.set_icon(icon)
		pygame.display.set_caption("Logika")
		
		self.size = [640, 480] #window size
		self.clock = pygame.time.Clock() #fps/frame
		self.screen = pygame.display.set_mode(self.size) #create window
		
		#block data
		self.x_block, self.y_block = 528, 44 #basic x and y coordinate first block
		self.block_list = pygame.sprite.LayeredUpdates() #group of blocks class Block (manages layers)
		self.old_block_list = pygame.sprite.Group() #the group of blocks which can not be moved
		self.render_up_block = False #render other sprites over block (pipe_u and playinf_field_board)
		
		#pipe data
		self.pipe_d_list = pygame.sprite.Group() #the group of pipe down path
		self.pipe_u_list = pygame.sprite.Group() #the group of pipe up path
		
		#drop point data
		self.x_drop, self.y_drop = 85, 50
		self.drop_list = [] #list drop point class Drop
		self.line = 0 #first line two-dimensional drop_list of first chance
		self.chance = 8 #the number of attempts
		self.chance_box = 4 #boxes at the chance
		self.delta_y = 85 #the magnitude of change y
		self.delta_x = 20 #the magnitude of change x
		
		#tumbler data
		self.tumbler_list = [] #list tumbler
		
		#result data
		self.result_list = [] #the list all sprites for result
		
		#candy data
		self.render_up_candy = True #render candy over other sprites
		
		#general game data
		self.variant_number = range(10) #all number which can be in secret combination (variant_number = id_number)
		self.secret_comb = [] #secret combination which must guess player
		self.end_game = None #check game over or not
		self.winning = None #check win or lose
		self.count_frame = 0 #count frame
		
		#switch event
		self.switch_event = False
		
		#menu Group
		self.main_menu = basic.MainMenu()
		
		#main menu data
		self.check_run_newgame = False
		self.check_run_rule = False
		self.check_run_about = False
		self.check_run_survival = None
		
		#bolt data
		self.bolt_list = [] #list bolts class Bolt
		self.check_rotate = True
		self.xy_pos_bolt = [[2, 2], [623, 2], [623, 463], [2, 463]] #list of coordinates of four bolts
	
	def create_object_game_static(self):
		"""Creating game objects not requiring a rebuild when you restart"""
		#Create objects playing field
		self.playing_field = basic.Sprite(os.path.join("image", "background",  "playing_field.png"), 0, 0)
		self.playing_field_board = basic.Sprite(os.path.join("image", "background",  "playing_field_board.png"), 0, 0)
		
		#Create button
		self.button_menu = basic.Button(os.path.join("image", "button", "menu_up_b.png"),
										  os.path.join("image", "button", "menu_down_b.png"),
										  self.x_drop*self.chance_box+68, 50)
		self.button_restart = basic.Button(os.path.join("image", "button", "restart_up_b.png"),
											 os.path.join("image", "button", "restart_down_b.png"),
											 self.x_drop*self.chance_box+113, 50)
		
		#Create object pipe_d, pipe_u
		for i in range(len(basic.Block.block_image)):
			pipe_d = basic.Sprite(os.path.join("image", "pipe", "pipe_down.png"), self.x_block-2, (self.y_block*i)+25)
			pipe_u = basic.Sprite(os.path.join("image", "pipe", "pipe_up.png"), self.x_block+54, (self.y_block*i)+25)
			
			self.pipe_d_list.add(pipe_d)
			self.pipe_u_list.add(pipe_u)
		
		#Create object drop, tumbler, result
		for i in range(self.chance):
			self.drop_list.append([])
			
			tumbler = basic.Tumbler(os.path.join("image", "tumbler", "tumbler_off.png"),
									  os.path.join("image", "tumbler", "tumbler_on.png"),
									  (self.x_drop*self.chance_box)+self.delta_x, (self.y_drop*i)+self.delta_y)
			self.tumbler_list.append(tumbler)
			
			result = basic.Result(os.path.join("image", "pictograms", "gamma.png"),
									os.path.join("image", "pictograms", "omega.png"),
									os.path.join("image", "board", "result.png"),
									(self.x_drop*self.chance_box)+self.delta_x*3, (self.y_drop*i)+self.delta_y)
			self.result_list.append(result)
			
			for j in range(self.chance_box):
				drop = basic.Sprite(os.path.join("image", "drop point", "drop_point.png"),
									 (self.x_drop*j)+self.delta_x, (self.y_drop*i)+self.delta_y)
				self.drop_list[i].append(drop)
		
		#Create object secret door, overall result, candy
		self.door_board = basic.Sprite(os.path.join("image", "door", "secret_door_board.png"), 15, 18)
		self.door = basic.Door(os.path.join("image", "door", "secret_door_top.png"),
										   os.path.join("image", "door", "secret_door_bottom.png"),
										   19, 22)
		self.cell = basic.Sprite(os.path.join("image", "door", "cell.png"), 19, 22)
		self.candy = basic.Candy(os.path.join("image", "door", "candy.png"), 150, 35)
		self.overall_result = basic.Sprite(os.path.join("image", "board", "overall_result.png"),
											 self.x_drop*self.chance_box+48, 18)
		
		#Create brain
		self.brain = basic.Brain(self.y_drop, self.block_list, self.old_block_list, self.drop_list, self.tumbler_list, self)
		
	def create_object_game_dynamic(self):
		"""Create game objects which need to be recreated after restart"""
		#Create object block
		for i in range(len(basic.Block.block_image)):
			block = basic.Block(os.path.join("image", "blocks", basic.Block.block_image[i]), self.x_block, (self.y_block*i)+27, i)
			
			self.block_list.add(block)
		
		#Create general game parameters
		for i in range(4): #create random secret combination
			number = random.choice(self.variant_number)
			self.secret_comb.append(number)
			self.variant_number.remove(number)
	
	def create_object_menu(self):
		"""Creating all necessary for main menu objects"""
		self.menu = basic.Sprite(os.path.join("image", "menu", "menu_back.png"), 0, 0)
		self.text_menu = basic.TextMenu(247, 330)
		
		self.rule = basic.Description(os.path.join("image", "menu", "rule.png"), 641, 0, self.size)
		self.about = basic.Description(os.path.join("image", "menu", "about.png"), 0, 481, self.size)
		
		self.button_left = basic.Button(os.path.join("image", "button", "left_up_b.png"),
										  os.path.join("image", "button", "left_down_b.png"),
										  157, 320)
		self.button_right = basic.Button(os.path.join("image", "button", "right_up_b.png"),
										   os.path.join("image", "button", "right_down_b.png"),
										   455, 320)
		self.button_enter = basic.Button(os.path.join("image", "button", "enter_up_b.png"),
										   os.path.join("image", "button", "enter_down_b.png"),
										   self.x_drop*self.chance_box+85, 100)
		
		self.main_menu.add(self.menu)
		self.main_menu.add(self.button_left)
		self.main_menu.add(self.button_right)
		self.main_menu.add(self.button_enter)
		self.main_menu.add(self.text_menu)
		
		for i in range(4):
			bolt = basic.Bolt(os.path.join("image", "menu", "bolt.png"), self.xy_pos_bolt[i])
			self.bolt_list.append(bolt)
			self.main_menu.add(bolt)
	
	def run_rule_brain(self):
		"""Start checking the rules of the game and return the required results (call in event_game)"""
		if not self.end_game:
			self.line, self.end_game, self.winning = self.brain.check_block_line(self.line, self.secret_comb, self.door)
	
	def __bolt_rotate(self, direction):
		"""Rotate all bolts"""
		for i in range(4):
			self.bolt_list[i].rotate(direction)
	
	def __launch_game(self):
		"""Launching the game (setting basic parameters before the game)"""
		if self.check_run_newgame:
			self.brain.run_survival(self.check_run_survival)
			self.__restart()
			self.main_menu.switch_state()
		else:
			self.check_run_newgame = True
			#then run start_game (animation bolt rotate)
	
	def __start_game(self):
		"""First run New Game"""
		if self.check_run_newgame and self.check_rotate:
			if self.count_frame < 150:
				self.__bolt_rotate(True)
				self.count_frame += 1
			else:
				self.check_rotate = False
				self.count_frame = 0
				self.brain.run_survival(self.check_run_survival)
				self.main_menu.switch_state()
	
	def __game_over(self):
		"""If players lose (lock), then game block"""
		if self.end_game and not self.winning:
			if self.count_frame < 60:
				self.count_frame += 1
			else:
				self.check_run_newgame = False
				self.text_menu.delete_optional()
				#change switch_event then player NOT IN main menu
				if self.switch_event:
					self.main_menu.switch_state()
				if self.count_frame < 258:
					self.count_frame += 1
					if self.count_frame > 130:
						self.__bolt_rotate(False)
				elif self.count_frame >= 150:
					self.check_rotate = True
					self.__restart()
					if self.check_run_survival:
						self.check_run_survival = False
						self.brain.run_survival(self.check_run_survival)
	
	def __restart(self):
		"""Restart game"""
		self.line = 0
		self.count_frame = 0
		self.variant_number = range(10)
		del self.secret_comb[:]
		
		self.block_list.empty()
		self.old_block_list.empty()
		self.brain.brain_restart()
		
		self.end_game = None
		self.winning = None
		self.render_up_block = False
		self.render_up_candy = True
		
		for i in range(self.chance):
			self.tumbler_list[i].restart_state()
			for j in range(self.chance_box):
				self.drop_list[i][j].restart_state()
		
		self.create_object_game_dynamic()
	
	def __run_option_menu(self):
		"""The execution of an option from the menu (call in event_menu)"""
		#new game
		if self.text_menu.current_text == 0:
			self.check_run_survival = False
			self.__launch_game()
		#rule
		elif self.text_menu.current_text == 1:
			self.rule.switch_state()
		#survival
		elif self.text_menu.current_text == 2:
			self.check_run_survival = True
			self.__launch_game()
		#exit
		elif self.text_menu.current_text == 3:
			sys.exit()
		#credits
		elif self.text_menu.current_text == 4:
			self.about.switch_state()
		#resume
		elif self.text_menu.current_text == 5:
			self.main_menu.switch_state()
	
	def __event_game(self, event):
		"""All the events of the game"""
		#event MOUSE
		if event.type == pygame.MOUSEBUTTONDOWN:
			for block in self.block_list:
				#check position mouse relatively blocks
				if block.check_mouse(self.m_pos):
					block.play_sound_take()
					self.block_list.move_to_front(block) #roaming sprite at the forefront
					self.render_up_block = True
			
			for tumbler in self.tumbler_list:
				if tumbler.check_mouse(self.m_pos):
					if self.tumbler_list.index(tumbler) > self.line:
						tumbler.play_sound_on()
						self.end_game = None
						tumbler.play_sound_off()
					else:
						self.run_rule_brain()
			
			if self.candy.check_mouse(self.m_pos) and self.door.state:
				self.candy.play_sound_candy()
				self.render_up_candy = self.door.switch_state()
			
			elif self.button_restart.check_mouse(self.m_pos):
				self.button_restart.change_image_d()
				
			elif self.button_menu.check_mouse(self.m_pos):
				self.button_menu.change_image_d()
		
		elif event.type == pygame.MOUSEBUTTONUP:
			for block in self.block_list:
				block.check_point(self.drop_list, self.line) #check where drop blocks
				self.render_up_block = False
			
			self.button_restart.change_image_u()
			self.button_menu.change_image_u()
			
			if self.button_restart.state:
				self.button_restart.restart_state()
				if self.button_restart.check_mouse(self.m_pos, False):
					self.__restart()
			
			elif self.button_menu.state:
				self.button_menu.restart_state()
				if self.button_menu.check_mouse(self.m_pos, False):
					self.main_menu.switch_state()
		
		#event KEY
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				self.button_restart.change_image_d()
			
			elif event.key == pygame.K_ESCAPE:
				self.button_menu.change_image_d()
		
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
				self.run_rule_brain()
			
			if event.key == pygame.K_BACKSPACE:
				self.button_restart.change_image_u()
				self.__restart()
			
			elif event.key == pygame.K_ESCAPE:
				#the switching event occurs in main_loop()
				self.button_menu.change_image_u()
	
	def __event_menu(self, event):
		"""All the events of the main menu"""
		#event MOUSE
		if event.type == MOUSEBUTTONDOWN:
			if self.button_left.check_mouse(self.m_pos):
				self.button_left.change_image_d()
			
			elif self.button_right.check_mouse(self.m_pos):
				self.button_right.change_image_d()
			
			elif self.button_enter.check_mouse(self.m_pos):
				self.button_enter.change_image_d()
		
		elif event.type == MOUSEBUTTONUP:
			self.button_left.change_image_u()
			self.button_right.change_image_u()
			self.button_enter.change_image_u()
			
			if self.button_left.state:
				self.button_left.restart_state()
				if self.button_left.check_mouse(self.m_pos, False):
					self.text_menu.left_text()
			
			elif self.button_right.state:
				self.button_right.restart_state()
				if self.button_right.check_mouse(self.m_pos, False):
					self.text_menu.right_text()
			
			elif self.button_enter.state:
				self.button_enter.restart_state()
				if self.button_enter.check_mouse(self.m_pos, False):
					self.__run_option_menu()
				
		#event KEY
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				self.button_left.change_image_d()
			
			elif event.key == pygame.K_RIGHT:
				self.button_right.change_image_d()
			
			elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
				self.button_enter.change_image_d()
		
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				self.button_left.change_image_u()
				self.text_menu.left_text()
			
			elif event.key == pygame.K_RIGHT:
				self.button_right.change_image_u()
				self.text_menu.right_text()
			
			elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
				self.button_enter.change_image_u()
				self.__run_option_menu()
	
	def main_loop(self):
		"""The main game loop"""
		while True:
			self.m_pos = pygame.mouse.get_pos() #coordinate mouse
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit() #if click on the cross button window
				
				elif event.type == pygame.KEYUP:
					#switching between main menu and game
					if event.key == pygame.K_ESCAPE:
						if self.check_run_rule:
							self.rule.switch_state()
						elif self.check_run_about:
							self.about.switch_state()
						else:
							if self.check_run_newgame:
								self.main_menu.switch_state()
				
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if self.check_run_rule:
						self.rule.switch_state()
					elif self.check_run_about:
						self.about.switch_state()
				
				if self.switch_event:
					#event for game
					self.__event_game(event)
				elif not self.check_run_rule and not self.check_run_about:
					#event for menu
					self.__event_menu(event)
			
			#render block
			self.block_list.update(self.m_pos)
			
			#render cell, candy, door
			if self.render_up_candy:
				self.cell.update(self.screen)
				self.candy.update(self.screen)
			else:
				self.candy.update(self.screen)
				self.cell.update(self.screen)
			self.door.update(self.screen)
			
			#render playing_field
			self.playing_field.update(self.screen)
			
			#render door board, overall result board
			self.door_board.update(self.screen)
			self.overall_result.update(self.screen)
			
			#render game button
			self.button_restart.update(self.screen)
			self.button_menu.update(self.screen)
			
			#render tumbler, result list, drop points
			for i in range(self.chance):
				self.tumbler_list[i].update(self.screen)
				self.result_list[i].update(self.screen)
				self.tumbler_list[i].check_work(self.end_game)
				for j in range(self.chance_box):
					self.drop_list[i][j].update(self.screen)
			
			#render old block list
			self.old_block_list.draw(self.screen)
			
			#render pipe down
			self.pipe_d_list.draw(self.screen)
			#render block (appear on the screen if game started)
			if self.check_run_newgame and self.switch_event:
				for block in self.block_list:
					block.change_state()
			#render block
			if not self.render_up_block:
				self.block_list.draw(self.screen)
				self.pipe_u_list.draw(self.screen)
				self.playing_field_board.update(self.screen)
			else:
				self.pipe_u_list.draw(self.screen)
				self.playing_field_board.update(self.screen)
				self.block_list.draw(self.screen)
			
			#render text
			self.brain.update(self.screen)
			
			#render main menu
			self.switch_event = self.main_menu.move()
			if self.switch_event:
				self.text_menu.new_optional()
			self.main_menu.draw(self.screen)
			
			#check run rule or about
			self.check_run_rule = self.rule.end_motion()
			self.check_run_about = self.about.end_motion()
			
			#run new game or game over
			self.__start_game()
			self.__game_over()
			
			#render rule, about
			self.rule.update(self.screen)
			self.about.update(self.screen)
			
			pygame.display.flip()

			self.clock.tick(60)

if __name__ == '__main__':
	print "You run module: game"
