from dataclasses import dataclass
from . import JSONable
from json import dumps as __dumps

@dataclass
class User_Data(JSONable):
    """
    User_Data is a dataclass which inherits from abstract base class
    JSONable. It represents all of the data necessary to convert
    a given user from the database into a json object.
    """
    id: str
    url: str
    host: str
    display_name: str
    object_type: str = 'author'

    def __str__(self):
        return f'{self.object_type}, {self.id}, {self.display_name}, {self.url}, {self.host}'
    
    def get_object_as_JSON(self):
        return __dumps({
                "type": self.object_type,
                'id': self.id,
                'host': self.host,
                'displayName': self.display_name,
                'url': self.url,
        })