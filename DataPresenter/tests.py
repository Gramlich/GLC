from django.urls import reverse, resolve
from django.test import TestCase
from .views import home, data, graph


class HomeTests(TestCase):

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/home/')
        self.assertEquals(view.func, home)

    def test_no_url_redirects_to_home_view(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/home/')


class DataTests(TestCase):

    def test_data_view_status_code(self):
        url = reverse('data')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_data_url_resolves_data_view(self):
        view = resolve('/data/')
        self.assertEquals(view.func, data)


class GraphTests(TestCase):

    def test_graph_view_status_code(self):
        url = reverse('graph')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_graph_url_resolves_graph_view(self):
        view = resolve('/graph/')
        self.assertEquals(view.func, graph)
