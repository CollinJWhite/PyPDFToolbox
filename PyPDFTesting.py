# extract_doc_info.py
# This script is testing for various featuers of PyPDF2, listed below:
# 1. Extracting metadata from a PDF file
# 2. Rotating pages in a PDF file and saving the result as a new file
# 3. Merging multiple PDF files into a single PDF file
# 4. Merging the first two pages of a PDF file on top of each other

from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter

def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        information = pdf.metadata

    txt = f"""
    Information about {pdf_path}: 

    Title: {information.title}
    Author: {information.author}
    Subject: {information.subject}
    Creator: {information.creator}
    Producer: {information.producer}
    """

    print(txt)
    return information

def rotate_pages(path):
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(90)
        writer.add_page(page)

    writer.write("rotated.pdf")

def merge_pdfs(paths):
    writer = PdfWriter()
    for path in paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)  

    writer.write("appended.pdf")

#merges the first two pages of a pdf on top of each other
def merge_pages(basePDF, overPDF):
    writer = PdfWriter()
    baseReader = PdfReader(basePDF)
    overReader = PdfReader(overPDF)

    basePage = baseReader.pages[0]
    overPage = overReader.pages[1]

    page = basePage
    page.merge_page(overPage)

    writer.add_page(page)

    writer.write("firstpagesmerged.pdf")




reportPath = 'reportlab-sample.pdf'
linkedInPath = 'CollinLinkedIn.pdf'
extractTextTutPath = 'extractText.pdf'
#metainfo = extract_information(reportPath)
#rotate_pages(reportPath)
#merge_pdfs([reportPath, linkedInPath, extractTextTutPath])
#merge_pages(linkedInPath, reportPath)