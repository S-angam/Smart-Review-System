import PyPDF2

class ReadPDF:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            return text
    
    def clean_text(self, text):
        cleaned_text = ' '.join(text.split())
        return cleaned_text