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
## Summary

- [Introduction](#introduction)
- [Database Type](#database-type)
- [Table Structure](#table-structure)
      - [user](#user)
      - [teacher](#teacher)
      - [student](#student)
      - [class](#class)
      - [subject](#subject)
      - [subject_class](#subject_class)
      - [student_subject](#student_subject)
      - [subject_teacher](#subject_teacher)
      - [teacher_subject_class](#teacher_subject_class)
      - [quiz](#quiz)
      - [question](#question)
      - [multiple_choice](#multiple_choice)
      - [attempt](#attempt)
      - [attempt_answer](#attempt_answer)
- [Relationships](#relationships)
- [Database Diagram](#database-diagram)

## Introduction

## Database type

- **Database system:** PostgreSQL
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

## Database Diagram
erDiagram
	teacher }o--|| user : references
	student }o--|| user : references
	student ||--|| class : references
	student_subject }o--|| student : references
	subject_class }o--|| class : references
	teacher ||--o{ subject_teacher : references
	subject ||--o{ subject_teacher : references
	subject_teacher ||--o{ teacher_subject_class : references
	quiz ||--o{ question : references
	teacher_subject_class ||--o{ quiz : references
	subject ||--o{ subject_class : references
	question ||--o{ multiple_choice : references
	multiple_choice ||--o{ attempt_answer : references
	question ||--o{ attempt_answer : references
	attempt ||--o{ attempt_answer : references
	student ||--o{ attempt : references
	quiz ||--o{ attempt : references

	user {
		INTEGER id
		VARCHAR(30) username
		VARCHAR(30) last_name
		VARCHAR(30) first_name
		VARCHAR(255) password
		CHAR(1) gender
		VARCHAR(20) role
	}

	teacher {
		INTEGER id
		INTEGER user_id
	}

	student {
		INTEGER id
		INTEGER user_id
		INTEGER class_id
	}

	class {
		INTEGER id
		VARCHAR(30) name
	}

	subject {
		INTEGER id
		VARCHAR(255) name
	}

	subject_class {
		INTEGER id
		INTEGER class_id
		INTEGER subject_id
	}

	student_subject {
		INTEGER id
		INTEGER student_id
		INTEGER subject_class_id
	}

	subject_teacher {
		INTEGER id
		INTEGER teacher_id
		INTEGER subject_id
	}

	teacher_subject_class {
		INTEGER id
		INTEGER subject_teacher_id
		INTEGER class_id
	}

	quiz {
		INTEGER id
		VARCHAR(255) title
		TEXT instructions
		INTEGER teacher_subject_class_id
		INTEGER duration
		TIMESTAMP start_date
		TIMESTAMP end_date
		DATE date_created
	}

	question {
		INTEGER id
		INTEGER quiz_id
		TEXT question_text
	}

	multiple_choice {
		INTEGER id
		INTEGER question_id
		TEXT choice_text
		BOOLEAN is_correct
	}

	attempt {
		INTEGER id
		INTEGER student_id
		INTEGER quiz_id
		INTEGER score
		BOOLEAN is_completed
	}

	attempt_answer {
		INTEGER id
		INTEGER attempt_id
		INTEGER question_id
		INTEGER multiple_choice_id
		BOOLEAN is_correct
	}