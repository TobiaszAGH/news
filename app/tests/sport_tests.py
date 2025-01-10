import unittest
from flask import Flask, url_for
from flask_testing import TestCase
from app import create_app, db
from app.blueprints.sport.models import SportArticle
from datetime import datetime

# Konfiguracja aplikacji testowej
class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app('testing')  # Użycie konfiguracji testowej
        return app

    def setUp(self):
        db.create_all()
        self.populate_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def populate_test_data(self):
        """Dodanie przykładowych danych do testów."""
        articles = [
            SportArticle(
                title="Football News 1",
                description="Description of football news 1",
                image_url="http://example.com/image1.jpg",
                pubDate=datetime(2024, 1, 10, 10, 0),
                link="http://example.com/football1",
                sport_type="football"
            ),
            SportArticle(
                title="Tennis News 1",
                description="Description of tennis news 1",
                image_url="http://example.com/image2.jpg",
                pubDate=datetime(2024, 1, 9, 10, 0),
                link="http://example.com/tennis1",
                sport_type="tennis"
            ),
        ]
        db.session.bulk_save_objects(articles)
        db.session.commit()

# Testy jednostkowe
class UnitTests(unittest.TestCase):
    def test_sport_article_model(self):
        """Test poprawności modelu SportArticle."""
        article = SportArticle(
            title="Test Article",
            description="Test Description",
            image_url="http://example.com/image.jpg",
            pubDate=datetime(2024, 1, 1, 12, 0),
            link="http://example.com/article",
            sport_type="football"
        )
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.sport_type, "football")
        self.assertIsNotNone(article.created_at)

# Testy integracyjne
class IntegrationTests(BaseTestCase):
    def test_home_page(self):
        """Test dostępności strony głównej sekcji sportowej."""
        response = self.client.get(url_for('sport.sport_home'))
        self.assert200(response)
        self.assertTemplateUsed('sport.html')

    def test_filter_by_discipline(self):
        """Test filtrowania artykułów według dyscypliny."""
        response = self.client.get(url_for('sport.sport_home', discipline='football'))
        self.assert200(response)
        self.assertIn(b"Football News 1", response.data)

    def test_pagination(self):
        """Test paginacji na stronie głównej."""
        response = self.client.get(url_for('sport.sport_home', page=1))
        self.assert200(response)
        self.assertIn(b"Football News 1", response.data)
        self.assertIn(b"Tennis News 1", response.data)

    def test_sport_preview(self):
        """Test widoku podglądu dyscyplin sportowych."""
        response = self.client.get(url_for('sport.sport_preview'))
        self.assert200(response)
        self.assertTemplateUsed('sport_preview.html')
        self.assertIn(b"Football News 1", response.data)

    def test_fetch_and_save_articles(self):
        """Test funkcji fetch_and_save_articles."""
        with self.client:
            from app.blueprints.sport.routes import fetch_and_save_articles
            fetch_and_save_articles()
            article_count = SportArticle.query.count()
            self.assertGreater(article_count, 2)  # Nowe artykuły zostały dodane

if __name__ == '__main__':
    unittest.main()
