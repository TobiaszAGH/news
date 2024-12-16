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
from data_visualization import generate_graph_html

class TestGraphHTML(unittest.TestCase):
    def setUp(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

    def tearDown(self):
        #self.driver.quit()
        pass

    def generate_html_fixture(self, data_dict, days):
        """Fixture generująca HTML wykresu dla różnych danych wejściowych."""
        return generate_graph_html(data_dict, days)

    def test_graph_rendering(self):
        # Przykładowe dane wejściowe
        data = {
            "x": [1, 2, 3, 4, 5],
            "y": [10, 15, 20, 25, 30],
            "label": ["X Axis", "Y Axis"],
            "name": ["Series 1"],
            "index_y2": [0]
        }
        html = self.generate_html_fixture(data, days=5)
        self.driver.get("data:text/html;charset=utf-8," + html)
        try:
            graph_element = self.driver.find_element(By.CLASS_NAME, "plotly-graph-div")
            self.assertIsNotNone(graph_element, "Wykres nie został poprawnie wyrenderowany.")
        except Exception as e:
            self.fail(f"Błąd podczas sprawdzania wykresu: {e}")

   

    def test_empty_data(self):
        # Puste dane wejściowe
        data = {
            "x": [],
            "y": [],
            "label": [],
            "name": [],
            "index_y2": []
        }
        html = self.generate_html_fixture(data, days=5)

        # Załaduj wygenerowany HTML do przeglądarki
        self.driver.get("data:text/html;charset=utf-8," + html)

        # Sprawdź, czy komunikat o błędzie jest widoczny
        try:
            error_message = self.driver.find_element(By.TAG_NAME, "h2").text
            self.assertIn("Błąd: Nieprawidłowe dane", error_message, "Nie wyświetlono oczekiwanego komunikatu o błędzie.")
        except Exception as e:
            self.fail(f"Błąd podczas sprawdzania obsługi pustych danych: {e}")


    def test_multiple_series_data_correctness(self):
        data = {
            "x": [1, 2, 3, 4, 5],
            "y": [[10, 15, 20, 25, 30], [5, 10, 15, 20, 25]],
            "label": ["X Axis", "Y Axis"],
            "name": ["Series 1", "Series 2"],
            "index_y2": [0, 0]
        }
        html = self.generate_html_fixture(data, days=5)
        self.driver.get("data:text/html;charset=utf-8," + html)

        try:
            plotly_data = self.driver.execute_script("""
                let rects = document.querySelectorAll('.xy rect');
                let data = [];
                rects.forEach(rect => {
                    data.push({
                        x: rect.getAttribute('x'),
                        y: rect.getAttribute('y'),
                        width: rect.getAttribute('width'),
                        height: rect.getAttribute('height')
                    });
                });
                return data;
            """)

            for i, series in enumerate(plotly_data):
                self.assertListEqual(series['x'], data['x'], f"Dane osi X dla serii {i+1} nie są zgodne.")
                self.assertListEqual(series['y'], data['y'][i], f"Dane osi Y dla serii {i+1} nie są zgodne.")
                self.assertEqual(series['name'], data['name'][i], f"Nazwa serii {i+1} nie jest zgodna.")

        except Exception as e:
            self.fail(f"Błąd podczas sprawdzania danych wykresu z wieloma seriami: {e}")


if __name__ == "__main__":
    unittest.main()
