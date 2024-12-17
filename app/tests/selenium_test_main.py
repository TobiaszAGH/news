import unittest
import sys
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

current_dir = os.path.dirname(os.path.abspath(__file__))
app_folder = os.path.join(current_dir, '..') 
sys.path.append(os.path.abspath(app_folder))

class TestGraphHTML(unittest.TestCase):
    def setUp(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

    def testThemeChange(self):
        print("DUPA")

if __name__ == "__main__":
    unittest.main()
