from datetime import datetime
from blueprints.sport.routes import fetch_and_save_articles, SPORT_API
from blueprints.sport.models import SportArticle
from config import db

def test_sport_home(client):
    # Testuje, czy endpoint sport_home działa poprawnie.
    response = client.get('/sport/')
    assert response.status_code == 200
    assert b'Narciarskie' in response.data  # Zakłada obecność sportów w widoku.

def test_sport_home_with_discipline(crime_client):
    with crime_client.application.app_context():
    # Dodaje przykładowy artykuł dla wybranej dyscypliny i testuje filtrację.
        article = SportArticle(
            title="Test Football Article",
            description="Test Description",
            image_url="test.jpg",
            pubDate=datetime.now(),
            link="test.com",
            sport_type="football"
        )
        db.session.add(article)
        db.session.commit()

    response = crime_client.get('/sport/?discipline=football')
    assert response.status_code == 200
    assert b'Test Football Article' in response.data
    assert db.session.query(SportArticle).count() == 1

def test_sport_preview(crime_client):
    with crime_client.application.app_context():
        # Dodaje przykładowe artykuły dla każdej dyscypliny i testuje widok podglądu.
        disciplines = ['football', 'tennis', 'ski_jumping', 'volleyball']
        for discipline in disciplines:
            article = SportArticle(
                title=f"Test {discipline} Article",
                description=f"Test {discipline} Description",
                image_url="test.jpg",
                pubDate=datetime.now(),
                link="test.com",
                sport_type=discipline
            )
            db.session.add(article)
        db.session.commit()

        response = crime_client.get('/sport/sport_preview')
        assert response.status_code == 200
        for discipline in disciplines:
            assert f"Test {discipline} Article".encode() in response.data


# def test_sport_home_pagination(crime_client):
#     with crime_client.application.app_context():
#         # Dodaje więcej artykułów, aby przetestować paginację.
#         for i in range(15):
#             article = SportArticle(
#                 title=f"Test Article {i}",
#                 description=f"Test Description {i}",
#                 image_url="test.jpg",
#                 pubDate=datetime.now(),
#                 link=f"test.com/{i}",
#                 sport_type="football"
#             )
#             db.session.add(article)
#         db.session.commit()

#         response = crime_client.get('/sport/?page=2')
#         assert response.status_code == 200
#         assert b"Article 0" not in response.data  # Pierwsza strona powinna być pominięta.
#         assert b"Article 7" in response.data  # Powinny być artykuły z drugiej strony.
        
# def test_fetch_and_save_articles(crime_client, mocked_responses):
#     with crime_client.application.app_context():
#         # Mockuje odpowiedzi API dla sportowych endpointów i sprawdza zapisywanie danych w bazie.
#         mock_data = {
#             "results": [{
#                 "title": "Test Sport Article",
#                 "description": "Test Description",
#                 "image_url": "test.jpg",
#                 "pubDate": "2023-12-25 12:00:00",
#                 "link": "test.com"
#             }]
#         }

#         for url in SPORT_API.values():
#             mocked_responses.get(url, json=mock_data)
            
        
#         fetch_and_save_articles()

#         articles = SportArticle.query.all()
#         assert articles[0].title == "Test Sport Article"
#         assert articles[0].description == "Test Description"
#         assert articles[0].sport_type in SPORT_API.keys()
#         assert len(articles) > 0
