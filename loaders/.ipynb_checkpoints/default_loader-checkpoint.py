from loaders.file_loader import FileLoader

class DefaultLoader(FileLoader):
    def load(self, file_path):
        print(f"Unsupported file type: {file_path}")