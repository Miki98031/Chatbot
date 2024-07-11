from loaders.file_loader import FileLoader
from langchain.document_loaders import PyPDFLoader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from langchain.document_loaders import UnstructuredFileLoader
import fitz
import pdfplumber
from loaders.image_loader import ImageLoader
from langchain.document_loaders.merge import MergedDataLoader
from pathlib import Path
from pycld2 import pycld2
import icu

class PDFLoader(FileLoader):
    def get_image_files(self, file):
        image_file_list = []
        path_to_poppler_exe = Path(r"C:\Program Files\poppler-23.11.0\Library\bin")
        
        pdf_pages = convert_from_path(
                file, 100, poppler_path=path_to_poppler_exe
        )
        
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            filename = f"page_{page_enumeration:03}.jpg"
            page.save(filename, "JPEG")
            image_file_list.append(filename)

        return image_file_list


    def readTextFromImages(self, image_file_list):
        output_file = "output_file.txt"
        
        with open(output_file, "w", encoding="utf-8") as output_file:
            for image_file in image_file_list:
                loader = ImageLoader()
                document = loader.load(image_file)
                text = document[0].page_content
                output_file.write(text)
            
        loader = UnstructuredFileLoader("output_file.txt")
        docs = loader.load()
        return docs
    
    
    def load(self, file):
        with pdfplumber.open(file) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            print('Text with naive loader')
            
        if text != '':
            print('ovde1')
            loader = PyPDFLoader(file_path=file)
            docs = loader.load()

        else:
            print('ovde2')
            loader = ImageLoader()
            image_file_list = self.get_image_files(file)
            docs = self.readTextFromImages(image_file_list)
                
        return docs
        