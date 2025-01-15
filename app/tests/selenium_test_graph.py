import unittest
import sys
import os
import tempfile
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

current_dir = os.path.dirname(os.path.abspath(__file__))
app_folder = os.path.join(current_dir, '..')
sys.path.append(os.path.abspath(app_folder))
from data_visualization import generate_graph_html

class TestWykresRenderowanie(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Konfiguracja Selenium i uruchomienie przeglądarki."""
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=options)

    @classmethod
    def tearDownClass(cls):
        """Zamykanie przeglądarki po zakończeniu testów."""
        cls.driver.quit()

    def render_and_verify_graph(self, data, days):
        """Pomocnicza funkcja do renderowania wykresu."""
        html = f'''
            <html>
            <head>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            </head>
            <body>
            {generate_graph_html(data, days)}
            </body>
            </html>
        '''
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(html)
            temp_file_path = temp_file.name

        self.driver.get(f"file://{temp_file_path}")

        # Czekaj na załadowanie wykresu
        WebDriverWait(self.driver, 4).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'plotly'))
        )


    def test_renderowanie_wykresu(self):
        """Test renderowania wykresu."""
        data =  {"x": ["2024-09-15", "2024-09-16", "2024-09-17", "2024-09-18", "2024-09-19"],
                "y": [[10, 15, 17, 26, 30], [15, 8, 6, 16, 32]],
                "label": ["X Axis", "Y Axis", "Y2 Axis"],
                "name": ["Series 1", "Series 2"],
                "index_y2": [0, 1]}
        days = 5
        self.render_and_verify_graph(data, days)

        # Weryfikacja, czy wykres jest widoczny
        plotly_div = self.driver.find_element(By.CLASS_NAME, 'plotly')
        self.assertTrue(plotly_div.is_displayed())

    def test_sprawdzenie_punktów(self):
        """Test renderowania wykresu."""
        data = {
            "x": ["2024-09-15", "2024-09-16", "2024-09-17", "2024-09-18", "2024-09-19"],
            "y": [[10, 15, 17, 26, 30], [15, 8, 6, 16, 32]],
            "label": ["X Axis", "Y Axis", "Y2 Axis"],
            "name": ["Series 1", "Series 2"],
            "index_y2": [0, 0]
        }
        days = 5
        self.render_and_verify_graph(data, days)

        # Weryfikacja, czy wykres jest widoczny
        plotly_div = self.driver.find_element(By.CLASS_NAME, 'plotly')
        self.assertTrue(plotly_div.is_displayed())

        # Pobranie punktów z wykresu
        points = self.driver.find_elements(By.CSS_SELECTOR, '.point')

        # Sprawdzenie liczby punktów
        expected_points_count = len(data["x"]) * len(data["y"])
        self.assertEqual(len(points), expected_points_count)


if __name__ == "__main__":
    unittest.main()