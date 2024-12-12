import pytest
from plotly.graph_objects import Figure
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_visualization import generate_graph_html

def test_generate_graph_html_valid_data():
    data_dict = {
        "x": ["Day 1", "Day 2", "Day 3"],
        "y": [[10, 20, 30], [5, 15, 25]],
        "label": ["Days", "Temperature", "Humidity"],
        "name": ["Temperature", "Humidity"],
        "index_y2": [0, 1],
    }
    days = 3
    html = generate_graph_html(data_dict, days)
    assert "<div" in html 
    assert "plotly" in html  
    assert "Temperature" in html  
    assert "Humidity" in html  


def test_generate_graph_html_missing_x_key():
    data_dict = {
        "y": [[10, 20, 30]],
        "label": ["Days", "Values"],
        "name": ["Data Series"],
        "index_y2": [0],
    }
    days = 3
    html = generate_graph_html(data_dict, days)
    assert "<h2>Błąd: Nieprawidłowe dane</h2>" in html


def test_generate_graph_html_missing_y_key():
    data_dict = {
        "x": ["Day 1", "Day 2", "Day 3"],
        "label": ["Days", "Values"],
        "name": ["Data Series"],
        "index_y2": [0],
    }
    days = 3
    html = generate_graph_html(data_dict, days)
    assert "<h2>Błąd: Nieprawidłowe dane</h2>" in html


def test_generate_graph_html_empty_y():
    data_dict = {
        "x": ["Day 1", "Day 2", "Day 3"],
        "y": [],
        "label": ["Days", "Values"],
        "name": [],
        "index_y2": [],
    }
    days = 3
    html = generate_graph_html(data_dict, days)
    assert "<h2>Błąd: Nieprawidłowe dane</h2>" in html


def test_generate_graph_html_wrong_y():
    data_dict = {
        "x": ["Day 1", "Day 2", "Day 3"],
        "y": ["auto", "rower"],
        "label": ["Days"],
        "name": ["name"],
        "index_y2": ["name"],
    }
    days = 3
    html = generate_graph_html(data_dict, days)
    assert "<h2>Błąd: Nieprawidłowe dane</h2>" in html


def test_generate_graph_html_single_series():
    data_dict = {
        "x": ["Day 1", "Day 2", "Day 3"],
        "y": [[10, 20, 30]],
        "label": ["Days", "Values"],
        "name": ["Temperature"],
        "index_y2": [0],
    }
    days = 3
    html = generate_graph_html(data_dict, days)
    assert "Temperature" in html


def test_generate_graph_html_days_exceeding_data():
    data_dict = {
        "x": ["Day 1", "Day 2", "Day 3"],
        "y": [[10, 20, 30]],
        "label": ["Days", "Values"],
        "name": ["Temperature"],
        "index_y2": [0],
    }
    days = 5
    html = generate_graph_html(data_dict, days)
    assert "Temperature" in html
    assert "Day 1" in html
    assert "Day 3" in html

