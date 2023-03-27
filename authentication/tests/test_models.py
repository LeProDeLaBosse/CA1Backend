from utils.setup_test import TestSetup
from authentication.models import User

# Defining a new test class TestModel which inherits from TestSetup
class TestModel(TestSetup):

    # Defining a test method test_should_create_user inside the TestModel class
    def test_should_create_user(self):

        # Defining a test method test_should_create_user inside the TestModel class
        user = self.create_test_user()

        # Asserting that the string representation of the user object is equal to the user's email
        self.assertEqual(str(user), user.email)