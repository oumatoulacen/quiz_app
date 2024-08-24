### Flask Application Documentation

#### Overview
This documentation outlines the routes available in the Flask application, describing each route's purpose, expected arguments, parameters, and the roles required to access specific routes.

---

### Routes

#### 1. **User Registration**
- **Endpoint**: `/register`
- **Method**: `GET`, `POST`
- **Description**: Allows a new user to register by providing a username, email, and password.

#### 2. **User Login**
- **Endpoint**: `/login`
- **Method**: `GET`, `POST`
- **Description**: Authenticates a user using their email and password.

#### 3. **User Logout**
- **Endpoint**: `/logout`
- **Method**: `GET`
- **Description**: Logs out the current user.

#### 4. **User Profile**
- **Endpoint**: `/profile`
- **Method**: `GET`
- **Description**: Displays the profile of the logged-in user, including their quiz results.

#### 5. **Home Page (List Quizzes)**
- **Endpoint**: `/`
- **Method**: `GET`
- **Description**: Displays all available quizzes.

#### 6. **Admin Dashboard**
- **Endpoint**: `/dashboard`
- **Method**: `GET`
- **Description**: Displays the admin dashboard. 
- **Admin Access Required**

#### 7. **Add a New Category**
- **Endpoint**: `/admin/add_category`
- **Method**: `GET`, `POST`
- **Description**: Allows an admin to create a new quiz category.
- **Admin Access Required**

#### 8. **Update a Category**
- **Endpoint**: `/admin/update_category/<int:category_id>`
- **Method**: `GET`, `POST`
- **Description**: Allows an admin to update an existing category.
- **Admin Access Required**
- **Parameters**:
  - **category_id** (int): The ID of the category to update.

#### 9. **Delete a Category**
- **Endpoint**: `/admin/delete_category/<int:category_id>`
- **Method**: `GET`
- **Description**: Allows an admin to delete a specific category.
- **Admin Access Required**
- **Parameters**:
  - **category_id** (int): The ID of the category to delete.

#### 10. **View All Categories**
- **Endpoint**: `/admin/categories`
- **Method**: `GET`
- **Description**: Lists all existing categories.
- **Admin Access Required**

#### 11. **Add a New Quiz**
- **Endpoint**: `/admin/add_quiz`
- **Method**: `GET`, `POST`
- **Description**: Allows an admin to create a new quiz.
- **Admin Access Required**

#### 12. **Update a Quiz**
- **Endpoint**: `/admin/update_quiz/<int:quiz_id>`
- **Method**: `GET`, `POST`
- **Description**: Allows an admin to update the details of an existing quiz.
- **Admin Access Required**
- **Parameters**:
  - **quiz_id** (int): The ID of the quiz to update.

#### 13. **Delete a Quiz**
- **Endpoint**: `/admin/delete_quiz/<int:quiz_id>`
- **Method**: `GET`
- **Description**: Allows an admin to delete a specific quiz.
- **Admin Access Required**
- **Parameters**:
  - **quiz_id** (int): The ID of the quiz to delete.

#### 14. **View All Quizzes**
- **Endpoint**: `/admin/quizzes`
- **Method**: `GET`
- **Description**: Lists all existing quizzes.
- **Admin Access Required**

#### 15. **Take a Quiz**
- **Endpoint**: `/quiz/<int:quiz_id>`
- **Method**: `GET`, `POST`
- **Description**: Allows a user to take a quiz and submit their answers.
- **Parameters**:
  - **quiz_id** (int): The ID of the quiz to take.

#### 16. **Add a New Question**
- **Endpoint**: `/admin/add_question`
- **Method**: `GET`, `POST`
- **Description**: Allows an admin to create a new question for a quiz.
- **Admin Access Required**

#### 17. **Update a Question**
- **Endpoint**: `/admin/update_question/<int:question_id>`
- **Method**: `GET`, `POST`
- **Description**: Allows an admin to update an existing question.
- **Admin Access Required**
- **Parameters**:
  - **question_id** (int): The ID of the question to update.

#### 18. **Delete a Question**
- **Endpoint**: `/admin/delete_question/<int:question_id>`
- **Method**: `GET`
- **Description**: Allows an admin to delete a specific question.
- **Admin Access Required**
- **Parameters**:
  - **question_id** (int): The ID of the question to delete.

#### 19. **View All Questions**
- **Endpoint**: `/admin/questions`
- **Method**: `GET`
- **Description**: Lists all questions, organized by quizzes.
- **Admin Access Required**

#### 20. **View Quiz Result**
- **Endpoint**: `/quiz_result/<int:quiz_result_id>`
- **Method**: `GET`
- **Description**: Displays the result of a specific quiz for the logged-in user.
- **Parameters**:
  - **quiz_result_id** (int): The ID of the quiz result to view.

#### 21. **Delete a Quiz Result**
- **Endpoint**: `/admin/delete_quiz_result/<int:quiz_result_id>`
- **Method**: `GET`
- **Description**: Allows a user to delete one of their quiz results.
- **Parameters**:
  - **quiz_result_id** (int): The ID of the quiz result to delete.

---

### Admin Note
- **Admin Role**: The `is_admin` attribute must be set manually for a user to access admin routes. This feature has not been implemented graphically in the application.