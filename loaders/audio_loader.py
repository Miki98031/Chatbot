from loaders.file_loader import FileLoader
from langchain.schema.document import Document
import io
import os
import numpy as np
try:
    import tensorflow  # required in Colab to avoid protobuf compatibility issues
except ImportError:
    pass
import torch
import pandas as pd
import urllib
import tarfile
import whisper
import torchaudio
from scipy.io import wavfile
from tqdm.notebook import tqdm
pd.options.display.max_rows = 100
pd.options.display.max_colwidth = 1000
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class AudioLoader(FileLoader):
    def load(self, file):
        model = whisper.load_model('medium')
        result = model.transcribe(file, task='translate')
        docs = []
        docs.append(Document(page_content=result['text'], metadata={"source": "local"}))
        return docs
