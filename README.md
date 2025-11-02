# Aluno
Fullstack Quiz app - ALUNO - with Django

# Users
- Students
- Teachers
- Admin

# Database Design
## Entities
- User
- Student
- Teacher
- Class
- Subject
- Quiz
- Question
- Choice

# Entities Relationship Design

## Database type

- **Database system:** PostgreSQL

## ERD Diagram Sketch
![](/screenshots/IMG_20251021_182005_266.jpg)

## Table structure

### user

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement |  | |
| **username** | VARCHAR(30) | not null, unique |  | |
| **last_name** | VARCHAR(30) | not null |  | |
| **first_name** | VARCHAR(30) | not null |  | |
| **password** | VARCHAR(255) | not null |  | |
| **gender** | CHAR(1) | not null |  | |
| **role** | VARCHAR(20) | not null |  | | 


### teacher

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement | fk_teacher_id_subject_teacher | |
| **user_id** | INTEGER | not null | fk_teacher_user_id_user |Foreign key references the users table. A teacher is a user. | 


### student

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement | fk_student_id_attempt | |
| **user_id** | INTEGER | not null | fk_student_user_id_user |Foreign key references the users table. A student is a user. |
| **class_id** | INTEGER | not null, unique | fk_student_class_id_class |Foreign key references the class table. A Student is enrolled to one class only. | 


### class

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement |  | |
| **name** | VARCHAR(30) | not null |  | | 


### subject

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement | fk_subject_id_subject_teacher,fk_subject_id_subject_class | |
| **name** | VARCHAR(255) | not null |  | | 


### subject_class

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement |  | |
| **class_id** | INTEGER | not null | fk_subject_class_class_id_class | |
| **subject_id** | INTEGER | not null |  | | 


### student_subject

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement |  | |
| **student_id** | INTEGER | not null | fk_student_subject_student_id_student | |
| **subject_class_id** | INTEGER | not null |  | | 


### subject_teacher

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement | fk_subject_teacher_id_teacher_subject_class | |
| **teacher_id** | INTEGER | not null |  | |
| **subject_id** | INTEGER | not null |  | | 


### teacher_subject_class

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement | fk_teacher_subject_class_id_quiz | |
| **subject_teacher_id** | INTEGER | not null |  | |
| **class_id** | INTEGER | not null |  | | 


### quiz

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement | fk_quiz_id_question,fk_quiz_id_attempt | |
| **title** | VARCHAR(255) | not null |  | |
| **instructions** | TEXT | not null |  | |
| **teacher_subject_class_id** | INTEGER | not null |  | |
| **duration** | INTEGER | not null |  | |
| **start_date** | TIMESTAMP | not null |  | |
| **end_date** | TIMESTAMP | null |  | |
| **date_created** | DATE | null |  | | 


### question

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement | fk_question_id_multiple_choice,fk_question_id_attempt_answer | |
| **quiz_id** | INTEGER | not null |  | |
| **question_text** | TEXT | not null |  | | 


### multiple_choice

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement | fk_multiple_choice_id_attempt_answer | |
| **question_id** | INTEGER | not null |  | |
| **choice_text** | TEXT | not null |  | |
| **is_correct** | BOOLEAN | not null |  | | 


### attempt

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement | fk_attempt_id_attempt_answer | |
| **student_id** | INTEGER | not null |  | |
| **quiz_id** | INTEGER | not null |  | |
| **score** | INTEGER | not null |  | |
| **is_completed** | BOOLEAN | not null |  | | 


### attempt_answer

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null, unique, autoincrement |  | |
| **attempt_id** | INTEGER | not null |  | |
| **question_id** | INTEGER | not null |  | |
| **multiple_choice_id** | INTEGER | not null |  | |
| **is_correct** | BOOLEAN | not null |  | | 


## Relationships

- **teacher to user**: many_to_one
- **student to user**: many_to_one
- **student to class**: one_to_one
- **student_subject to student**: many_to_one
- **subject_class to class**: many_to_one
- **teacher to subject_teacher**: one_to_many
- **subject to subject_teacher**: one_to_many
- **subject_teacher to teacher_subject_class**: one_to_many
- **quiz to question**: one_to_many
- **teacher_subject_class to quiz**: one_to_many
- **subject to subject_class**: one_to_many
- **question to multiple_choice**: one_to_many
- **multiple_choice to attempt_answer**: one_to_many
- **question to attempt_answer**: one_to_many
- **attempt to attempt_answer**: one_to_many
- **student to attempt**: one_to_many
- **quiz to attempt**: one_to_many

## Tools used
- Python 3.14
- Django 5.2.7
- SQLite3 (Migrating to PostGreSQL using Supabase)
- HTML, Tailwind CSS, & JavaScript
- DrawDB.app (https://www.drawdb.app/) for ERD Design

## Security
1. Role based access
- Teachers, Students, and admin have different views to access the system according to their role.

2. Password Hashing
- All stored passwords are hashed using Django Authentication system.

3. Quiz expiration time and permission to take quiz
- Active quizzes have expiration time set by the teacher and students can not take expired quizzes if their due dates have passed. A timer is set on the duration of the quiz when the student is taking the active quiz, once the allowed time has elapsed, the platform warns the student that time has expired and submits the answers and grades the student. Students are allowed to take quiz only once.

# Students View
1. Landing Page
![Screenshot of the landing page](./screenshots/Screenshot%202025-11-02%20154607.png)

2. Login Page
![Screenshot of the login page](./screenshots/Screenshot%202025-11-02%20154622.png)

3. Student Dashboard Page
![Screenshot of the student dashboard page](./screenshots/Screenshot%202025-11-02%20145615.png)

4. All quizzes Page
![Screenshot of the all quizzes page](./screenshots/Screenshot%202025-11-02%20145634.png)

5. Student reports Page
![Screenshot of the reports page](./screenshots/Screenshot%202025-11-02%20145738.png)

6. Quiz details Page
![Screenshot of the quiz details page](./screenshots/Screenshot%202025-11-02%20145721.png)

7. Student profile Page
![Screenshot of the student profile page](./screenshots/Screenshot%202025-11-02%20145756.png)

7. Student change password Page
![Screenshot of the student profile page](./screenshots/Screenshot%202025-11-02%20145825.png)

# Teacher's view
1. Teacher dashboard Page
![Screenshot of the teacher dashboard page](./screenshots/Screenshot%202025-11-02%20145909.png)

2. Student reports Page
![Screenshot of the student reports page](./screenshots/Screenshot%202025-11-02%20145929.png)

3. Create quiz page
![Screenshot of the create quiz page](./screenshots/Screenshot%202025-11-02%20145950.png)
![Screenshot of the create quiz page](./screenshots/Screenshot%202025-11-02%20150003.png)

4. View Students Page
![Screenshot of the student page](./screenshots/Screenshot%202025-11-02%20150602.png)

5. Edit quiz Page
![Screenshot of the edit quiz page](./screenshots/Screenshot%202025-11-02%20150037.png)
![Screenshot of the edit quiz page](./screenshots/Screenshot%202025-11-02%20150049.png)

