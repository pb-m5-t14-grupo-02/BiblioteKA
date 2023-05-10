import json
from django.core.management.base import BaseCommand
from books.models import Book
from authors.models import Author

def read(filepath: str): 
    with open(filepath, 'r', encoding='utf-8') as json_file: 
        loaded_data = json.load(json_file)
        
    return loaded_data

class Command(BaseCommand):
    help = 'Create multiple books from an array'


    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        list_authors = read("books/management/author_A.json")
        for author in list_authors:
            if author['image']:
                curr_author = Author.objects.create(name=author['author'], about=author['about'], image=author['image'])
            else:
                curr_author = Author.objects.create(name=author['author'], about=author['about'])
            if len(author['books']):
                for book in author['books']:
                    Book.objects.create(**book, author=curr_author)