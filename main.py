import cv2
from page_formatter import initialise_page, write_character, write_line, write_page, write_word
import config

def main():
    # fetch the text files as input
    input_file = open("text.txt","r",encoding="utf8")

    # read all the lines from the file
    all_lines = input_file.readlines()

    # initialise a new blank page
    initialise_page()

    # iterate through all the characters
    # and concatenate the corresponding picture to the page
    for line in all_lines:
        config.current_line_img = cv2.imread("Alphabet/Set 1/wh.png")            # initialise a new line
        
        # for all the words in a line
        for word in line.split():
            config.current_word_img = cv2.imread("Alphabet/Set 1/32.png")        # initialise a blank word starting with a space

            # loop for each character in a word
            for n,character in enumerate(word):
                write_character(character)                          # write the character 

            write_word()
        
        write_line()                                                # write the current line to the page

    # write the final page in the OP folder
    write_page()


main()