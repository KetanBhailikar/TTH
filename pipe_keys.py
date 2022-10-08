import config
from page_formatter import  initialise_line, initialise_word, write_line, write_page, write_word
import re
import cv2

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