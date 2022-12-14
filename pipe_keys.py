import config
from page_formatter import  complete_line, initialise_line, initialise_word, write_character, write_line, write_page, write_word
import re
import numpy as np

color_var = None

# Function Name: new_line()
# Description : Writes the current line to the page
#   and initialises a new blank line
def new_line() -> None:
    '''new_line() -> None\n\nWrites the current line to the page and initialises a new blank line'''
    if color_var != None: config.current_word_img[np.where((config.current_word_img<=[200, 200, 200]).all(axis=2))] = color_var
    write_word()        # write the current word before moving to the next line
    initialise_word()   # create a new blank word
    write_line()        # write the current line to the paper
    initialise_line()   # start with a new blank line


# Function Name : new_line()
# Description : Used to give vertical space between two lines
def vertical_space() -> None:
    '''vertical_space() -> None\n\nUsed to give vertical space between two lines'''
    # extract the number of vertical spaces
    vertical_spaces = int(config.key_buffer.split(":")[1][:-1])
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
    horizontal_spaces = int(config.key_buffer.split(":")[1][:-1])

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
    tab_spaces = int(config.key_buffer.split(":")[1][:-1])

    # concatenate spaces n times
    write_word()           # write the current word to the line
    initialise_word()      # create a blank word
    
    # keep on concatenating the blank word to the line n times
    for i in range(tab_spaces * 4):
        write_word()   


# Function Name : color()
# Description : Changes the color of the text present
#   in the key to the given color.
def color(key_buffer) -> None:
    '''color() -> None\n\nChanges the color of the text present in the key to the given color'''

    global color_var

    # local variable limited to this function
    is_first_word = True
    current_key_symbols_encountered_local = 0
    local_key_buffer = ""

    # extract color and text from the key
    extracted_text = key_buffer[key_buffer.find("]"):][key_buffer[key_buffer.find("]"):].find(",")+1:][:-1]


    extracted_color = [int(x) for x in key_buffer.split(":")[1].split("]")[0].strip()[1:].split(",")][::-1]
    color_var = extracted_color

    # write the current word to the line before colouring the next few characters
    write_word()
    # create a new blank word
    initialise_word()

    # concatenate all the extracted text to the blank word
    for words in extracted_text.split():
        initialise_word()
        for chars in words:
            # if a start/end symbol is encountered, then key has started or closed
            if chars == config.key_start_symbol:
                current_key_symbols_encountered_local += 1
            elif chars == config.key_end_symbol:
                current_key_symbols_encountered_local -= 1

            # if a key is being encountered then don't write it on paper,
            # instead, put it in the pipe key buffer for further analysis
            if current_key_symbols_encountered_local > 0 or chars == ">":
                local_key_buffer += chars
            else:
                write_character(chars)                      # write the character 

            # if the last pipe is encountered then the key has ended
            if current_key_symbols_encountered_local == 0 and local_key_buffer !="":
                analyse_key(local_key_buffer)
                current_key_symbols_encountered_local = 0          # reset the pipe counter
                local_key_buffer = ""                              # reset the pipe key buffer

        if is_first_word:    
            # remove the default extra space in front of the word
            config.current_word_img = config.current_word_img[:,27:]
            is_first_word = False

        # color the word
        config.current_word_img[np.where((config.current_word_img<=[200, 200, 200]).all(axis=2))] = color_var

        if current_key_symbols_encountered_local > 0 or chars == config.key_end_symbol:
            local_key_buffer += " "
        else:
            write_word()
    
    initialise_word()
    color_var = None

# Function Name : duplicate()
# Description : Changes the color of the text present
#   in the key to the given color.
def duplicate(key_buffer) -> None:
    '''duplicate() -> None\n\nWrites a given text n number of times'''

    is_first_word = True
    current_key_symbols_encountered_local = 0
    local_key_buffer = ""

    # extract text from the key
    extracted_text = key_buffer[key_buffer.find(",")+1:-1]

    # extract n from the key
    n = int(key_buffer[key_buffer.find(":")+1:key_buffer.find(",")])

    # write the current word to the line before duplicating the next few characters
    write_word()
    # create a new blank word
    initialise_word()

    for repeat in range(n):
        # concatenate all the extracted text to the blank word
        for words in extracted_text.split():
            initialise_word()
            for chars in words:
                # if a start/end symbol is encountered, then key has started or closed
                if chars == config.key_start_symbol:
                    current_key_symbols_encountered_local += 1
                elif chars == config.key_end_symbol:
                    current_key_symbols_encountered_local -= 1

                # if a key is being encountered then don't write it on paper,
                # instead, put it in the pipe key buffer for further analysis
                if current_key_symbols_encountered_local > 0 or chars == ">":
                    local_key_buffer += chars
                else:
                    write_character(chars)                      # write the character 

                # if the last pipe is encountered then the key has ended
                if current_key_symbols_encountered_local == 0 and local_key_buffer !="":
                    analyse_key(local_key_buffer)
                    current_key_symbols_encountered_local = 0          # reset the pipe counter
                    local_key_buffer = ""                              # reset the pipe key buffer

            if is_first_word:    
                # remove the default extra space in front of the word
                config.current_word_img = config.current_word_img[:,27:]
                is_first_word = False

            if current_key_symbols_encountered_local > 0 or chars == config.key_end_symbol:
                local_key_buffer += " "
            else:
                write_word()
    
    initialise_word()

# Function Name : font_size()
# Description : Changes the font size of the text
#   present in the key to the given scale
# !! Important Note: The font_size funtion changes the size of a single line and crops 
def font_size(key_buffer) -> None:
    '''font_size() -> None\n\nChanges the font size of the text present in the key to the given scale'''

    # local variables limited only to this function
    current_key_symbols_encountered_local = 0
    local_key_buffer = ""

    # get the extracted text from the key
    extracted_text = key_buffer[key_buffer.find(",")+1:][:-1]
    extracted_scale = float(key_buffer.split(",")[0].split(":")[-1])

    # write the existing word to the line and line to the page and start from a new line as the size is different
    write_word()
    write_line()

    # apply the scale
    config.scale = extracted_scale

    # start in a new line
    initialise_line()

    # for every word in the extracted text
    for words in extracted_text.split():
        initialise_word()           # start a new word  
        for chars in words:         # for every character in the word
            # if a start/end symbol is encountered, then key has started or closed
            if chars == config.key_start_symbol:
                current_key_symbols_encountered_local += 1
            elif chars == config.key_end_symbol:
                current_key_symbols_encountered_local -= 1

            # if a key is being encountered then don't write it on paper,
            # instead, put it in the pipe key buffer for further analysis
            if current_key_symbols_encountered_local > 0 or chars == ">":
                local_key_buffer += chars
            else:
                write_character(chars)                      # write the character 

            # if the last pipe is encountered then the key has ended
            if current_key_symbols_encountered_local == 0 and local_key_buffer !="":
                analyse_key(local_key_buffer)
                current_key_symbols_encountered_local = 0          # reset the pipe counter
                local_key_buffer = ""                              # reset the pipe key buffer

        # color the word
        if color_var != None:
            config.current_word_img[np.where((config.current_word_img<=[200, 200, 200]).all(axis=2))] = color_var

        if current_key_symbols_encountered_local > 0 or chars == ">":
            local_key_buffer += " "
        else:
            write_word()

    write_line()           # write the line
    complete_line()        # complete the line
    config.scale = 1       # reset the scale
    initialise_word()      # initialise the word
    initialise_line()      # initialise a new line
    

# Function Name : font
# Description : This function is basically a combination of
#   color and fontsize functions


# Function Name: analyse_key()
# Description : This functions checks the pipe key buffer
#    and performs the operation based on the pipe key 
#    encountered. This function acts like a switch case.
def analyse_key(key_buffer) -> None:
    '''analyse_key() -> None\n\nThis functions checks the pipe key buffer and performs the operation based on the pipe key encountered.'''

    # if nl key is encountered, then move to the new line
    if re.search("^"+config.key_start_symbol+" *nl *"+config.key_end_symbol,key_buffer):
        new_line()
    
    # if vs:n key is encountered, then skip n lines
    if re.search("^"+config.key_start_symbol+" *vs *: *[0-9]*"+config.key_end_symbol,key_buffer):
        vertical_space()

    # if |np| is encountered, then start with a new page
    if re.search("^"+config.key_start_symbol+" *np *"+config.key_end_symbol,key_buffer):
        new_page()
    
    # if |hs:n| is encountered
    if re.search("^"+config.key_start_symbol+" *hs *: *[0-9]*"+config.key_end_symbol, key_buffer):
        horizontal_space()
    
    # if |ts:n| is encountered
    if re.search("^"+config.key_start_symbol+" *ts *: *[0-9]*"+config.key_end_symbol, key_buffer):
        tab_space()
    
    # if |color: [R,G,B], TEXT| is encountered
    if re.search("^"+config.key_start_symbol+" *color *: *\[ *.*,.*,.*\] *,.*"+config.key_end_symbol,key_buffer):
        color(key_buffer)
    
    # if |fontsize: x, TEXT| is encountered
    if re.search("^"+config.key_start_symbol+" *fontsize *: *.* *,.*"+config.key_end_symbol,key_buffer):
        font_size(key_buffer)
    
    # if |dup: x, TEXT| is encountered
    if re.search("^"+config.key_start_symbol+" *dup *: *.* *,.*"+config.key_end_symbol,key_buffer):
        duplicate(key_buffer)