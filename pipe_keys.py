import cv2
import config
from page_formatter import  complete_line, initialise_line, initialise_word, write_character, write_line, write_page, write_word
import re
import numpy as np

# Function Name: new_line()
# Description : Writes the current line to the page
#   and initialises a new blank line
def new_line() -> None:
    '''new_line() -> None\n\nWrites the current line to the page and initialises a new blank line'''
    write_word()        # write the current word before moving to the next line
    initialise_word()   # create a new blank word
    write_line()        # write the current line to the paper
    initialise_line()   # start with a new blank line


# Function Name : new_line()
# Description : Used to give vertical space between two lines
def vertical_space() -> None:
    '''vertical_space() -> None\n\nUsed to give vertical space between two lines'''
    # extract the number of vertical spaces
    vertical_spaces = int(config.pipe_key_buffer.split(":")[1][:-1])
    # skip n lines
    for i in range(vertical_spaces):
        write_line()
        initialise_line()


# Function Name : new_page()
# Description : Writes the current line to the current page and then starts with a new page
def new_page() -> None:
    '''new_page() -> None\n\nWrites the current line to the current page and then starts with a new page'''
    # write the current line before writing the page
    new_line()
    write_page()


# Function Name : horizontal_space()
# Description : Adds horizontal space n times
def horizontal_space() -> None:
    '''horizontal_space() -> None\n\nAdds horizontal space n times'''
    
    # extract n from the key
    horizontal_spaces = int(config.pipe_key_buffer.split(":")[1][:-1])

    # concatenate spaces n times
    write_word()           # write the current word to the line
    initialise_word()      # create a blank word
    
    # keep on concatenating the blank word to the line n times
    for i in range(horizontal_spaces):
        write_word()       


# Function Name : tab_space()
# Description : Adds horizontal space n times
def tab_space() -> None:
    '''tab_space() -> None\n\nAdds horizontal space n times'''
    
    # extract n from the key
    tab_spaces = int(config.pipe_key_buffer.split(":")[1][:-1])

    # concatenate spaces n times
    write_word()           # write the current word to the line
    initialise_word()      # create a blank word
    
    # keep on concatenating the blank word to the line n times
    for i in range(tab_spaces * 4):
        write_word()   


# Function Name : color()
# Description : Changes the color of the text present
#   in the key to the given color.
def color() -> None:
    '''color() -> None\n\nChanges the color of the text present in the key to the given color'''

    # extract color and text from the key
    extracted_text = config.pipe_key_buffer.split(",")[-1][:-1]
    extracted_color = [int(x) for x in config.pipe_key_buffer.split(":")[1].split("]")[0].strip()[1:].split(",")][::-1]

    # write the current word to the line before colouring the next few characters
    write_word()
    # create a new blank word
    initialise_word()

    # concatenate all the extracted text to the blank word
    for chars in extracted_text:
        write_character(chars)
    
    # remove the default extra space in front of the word
    config.current_word_img = config.current_word_img[:,27:]

    # color the word
    config.current_word_img[np.where((config.current_word_img<=[200, 200, 200]).all(axis=2))] = extracted_color


# Function Name : font_size()
# Description : Changes the font size of the text
#   present in the key to the given scale
# !! Important Note: The font_size funtion changes the size of a single line and crops 
def font_size() -> None:
    '''font_size() -> None\n\nChanges the font size of the text present in the key to the given scale'''
    # get the extracted text from the key
    extracted_text = config.pipe_key_buffer.split(",")[-1][:-1]
    extracted_scale = float(config.pipe_key_buffer.split(",")[0].split(":")[-1])

    # write the existing word to the line and line to the page and start from a new line as the size is different
    new_line()

    # write the extracted text to th line
    for chars in extracted_text:
        write_character(chars)

    # write the word to the new line
    write_word()
    initialise_word()

    config.scale = extracted_scale
    # complete the line
    complete_line()

    # change the scale of this line
    config.current_line_img = cv2.resize(config.current_line_img,(int(config.current_line_img.shape[1]*extracted_scale),int(config.current_line_img.shape[0]*extracted_scale)) , interpolation= cv2.INTER_LINEAR)[:,int(27*extracted_scale-27):config.page_width+int(27*extracted_scale-27)]
    
    # write this scaled line to the page
    write_line()
    config.scale = 1
    initialise_line()
    

# Function Name : font
# Description : This function is basically a combination of
#   color and fontsize functions


# Function Name: analyse_key()
# Description : This functions checks the pipe key buffer
#    and performs the operation based on the pipe key 
#    encountered. This function acts like a switch case.
def analyse_key() -> None:
    '''analyse_key() -> None\n\nThis functions checks the pipe key buffer and performs the operation based on the pipe key encountered.'''

    # if |nl| is encountered, then move to the new line
    if re.search("\| *nl *\|",config.pipe_key_buffer):
        new_line()
    
    # if |vs:n| is encountered, then skip n lines
    if re.search("\| *vs *: *[0-9]*\|",config.pipe_key_buffer):
        vertical_space()

    # if |np| is encountered, then start with a new page
    if re.search("\| *np *\|",config.pipe_key_buffer):
        new_page()
    
    # if |hs:n| is encountered
    if re.search("\| *hs *: *[0-9]*\|", config.pipe_key_buffer):
        horizontal_space()
    
    # if |ts:n| is encountered
    if re.search("\| *ts *: *[0-9]*\|", config.pipe_key_buffer):
        tab_space()
    
    # if |color: [R,G,B], TEXT| is encountered
    if re.search("\| *color *: *\[ *.*,.*,.*\] *,.*\|",config.pipe_key_buffer):
        color()
    
    # if |fontsize: x, TEXT| is encountered
    if re.search("\| *fontsize *: *.* *,.*\|",config.pipe_key_buffer):
        font_size()