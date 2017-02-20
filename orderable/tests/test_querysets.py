from django.test import TestCase

from .models import Task


class TestOrderableQueryset(TestCase):
    def test_set_orders(self):
        """The sort_order values are rearranged effectively in-place."""
        task_1 = Task.objects.create(sort_order=4, pk=1)
        task_2 = Task.objects.create(sort_order=7, pk=2)

        Task.objects.set_orders([2, 1])

        task_1.refresh_from_db()
        task_2.refresh_from_db()
        self.assertEqual(task_1.sort_order, 7)
        self.assertEqual(task_2.sort_order, 4)

    def test_set_orders_wrong_pks(self):
        """
        When a pk is submitted that doesn't match an existing Task, we get a
        descriptive error message.
        """
        Task.objects.create(sort_order=1, pk=1)

        expected_msg = 'The following object_pks are not in this queryset: [2]'
        with self.assertRaises(TypeError, msg=expected_msg):
            Task.objects.set_orders([1, 2])

    def test_set_orders_subset(self):
        """
        When only some Tasks are mentioned in the object_pks list, they're swapped around
        and the others are unaffected.
        """
        task_1 = Task.objects.create(sort_order=1, pk=1)
        task_2 = Task.objects.create(sort_order=4, pk=2)
        task_3 = Task.objects.create(sort_order=5, pk=3)
        task_4 = Task.objects.create(sort_order=8, pk=4)

        Task.objects.set_orders([3, 2])

        self.assertSequenceEqual(Task.objects.all(), [task_1, task_3, task_2, task_4])
        self.assertSequenceEqual(
            Task.objects.values_list('sort_order', flat=True),
            [1, 4, 5, 8],
        )
