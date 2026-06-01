from neo4j import GraphDatabase

# Connection settings for the Neo4j database
URI = "bolt://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "our_password_v1"

# Create database driver
# Communication with the Neo4j database.
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


def list_students():
    """
    Retrieves all students from the database
    and displays them in alphabetical order.
    """
    # Cypher query that retrieves all students
    # and sorts them alphabetically by name.
    query = """
    MATCH (s:Student)
    RETURN s.name AS name, s.matriculationNumber AS matriculationNumber
    ORDER BY s.name
    """

    with driver.session() as session:
        result = session.run(query)

        print("\nStudents:")
        for record in result:
            print(f"- {record['name']} ({record['matriculationNumber']})")


def delete_student():
    """
    Deletes a student identified by matriculation number.

    Before deletion, a Notification node is created
    that stores information about:
    - who was deleted
    - when the deletion happened
    - why the deletion was performed
    """

    # Request user input from the console.
    # The matriculation number uniquely identifies a student.
    matriculation_number = input("Enter matriculation number: ")
    reason = input("Enter reason for deletion: ")

    # Parameterized query.
    # Using parameters instead of string concatenation
    # protects against Cypher injection attacks.
    query = """
    MATCH (s:Student {matriculationNumber: $matriculationNumber})
    WITH s, s.name AS deletedName, s.matriculationNumber AS deletedMatriculationNumber

    CREATE (:Notification {
        deletedType: "Student",
        deletedName: deletedName,
        deletedMatriculationNumber: deletedMatriculationNumber,
        deletedAt: datetime(),
        reason: $reason
    })

    DETACH DELETE s

    RETURN deletedName
    """

    # Open a database session and execute the query.
    # The session is automatically closed afterwards.
    with driver.session() as session:
        result = session.run(
            query,
            matriculationNumber=matriculation_number,
            reason=reason
        )

        record = result.single()
        # Iterate over all returned records and display them.
        if record:
            print(f"\nDeleted student: {record['deletedName']}")
        else:
            print("\nNo student found with that matriculation number.")


def show_notifications():
    """
    Displays all notification nodes that were
    created when students were deleted.
    """

    query = """
    MATCH (n:Notification)
    RETURN n.deletedName AS name,
           n.deletedMatriculationNumber AS matriculationNumber,
           n.deletedAt AS deletedAt,
           n.reason AS reason
    ORDER BY n.deletedAt DESC
    """

    with driver.session() as session:
        result = session.run(query)

        print("\nNotifications:")

        for record in result:
            print(
                f"- Deleted {record['name']} "
                f"({record['matriculationNumber']}) "
                f"at {record['deletedAt']} "
                f"because: {record['reason']}"
            )


def menu():
    """
    Simple text-based user interface.
    Allows the user to:
    1. List students
    2. Delete students
    3. View notifications
    4. Exit the application
    """

    # Infinite loop keeps the application running
    # until the user explicitly chooses Exit.
    while True:
        # Dispatch user choice to the corresponding function.
        print("\n=== Graph Database Student Admin ===")
        print("1. List students")
        print("2. Delete student and create notification")
        print("3. Show notifications")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            list_students()
        elif choice == "2":
            delete_student()
        elif choice == "3":
            show_notifications()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


try:
    # Verify that the Neo4j server is reachable
    # before starting the application.
    driver.verify_connectivity()

    print("Connected to Neo4j!")

    # Launch the main application menu.
    menu()

finally:
    # Always close the database connection,
    # even if an exception occurs.
    driver.close()