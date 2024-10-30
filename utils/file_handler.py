import os
from pathlib import Path

class FileHandler:
    @staticmethod
    def get_docs_files():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        docs_dir = os.path.join(script_dir, '..', 'docs')

        pdf_files = []
        for filename in ['test.pdf', 'test2.pdf']:
            file_path = os.path.join(docs_dir, filename)
            if os.path.exists(file_path):
                pdf_files.append(file_path)
            else:
                raise FileNotFoundError(f"Файл {filename} не найден в папке docs/")

        return pdf_files
