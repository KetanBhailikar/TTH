import cv2
from page_formatter import initialise_line, initialise_word, initialise_page, write_character, write_line, write_page, write_word
import config
from pipe_keys import analyse_key

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
        # initialise a new line           
        initialise_line()   
        
        # for all the words in a line
        for word in line.split():
            # initialise a blank word starting with a space
            initialise_word()

            # loop for each character in a word
            for n,character in enumerate(word):

                # if a pipe is encountered, then key has started or closed
                if character == "|":
                    config.current_key_pipes_encountered += 1

                # if a key is being encountered then don't write it on paper,
                # instead, put it in the pip key buffer for further analysis
                if config.current_key_pipes_encountered > 0 and config.current_key_pipes_encountered < 3:
                    config.pipe_key_buffer += character
                else:
                    write_character(character)                      # write the character 

                # if the last pipe is encountered then the key has ended
                if config.current_key_pipes_encountered == 2:
                    analyse_key()
                    config.current_key_pipes_encountered = 0          # reset the pipe counter
                    config.pipe_key_buffer = ""         # reset the pipe key buffer

            write_word()
        
        write_line()                                                # write the current line to the page

    # write the final page in the OP folder
    write_page()


main()