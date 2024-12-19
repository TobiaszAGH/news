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

# Import funkcji generującej HTML wykresu
current_dir = os.path.dirname(os.path.abspath(__file__))
app_folder = os.path.join(current_dir, '..')
sys.path.append(os.path.abspath(app_folder))
from data_visualization import generate_graph_html

class TestWykresRenderowanie(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Konfiguracja Selenium i uruchomienie przeglądarki."""
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")  # Tryb bezgłowy (opcjonalnie)
        options.add_argument("--disable-gpu")
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=options)

    @classmethod
    def tearDownClass(cls):
        """Zamykanie przeglądarki po zakończeniu testów."""
        cls.driver.quit()

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

        # Generowanie HTML za pomocą funkcji
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
        print(html)


        # Zapisanie HTML do pliku tymczasowego
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(html)
            temp_file_path = temp_file.name

        print(f"HTML zapisany do pliku: {temp_file_path}")

        # Załaduj plik HTML w przeglądarce
        self.driver.get(f"file://{temp_file_path}")

        # Sprawdzenie, czy główny kontener wykresu istnieje
        graph_div = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "plot-container"))
        )
        self.assertIsNotNone(graph_div, "Nie znaleziono kontenera wykresu.")
        print("Wykres Plotly został poprawnie załadowany.")

        # Pobranie wszystkich punktów danych na wykresie
        points = self.driver.find_elements(By.CSS_SELECTOR, '.point')
        self.assertGreater(len(points), 0, "Brak punktów danych na wykresie.")
        print(f"Znaleziono {len(points)} punktów na wykresie.")

        # Pobranie danych ze wszystkich punktów za pomocą JavaScript
        all_points_data = self.driver.execute_script("""
            let points = document.querySelectorAll('.point');
            let data = [];
            points.forEach(point => {
                let d = point.__data__;
                data.push({x: d.x, y: d.y});
            });
            return data;
        """)

        # Sprawdzenie danych punktów z wykresu
        for index, point_data in enumerate(all_points_data):
            print(f"Point {index}: x={point_data['x']}, y={point_data['y']}")
            self.assertIsInstance(point_data['x'], (int, float), "Wartość x nie jest liczbą.")
            self.assertIsInstance(point_data['y'], (int, float), "Wartość y nie jest liczbą.")
            self.assertIn(point_data['y'], data["y"][0] + data["y"][1], "Nieprawidłowa wartość y.")

        # Opóźnienie dla wizualnej inspekcji (opcjonalne)
        time.sleep(3)

if __name__ == "__main__":
    unittest.main()
