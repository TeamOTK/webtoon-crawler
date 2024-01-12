from datetime import datetime
from typing import List
from dataclasses import dataclass, field

@dataclass
class Webtoon:
    id: int = 0
    link: str = ''
    title: str = ''
    author: str = ''
    genre: str = ''
    description: str = ''
    
    def __eq__(self, other):
        return isinstance(other, Webtoon) and (self.id) == (other.id)

    def __hash__(self):
        return hash((self.id, self.link, self.title, self.author, self.genre, self.description))