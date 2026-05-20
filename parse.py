from pypdf import PdfReader

file = input("Enter file name after adding it in the ./pdf: ")  # D:\Coding2\MLAI\New Project\pdf\JD.pdf
file = f".\pdf\{file}.pdf"
reader = PdfReader(file)



number_of_pages = len(reader.pages)
if number_of_pages != 1:
    print(f"There are {number_of_pages} pages in pdf, let me read the first page...\n\n")
else:
    print(f"There is only {number_of_pages} page in pdf, let me read the page...\n\n")
page = reader.pages[0]
text = page.extract_text()
print(f"The first page says---------------------------\n{text}")


def main():
    print("Hello from new-project!")
    file = input("Enter file name after adding it in the .\pdf: ")  # .\pdf\JD.pdf
    file = f".\pdf\{file}.pdf"
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    if number_of_pages != 1:
        print(f"There are {number_of_pages} pages in pdf.\nReading the first page...\n\n")
    else:
        print(f"There is only {number_of_pages} page in pdf.\nReading the page...\n\n")
    page = reader.pages[0]
    text = page.extract_text()
    # print(f"The first page says---------------------------\n{text}")



# if __name__ == "__main__":
#     main()
