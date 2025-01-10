# Aplikacja webowa `news`

## Dokumentacja API 📖

### API Aplikacji

1. Endpoint: `/` 🎉✨🌟

**GET /** - **Opis**: Wyświetla stronę główną aplikacji.

- **Metoda HTTP**: GET
- **URL**: `/`
- **Parametry**: Brak
- **Przykład żądania**:
  ```http
  GET / HTTP/1.1
  Host: example.com
  ```

2. Endpoint: `/weather` 🌦️🌍☁️

**GET /weather** - **Opis**: Wyświetla stronę z aktualnymi danymi pogodowymi oraz prognozą dla domyślnego miasta (Kraków).

- **Metoda HTTP**: GET
- **URL**: `/weather`
- **Parametry**: Brak
- **Przykład żądania**:
  ```http
  GET /weather HTTP/1.1
  Host: example.com
  ```

3. Endpoint: `/weather/widget` 🌞🌀🌧️

**GET /weather/widget** - **Opis**: Wyświetla widget z informacjami o aktualnej pogodzie w wybranym mieście (Kraków).

- **Metoda HTTP**: GET
- **URL**: `/weather/widget`
- **Parametry**: Brak
- **Przykład żądania**:
  ```http
  GET /weather/widget HTTP/1.1
  Host: example.com
  ```

4. Endpoint: `/economy` 💵📈🌍

**GET /economy** - **Opis**: Wyświetla stronę z aktualnymi kursami wybranych walut (euro, dolar amerykański, frank szwajcarski).

- **Metoda HTTP**: GET
- **URL**: `/economy`
- **Parametry**: Brak
- **Przykład żądania**:
  ```http
  GET /economy HTTP/1.1
  Host: example.com
  ```

5. Endpoint: `/economy/economy_preview` 📊💶📉

**GET /economy/economy_preview** - **Opis**: Wyświetla widżet przedstawiający kursy wybranych walut (euro, dolar amerykański, frank szwajcarski).

- **Metoda HTTP**: GET
- **URL**: `/economy/economy_preview`
- **Parametry**: Brak
- **Przykład żądania**:
  ```http
  GET /economy/economy_preview HTTP/1.1
  Host: example.com
  ```

6. Endpoint: `/news` 📰🕵️‍♂️🚓

**GET /news** - **Opis**: Wyświetla informacje o najnowszych wydarzeniach związanych z kryminalistyką dla Krakowa.

- **Metoda HTTP**: GET
- **URL**: `/news`
- **Parametry**: Brak
- **Przykład żądania**:
  ```http
  GET /news HTTP/1.1
  Host: example.com
  ```

7. Endpoint: `/news/news_preview` 📜🔍📢

**GET /news/news_preview** - **Opis**: Wyświetla widżet pokazujący karuzelę z najnowszymi wiadomościami kryminalnymi dla Krakowa.

- **Metoda HTTP**: GET
- **URL**: `/news/news_preview`
- **Parametry**: Brak
- **Przykład żądania**:
  ```http
  GET /news/news_preview HTTP/1.1
  Host: example.com
  ```

8. Endpoint: `/sport` ⚽🏀🏋️‍♂️

**GET /sport** - **Opis**: Wyświetla stronę, na której znajdują się informacje o najnowszych wydarzeniach sportowych.

- **Metoda HTTP**: GET
- **URL**: `/sport`
- **Parametry**: Brak
- **Przykład żądania**:
  ```http
  GET /sport HTTP/1.1
  Host: example.com
  ```

9. Endpoint: `/sport/sport_preview` 🏆🏅🎾

**GET /sport/sport_preview** - **Opis**: Wyświetla widget z informacjami o najnowszych wydarzeniach sportowych.

- **Metoda HTTP**: GET
- **URL**: `/sport/sport_preview`
- **Parametry**: Brak
- **Przykład żądania**:
  ```http
  GET /sport/sport_preview HTTP/1.1
  Host: example.com
  ```

10. Endpoint: `/calendar/calendar_preview` 📅🎉🕰️

**GET /calendar/calendar_preview** - **Opis**: Wyświetla widżet pokazujący kartkę z kalendarza z informacjami dotyczącymi: daty, imienin, świąt, przysłów i aktualnymi wydarzeniami.

- **Metoda HTTP**: GET
- **URL**: `/calendar/calendar_preview`
- **Parametry**: Brak
- **Przykład żądania**:
  ```http
  GET /calendar/calendar_preview HTTP/1.1
  Host: example.com
  ```

### API Zewnętrzne

#### Sekcja sportowa 📰🏃‍♂️🌍

Dane o wydarzeniach sportowych pobierane są z API **Newsdata.io**:

- **Dokumentacja API**: [https://newsdata.io/](https://newsdata.io/)
- **Opis**: Używane do pobierania informacji o najnowszych wydarzeniach sportowych na świecie.
- **Przykładowe żądanie**:
  ```http
  GET https://newsdata.io/api/1/news?apikey=YOUR_API_KEY&category=sports
  Host: newsdata.io
  ```

#### Informacje pogodowe 🌦️🌡️🌐

Dane pogodowe pobierane są z API **OpenWeatherMap**:

- **Dokumentacja API**: [https://openweathermap.org/](https://openweathermap.org/)
- **Opis**: Używane do uzyskania aktualnych danych pogodowych oraz prognoz dla określonej lokalizacji.
- **Przykładowe żądanie**:
  ```http
  GET https://api.openweathermap.org/data/2.5/weather?q=Krakow&appid=YOUR_API_KEY
  Host: api.openweathermap.org
  ```
#### Informacje ekonomiczne 💰💸

Dane ekonomiczne pobierane są z API **NBP Web API**:

- **Dokumentacja API**: [https://api.nbp.pl/](https://api.nbp.pl/)
- **Opis**: Używane do uzyskania aktualnych danych walutowych oraz historycznych kursów walut
- **Przykładowe żądanie**:
 'https://api.nbp.pl/api/exchangerates/tables/{table}/last/{topCount}/'

'https://api.nbp.pl/api/exchangerates/rates/c/usd/today/'

#### Kartka z kalendarza 📖🕊️🎊

1. **Imieniny**:

   - **Źródło**: [Nameday API](https://nameday.abalin.net/docs/)
   - **Opis**: Pobierane informacje o imieninach w wybranym kraju i dniu.
   - **Przykładowe żądanie**:
     ```http
     GET https://nameday.abalin.net/api/V1/today?country=pl
     Host: nameday.abalin.net
     ```

2. **Święta**:
   - **Źródło**: [Kalendarz Świąt Nietypowych](https://github.com/pniedzwiedzinski/kalendarz-swiat-nietypowych)
   - **Opis**: Pobierane dane o nietypowych świętach przypadających na dany dzień.

#### Sekcja wiadomości kryminalnych 🚔🔎📰

Dane o najnowszych wydarzeniach kryminalnych są zbierane ze strony **Krakowskiej Policji**:

- **Źródło**: [https://krakow.policja.gov.pl/kr1/aktualnosci](https://krakow.policja.gov.pl/kr1/aktualnosci)
- **Opis**: Dane są pozyskiwane poprzez scraping, co umożliwia prezentację najnowszych informacji z regionu Krakowa.
- **Przykład pozyskiwanych danych**:
  - Tytuł artykułu
  - Data publikacji
  - Link do pełnej treści 🌟📌🔖
