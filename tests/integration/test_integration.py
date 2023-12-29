from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class TaskIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_task_workflow(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create a task
        create_response = self.client.post(reverse('task-create'), {
            'title': 'New Task',
            'description': 'New Description',
            'complete': False,
        })
        self.assertEqual(create_response.status_code, 302)  # Redirect status code
        self.assertEqual(Task.objects.filter(title='New Task').count(), 1)

        # Retrieve the created task
        created_task = Task.objects.get(title='New Task')

        # Update the task
        update_response = self.client.post(reverse('task-update', kwargs={'pk': created_task.pk}), {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'complete': True,
        })
        self.assertEqual(update_response.status_code, 302)  # Redirect status code
        self.assertEqual(Task.objects.get(pk=created_task.pk).title, 'Updated Task')

        # Delete the task
        delete_response = self.client.post(reverse('task-delete', kwargs={'pk': created_task.pk}))
        self.assertEqual(delete_response.status_code, 302)  # Redirect status code
        self.assertEqual(Task.objects.filter(pk=created_task.pk).count(), 0)

    def test_task_reorder_workflow(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create tasks
        task1 = Task.objects.create(user=self.user, title='Task 1', description='Description 1', complete=False)
        task2 = Task.objects.create(user=self.user, title='Task 2', description='Description 2', complete=False)
        task3 = Task.objects.create(user=self.user, title='Task 3', description='Description 3', complete=False)

        # Define the initial order
        initial_order = f"{task1.id},{task2.id},{task3.id}"

        # Reorder tasks
        reorder_response = self.client.post(reverse('task-reorder'), {'position': initial_order})
        self.assertEqual(reorder_response.status_code, 302)  # Redirect status code

        # Retrieve the updated task order
        updated_order = Task.objects.filter(user=self.user).values_list('id', flat=True)
        updated_order_str = ",".join(map(str, updated_order))

        # Compare the initial order with the updated order
        self.assertEqual(initial_order, updated_order_str)

    # Add more integrated tests for other workflows...
