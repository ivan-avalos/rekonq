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

import tools as t

class cell_flags(object):
        FLAG_OCCUPIED = 1
        FLAG_CROSS = 2
        FLAG_PERMANENT = 4
        FLAG_PLAYER_B = 8

def isset_flag(flags, flag):
    return (flags & flag == flag)

def set_flag(flag, flags):
    return (flags | flag)

def unset_flag(flag, flags):
    return (flags ^ flag)

def get_cell_char (flags):
    cell_char = ''
    # Occupied
    if not isset_flag(flags, cell_flags.FLAG_OCCUPIED):
        return '.'
        
    # Cross
    if isset_flag(flags, cell_flags.FLAG_CROSS):
        # Permanent
        if isset_flag(flags, cell_flags.FLAG_PERMANENT):
            cell_char = t.bcolors.BOLD+'#'+t.bcolors.ENDC
        else:
            cell_char = '*'
    else:
        # Permanent
        if isset_flag(flags, cell_flags.FLAG_PERMANENT):
            cell_char = t.bcolors.BOLD+'@'+t.bcolors.ENDC
        else:
            cell_char = 'o'
            
    # Player
    if not isset_flag(flags, cell_flags.FLAG_PLAYER_B):
        cell_char = t.bcolors.OKBLUE + cell_char + t.bcolors.ENDC
    else:
        cell_char = t.bcolors.FAIL + cell_char + t.bcolors.ENDC

    return cell_char


class Rekonq:
    board = []
    hist  = []
    
    def __init__(self):
        # Create empty matrix
        board = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(0)
            self.board.append(row)
                
        # Initialize game
        self.board[0][0] = cell_flags.FLAG_OCCUPIED
        self.board[7][7] = cell_flags.FLAG_OCCUPIED | cell_flags.FLAG_PLAYER_B
        self.hist = []

    def print_board (self):
        t.print_color(t.bcolors.BOLD, '  ', end='')
        for i in range(len(self.board)):
            t.print_color(t.bcolors.BOLD, t.one_to_a(i) + ' ', end='')
        print('')

        # Rows
        for i in range(len(self.board)):
            t.print_color(t.bcolors.BOLD, str(i+1)+' ', end='')
        
            # Cols
            for j in range(len(self.board[i])):
                print(get_cell_char(self.board[j][i]) + ' ', end='')

            t.print_color(t.bcolors.BOLD, str(i+1)+' ')

        t.print_color(t.bcolors.BOLD, '  ', end='')
        for i in range(len(self.board)):
            t.print_color(t.bcolors.BOLD, t.one_to_a(i) + ' ', end='')
        print('')


    def exec_move(self, player, a, b, bcross):
        # Player A = False, Player B = Truep
        # Bcross: X = False, Cross = True
        # Cell format 'a1'
        arow = t.a_to_one(a[0])
        acol = int(a[1])-1
        brow = t.a_to_one(b[0])
        bcol = int(b[1])-1

        # DEBUG
        #print('From: '+' [row='+ str(arow) + ', col=' + str(acol)+']')
        #print('To  : '+' [row='+ str(brow) + ', col=' + str(bcol)+']')

        # Check values to avoid "out of range" error -_-
        if not (arow >= -1 and arow <= 7):
            return False
        if not (acol >= -1 and acol <= 7):
            return False
        if not (brow >= -1 and brow <= 7):
            return False
        if not (bcol >= -1 and bcol <= 7):
            return False

        a = self.board[arow][acol]
        b = self.board[brow][bcol]
        
        # Filter based verification

        # Step 1. Avoid eating your own kingdom or using the other player's cells
        if isset_flag(b, cell_flags.FLAG_OCCUPIED):
            # Step 1a. _to_ occupied
            if isset_flag(b, cell_flags.FLAG_PLAYER_B) == player:
                return False
        else:
            # Step 1b. _to_ empty
            if isset_flag(a, cell_flags.FLAG_PLAYER_B) != player:
                return False
        
        # Step 2. Wrong move orientation FLAG_CROSS
        if not isset_flag(a, cell_flags.FLAG_CROSS):
            # Step 2a. X Verification
            if not ((arow - 1 == brow and acol - 1 == bcol) or (arow - 1 == brow and acol + 1 == bcol) or \
               (arow + 1 == brow and acol + 1 == bcol) or (arow + 1 == brow and acol - 1 == bcol)):
                return False
        else:
            # Step 2b. Cross verification
            if not ((arow - 1 == brow and acol == bcol) or (arow == brow and acol + 1 == bcol) or \
               (arow + 1 == brow and acol == bcol) or (arow == brow and acol - 1 == bcol)):
                return False
        # Step 3. Permanent
        if isset_flag(b, cell_flags.FLAG_PERMANENT):
            return False
        
        # Step 4. Set new cell flags
        self.board[brow][bcol] = cell_flags.FLAG_OCCUPIED
        if bcross:
            self.board[brow][bcol] |= cell_flags.FLAG_CROSS
        if isset_flag(b, cell_flags.FLAG_OCCUPIED):
            self.board[brow][bcol] |= cell_flags.FLAG_PERMANENT
        if player:
            self.board[brow][bcol] |= cell_flags.FLAG_PLAYER_B
        return True
    
    def get_winner(self):
        acount = 0
        bcount = 0
        
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                # Player A
                if isset_flag(self.board[j][i], cell_flags.FLAG_OCCUPIED):
                    if not isset_flag(self.board[j][i], cell_flags.FLAG_PLAYER_B):
                        acount += 1
                    else:
                        bcount += 1
        
        if acount > bcount:
            return [0, acount, bcount] # A wins!
        elif acount < bcount:
            return [1, acount, bcount] # B wins!
        elif acount == bcount:
            return [2, acount, bcount] # Tie!        
