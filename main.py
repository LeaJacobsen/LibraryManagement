# Libraries
import sqlite3      #Til database (persistence-layer)


# Display class til books og members, til lists i CLI og nemmere videreudvikling.
class Displayable:
    def display(self):
        raise NotImplementedError("Subclasses must override display()")

##########################################
#BOOK CLASS
##########################################
class Book(Displayable):
    def __init__(self, title, author, copies, book_ID): #Private attributes
        self.__title = title
        self.__author = author
        self.__copies = copies
        self.__book_ID = str(book_ID)   # BookID er i string-format, så flere ID-systemer kan bruges
        self.__availability = True      # Når en ny bog tilføjes, sættes den som available for udlån
        self.__comments = []            # Opretter muligheden for at en bruger kan give en anmeldelse af bogen efter aflevering
        
    ### GETTERS

    def get_book_info(self):            # Henter information om bogen
        return (
            f"Title: {self.__title}\n"
            f"Author: {self.__author}\n"
            f"Copies: {self.__copies}\n"
            f"ID: {self.__book_ID}"
        )

    def check_availability(self):       # Tjekker om en given bog kan lånes
        return "Available" if self.__copies > 0 else "Not Available"    # Fortæller user om den kan lånes eller ej
    
    def get_comments(self):             # Gør det muligt for en user at se anmeldelser på en bog
        if not self.__comments:
            return "No comments yet."   # Hvis ingen comments, får user beskeden "No comments yet"
        return "\n".join(f"- {c}" for c in self.__comments)

    def display(self):                  # Henter book info til CLI
        return self.get_book_info()

    ### BORROWING & RETURNING

    def borrow_book(self):              # Lader user låne en bog, hvis der er tilgængelige copies.
        if self.__copies > 0:
            self.__copies -= 1
            return f"You have successfully borrowed '{self.__title}'."
        else:
            return f"No copies of '{self.__title}' are available."

    def return_book(self):              # Når en bog afleveres, tilføjes en kopi af den til udlån igen.
        self.__copies += 1
        return f"You have returned '{self.__title}'. Thank you!"    # Fortæller user at bogen er afleveret.

    ### GETTERS til Library Class

    def get_id(self):
        return self.__book_ID

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author
    
    def add_comment(self, comment):                 # Gør det muligt at tilføje en anmeldelse på maks 200 characters.
        if len(comment) > 200:
            return "Review too long. Max 200 characters."
        self.__comments.append(comment)
        return "Review added successfully."        # Fortæller user at deres anmeldelse er tilføje

##########################################
# MEMBER CLASS
##########################################

class Member(Displayable):
    def __init__(self, member_id, name, borrowed_books=None):       #Private attributes
        self.__member_id = member_id
        self.__name = name
        self.__borrowed_books = [] if borrowed_books is None else borrowed_books    # Opretter liste med låne bøger, eller tilføjer flere bøger til eksisterende liste

    ### DISPLAY INFO

    def get_member_info(self):      #Fortæller member navn og ID
        return f"Member Name: {self.__name}\nMember ID: {self.__member_id}"
    
    def display(self):              #Display til CLI
        return self.get_member_info()

    ### BORROW/RETURN METHODS

    def borrow_book(self, book):
        if book.check_availability() == "Available":
            msg = book.borrow_book()
            self.__borrowed_books.append(book)      # Tilføjer lånt bog til liste af lånte bøger, hvis der er en kopi til udlån
            return msg
        else:
            return f"'{book.get_title()}' is not available."    # Fortæller user hvis der ikke er en available bog til udlån

    def return_book(self, book):
        if book in self.__borrowed_books:
            msg = book.return_book()
            self.__borrowed_books.remove(book)      # Fjerne bog fra members udlånsliste
            return msg
        else:
            return f"You have not borrowed '{book.get_title()}'."   # Error, hvis bruger forsøger at returnere bog de ikke har lånt

    ### GETTERS til Library Class
    
    def get_id(self):
        return self.__member_id

    def get_name(self):
        return self.__name

##########################################
# LIBRARY CLASS
##########################################

class Library:
    def __init__(self):
        self.conn = sqlite3.connect("library.db")   # Forbinder til database
        self.cursor = self.conn.cursor()            # Kører SQL commands

    ### DATABASE TABLES
    
        # Opretter books table i database
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,
                title TEXT,
                author TEXT,
                copies INTEGER
            );
        """)

        # Opretter members table i database
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
        """)

        # Opretter comments table i database
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id TEXT,
                comment TEXT
            );
        """)

        self.conn.commit()

        # Python lists til working memory
        self.__books = []
        self.__members = []

        # Load data fra SQLite Databasen
        self.load_books()
        self.load_members()         
        self.load_comments()

    ### BOOK MANAGEMENT
    
    def add_book(self, book):       #Tilføjer bøger til python-listen
        self.__books.append(book)
        print(f"Book '{book.get_title()}' has been added.")

        # Gemmer python-listen i databasen
        self.cursor.execute("""
            INSERT OR REPLACE INTO books (id, title, author, copies)
            VALUES (?, ?, ?, ?)
        """, (book.get_id(), book.get_title(), book.get_author(), book._Book__copies))

        self.conn.commit()
    
    def remove_book(self, book_id): # Fjerner bøger fra python-listen
        for book in self.__books:
            if book.get_id() == book_id:
                self.__books.remove(book)
                print(f"Book '{book.get_title()}' removed from memory.")    # Fortæller user at bog er fjernet fra python-list, ie 'memory'

            # Fjerner bøger fra databasen
                self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
                self.cursor.execute("DELETE FROM comments WHERE book_id = ?", (book_id,))
                self.conn.commit()

                print(f"Book '{book.get_title()}' removed from database.")  # Fortæller user at bog er fjernet fra databasen
                return
            
        print("Book ID not found.")     # Error-message, hvis user forsøger at fjerne bog som ikke er til stede i forvejen.
    
    def update_book(self, book_id, new_title=None, new_author=None, new_copies=None):   # Opdaterer bog, så evt., stavefejl eller andet kan rettes
        for book in self.__books:
            if book.get_id() == book_id:
                if new_title: book._Book__title = new_title
                if new_author: book._Book__author = new_author
                if new_copies is not None: book._Book__copies = new_copies
                print("Book updated successfully.")
                return
        print("Book ID not found.")     # User kan ikke opdatere en bog, som ikke er i systemet.

    def display_books(self):    # Til CLI book-list
        if not self.__books:
            print("No books in the library.")   # Hvis library er tomt, og user vælger menu 2, siger terminal "No books..."

        for book in self.__books:   
            print(book.get_book_info())
            print("Reviews:")      
            print(book.get_comments())   # Lader user se reviews på bøger
            print()

    ### Henter Books i database
    
    def load_books(self):
        self.cursor.execute("SELECT id, title, author, copies FROM books")
        rows = self.cursor.fetchall()

        for book_id, title, author, copies in rows:
            book = Book(title, author, copies, book_id)
            self.__books.append(book)

    ### Henter members fra databasen

    def load_members(self):
        self.cursor.execute("SELECT id, name FROM members")
        rows = self.cursor.fetchall()

        for member_id, name in rows:
            member = Member(member_id, name)
            self.__members.append(member)

    ### Henter comments fra databasen
    
    def load_comments(self):
        self.cursor.execute("SELECT book_id, comment FROM comments")
        rows = self.cursor.fetchall()

        for book_id, comment in rows:
            book = next((b for b in self.__books if b.get_id() == book_id), None)
            if book:
                book.add_comment(comment)

    ### MEMBER MANAGEMENT
    
    def add_member(self, member):       # Tilføj member til python member list og databasen
        self.__members.append(member)
        print(f"Member '{member.get_name()}' added.")
        self.cursor.execute("""
            INSERT OR REPLACE INTO members (id, name)
            VALUES (?, ?)
        """, (member.get_id(), member.get_name()))

        self.conn.commit()

    def remove_member(self, member_id):     # Fjern member fra python list og databasen
        for member in self.__members:
            if member.get_id() == member_id:
                self.__members.remove(member)
                print(f"Member '{member.get_name()}' removed from memory.")
                self.cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
                self.conn.commit()

                print(f"Member '{member.get_name()}' removed from database.")
                return
        print("Member ID not found.")


    def update_member(self, member_id, new_name=None):  # Opdaterer member i både pythonlist og database. Gør det muligt fx at skifte navn
        for member in self.__members:
            if member.get_id() == member_id:
                if new_name:
                    member._Member__name = new_name
                    self.cursor.execute("""
                        UPDATE members
                        SET name = ?
                        WHERE id = ?
                    """, (new_name, member_id))
                    self.conn.commit()
                print("Member updated.")
                return
        print("Member ID not found.")


    def display_members(self):  # Til CLI menu 4 respons
        if not self.__members:
            print("No members registered.")     # Hvis der ikke er nogen members registreret
        for member in self.__members:
            print(member.get_member_info() + "\n")

    ### Udlån og aflevering af bøger

    # Udlån af bog
    def issue_book(self, member_id, book_id):
        member = next((m for m in self.__members if m.get_id() == member_id), None)
        book = next((b for b in self.__books if b.get_id() == book_id), None)

        if not member:
            return "Member not found."      # Hvis member ikke eksisterer -> "Member not found"
        if not book:
            return "Book not found."        # Hvis bog ikke eksisterer -> "Book not found"

        msg = member.borrow_book(book)    
        
        # Opdater databasen med antal kopier af bogen efter udlån
        self.cursor.execute("""
            UPDATE books
            SET copies = ?
            WHERE id = ?
        """, (book._Book__copies, book.get_id()))

        self.conn.commit()
        return msg

    # Aflevering af bog
    def return_book(self, member_id, book_id):
        member = next((m for m in self.__members if m.get_id() == member_id), None)
        book = next((b for b in self.__books if b.get_id() == book_id), None)

        if not member:
            return "Member not found."
        if not book:
            return "Book not found."

        msg = member.return_book(book)

        self.cursor.execute("""
            UPDATE books
            SET copies = ?
            WHERE id = ?
        """, (book._Book__copies, book.get_id()))

        self.conn.commit()
        return msg

    # CLI funktioner
    
    # Kalder på list af members og bøger og printer det til terminalen, menu 9. Der kan tilføjes flere lists, hvis man har lyst
    def display_all(self, items):    
        for obj in items:
            print(obj.display())     
            print()
    
    # Til at søge efter bogtitler
    def search_by_title(self, query):
        return [b for b in self.__books if query.lower() in b.get_title().lower()]
    # Til at søge efter forfatternavne
    def search_by_author(self, query):
        return [b for b in self.__books if query.lower() in b.get_author().lower()]

##########################################        
### CLI - Command Line Interface
##########################################

def run_cli():          # Starter Command Line Interface, så programmet kan benyttes i terminalen på en brugervenlig måde
    library = Library()

    while True:         # Dette er selve menuen
        print("\n---- Library Menu ----")
        print("1. Add Book")
        print("2. List Books")
        print("3. Add Member")
        print("4. List Members")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Remove Book")       
        print("8. Remove Member")
        print("9. Find Book/Author")
        print("10. Display ALL items (polymorphic)")
        print("0. Exit")

        choice = input("Enter your choice: ")

        # 1. Add Book
        if choice == "1":
            title = input("Book title: ")
            author = input("Author: ")
            copies = int(input("Number of copies: "))
            book_id = input("Book ID (Numbers, letters and symbols allowed): ")  #Fordi book_id er en string, kan man selv vælge hvilken type ID-system man vil bruge
            new_book = Book(title, author, copies, book_id)
            library.add_book(new_book)

        # 2. List Books
        elif choice == "2":
            library.display_books()

        # 3. Add Member
        elif choice == "3":
            member_id = int(input("Member ID: "))
            name = input("Member name: ")
            new_member = Member(member_id, name)
            library.add_member(new_member)

        # 4. List Members
        elif choice == "4":
            library.display_members()

        # 5. Borrow Book
        elif choice == "5":
            member_id = int(input("Member ID: "))
            book_id = int(input("Book ID: "))
            print(library.issue_book(member_id, book_id))

        # 6. Return Book
        elif choice == "6":
            member_id = int(input("Member ID: "))
            book_id = int(input("Book ID: "))
            
            msg = library.return_book(member_id, book_id)
            print(msg)
            
            book = next((b for b in library._Library__books if b.get_id() == book_id), None)
            
            if book:
                add_comment = input("Would you like to leave a short comment about the book? (y/n): ")

                if add_comment.lower() == "y":
                    comment = input("Enter your comment (max 200 characters): ")
                    result = book.add_comment(comment)
                    print(result)

        # 7. Remove Book
        elif choice == "7":
            book_id = input("Enter the Book ID to remove: ")
            confirm = input("Are you sure you want to delete this book? (y/n): ")
            if confirm.lower() == "y":
                library.remove_book(book_id)


        # 8. Return Book
        elif choice == "8":
            member_id = int(input("Enter the Member ID to remove: "))
            confirm = input("Are you sure you want to delete this member? (y/n): ")
            if confirm.lower() == "y":
                library.remove_member(member_id)

        # 9. Search
        elif choice == "9":
            print("\n--- Book Search ---")
            print("1. Search by Title")
            print("2. Search by Author")
            print("0. Back")

            search_choice = input("Choose search type: ")

            if search_choice == "1":
                query = input("Enter title keyword: ")
                results = library.search_by_title(query)
                if results:
                    print("\nSearch Results:")
                    for book in results:
                        print(book.get_book_info(), "\n")
                else:
                    print("No books found with that title.")

            elif search_choice == "2":
                query = input("Enter author keyword: ")
                results = library.search_by_author(query)
                if results:
                    print("\nSearch Results:")
                    for book in results:
                        print(book.get_book_info(), "\n")
                else:
                    print("No books found with that author.")
            else:
                print("Returning to main menu...")

        # 10. Vis alle lister
        elif choice == "10":
            print("\n--- DISPLAYING ALL ITEMS (POLYMORPHISM) ---\n")
    
            # Books listen
            print("Books:\n")
            library.display_all(library._Library__books)

            # Members liste
            print("\nMembers:\n")
            library.display_all(library._Library__members)

        # Exit programmet
        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

# Start CLI ved opstart
if __name__ == "__main__":
    run_cli()