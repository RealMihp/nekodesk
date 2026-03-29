import os

class FileScanner:
    @staticmethod
    def get_directory_structure(root_path):
        """Returns a list of folder contents"""
        try:
            return os.listdir(root_path)
        except PermissionError:
            return []
        
    