from django.test import TestCase
from django.core.exceptions import ValidationError
from assignment_system.models import Assignee


class AssigneeTestCase(TestCase):
    def test_when_valid_props_success(self):
        Assignee.objects.create(
            name="John",
            last_name="Doe",
            email="john.doe@gmail.com"
        )

        assignee = Assignee.objects.get(name="John")
        self.assertEqual(assignee.name, "John")
        self.assertEqual(assignee.last_name, "Doe")
        self.assertEqual(assignee.email, "john.doe@gmail.com")
        self.assertEqual(assignee.role, Assignee.JUST_ASSIGNEE)

    def test_when_name_is_longer_than_30_should_fail(self):
        with self.assertRaises(Exception) as cm:
            Assignee.objects.create(
                name="JohnJohnJohnJohnJohnJohnJohnJohn",
                last_name="Doe",
                email="john.doe@gmail.com"
            )
        e = cm.exception
        self.assertEqual(
            e.args[1],
            "Data too long for column 'name' at row 1"
        )

    def test_when_last_name_is_longer_than_30_should_fail(self):
        with self.assertRaises(Exception) as cm:
            Assignee.objects.create(
                name="John",
                last_name="DoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoe",
                email="john.doe@gmail.com"
            )
        e = cm.exception
        self.assertEqual(
            e.args[1],
            "Data too long for column 'last_name' at row 1"
        )

    def test_when_email_is_not_valid_email_should_fail(self):
        a = Assignee(
            name="John",
            last_name="Doe",
            email="john"
        )
        with self.assertRaises(ValidationError) as cm:
            a.full_clean()
        e = cm.exception
        self.assertEqual(
            e.message_dict['email'][0],
            "Enter a valid email address."
        )
