from pypdf import PdfReader


def parsePdf(file):
    file = f".\pdf\{file}.pdf"
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    if number_of_pages < 1:
        return "No_Pages_Found"
    elif number_of_pages != 1:
        print(f"There are {number_of_pages} pages in pdf.\nReading the first page...\n\n")
    else:
        print(f"There is only {number_of_pages} page in pdf.\nReading the page...\n\n")

    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        text = text.replace("\uf0b7", "•")

        if i == 0:
            # Writing to the file
            with open(".\processing_files\output.txt", "w", encoding="utf-8") as file:
                file.write(f"\n________ Page {i+1} _________\n")
                file.write(text)
        else:
            # Appending to the file
            with open(".\processing_files\output.txt", "a", encoding="utf-8") as file:
                file.write(f"\n________ Page {i+1} _________\n")
                file.write(text)

    return "Extracted into .\processing_files\output.txt"


# if __name__ == "__main__":
#     file = input("Enter file name after adding it in the .\pdf: ")
#     parsePdf(file)
