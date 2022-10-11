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
#   7. initialise_line()                                #
#   8. initialise_word()                                #
#                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import cv2
import os
import config
import random

# Function Name: complete_line
# Description : Concatenates white pixels to the current
#   line image so that it's length is equal to the page width.
def complete_line() -> None:
    '''complete_line()\n\nConcatenates white pixels to the current line image so that its length is equal to the page width.'''
    
    # get the length of the current line image
    current_line_img_length = config.current_line_img.shape[1]
    
    # white pixel to fill in the missing gap
    white_pixel = cv2.imread("Alphabet/Set 1/wh.png")

    # scale this up in the y - direction
    scaled_white_pixel = cv2.resize(white_pixel,(1,int(white_pixel.shape[0]*config.scale)) , interpolation= cv2.INTER_LINEAR)[:,0:1]

    # add the extra white pixels
    for i in range(config.page_width - current_line_img_length):
        config.current_line_img = cv2.hconcat([config.current_line_img, scaled_white_pixel])

    

# Function Name: initialise_page
# Description : Initialises a blank line in the beginning of the page
def initialise_page() -> None:
    '''initialise_page(page_width) -> Mat\n\nInitialises a blank line in the beginning of the page'''

    # initialise a new blank page
    config.current_page_img = cv2.imread("Alphabet/Set 1/wh.png")
    # By default, the page will contain a blank line
    for i in range(1,config.page_width):
        config.current_page_img = cv2.hconcat([config.current_page_img,cv2.imread("Alphabet/Set 1/wh.png")])


# Function Name: write_line
# Description : Concatenates the current line image to the current page image vertically
def write_line() -> None:
    '''write_line() -> None\n\nConcatenates the current line image to the current page image vertically'''
    complete_line()    # add the extra white pixels to the current line 

    # if the page is full, move to a new page
    if(config.current_page_img.shape[0] >= config.page_height):
       write_page()

    # append the current line to the page
    config.current_page_img = cv2.vconcat([config.current_page_img,config.current_line_img])


# Function Name: write_page
# Description : Saves the current page in the output folder and initialises a new blank page
def write_page() -> None:
    '''write_page() -> None\n\nSaves the current page in the output folder and initialises a new blank page'''

    # if the page is not complete, then we add blank lines to fill it up
    if(config.current_page_img.shape[0] < config.page_height):  
        initialise_line()   # create a blank line
        complete_line()     # complete the blank line with white pixels

        # repeatedly write this blank line to the page until it is full
        while config.current_page_img.shape[0] < config.page_height:
            write_line()

    cv2.imwrite("OP/" +str(config.current_page_number) +".png",config.current_page_img)   # save the current page image
    print("Completed Writing Page",config.current_page_number)                            # print the prompt
    initialise_page()                                                                     # initialise a new blank page 
    config.current_page_number += 1                                                       # increment the page number


# Function Name : write_word
# Description : Concatenates the current word image to the current line image horizontally
def write_word() -> None:
    '''write_word() -> None\n\nConcatenates the current word image to the current line image horizontally'''
    # if the current line length is exceeding the page lenght after concatenating
    # the current character then move to the next line before concatenating it
    if(config.current_line_img.shape[1] + config.current_word_img.shape[1] > config.page_width):
        write_line()                                                         # write the current line on to the page
        initialise_line()                                                    # initialise a new blank line

    # concatenate the current word to the line
    config.current_line_img = cv2.hconcat([config.current_line_img, config.current_word_img])


# Function Name: write_character
# Description : Concatenates the current character image to the current word image
# Argument 1: The character to be concatenated
def write_character(character:str) -> None:
    '''write_character(character) -> None\n\nConcatenates the current character image to the current word image'''
    # if the current character is not available then skip it
    if os.path.exists("Alphabet/Set "+str(random.randint(1,3))+"/"+str(ord(character))+".png"):
        # get the individual image of the current character
        config.current_character_img = cv2.imread("Alphabet/Set "+str(random.randint(1,3))+"/"+str(ord(character))+".png")

        # scale the character accordingly
        config.current_character_img = cv2.resize(config.current_character_img,(int(config.current_character_img.shape[1]*config.scale),int(config.current_character_img.shape[0]*config.scale)) , interpolation= cv2.INTER_LINEAR)

        # concatenate the current chatacter to the current line
        config.current_word_img = cv2.hconcat([config.current_word_img, config.current_character_img])



# Function Name : initialise_line
# Description : Creates a line starting with white pixels
def initialise_line() -> None:
    '''initialise_line() -> None\n\nCreates a line starting with white pixels'''
    # load the white pixel
    white_pixel = cv2.imread("Alphabet/Set 1/wh.png")
    # scale it up in the y - direction
    scaled_white_pixel = cv2.resize(white_pixel,(1,int(white_pixel.shape[0]*config.scale)) , interpolation= cv2.INTER_LINEAR)

    config.current_line_img = scaled_white_pixel


# Function Name : initialise_line
# Description : Creates a line starting with white pixels
def initialise_word() -> None:
    '''initialise_line() -> None\n\nCreates a line starting with white pixels'''
    # load the white pixel
    white_pixel = cv2.imread("Alphabet/Set 1/32.png")
    # scale it in the y direction
    scaled_white_pixel = cv2.resize(white_pixel,(int(white_pixel.shape[1]*config.scale),int(white_pixel.shape[0]*config.scale)) , interpolation= cv2.INTER_LINEAR)
    config.current_word_img = scaled_white_pixel