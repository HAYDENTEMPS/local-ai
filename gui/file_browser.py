from PySide6.QtWidgets import QFileSystemModel, QTreeView
from PySide6.QtCore import QModelIndex
import os

# Dynamically detect workspace directory (one level up from gui folder)
WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class FileBrowser(QTreeView):
    def __init__(self):
        super().__init__()

        self.model = QFileSystemModel()
        self.model.setRootPath(WORKSPACE)

        self.setModel(self.model)
        self.setRootIndex(self.model.index(WORKSPACE))
        self.setColumnWidth(0, 250)
        self.setHeaderHidden(True)
