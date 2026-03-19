import datetime
from django.utils import timezone
from django.test import TestCase, SimpleTestCase, TransactionTestCase, LiveServerTestCase
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for past, positive for future).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        q = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [q])

    def test_two_past_questions(self):
        q1 = create_question(question_text="Past question 1.", days=-30)
        q2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [q2, q1])


class SimpleExampleTest(SimpleTestCase):
    def test_math(self):
        self.assertEqual(2 + 2, 4)


class TransactionExampleTest(TransactionTestCase):
    def test_database_write(self):
        Question.objects.create(question_text="Transaction Test", pub_date=timezone.now())
        self.assertEqual(Question.objects.count(), 1)


class LiveServerExampleTest(LiveServerTestCase):
    def test_homepage(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)