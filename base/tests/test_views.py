from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from base.models import ElectionEvent, Candidate, Vote
from django.utils import timezone
from datetime import timedelta


class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.election_event = ElectionEvent.objects.create(
            type='Presidential',
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1)
        )
        self.candidate = Candidate.objects.create(
            name='John',
            surname='Doe',
            description='A candidate',
            id_election=self.election_event
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_all_elections_view(self):
        response = self.client.get(reverse('all_elections'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'elections/all_elections.html')

    def test_vote_view_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('vote', args=[self.election_event.id_election]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'elections/vote.html')

    def test_vote_view_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('vote', args=[self.election_event.id_election]), {
            'candidate': self.candidate.id_candidate
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('thank_you'))
        self.candidate.refresh_from_db()
        self.assertEqual(self.candidate.votes, 1)
        self.assertTrue(Vote.objects.filter(user=self.user, id_election=self.election_event).exists())

    def test_thank_you_view(self):
        response = self.client.get(reverse('thank_you'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'elections/thank_you.html')

    def test_election_results_view(self):
        response = self.client.get(reverse('election_results', args=[self.election_event.id_election]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'elections/results.html')

    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_view_post(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'email': 'newuser@example.com',
            'name': 'New',
            'last_name': 'User',
            'birth_date': '2000-01-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
