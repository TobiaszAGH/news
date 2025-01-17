from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# Ustawienia dla przeglądarki Chrome i sterownika
options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Test dla strony głównej artykułów
def test_news_home():
    url = "http://news.tobiasz.xyz/news"  # Adres URL strony z artykułami
    driver.get(url)  # Otwiera stronę w przeglądarce
    
    # Pobiera listę artykułów na stronie
    articles = driver.find_elements(By.CSS_SELECTOR, "table tr")
    initial_articles = [article.text for article in articles]
    print(f"Znaleziono {len(articles)} artykułów na pierwszej stronie")
    
    # Przechodzi do następnej strony z artykułami
    next_page = driver.find_element(By.XPATH, "//a[contains(text(), 'Następna')]")
    driver.execute_script("arguments[0].scrollIntoView();", next_page)  # Przewija stronę do przycisku
    time.sleep(1)  # Czeka na załadowanie strony
    next_page.click()  # Kliknięcie przycisku "Następna"
    time.sleep(1)  # Czeka na przejście
    
    # Pobiera listę artykułów na nowej stronie i porównuje z poprzednią
    new_articles = driver.find_elements(By.CSS_SELECTOR, "table tr")
    assert [article.text for article in new_articles] != initial_articles, "Artykuły nie zmieniły się po przejściu na następną stronę!"

# Test dla podglądu wiadomości w widżecie karuzeli
def test_news_preview():
    url = "http://news.tobiasz.xyz/news/news_preview"  # Adres URL podglądu wiadomości
    driver.get(url)
    
    # Pobiera elementy karuzeli
    carousel_items = driver.find_elements(By.CLASS_NAME, "carousel-item")
    assert len(carousel_items) > 0, "Nie znaleziono elementów karuzeli!"
    print(f"Znaleziono {len(carousel_items)} elementów karuzeli")
    
    # Sprawdza, czy karuzela zmienia slajd po kliknięciu strzałki
    initial_caption = driver.find_element(By.CLASS_NAME, "carousel-caption").text
    
    next_button = driver.find_element(By.CLASS_NAME, "carousel-control-next")
    next_button.click()
    time.sleep(1)
    
    next_caption = driver.find_element(By.CLASS_NAME, "carousel-caption").text
    assert next_caption != initial_caption, "Karuzela nie przesunęła się po kliknięciu strzałki w prawo!"
    
    # Weryfikuje, czy karuzela wraca do poprzedniego slajdu
    prev_button = driver.find_element(By.CLASS_NAME, "carousel-control-prev")
    prev_button.click()
    time.sleep(1)
    
    prev_caption = driver.find_element(By.CLASS_NAME, "carousel-caption").text
    assert prev_caption == initial_caption, "Karuzela nie wróciła do poprzedniego slajdu!"

# Test dla podglądu wiadomości na stronie głównej
def test_main_page_news_preview():
    url = "http://news.tobiasz.xyz"  # Adres URL strony głównej
    driver.get(url)
    
    # Przełącza się do ramki iframe zawierającej karuzelę wiadomości
    news_frame = driver.find_element(By.CLASS_NAME, "iframe-news")
    driver.switch_to.frame(news_frame)
    
    # Sprawdza, czy karuzela na stronie głównej zawiera elementy
    carousel_items = driver.find_elements(By.CLASS_NAME, "carousel-item")
    assert len(carousel_items) > 0, "Nie znaleziono elementów karuzeli na stronie głównej!"
    print(f"Znaleziono {len(carousel_items)} elementów karuzeli na stronie głównej")

# Test dla szczegółowego widoku artykułu z powrotem do listy artykułów
def test_single_news_with_return():
    url = "http://news.tobiasz.xyz/news"  # Adres URL listy artykułów
    driver.get(url)
    
    # Otwiera szczegóły pierwszego artykułu z listy
    first_article = driver.find_element(By.CSS_SELECTOR, "td.summary a")
    article_title = first_article.text
    first_article.click()
    time.sleep(1)
    
    # Sprawdza, czy wyświetlane są tytuł i treść artykułu
    news_title = driver.find_element(By.CLASS_NAME, "news-title")
    news_content = driver.find_element(By.CLASS_NAME, "news-content")
    assert news_title.is_displayed() and news_content.is_displayed(), "Treść artykułu nie została wyświetlona!"
    print(f"Pomyślnie otworzono artykuł: {article_title}")

    # Wraca do listy artykułów i sprawdza, czy lista jest widoczna
    return_button = driver.find_element(By.CLASS_NAME, "sticky-back-button")
    return_button.click()
    time.sleep(1)
    
    articles_table = driver.find_element(By.TAG_NAME, "table")
    assert articles_table.is_displayed(), "Nie wrócono do strony z listą artykułów!"

    # Kończy pracę z przeglądarką
    driver.quit()
