#Unit test til programmet
#KÆMPE ADVARELSE!!!!!!!!!: Den SLETTER AL DATA som en del af testen. Hvis du vil teste UDEN at wipe memory, så skal du oprette en testdatabase.
# ... Det gad jeg ikke.
import unittest
from main import Book, Member, Library  #Henter objects i main program


class TestBook(unittest.TestCase):

    def test_borrow_reduces_copies(self):   #Attempts to borrow a book and checks whether the amount of copies available goes down
        book = Book("TestTitle", "Author", 3, "001")
        book.borrow_book()
        self.assertEqual(book._Book__copies, 2)

    def test_return_increases_copies(self): #Returns a book, checks if copies available increases
        book = Book("TestTitle", "Author", 3, "001")
        book.borrow_book()
        book.return_book()
        self.assertEqual(book._Book__copies, 3)

    def test_availability(self):            #Checks book availability
        book = Book("Title", "Author", 1, "001")
        book.borrow_book()
        self.assertEqual(book.check_availability(), "Not Available")


class TestMember(unittest.TestCase):

    def test_member_borrow_book(self):      #Tests wheher a member can borrow a book
        book = Book("Title", "Author", 1, "001")
        member = Member(1, "User")
        msg = member.borrow_book(book)
        self.assertIn("successfully borrowed", msg)

    def test_member_return_book(self):      #Tests whether a member can return the book again.
        book = Book("Title", "Author", 1, "001")
        member = Member(1, "User")
        member.borrow_book(book)
        msg = member.return_book(book)
        self.assertIn("Thank you", msg)


class TestLibrary(unittest.TestCase):

    def setUp(self):    #WARNING: THIS PART IS WHAT WIPES THE DATABASE AND LIST
        """Runs before EVERY test — resets DB + Python lists"""
        self.lib = Library()

        # BEMÆRK AT: Denne unittest LAVER ET KOMPLET RESET AF LIST OG DATABASE
        #DATABASE CLEAR
        self.lib.cursor.execute("DELETE FROM books")
        self.lib.cursor.execute("DELETE FROM members")
        self.lib.cursor.execute("DELETE FROM comments")
        self.lib.conn.commit()
        #LIST CLEAR
        self.lib._Library__books.clear()
        self.lib._Library__members.clear()


    def test_add_book(self):    #Tries to add a book
        b = Book("T", "A", 2, "001")
        self.lib.add_book(b)
        self.assertIn(b, self.lib._Library__books)

    def test_add_member(self):  #Tries to add member
        m = Member(1, "User")
        self.lib.add_member(m)
        self.assertIn(m, self.lib._Library__members)

    def test_issue_book(self):  #Member borrows book
        b = Book("T", "A", 2, "001")
        m = Member(1, "User")
        self.lib.add_book(b)
        self.lib.add_member(m)

        self.lib.issue_book(1, "001")

        # Checker om der er præcis én kopi af bogen i library
        book_in_lib = next(bk for bk in self.lib._Library__books if bk.get_id() == "001")
        self.assertEqual(book_in_lib._Book__copies, 1)

    def test_return_book(self): #Returns book
        b = Book("T", "A", 2, "001")
        m = Member(1, "User")
        self.lib.add_book(b)
        self.lib.add_member(m)

        self.lib.issue_book(1, "001")    # Tjekker om copies går fra  2 → 1
        self.lib.return_book(1, "001")   # Tjekker om copies går fra 1 → 2

        # Tjekker book object er korrekt
        book_in_lib = next(bk for bk in self.lib._Library__books if bk.get_id() == "001")
        self.assertEqual(book_in_lib._Book__copies, 2)

#Vælger hvilket dokument (her, main.py,) der skal udføres en unit test på.
if __name__ == "__main__":
    unittest.main()