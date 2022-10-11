# This file contains the global variables that
# have to be shared among all the other python modules.

# Global variables
page_width = 1700                   # width of the page in pixels
page_height = 2404                  # height of the page in pixels
key_buffer = ""                # stores the characters after a pipe is encountered
current_key_symbols_encountered = 0   # holds the number of pipes encountered in the current key
current_page_number = 1             # holds the current page number
scale = 1                           # the functions import an image and scale it according to this value
key_start_symbol = "<"              # customizable key start symbol
key_end_symbol = ">"                # customizable key end symbol


# Image variables set to None ( Initially )
current_character_img = None        # holds the image of the current character
current_word_img = None             # holds the image of the current word
current_line_img = None             # holds the image of the current line
current_page_img = None             # holds the image of the current page