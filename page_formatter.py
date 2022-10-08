# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                       #
#                        READ ME                        #
#                                                       #
#   This module contains all the functions required     #
#   to run the main.py file. The functions defined in   #
#   this module are mentioned below. If you add or      #
#   remove any functions, then please change the given  #
#   given list as well.                                 #
#                                                       #
#   Defined Functions:                                  #
#   1. new_line()                                       #
#   2. initialise_page()                                #
#   3. write_page()                                     #
#   4. write_line()                                     #
#   5. write_word()                                     #
#   6. write_character()                                #
#                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import cv2
import os
import config
import random

# Function Name: new_line
# Description : Concatenates white pixels to the current
#   line image so that it's length is equal to the page width.
def new_line() -> None:
    '''new_line()\n\nConcatenates white pixels to the current line image so that its length is equal to the page width.'''
    
    # get the length of the current line image
    current_line_img_length = config.current_line_img.shape[1]

    # add the extra white pixels
    for i in range(config.page_width - current_line_img_length):
        config.current_line_img = cv2.hconcat([config.current_line_img, cv2.imread("Alphabet/Set 1/wh.png")])
    

# Function Name: initialise_page
# Description : Initialises a blank line in the beginning of the page
def initialise_page() -> None:
    '''initialise_page(page_width) -> Mat\n\nInitialises a blank line in the beginning of the page'''

    # initialise a new blank page
    config.current_page_img = cv2.imread("Alphabet/Set 1/wh.png")
    # By default, the page will contain a blank line
    for i in range(1,config.page_width):
        config.current_page_img = cv2.hconcat([config.current_page_img,cv2.imread("Alphabet/Set 1/wh.png")])


# Function Name: write_page
# Description : Saves the current page in the output folder and initialises a new blank page
def write_page() -> None:
    '''write_page() -> None\n\nSaves the current page in the output folder and initialises a new blank page'''
    cv2.imwrite("OP/" +str(config.current_page_number) +".png",config.current_page_img)   # save the current page image
    print("Completed Writing Page",config.current_page_number)
    initialise_page()                                                                     # initialise a new blank page 
    config.current_page_number += 1                                                       # increment the page number


# Function Name: write_line
# Description : Concatenates the current line image to the current page image vertically
def write_line() -> None:
    '''write_line() -> None\n\nConcatenates the current line image to the current page image vertically'''
    new_line()    # add the extra white pixels to the current line 

    # if the page is full, move to a new page
    if(config.current_page_img.shape[0] >= config.page_height):
       write_page()

    # append the current line to the page
    config.current_page_img = cv2.vconcat([config.current_page_img,config.current_line_img])


# Function Name : write_word
# Description : Concatenates the current word image to the current line image horizontally
def write_word() -> None:
    '''write_word() -> None\n\nConcatenates the current word image to the current line image horizontally'''
    # if the current line length is exceeding the page lenght after concatenating
    # the current character then move to the next line before concatenating it
    if(config.current_line_img.shape[1] + config.current_word_img.shape[1] > config.page_width):
        write_line()                                            # write the current line on to the page
        config.current_line_img = cv2.imread("Alphabet/Set 1/wh.png")        # initialise a new blank line

    # concatenate the current word to the line
    config.current_line_img = cv2.hconcat([config.current_line_img, config.current_word_img])


# Function Name: write_character
# Description : Concatenates the current character image to the current word image
# Argument 1: The character to be concatenated
def write_character(character:str) -> None:
    '''write_character() -> None\n\nConcatenates the current character image to the current word image'''
    # if the current character is not available then skip it
    if os.path.exists("Alphabet/Set "+str(random.randint(1,3))+"/"+str(ord(character))+".png"):
        # get the individual image of the current character
        config.current_character_img = cv2.imread("Alphabet/Set "+str(random.randint(1,3))+"/"+str(ord(character))+".png")
        
        # concatenate the current chatacter to the current line
        config.current_word_img = cv2.hconcat([config.current_word_img, config.current_character_img])