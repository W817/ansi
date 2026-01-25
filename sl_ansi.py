#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Data processing
    <<Khufu Coded>> 2018-2020
    notes
    list of lists: [[0,1,2],[3,4,5]] aka fortranarray
    dictionary of dictionary: {'1':{'2':'twee','3':'drie'}, '4':'vier'}
    list of dict, list of list, dict of list, dict of dict.. --> Json

    Other denomination / Synoniems
    Dictionary >> object, record, struct, hash table, keyed list, or associative array
    List >> array, vector, or sequence

"""
#--------------------------------------------------------------------------------------
# Imports
import re
import os
import sys
import random

from sl_data import sl_replace, in_range

if sys.version.startswith('3'):
    # For Python 3.0 and later
    #URL LIB correction
    #from urllib.request import urlopen, Request
    #print ('[INFO] Processing with urllib for {}'.format(sys.version))

    xrange = range
    # Unicode dummy class creation
    class unicode():
        def __init__(self,txt):
            self.txt = (str(bytes(txt)))
            self.conversion()

        def conversion(self):
            return self.txt
    #print ('[INFO] Dummy class unicode and basestring created for {}'.format(sys.version)
    def struct_unpack(fmt, buf):
        return  struct.unpack(fmt, buf)

#-------------------------------------------------------------------------------------
# Definitions/Class

""" PRINTING AND COLORING INTERMEZZO
#
# ANSI Color code (16colors)
#
#  http://ascii-table.com/ansi-escape-sequences.php
#  http://archive.linux.or.jp/JF/JFdocs/Bash-Prompt-HOWTO-5.html


# Escape sequence
#   \033[<code>m or \e[<code>m
#
#   color : \[\033[ <code>m\] \]
#
#   e.g.
#    bg=Blue, Bold, fg=Red
#     1. \033[44;1;31m
#     2. \033[44m\033[1;31m


# Text attributes
#  0  All attributes off
#  1  Bold on
#  4  Underscore (on monochrome display adapter only)
#  5  Blink on
#  7  Reverse video on
#  8  Concealed on


# Background colors
#  40   Black
#  41   Red
#  42   Green
#  43   Yellow
#  44   Blue
#  45   Magenta
#  46   Cyan
#  47   White

###############################################################################
"""

attrs = {'off' : '0', #normal
         'bold' : '1', #bright
         'underline' :'4',
         'blink' : '5',
         'reverse' : '7',
         'concealed' : '8',
         'black': '30',
         'red': '31',
         'green': '32',
         'yellow': '33',
         'blue': '34',
         'magenta': '35',
         'cyan': '36',
         'white': '37',
         'bg_black': '40',
         'bg_red':'41',
         'bg_green':'42',
         'bg_yellow':'43',
         'bg_blue':'44',
         'bg_magenta':'45',
         'bg_cyan':'46',
         'bg_white':'47'
          }

#memo default coloring mainly for sl_p2p
coloring =[{'txt': 'BLACK', 'attr': ['black', 'bold']},
           {'txt': 'RED', 'attr': ['red','bold']},
           {'txt': 'GREEN', 'attr': ['green','bold']},
           {'txt': 'YELLOW', 'attr': ['yellow','bold']},
           {'txt': 'BLUE', 'attr': ['blue','bold']},
           {'txt': 'MAGENTA', 'attr': ['magenta','bold']},
           {'txt': 'CYAN', 'attr': ['cyan','bold']},
           {'txt': 'WHITE', 'attr': ['white','bold']}
          ]

data_bg = [{'char':' ', 'attr':['bg_black'], 'range' : '[0,40]', 'char_bg':' ', 'attr_bg':['bg_black']},
           {'char':' ', 'attr':['bg_green'], 'range': ']40,80]', 'char_bg':' ', 'attr_bg':['bg_white']},
           {'char':' ', 'attr':['bg_red'], 'range': ']80,100]', 'char_bg':' ', 'attr_bg':['bg_black']}
          ]

def ansi_color(payload, coloring=coloring, attrs=attrs):
    # TODO if payload needs to be wrapped eg payload = attrs['txt'] or attrs['txt'] empty >> simplify
    for idx0, item in enumerate(coloring):
        template_core =''
        for idx1, item1 in enumerate(item['attr']):
            try:
                template_core += '{};'.format(attrs[item1])
            except:
                template_core += '{};'.format(str(item1))
        template = r'{}{}{}'.format('\033[',template_core[:-1],'m{}\033[0m')
        item['txt_color']=template.format(item['txt'])
        payload = sl_replace(payload, item['txt'], item['txt_color'], re_flags=re.DOTALL)
    return (payload)

def ansi_locate(payload=".", x=0, y=0):
    x=int(x)
    y=int(y)
    if x>255: x=255
    if y>255: y=255
    if x<0: x=0
    if y<0: y=0
    pos = {'string': payload, 'x':str(x),'y':str(y)}
    return("\033[{y};{x}f{string}".format(**pos))

def ansi_line(value, data_bg=data_bg): #horizontal line generator
    hresult = ['']*len(data_bg) # this creates the parts in the background
    vresult = ['']*len(data_bg)
    vline = ""

    def bg(vline):
        for idx1, y in enumerate(range(0,dvalue)):
            vline += ansi_locate(ansi_color(data_bg[idx0]['char_bg'],
                                 coloring=[{'txt':data_bg[idx0]['char_bg'],
                                 'attr': data_bg[idx0]['attr_bg']}]), 20, y)
        return (vline)

    def fg(vline):
        for idx1, y in enumerate(range(0,dvalue)):
            vline += ansi_locate(ansi_color(data_bg[idx0]['char'],
                                 coloring=[{'txt':data_bg[idx0]['char'],
                                 'attr': data_bg[idx0]['attr']}]), 20, y)
        return (vline)

    for idx0, item in enumerate(data_bg):
        value_range = in_range(value,item['range'])
        if value_range['bool'] is False and value <= int(value_range['min']): #higher > full range
            dvalue = int(value_range['max']) - int(value_range['min'])
            hline = ansi_color(data_bg[idx0]['char_bg']*dvalue,
                               coloring=[{'txt':data_bg[idx0]['char_bg']*dvalue,
                               'attr': data_bg[idx0]['attr_bg']}])

            vline = bg(vline)

        elif value_range['bool'] is True: #in range > partial
            dvalue = value - int(value_range['min'])
            #line = line_part(dvalue, data_bg[idx0])
            hline = ansi_color(data_bg[idx0]['char']*dvalue, coloring=[{'txt':data_bg[idx0]['char']*dvalue, 'attr': data_bg[idx0]['attr']}])
            vline = fg(vline)

            dvalue = int(value_range['max']) - value
            hline += ansi_color(data_bg[idx0]['char_bg']*dvalue, coloring=[{'txt':data_bg[idx0]['char_bg']*dvalue, 'attr': data_bg[idx0]['attr_bg']}])
            vline = bg(vline)

        elif value_range['bool'] is False and value >= int(value_range['max']): # lower > set to zero
            dvalue = int(value_range['max']) - int(value_range['min'])
            hline = ansi_color(data_bg[idx0]['char']*dvalue, coloring=[{'txt':data_bg[idx0]['char']*dvalue, 'attr': data_bg[idx0]['attr']}])
            vline = fg(vline)

        hresult[idx0] = hline
        vresult[idx0] = vline

    hresult = "".join(hresult)
    vresult = "".join(vresult)
    #print (vresult)
    return (hresult)


### End printing
#--------------------------------------------------------------------------------------
# Main Function
if __name__ == '__main__':
    print ("### basic ANSI colorprint testing ###")
    payload = 'This is a color test for [BLACK] [RED] [GREEN] [YELLOW] [BLUE] [MAGENTA] [CYAN] [WHITE]'
    print (payload) #uncolored
    print (ansi_color(payload,coloring)) #colored

    import time

    #location
    x=5
    y=15
    for idx0, key in enumerate(range(0,100)):
        value = int(random.random()*100)

        # gradations
        print (ansi_locate(" "*105,x,y))
        print (ansi_locate('|....'*21,x,y+1)) #blank line
        print (ansi_locate('|....'*21,x,y+3)) #blank line

        # indicators
        print (ansi_locate('{:02}'.format(value),x+value,y))
        print (ansi_locate('▼', x+value,y+1))
        print (ansi_locate('▲', x+value,y+3))

        # actual bar
        result = ansi_line(value, data_bg)
        print (ansi_locate(result,x+1,y+2)) #background bar

        time.sleep(0.1)

    print ("Finished")

