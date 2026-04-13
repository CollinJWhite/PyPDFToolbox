from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
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

def make_number_stamp(number, width, height):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))

    c.setFont("Helvetica-Bold", 36)
    c.setFillColor("red")

    # Position: top-right corner with padding
    text = f"Page {number}"
    text_width = c.stringWidth(text, "Helvetica-Bold", 36)

    x = width - text_width - 20   # 20pt padding from right
    y = height - 50               # 50pt down from top

    c.drawString(x, y, text)
    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

#numbers all pages in a PDF file, saving the new file as "numbered.pdf"
pdf_path = get_input_file()

numbered_writer = PdfWriter()
reader = PdfReader(pdf_path)

for i, page in enumerate(reader.pages, start=1):
    w = float(page.mediabox.width)
    h = float(page.mediabox.height)

    stamp = make_number_stamp(i, w, h)
    page.merge_page(stamp)

    numbered_writer.add_page(page)

numbered_writer.write("numbered.pdf")