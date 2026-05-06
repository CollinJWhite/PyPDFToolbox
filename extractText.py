from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
import os
import sys
import logging
logging.basicConfig(filename='myProgramLog.txt', filemode='w', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

#gets a valid PDF file from the user, quitting if they choose
def get_input_file():
    validFile = False
    validExtensions = ['.pdf']
    directory=''
    while(not validFile):
        directory = input(f'Please enter a file (.pdf) to extract text from (press q to quit)\nNote a pdf file must be in a table format with commas as separators: ')
        if(directory.lower().strip() == "q"):
            logging.debug('Quitting due to user input...')
            sys.exit()
        logging.debug(f'Validating path %s', directory)
        if(os.path.isfile(directory)):
            if(os.path.splitext(directory)[1].lower() in validExtensions):
                validFile = True
            else:
                basename = os.path.basename(directory)
                logging.warning('User tried using this file: %s. Prompting Again.', basename)
                print(f'{basename} is not a valid file type. Try Again.')
        else:
            logging.warning('User gave an invalid file path: %s. Prompting Again.', directory)
            print('Invalid file path. Try Again.')
    return directory

pdf_path = get_input_file()
logging.info("PDF file got, creating reader object...")
reader = PdfReader(pdf_path)
logging.debug("Prompting page to extract text from...")
print(f"You entered {pdf_path} as the file to extract text from.")
page_to_read = input(f"What page would you like to extract text from? (1 - {len(reader.pages)}) (if all, type -1) (to specify range, type -2): ")

extracted_text = []

if((int(page_to_read) == -1)):
    logging.info(f"User input: {page_to_read}, extracting all pages text")
    i = 0
    for page in reader.pages:
        logging.debug(f"Extracting text for page {i}")
        extracted_text.append(page.extract_text())
        i = i + 1
        
elif((int(page_to_read) == -2)):
    #ask to specify page range
    logging.info(f"User input: {page_to_read}, prompting for page range to extract text from...")
    page_range = input('What page range would like to extract text from? (ex: 1-3, 5-7, etc.) (-1): ')
    nums = page_range.split('-')
    begIndex = int(nums[0]) - 1
    endIndex = int(nums[1]) - 1
    logging.info(f"Extracting text from page range {begIndex} to {endIndex}")
    for i in range(begIndex, endIndex + 1):
        logging.debug(f"Extracting text for page {i}")
        page = reader.pages[i]
        extracted_text.append(page.extract_text())

else:
    logging.info(f"Extracting text from page {page_to_read}")
    page = reader.pages[int(page_to_read) - 1]
    extracted_text.append(page.extract_text())

with open("extracted.txt", "w", encoding="utf-8") as file:
    for text in extracted_text:
        file.write(f"{text}\n")

logging.info("Done.")
