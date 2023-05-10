from django.core.management.base import BaseCommand
from books.models import Book
from authors.models import Author
from core.constrains import IMAGE, JSON_FILE, ABOUT, BOOKS
import json

def read(filepath: str): 
    with open(filepath, "r", encoding="utf-8") as json_file:
        loaded_data = json.load(json_file)
        
    return loaded_data
from ipdb import set_trace
class Command(BaseCommand):
    help = "Create multiple books and authors from an array"

    def handle(self, *args, **options):
        list_authors = read("books/management/author_A.json")
        for author in list_authors:
            curr_author = Author(name=author["author"], about=author[ABOUT])
            if author["image"]:
                curr_author.image = author[IMAGE]
            curr_author.save()
            if len(author[BOOKS]):
                for book in author[BOOKS]:
                    Book.objects.create(**book, author=curr_author)
        print("\033[32mFinish create books and authors ;)")
