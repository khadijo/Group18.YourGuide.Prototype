# Gruppe_18 - Software Engineering Group Project

## Team Members
- Maream Sefan
- Kosovare Isulfi
- Khadijo Mumin Ali
- Chanipa Dencharoen
- Maryjane Porbusa Farstad

## Application Guidelines

### Installation

1. Install PyCharm from JetBrains to run our application. (python version 3.9 or 3.10 works)
2. Install required dependencies using the following terminal command:

   ```bash
   pip install -r requirements.txt
   
### To run app and test the prototype: 

## Explore as a User
- Use the provided user account:

  - **Username:** user
  - **Password:** user

1. Register an account with correct information(or use the username and password above).
2. Login with your credentials.
3. Explore different tours available for booking.

### Use the following functionalities:

- **Search:**
  - Search by title and destination. It is not case-sensitive and matches partial input.

- **Filter:**
  - Filter tours by destination, language, and price range.

- **Profile Icon:**
  - View your profile or view booked tours.

- **Book a Tour:**
  - Select a destination, view details, and click "Join the tour" to book.

- **Profile:**
  - View and update your profile information. Option to delete the profile.

- **Cancel a Tour:**
  - Navigate to "My tours" and cancel a booked tour.

## Administrator

- Use the provided admin account:

  - **Username:** admin
  - **Password:** admin

- Options available:

  - **Dashboard:**
    - Displays statistics on the application.

  - **Published Tours:**
    - View or delete available tours.

  - **Users:**
    - View all users and perform actions like delete or upgrade their role.

## Guide Role
- Use the provided guide account:

  - **Username:** guide
  - **Password:** guide


- Log in after being promoted to the guide role by the admin(or use the username and password above).
- Similar to the user role with an additional function to publish a tour.
- Provide required information in the correct format to publish a tour.


### Run tests

# Test account controller
pytest Gruppe_18/test/test_account_controller.py

# Test account repository
pytest Gruppe_18/test/test_account_repository.py

# Test tour controller
pytest Gruppe_18/test/test_tour_controller.py

# Test tour repository
pytest Gruppe_18/test/test_tour_repository.py

### Run with coverage

# Test account controller with coverage
coverage run -m pytest Gruppe_18/test/test_account_controller.py

# Test account repository with coverage
coverage run -m pytest Gruppe_18/test/test_account_repository.py

# Test tour controller with coverage
coverage run -m pytest Gruppe_18/test/test_tour_controller.py

# Test tour repository with coverage
coverage run -m pytest Gruppe_18/test/test_tour_repository.py

### To view the coverage report: 

# View coverage report in terminal 
coverage report

# View in HTML (open index.html file in htmlcov directory)
coverage html

### Locust Tests

1. Locate `locust_test.py` in the test directory.
2. Ensure `app.py` is not running.
3. Run `locust_test.py` and find the locust test port in the terminal (8888).
4. Click on the port to access the locust test interface.
5. Start swarming to send users to the prototype.
6. Stop when testing is complete, and stop the locust test from run terminal by clicking on: 
   the stop button on the left side of the run terminal. 
