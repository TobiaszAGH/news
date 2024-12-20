import unittest
import sys
import os
import tempfile

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
        #options.add_argument("--headless") 
        options.add_argument("--disable-gpu")
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=options)

    @classmethod
    def tearDownClass(cls):
        """Zamykanie przeglądarki po zakończeniu testów."""
        #cls.driver.quit()
        pass

    def render_and_verify_graph(self, data, days):
        """Pomocnicza funkcja do renderowania i weryfikacji wykresu."""
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

        return html

    def test_wykres_renderowanie(self):
        """Test sprawdzający, czy wykres renderuje się poprawnie i dane są zgodne."""
        data = {
            "x": [1, 2, 3, 4, 5],
            "y": [[10, 15, 20, 25, 30], [5, 10, 15, 20, 25]],
            "label": ["X Axis", "Y Axis", "Secondary Y Axis"],
            "name": ["Series 1", "Series 2"],
            "index_y2": [0, 1]
        }
        days = 5
        self.render_and_verify_graph(data, days)

        graph_div = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "plot-container"))
        )
        self.assertIsNotNone(graph_div, "Nie znaleziono kontenera wykresu.")

        points = self.driver.find_elements(By.CSS_SELECTOR, '.point')
        self.assertGreater(len(points), 0, "Brak punktów danych na wykresie.")

    def test_empty_data(self):
        """Test dla pustych danych."""
        data = {
            "x": [],
            "y": [],
            "label": [],
            "name": [],
            "index_y2": []
        }
        days = 0
        self.render_and_verify_graph(data, days)

        error_message = self.driver.find_element(By.TAG_NAME, "h2").text
        self.assertEqual(error_message, "Błąd: Nieprawidłowe dane", "Nie wyświetlono oczekiwanego komunikatu o błędzie.")

    def test_incomplete_data(self):
        """Test dla niepełnych danych."""
        data = {
            "x": [1, 2, 3],
            "y": [[10, 15], [5]],
            "label": ["X Axis", "Y Axis"],
            "name": ["Series 1"],
            "index_y2": []
        }
        days = 3
        self.render_and_verify_graph(data, days)

        error_message = self.driver.find_element(By.TAG_NAME, "h2").text
        self.assertEqual(error_message, "Błąd: Nieprawidłowe dane", "Nie wyświetlono oczekiwanego komunikatu o błędzie.")

    def test_uneven_data_lengths(self):
        """Test dla danych z nierównymi długościami list."""
        data = {
            "x": [1, 2, 3, 4, 5, 6],
            "y": [[10, 15, 20, 25], [5, 10, 15]],
            "label": ["X Axis", "Y Axis"],
            "name": ["Series 1", "Series 2"],
            "index_y2": []
        }
        days = 6
        self.render_and_verify_graph(data, days)

        error_message = self.driver.find_element(By.TAG_NAME, "h2").text
        self.assertEqual(error_message, "Błąd: Nieprawidłowe dane", "Nie wyświetlono oczekiwanego komunikatu o błędzie.")

if __name__ == "__main__":
    unittest.main()
