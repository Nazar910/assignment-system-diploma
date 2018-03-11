from django.test import TestCase
from django.utils.encoding import smart_text
from assignment_system.models import Assignee
import time


class AssigneeCyrillicTestCase(TestCase):
    def test_when_name_is_in_cyrilic(self):
        Assignee.objects.create(
            name="Іван",
            patronymic="Іванович",
            last_name="Іванченко",
            email="ivan.ivanchenko@gmail.com"
        )

        assignee = Assignee.objects.get(name="Іван")
        self.assertEqual(assignee.name, "Іван")
        self.assertEqual(assignee.last_name, "Іванченко")
        self.assertEqual(assignee.email, "ivan.ivanchenko@gmail.com")
