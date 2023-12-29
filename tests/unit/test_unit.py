from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class TaskListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            complete=False
        )

    def test_task_list_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_task_list_view_displays_tasks_for_logged_in_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    # Add more test cases for other views similarly...

class TaskCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_task_create_view_creates_task_for_logged_in_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('task-create'), {
            'title': 'New Task',
            'description': 'New Description',
            'complete': False,
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Task.objects.filter(title='New Task').count(), 1)

    # Add more test cases for other views similarly...

class TaskReorderViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Add tasks for the user...

    def test_task_reorder_view_updates_task_order(self):
        self.client.login(username='testuser', password='testpassword')
        task1 = Task.objects.create(user=self.user, title='Task 1', description='Description 1', complete=False)
        task2 = Task.objects.create(user=self.user, title='Task 2', description='Description 2', complete=False)
        task3 = Task.objects.create(user=self.user, title='Task 3', description='Description 3', complete=False)

        # Define the initial order
        initial_order = f"{task1.id},{task2.id},{task3.id}"

        response = self.client.post(reverse('task-reorder'), {'position': initial_order})
        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Retrieve the updated task order
        updated_order = Task.objects.filter(user=self.user).values_list('id', flat=True)
        updated_order_str = ",".join(map(str, updated_order))

        # Compare the initial order with the updated order
        self.assertEqual(initial_order, updated_order_str)

