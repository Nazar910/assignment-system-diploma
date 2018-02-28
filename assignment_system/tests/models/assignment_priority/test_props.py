from django.test import TestCase
from assignment_system.models import AssignmentPriority


class AssignmentPriorityTestCase(TestCase):
    def test_assignment_priority_has_correct_props(self):
        AssignmentPriority.objects.create()

        assignee = AssignmentPriority.objects.get(level=AssignmentPriority.LOW)
        self.assertEqual(assignee.level, "l")
