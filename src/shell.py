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

import ast
import sys

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
\t<from> <to> [*|o]   Make a move
\tboard               Print board
\thistory             Show moves history
\tcalc                Simple calculator
\tfinish              Finish game and annouce winner
\texit                Quit game
\twelcome             Print ASCII welcome message
\thelp                Show this help menu
\tabout               Copyright information

Example:
\ta1 b2 *             Move from a1 to b2 and put a '*'
\tb2 b3 o             Move from b2 to b3 and put a 'o'
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

calc_help_message ="""Commands:
\t<expression>   Evaluate expression
\thelp           Show this help menu
\texit           Exit from calc
"""

class Shell:
    rekonq = None
    
    def __init__(self):
        self.rekonq = b.Rekonq()

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

            # Commands
            if cmd == 'board':
                self._board ()
                nprint = True
                continue
            elif cmd == 'history':
                self._history()
                nprint = True
                continue
            elif cmd == 'finish':
                self._finish()
                break
            elif cmd == 'calc':
                self._calc()
                continue
            elif cmd == 'exit':
                break
            elif cmd == 'help':
                self._help()
                nprint = True
                continue
            elif cmd == 'welcome':
                self._welcome()
                nprint = True
                continue
            elif cmd == 'about':
                self._about()
                nprint = True
                continue
            
            # Verify, parse and execute a move
            if not self.parse_move_and_exec (cmd, player):
                err = True
            else:
                player = not player

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
        if not len(cmd) == 7:
            print('Invalid command!')
            return False

        if (not cmd[0].isalpha()) or (not cmd[3].isalpha()) or (not cmd[1].isdigit()) or (not cmd[4].isdigit()) or \
           (cmd[6] != '*' and cmd[6] != 'o'):
            print('Invalid command!')
            return False

        _from = cmd[0] + cmd[1]
        to = cmd[3] + cmd[4]
        cross = cmd[6] == '*'
        if not self.rekonq.exec_move(player, _from, to, cross):
            print('Invalid move!')
            return False
            
        self.rekonq.hist.append([player, cmd])
        return True
        

    def _board(self):
        self.rekonq.print_board()

    def _history(self):
        for i in range(len(self.rekonq.hist)):
            if not self.rekonq.hist[i][0]:
                t.print_color(t.bcolors.OKBLUE, str(i+1) + '. ' + self.rekonq.hist[i][1])
            else:
                t.print_color(t.bcolors.FAIL, str(i+1) + '. ' + self.rekonq.hist[i][1])

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

    def _welcome(self):
        t.print_color(t.bcolors.HEADER, welcome_message)

    def _help(self):
        print(help_message)

    def _about(self):
        print(copying_message)
