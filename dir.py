import os.path


current_file = os.path.abspath(__file__)  # E:\Desktop\qa_guru\selene\dir.py
current_dir = os.path.dirname(current_file)  # E:\Desktop\qa_guru\selene

TMP_DIR = os.path.join(current_dir, r"files\tmp")  # E:\Desktop\qa_guru\selene\files\tmp
