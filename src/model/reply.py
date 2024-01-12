from datetime import datetime
from typing import List
from dataclasses import dataclass, field

@dataclass
class Reply:
    id: int = 0
    link: str = ''
    title: str = ''
    replyList: List[int] = field(default_factory=list)

    def __hash__(self):
        return hash((self.id, self.link, self.title, self.replyList))