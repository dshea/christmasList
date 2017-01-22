#!/usr/bin/env python

#############
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#############

#############
# Christmas Gift Exchange Name Matcher
# Copyright (c)2010, Adam Monsen <haircut@gmail.com>
# heavily modified by Don Shea <don@shea.cc>
#
# Rules:
# 1. give to a different person than last year
# 2. partners can't be nuclear family members
# 3. can't choose yourself
# 4. participants give one gift only
# 5. participants receive one gift only
#############

#############
# history CSV file
#
# first column is the year (not used in the program)
# first row is the participants
# all other rows are the past years matches in decreasing years
#
# for example:
#
# year,John,Mary,Beth,Jack
# 2000,Jack,John,Mary,Beth
# 2001,Mary,Beth,Jack,John
#
# so Mary gave presents to John in 2000 and Beth in 2001
# note that the year increases with each line and
# the program will append this year to the end of the file.
#
#############


#families = [
#    ('Mike', 'Sherrol'),
#    ('Tom', 'Patty','Michael Marie'),
#    ('Kathy','Greg','Haley','Morgan'),
#    ('Marie','Bo','Pierce','Sophie'),
#    ('Don','Kari','Mallory','Jack','Jocelyn'),
#    ('Bill'),
#    ('Beth','Clay','Michael Robert','Melanie'),
#    ('Jim','Gaby','Michael J','Maria')
#]

families = []


import random
import sys
import csv
from datetime import date

debug_on = False
debug_fine_on = False

from copy import copy

def debug(msg):
    if debug_on: print msg

def debug_fine(msg):
    if debug_fine_on: print msg

def possible_givers(participants, chosen):
    # rule 4 - participants give one gift only
    possible_givers = copy(participants)
    for giver in map(lambda x: x[0], chosen):
        possible_givers.remove(giver)
    return possible_givers

def possible_recipients(giver, participants, chosen, previous_years, families):
    """Exclude all rule-breaking recipients and return whatever's left, if
    anything."""

    possible_recipients = copy(participants)

    # rule 3 - can't choose yourself
    possible_recipients.remove(giver)

    # rule 1 - different pairing than the last few years
    for dude in previous_years[giver]:
        if dude in possible_recipients:
            debug_fine("%s gave to %s last few years, excluding" % (giver, dude))
            possible_recipients.remove(dude)

    # rule 2 - give outside nuclear family
    for family in families:
        if giver in family:
            for recipient in family:
                if recipient in possible_recipients:
                    debug_fine("%s and %s are family, excluding" % (giver, recipient))
                    possible_recipients.remove(recipient)

    # rule 5 - participants receive one gift only
    for pair in chosen:
        if pair[1] in possible_recipients:
            debug_fine("%s is already paired, excluding" % pair[1])
            possible_recipients.remove(pair[1])

    return possible_recipients

def verify_name(name):
    """Is this name in one of the families.  Help check for typos in the data file."""
    for family in families:
        if name in family:
            return True
    return False

def readFamilies():
    """
    read the families CSV file into the families list.
    one family on a line, members seperated by a comma.
    """
    global families  
    
    # open the CSV file
    f = open("families.csv", 'rbU')
    reader = csv.reader(f)

    for line in reader:
        if len(line) > 0:
            families.append(line)

            

def print_usage():
    print 'usage: ', sys.argv[0], ' <history_CSV_File> [#years]'

if __name__ == '__main__':
    chosen = []
    fileName = ''
    num_years = 100
    previous_years = {}

    if len(sys.argv) > 1:
        fileName = sys.argv[1]
        if len(sys.argv) > 2:
            num_years = int(sys.argv[2])
            if num_years <= 0:
                print("Error - num_years(", num_years, ") must be positive.")
                sys.exit(1)
                
    else:
        print_usage()
        sys.exit(0)

    # load the families list
    readFamilies()

    # open the history CSV file
    try:
        f = open(fileName, 'rbU')
    except IOError:
        print "Error: File does not appear to exist."
        sys.exit(1)
    
    pickHistory = []
    reader = csv.reader(f)

    # fill up the participants variable with the first row of the CSV file
    participants = reader.next()
    del participants[0]             # get rid of first column

    # make sure participants are in a family
    # helps with typos
    need_to_die = False
    for dude in participants:
        if not verify_name(dude):
            need_to_die = True
            print dude, 'is not in a family'
    if need_to_die:
        sys.exit(1)

    # read in whole history file
    for line in reader:
        if len(line) > 0:
            pickHistory.append(line)
    f.close()

    # truncate the history to the number of years requested
    while len(pickHistory) > num_years:
        del pickHistory[0]

    # make dictionary of empty arrays
    for dude in participants:
        previous_years[dude] = []

    # fill up the previous years dictionary
    for line in pickHistory:
        del line[0]                 # get rid of first column
        i = 0
        debug_fine("")
        for dude in line:
            if dude not in participants:
                print dude, 'in file', fileName, 'is an illegal name'
                sys.exit(1)
            previous_years[participants[i]].append(dude)
            debug_fine("%s = %s" % (participants[i], dude))
            i = i + 1

    num_tries = 1
    while len(chosen) != len(participants):
        if num_tries > 10:
            print "Need to try again or decrease the number of previous years"
            sys.exit(1)
            
        givers = possible_givers(participants, chosen)
        # if we omit randomization here, our "abort/retry" (below) may fail,
        # although I'm not really sure why
        giver = random.choice(givers)
        debug_fine("GIVER: %s" % giver)
        recipients = possible_recipients(giver, participants, chosen, previous_years, families)
        # brute force abort/retry
        if len(recipients) == 0:
            debug("No recipients, trying a different giver...")
            if len(givers) <= 1:
                debug("No other givers to try! Starting over...")
                chosen = []
                num_tries += 1
            if len(givers) == 2:
                debug("Stalemate! Two givers left but they can't give to eachother. Starting over...")
                chosen = []
                num_tries += 1
            continue
        recipient = random.choice(recipients)
        debug_fine("RECIPIENT: %s" % recipient)
        chosen.append( (giver, recipient) )
        debug("PAIRS ARE NOW: %s" % chosen)

    # append line to end of history CSV file
    year = date.today().year
    line = "\n%d" % year
    for dude in participants:
        for giver, recipient in chosen:
            if dude == giver:
                line += ','
                line += recipient
    f = open(fileName, 'a')
    f.write(line)
    f.close()

    # print out the pairs on the order of the columns of the CSV file
    for dude in participants:
        for giver, recipient in chosen:
            if dude == giver:
                print "%s gives to %s" % (giver, recipient)
        
    sys.exit(0)
    