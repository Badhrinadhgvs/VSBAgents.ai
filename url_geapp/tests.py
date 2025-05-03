from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import DynamicPage
from unittest.mock import patch
import uuid

class DynamicPageModelTest(TestCase):
    def setUp(self):
        self.page = DynamicPage.objects.create(
            name="Test Page",
            description="Test Description",
            api_key="gsk_test_api_key",
            keywords="test, page"
        )

    def test_dynamic_page_creation(self):
        """Test that DynamicPage is created with correct fields."""
        self.assertEqual(self.page.name, "Test Page")
        self.assertEqual(self.page.description, "Test Description")
        self.assertEqual(self.page.api_key, "gsk_test_api_key")
        self.assertEqual(self.page.keywords, "test, page")
        self.assertTrue(isinstance(self.page.slug, str))
        try:
            uuid.UUID(self.page.slug)
        except ValueError:
            self.fail("Slug is not a valid UUID")

    def test_dynamic_page_str(self):
        """Test the __str__ method of DynamicPage."""
        self.assertEqual(str(self.page), "Test Page")

class UrlGeappViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.page = DynamicPage.objects.create(
            name="Test Page",
            description="Test Description",
            api_key="gsk_test_api_key",
            keywords="test, page"
        )

    def test_home_view_get(self):
        """Test home view renders home.html on GET request."""
        response = self.client.get(reverse('url_geapp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Create a New Dynamic Page')

    @patch('url_geapp.views.verify_groq_api_key')
    def test_home_view_post_valid(self, mock_verify):
        """Test home view creates page and redirects on valid POST."""
        mock_verify.return_value = True
        data = {
            'name': 'New Page',
            'description': 'New Description',
            'api_key': 'gsk_new_api_key',
            'keywords': 'new, page'
        }
        response = self.client.post(reverse('url_geapp:home'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        page = DynamicPage.objects.get(name='New Page')
        self.assertEqual(page.description, 'New Description')
        self.assertRedirects(response, reverse('url_geapp:success', args=[page.slug]))

    @patch('url_geapp.views.verify_groq_api_key')
    def test_home_view_post_invalid_api_key(self, mock_verify):
        """Test home view shows error on invalid API key."""
        mock_verify.return_value = False
        data = {
            'name': 'Invalid Page',
            'description': 'Invalid Description',
            'api_key': 'invalid_key',
            'keywords': 'invalid, page'
        }
        response = self.client.post(reverse('url_geapp:home'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid Groq API key. Please provide a valid key.")
        self.assertContains(response, 'Invalid Page')  # Form data preserved

    def test_success_view(self):
        """Test success view renders success.html with page data."""
        response = self.client.get(reverse('url_geapp:success', args=[self.page.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')
        self.assertContains(response, 'URL Generated Successfully')
        self.assertContains(response, self.page.name)

    def test_dynamic_page_view(self):
        """Test dynamic_page view renders dynamic_page.html with chat interface."""
        response = self.client.get(reverse('url_geapp:dynamic_page', args=[self.page.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dynamic_page.html')
        self.assertContains(response, self.page.name)
        self.assertContains(response, 'chat-container')
        self.assertContains(response, 'typing-container')

    @patch('url_geapp.views.Agent')
    def test_chat_view_post_valid(self, mock_agent):
        """Test chat view returns AI response on valid POST."""
        mock_agent_instance = mock_agent.return_value
        mock_agent_instance.run.return_value.content = "AI Response"
        data = {'message': 'Hello'}
        response = self.client.post(
            reverse('url_geapp:chat', args=[self.page.slug]),
            data,
            content_type='application/x-www-form-urlencoded',
            HTTP_X_CSRFTOKEN='test_csrf_token'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'response': 'AI Response'})

    def test_chat_view_post_empty_message(self):
        """Test chat view returns error on empty message."""
        response = self.client.post(
            reverse('url_geapp:chat', args=[self.page.slug]),
            {},
            content_type='application/x-www-form-urlencoded',
            HTTP_X_CSRFTOKEN='test_csrf_token'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'No message provided'})

    def test_chat_view_get(self):
        """Test chat view returns error on GET request."""
        response = self.client.get(reverse('url_geapp:chat', args=[self.page.slug]))
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {'error': 'Invalid request method'})