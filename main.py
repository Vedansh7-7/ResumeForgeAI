from parse import parsePdf
def main():
    
    # Reading a file
    with open(".\processing_files\output.txt", "r", encoding="utf-8") as file:
        content = file.read()
    print(content)

if __name__ == "__main__":
    print("Hello from new-project!\n\n")
    file = input("Enter file name after adding it in the .\pdf: ")
    result = parsePdf(file)
    if result == r"Extracted into .\processing_files\output.txt":
        main()
    else:
        print("Please check your pdf, we are not able to see any pages in it.")
