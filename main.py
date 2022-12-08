from fpdf import FPDF
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
            # initialise a blank word starting with a space if the key is not being read
            if config.current_key_symbols_encountered == 0 :
                initialise_word()

            # loop for each character in a word
            for character in word:

                # if a start/end symbol is encountered, then key has started or closed
                if character == config.key_start_symbol:
                    config.current_key_symbols_encountered += 1
                elif character == config.key_end_symbol:
                    config.current_key_symbols_encountered -= 1

                # if a key is being encountered then don't write it on paper,
                # instead, put it in the pipe key buffer for further analysis
                if config.current_key_symbols_encountered > 0 or character == ">":
                    config.key_buffer += character
                else:
                    write_character(character)                      # write the character 

                # if the last pipe is encountered then the key has ended
                if config.current_key_symbols_encountered == 0 and config.key_buffer !="":
                    analyse_key(config.key_buffer)
                    config.current_key_symbols_encountered = 0          # reset the pipe counter
                    config.key_buffer = ""         # reset the pipe key buffer

            # if the key has multiple words in its text, then don't write those words to the line, instead,
            # add a space between the words in the pipe key buffer
            if config.current_key_symbols_encountered > 0 or character == ">":
                    config.key_buffer += " "
            else:
                write_word()
        
        write_line()                                                # write the current line to the page

    # write the final page in the OP folder
    write_page()

    # convert the images to pdf
    pdf = FPDF()
    for i in range(1,config.current_page_number):
        pdf.add_page()
        pdf.image("OP/"+str(i)+".png",0,0,210,297)
    pdf.output("Assignment.pdf", "F")    

main()