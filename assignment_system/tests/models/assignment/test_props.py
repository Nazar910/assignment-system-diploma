from django.test import TestCase
from assignment_system.models import Assignment, Assignee
from datetime import datetime
import pytz


class AssignmentTestCase(TestCase):
    assignee = None

    def setUp(self):
        self.assignee = Assignee(
            name="John",
            last_name="Doe",
            email="john.doe@gmail.com"
        )
        self.assignee.save()

    def test_assignment_has_correct_props(self):
        title = "Some important assignment"
        description = "Description of important assignment"

        now = datetime.now(tz=pytz.utc)
        assigned_at = now
        started_at = now
        finished_at = now

        stored_assignment = Assignment(
            title=title,
            description=description,
            assigned_at=assigned_at,
        )
        stored_assignment.save()
        stored_assignment.assignees.add(self.assignee)

        assignment = Assignment.objects.get(title=title)

        self.assertEqual(assignment.title, title)
        self.assertEqual(assignment.description, description)
        self.assertEqual(assignment.priority_level, Assignment.LOW_PRIORITY)
        self.assertIn(self.assignee, assignment.assignees.all())
        self.assertEqual(assignment.assigned_at, assigned_at)
