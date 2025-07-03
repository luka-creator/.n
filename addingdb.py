import sys 
import random
from pymongo import MongoClient
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



client = MongoClient("mongodb://localhost:27017")
db = client["forquiz"]
collection=db["students"]


points = [str(i) for i in range(101)]
ch = random.choice

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("forquiz")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.add_btn = QPushButton("Add all records")
        self.search_btn = QPushButton("Search")
        self.update_btn = QPushButton("Update")
        self.remove_btn = QPushButton("Remove ")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("type to search")


        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addWidget(self.add_btn)
        layout.addWidget(QLabel("search somehting:"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.remove_btn)
        layout.addWidget(QLabel("output:"))
        layout.addWidget(self.output)

        self.setLayout(layout)

        self.add_btn.clicked.connect(self.add_records)
        self.search_btn.clicked.connect(self.search_records)
        self.update_btn.clicked.connect(self.update_records)
        self.remove_btn.clicked.connect(self.remove_records)


    def add_records(self):
        self.output.clear()
        for _ in range(10):
            record = {
                "last_name": ch(LNames),
                "first_name": ch(FNames),
                "subject": ch(Subject),
                "score": ch(points)
            }
            result = collection.insert_one(record)
            self.output.append(f"added: {record} id: {result.inserted_id}")

    
        
    def search_records(self):
        word = self.search_input.text()
        self.output.clear()

        if word == "":
            self.output.setText("enter search.")
            return

        results = collection.find()
        found = False
        for answer in results:
            if word in answer.get("first_name", "") or word in answer.get("last_name", "") or word in answer.get("subject", "") or word in answer.get("score", ""):
                self.output.append(str(answer))
                found=True

        if not found:
            self.output.setText("name not found")

    
    
    def update_records(self):
        word = self.search_input.text().strip()
        self.output.clear()

        if word == "":
            self.output.setText("Enter a value to update.")
            return

        results = collection.find()
        updated = False
        for result in results:
            if word in result.get("first_name", "") or word in result.get("last_name", "") or word in result.get("subject", "") or word in result.get("score", ""):
                new_score = ch(points)
                collection.update_one({"_id": result["_id"]}, {"$set": {"score": new_score}})
                self.output.append(f"Updated score for {result['first_name']} {result['last_name']} to {new_score}")
                updated = True

        if not updated:
            self.output.setText("No matching records found to update.")

    
    def remove_records(self):
        word = self.search_input.text().strip()
        self.output.clear()

        if word == "":
            self.output.setText("Enter a value to delete.")
            return

        results = collection.find()
        deleted = False
        for result in results:
            if word in result.get("first_name", "") or word in result.get("last_name", "") or word in result.get("subject", "") or word in result.get("score", ""):
                collection.delete_one({"_id": result["_id"]})
                self.output.append(f"Deleted: {result['first_name']} {result['last_name']} - {result['subject']}, {result['score']}")
                deleted = True

        if not deleted:
            self.output.setText("No matching records found")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
