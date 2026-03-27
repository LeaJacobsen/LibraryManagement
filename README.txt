Library Management System, Python OOP assignment project by Lea Mette Jacobsen
##########################################
Introduction:
    Dette bibliotekssystem er lavet som led i en opgave i faget programming på Zealands Erhvervsakademi.
Kravene for opgaven er at skrive et library management system i Python og fokuserer på brugen af classes, object, inheritance og polymorphism.
Jeg har valgt at fokusere på at lave et system, som kan bruges af privatpersoner, til at oprette deres egen samling af bøger.
Ideen er at en familie eller en bogklub kan oprette et simpelt register, tilføje deres egne bøger og låne af hinanden.

##########################################
Index:
1. Project Description
2. Features
3. Object-Orientated Concepts
4. How to run the program
5. Database
6. Code structure
7. Unit test
8. Polymorphism
9. Extra features
10. Further development ideas
11. Credit


##########################################
1. Project Description
    This program is a library management system, build to get a better understanding of Object-Orientated Programming (OOP).
With this program, you can create and manage members and a book collection. You can borrow, return and leave a short review on a book.
To support persistence, I chose to add a SQLite database. The program also has a unittest, but use this with caution.


##########################################
2. Features
    The program has the following features, and those will be explained further down:
Add, Remove, Update books
Display all books
Add, Remove, Update members members
Display members
Borrow / return books
Write and store reviews for books
Search for book or author by name
Save everything in SQLite database
CLI interface


##########################################
3. Object‑Oriented Concepts Used
    The program has four classes:
        Book which represents a book with title, author, copies, ID, and user comments.
        Member, representing a library user who can borrow and return books.
        Library, that manages the system and handles books, members, storing data, loading from database, etc.
        Displayable, just a simple parent class that requires subclasses to implement a display() method.

    Book, member and library classes all have private encapsulations.
        The encapsulations are not strictly necesarry in this program, but they keep structure and prevents accidents like adding 20000 books at once.
        There are no private encapsulations, but these could be added if we had a subclass that needed a degree of priviledges to change things. A librarian, perhaps.
    The displayclass is a parentclass to show polymorphism and inheritance.


##########################################
4. How to run the program:
    Install Python
    Go to the folder where this ReadMe file is
    Run the main.py with Python
    The Command Line Interface (CLI) will automatically run
    Use the numbers to navigate the menu with your keyboard


##########################################
5. Database (SQLite)
    When the program is run for the first time, it will make a database file called library.db
This file allows users to save their library over multiple sessions, giving the program persistence.
The database will simply be loaded whenever the program is run again.
Without the database file, the program only runs on python lists. Those will reset inbetween sessions.

Deleting the library.db file will result in a complete reset of the database.
If the program is run after having deleted the file, it will make a new, empty library.db file.

The database has the following lists:
    Members, with the sublist 'borrowed books'
    Books, with the sublist 'comments'
So four lists in total.


##########################################
6. Code Structure
Provide a simple file overview:
main.py
    Contains three Classes 
        Books
        Members
        Library
    And the CLI menu
        Option 0 to 10
library.db
    Database with books and members
        This is auto-generated when the program runs
unittest.py
    Unit test for testing main.py
        WARNING: This WILL wipe your database. There is NO test database.
README.md
    Contains information about the library management system
        You are currently reading this document :-)

##########################################
7. Unit Testing
    The test checks the functionality of the program
    !!Warning: It resets the database. A test database would be great, but I have not made that yet.
How it works:
    The test will go through:
    1. Book class
        Creates book
        Borrow
        Return
        Checks availability
    2. Member class
        Borrow
        Return
    3. Library Classe
        Wipes database and list
        Add book
        Add member
        Borrow
        Return

I would like to reiterate: Database and list is reset before each test
Run the test with:
python unittest.py

##########################################
8. Polymorphism Explanation (Required by assignment)
    To implement polymorphism, I added a displayclass. It works by giving classes a blueprint to override, so the CLI agent can call on it for listing data.
The displayclass is necesarry for a small part of the CLI-menu. Because I added it later, it can be removed without causing massive damage to the entire program.
However, the display class makes it possible to add more parameters and use the same blueprint.


##########################################
9. Optional Features Added
    Some of the features added were not part of the original assignment. Here, I explain my choices
SQL database: Not having persistence in a program designed to store potentially large sheets of data made no sense to me.
Comments: I thought a library management system for a bookclub would be a fun idea. Naturally, they have to be able to comment on the books.
Search function: It was easy to implement.
CLI: Learning to add a CLI to a program, was essential for my understanding of how the program works in the end.
Safe delete: Added in case of missclicks


##########################################
10. Future feature suggestions:
    -Make a test database, so the main library database does not get wiped.
    -Track members borrow-history and currently borrowed books.
    -More multilayers in CLI for ease of access and future options for the program.
    -Log-ins and security.
    -Wishlists for members.
    -Add other things that could be borrowed, like CDs, movies etc.
    -Make a subclass of members for admin priviledges, this would be usefull for a bookclub leader or librarian.


##########################################
11. Kilder/Credit:
    Created by Lea Mette Jacobsen
With help from and thanks to our educator Zuhair Haroon Khan

Sources used:
https://medium.com/@sabaumar07/building-a-library-management-system-with-object-oriented-programming-oop-in-python-45df56704456
https://www.geeksforgeeks.org/python/library-management-system-using-python/
https://www.youtube.com/watch?v=Bmxt1c09I30
Copilot AI, Microsoft

Date: 24th of March, 2026