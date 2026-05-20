from pypdf import PdfReader


def parsePdf(file):
    file = f".\pdf\{file}.pdf"
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    if number_of_pages != 1:
        print(f"There are {number_of_pages} pages in pdf.\nReading the first page...\n\n")
    else:
        print(f"There is only {number_of_pages} page in pdf.\nReading the page...\n\n")
    page = reader.pages[0]
    text = page.extract_text()



if __name__ == "__main__":
    file = input("Enter file name after adding it in the .\pdf: ")
    parsePdf(file)
