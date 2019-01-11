# Rekonq - Strategy game in which you shall conquer to win.
# Copyright (C) 2018  Iván Alejandro Ávalos Díaz <ivan.avalos.diaz@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# -*- mode: python-mode; python-indent-offset: 4 -*-

import sys
import time
import math

import board as b
import tools as t

welcome_message = """
  _____      _                     
 |  __ \    | |                    
 | |__) |___| | _____  _ __   __ _ 
 |  _  // _ \ |/ / _ \| '_ \ / _` |
 | | \ \  __/   < (_) | | | | (_| |
 |_|  \_\___|_|\_\___/|_| |_|\__, |
                                | |
                                |_|
Welcome to Rekonq!

Type "help" for help.
"""

help_message = """Commands:
    <from> <to> [*|o]   Make a move
    board               Print board
    history             Show moves history
    save <file>         Save game to file
    calc                Simple calculator
    finish              Finish game and annouce winner
    exit                Quit game
    welcome             Print ASCII welcome message
    help                Show this help menu
    about               Copyright information

Example:
    a1 b2 *             Move from a1 to b2 and put a '*'
    b2 b3 o             Move from b2 to b3 and put a 'o'
"""

copying_message ="""Rekonq - Strategy game in which you shall conquer to win.
Copyright (C) 2018  Iván Alejandro Ávalos Díaz <ivan.avalos.diaz@hotmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

msg_invalid_command = 'Error: Invalid command!'
msg_invalid_move = 'Error: Invalid move!'
msg_save_success = 'Game saved successfully!'
msg_save_error = 'Error: cannot write output file!'
msg_load_error = 'Error: cannot load input file!'

calc_help_message ="""Commands:
\t<expression>   Evaluate expression
\thelp           Show this help menu
\texit           Exit from calc
"""

class Shell:
    rekonq = None
    
    def __init__(self, load):
        if not load:
            self.rekonq = self.init_with_size()

    def start_shell (self):
        cmd = ''
        player = False
        err = False
        nprint = False
        # Welcome message
        self._welcome()
        while(True):
            # Determine whether print board or not
            if not (err or nprint):
                self.rekonq.print_board()
            if err:
                err=False
            if nprint:
                nprint=False

            cmd = self.prompt_get_input(player)
            _cmd = cmd.split(' ')[0]

            # Commands
            if cmd == '':
                nprint = True
            elif _cmd == 'board':
                self._board ()
                nprint = True
            elif _cmd == 'history':
                self._history()
                nprint = True
            elif _cmd == 'save':
                self._save(cmd)
                nprint = True
            elif _cmd == 'finish':
                self._finish()
                break
            elif _cmd == 'calc':
                self._calc()
            elif _cmd == 'exit':
                break
            elif _cmd == 'help':
                self._help()
                nprint = True
            elif _cmd == 'welcome':
                self._welcome()
                nprint = True
            elif _cmd == 'about':
                self._about()
                nprint = True
            else:
                # Verify, parse and execute a move
                if not self.parse_move_and_exec (cmd, player):
                    err = True
                else:
                    player = not player

    def init_with_size (self):
        size = 0
        while True:
            try:
                size = int(input(t.bcolors.BOLD+'BOARD SIZE ('+str(b.min_size)+'..'+str(b.max_size)+'): '+t.bcolors.ENDC))
                if size < b.min_size or size > b.max_size:
                    print ('Number out of range!')
                else:
                    return b.Rekonq(size)
            except ValueError:
                print ('Write a valid number!')

    def prompt_get_input (self, player):
        cmd = ''
        
        if not player:
            cmd = input(t.bcolors.OKBLUE+t.bcolors.BOLD+'[PLAYER A]$ '+t.bcolors.ENDC)
        else:
            cmd =  input(t.bcolors.FAIL+t.bcolors.BOLD+'[PLAYER B]$ '+t.bcolors.ENDC)
        cmd = cmd.strip()
        cmd = cmd.lower()
        return cmd

    def parse_move_and_exec (self, cmd, player):

        args = cmd.split(' ')
        # Verify syntax
        if len(args) != 3:
            print(msg_invalid_command)
            return False
        if len(args[0]) < 2 or len(args[1]) < 2 or len(args[2]) != 1:
            print(msg_invalid_command)
            return False
        if (not args[0][:1].isalpha()) or (not args[1][:1].isalpha()) or \
           (not args[0][1:].isdigit()) or (not args[1][:1].isalpha()) or \
           (args[2] != '*' and args[2] != 'o'):
            print(msg_invalid_command)
            return False

        _from = [args[0][:1], args[0][1:]]
        to = [args[1][:1], args[1][1:]]
        cross = args[2] == '*'
        if not self.rekonq.exec_move(player, _from, to, cross):
            print(msg_invalid_move)
            return False

        return True

    def load_game(self, filename):
        try:
            f = open(filename, 'r')
            content = f.readlines()
            content = [x.strip() for x in content]
            # Initialize board with size in line 0
            print(int(content[0]))
            self.rekonq = b.Rekonq(int(content[0]))
            # Parse and execute moves in file
            for i in range(1, len(content)):
                parts = content[i].split('.')
                player = parts[0].strip()
                move = parts[1].strip()
                if player == 'b':
                    player = True
                elif player == 'a':
                    player = False
                
                self.parse_move_and_exec(move, player)

            
        except (OSError, IOError):
            print(msg_load_error)

    def _board(self):
        self.rekonq.print_board()

    def _history(self):
        for i in range(len(self.rekonq.hist)):
            if not self.rekonq.hist[i][0]:
                t.print_color(t.bcolors.OKBLUE, str(i+1) + '. ' + self.rekonq.hist[i][1])
            else:
                t.print_color(t.bcolors.FAIL, str(i+1) + '. ' + self.rekonq.hist[i][1])

    def _save(self, _cmd):
        # Verify syntax
        cmd = _cmd.split(' ')
        if len(cmd) != 2:
            print(msg_invalid_command)
            return False

        # Write file
        try:
            f = open(cmd[1], 'w')
            o = str(self.rekonq.size) + "\n"
            for i in self.rekonq.hist:
                if i[0]:
                    o += 'b.'
                else:
                    o += 'a.'
                o += i[1] + "\n"
            f.write(o)

            print (msg_save_success + ' ' + cmd[1])
            return True
        except (OSError, IOError):
            print(msg_save_error)
            return False

    def _calc(self):
        expression = ''
        print('Type "help" for help')
        while True:
            try:
                expression = input('> ')
            except UnicodeDecodeError:
                e = sys.exc_info()
                print('Error: ' + str(e[1]))
                continue
            if expression == 'exit':
                return
            elif expression == 'help':
                print(calc_help_message)
                continue
            else:
                try:
                    print(str(eval(expression)))
                except (NameError, SyntaxError, ZeroDivisionError):
                    e = sys.exc_info()
                    print('Error: ' + str(e[1]))
            

    def _finish(self):
        winner = self.rekonq.get_winner()
        # Print count
        print(t.bcolors.OKBLUE+'A:'+str(winner[1])+t.bcolors.ENDC+'-'+t.bcolors.FAIL+'B:'+str(winner[2])+t.bcolors.ENDC)
        # Print winner
        if winner[0] == 0:
            print(t.bcolors.OKBLUE+'Player A wins!'+t.bcolors.ENDC)
        elif winner[0] == 1:
            print(t.bcolors.FAIL+'Player B wins!'+t.bcolors.ENDC)
        elif winner[0] == 2:
            print(t.bcolors.HEADER+t.bcolors.BOLD+'Tie!'+t.bcolors.ENDC)

        # Delay before exiting to be able to see 'finish' result in screen mode.
        print('Exit in 5 seconds...')
        time.sleep (5)

    def _welcome(self):
        t.print_color(t.bcolors.HEADER, welcome_message)

    def _help(self):
        print(help_message)

    def _about(self):
        print(copying_message)
