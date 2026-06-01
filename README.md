# Graph Database Homework - Step 3

## Description

This application is a simple Python console application that communicates with a Neo4j graph database.

The application provides the following functionality:

* List all students stored in the database
* Delete a student using the matriculation number
* Automatically create a Notification node whenever a student is deleted
* Display all previously created notifications

## Database Access

The application uses the official Neo4j Python Driver to connect to the database via the Bolt protocol.

Connection:

* URI: bolt://127.0.0.1:7687
* Authentication: Username / Password

## Security

The application uses parameterized Cypher queries instead of string concatenation. This prevents Cypher injection attacks and ensures safe handling of user input.

## Main Functions

### list_students()

Retrieves and displays all students sorted alphabetically.

### delete_student()

Deletes a student identified by the matriculation number and creates a Notification node containing:

* Student name
* Matriculation number
* Deletion timestamp
* Reason for deletion

### show_notifications()

Displays all stored deletion notifications.

## Technologies

* Python
* Neo4j
* Neo4j Python Driver
