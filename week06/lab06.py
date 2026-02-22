"""
Lab 06: Object-Oriented Programming
Student implementation of Book and EBook classes with inheritance.
"""


class Book:
    """Represents a book with title, author, and publication year."""

    def __init__(self, title: str, author: str, year: int):
        """
        Initialize a new book.
        
        Args:
            title: The title of the book
            author: The author of the book
            year: The publication year
        """
        self.title = title
        self.author = author
        self.year = year

    def get_age(self) -> int:
        """
        Calculate and return the age of the book based on its publication year.
        
        Returns:
            The age of the book in years (assuming current year is 2025)
        """
        current_year = 2025  # As specified in lab instructions
        return current_year - self.year

    def __str__(self) -> str:
        """
        Return a user-friendly string representation of the book.
        
        Returns:
            A formatted string with book information
        """
        return f'"{self.title}" by {self.author} ({self.year})'


class EBook(Book):
    """Electronic book that inherits from Book with additional file size attribute."""

    def __init__(self, title: str, author: str, year: int, file_size: int):
        """
        Initialize an EBook with all Book attributes plus file size.
        
        Args:
            title: The title of the book
            author: The author of the book
            year: The publication year
            file_size: The file size in megabytes (MB)
        """
        # Call the parent class constructor
        super().__init__(title, author, year)
        # Add the EBook-specific attribute
        self.file_size = file_size

    def __str__(self) -> str:
        """
        Override to include file size information.
        
        Returns:
            A formatted string with book information and file size
        """
        # Get the base string from the parent class
        parent_str = super().__str__()
        # Append the file size information
        return f"{parent_str} ({self.file_size} MB)"


if __name__ == '__main__':
    print("=== Testing Book Class ===")
    
    # Create and test Book instances
    book1 = Book("The Hobbit", "J.R.R. Tolkien", 1937)
    print(f"Book 1: {book1}")
    print(f"Age: {book1.get_age()} years")
    print()
    
    book2 = Book("Clean Code", "Robert Martin", 2008)
    print(f"Book 2: {book2}")
    print(f"Age: {book2.get_age()} years")
    print()
    
    print("=== Testing EBook Class ===")
    
    # Create and test EBook instances
    ebook1 = EBook("Dune", "Frank Herbert", 1965, 5)
    print(f"EBook 1: {ebook1}")
    print(f"Age: {ebook1.get_age()} years (inherited method)")
    print()
    
    ebook2 = EBook("Automate the Boring Stuff with Python", "Al Sweigart", 2015, 12)
    print(f"EBook 2: {ebook2}")
    print(f"Age: {ebook2.get_age()} years")
    print()
    
    print("=== Library Collection ===")
    library = [book1, book2, ebook1, ebook2]
    for i, item in enumerate(library, 1):
        print(f"{i}. {item} - {item.get_age()} years old")
