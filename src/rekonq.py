#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import getopt

import shell as sh

rekonq_help_message="""Usage: rekonq.py [OPTIONS...]
Or:    rekonq.py -h

Options:
    -i <file>  Recover saved game from file
    -h         Show this help menu
"""

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hi:')
except getopt.GetoptError:
    print(rekonq_help_message)
    sys.exit(1)

for opt, arg in opts:
    if opt == '-h':
        print(rekonq_help_message)
        sys.exit(0)
    elif opt in ['-i', '--input-file=']:
        # Load game from file
        shell = sh.Shell(True)
        shell.load_game(arg)
        shell.start_shell()
        sys.exit(0)

shell = sh.Shell(False)
shell.start_shell()
