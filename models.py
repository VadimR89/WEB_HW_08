from mongoengine import Document
from mongoengine.fields import StringField, ReferenceField, ListField, ObjectIdField


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)