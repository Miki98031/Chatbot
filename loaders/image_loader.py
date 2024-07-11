from loaders.file_loader import FileLoader
from pathlib import Path
from llama_index import download_loader
from pycld2 import pycld2
import icu
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import cv2
from deskew import determine_skew
from skimage.transform import rotate, resize
from skimage import io as ioski

class ImageLoader(FileLoader):
    def preprocess_image(self, image):
        read_img = cv2.imread(image, 0)
        dilated_img = cv2.dilate(read_img, np.ones((7,7), np.uint8)) 
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(read_img, bg_img)
        norm_img = diff_img.copy() # Needed for 3.x compatibility
        cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        _, thr_img = cv2.threshold(norm_img, 230, 0, cv2.THRESH_TRUNC)
        cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        angle = determine_skew(thr_img)
        rotated_img = rotate(thr_img, angle)*255
        rotated_img = Image.fromarray(rotated_img.astype(np.uint8))
        threshold = 244  # range from 0 to 255
        image_file = rotated_img.point( lambda p: 255 if p > threshold else 0 )
        image_file = image_file.convert('1')
        image_file.save(f'konv_{image}.jpg')
        conv_image_file = f'konv_{image}.jpg'
        return conv_image_file
    
    def get_language_code(self, docs):
        language_names_and_code = {
            'ENGLISH' : 'eng',
            'BOSNIAN' : 'bos',
            'SERBIAN' : 'srp+srp_latn',
            'GERMAN' : 'deu'
        }

        text = str(dict(docs[0])['text'])
        
        result = pycld2.detect(text)
        print(result)
        (isReliable, textBytesFound, details) = result
        print(details[0][0],'-',details[0][1])
        language_name = details[0][0]

        language_code = language_names_and_code.get(language_name, '')
        if language_code == '':
            raise KeyError('Cannot found source language.')

        return language_code
        

    def get_text_from_image(self, file, lang_code=''):
        ImageReader = download_loader("ImageReader")
        
        if lang_code == '':
            loader = ImageReader(text_type = "plain_text")
        else:
            loader = ImageReader(text_type = "plain_text", model_kwargs=dict(lang=lang_code))

        docs = loader.load_data(file=file)

        return docs
        
    
    def load(self, file):
        image_file = self.preprocess_image(file)
        docs_unstructured = self.get_text_from_image(image_file)
        lang_code = self.get_language_code(docs_unstructured)
        docs_structured = self.get_text_from_image(image_file, lang_code)
        
        docs = [d.to_langchain_format() for d in docs_structured]
        return docs
        