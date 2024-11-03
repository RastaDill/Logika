#!/usr/bin/env python
#  logika.py
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

import game


def main():
    play = game.Game()
    play.create_object_game_static()
    play.create_object_game_dynamic()
    play.create_object_menu()
    play.main_loop()


if __name__ == "__main__":
    main()
