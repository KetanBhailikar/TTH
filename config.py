# This file contains the global variables that
# have to be shared among all the other python modules.

# Customizable Variables
left_margin = 20
right_margin = 20
top_margin = 20
bottom_margin = 20
min_justify_limit = 0.75            # the text in a line will be justified only when this much of a line is full
page_width = 1700                   # width of the page in pixels
page_height = 2404                  # height of the page in pixels

# Global variables
key_buffer = ""                     # stores the characters after a pipe is encountered
current_key_symbols_encountered = 0 # holds the number of pipes encountered in the current key
current_page_number = 1             # holds the current page number
scale = 1                           # the functions import an image and scale it according to this value
key_start_symbol = "<"              # customizable key start symbol
key_end_symbol = ">"                # customizable key end symbol
line_word_end_data = []             # holds positions of the spaces in a line

# Image variables set to None ( Initially )
current_character_img = None        # holds the image of the current character
current_word_img = None             # holds the image of the current word
current_line_img = None             # holds the image of the current line
current_page_img = None             # holds the image of the current page

# Final Calculations
page_width = page_width - (left_margin + right_margin)
page_height = page_height - (top_margin + bottom_margin)