from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatTypeFilter(BaseFilter):  
    def __init__(self, chat_type: Union[str,list]) -> None:
        self.chat_type = chat_type


    async def __call__(self, message: Message) -> bool:  
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type
        
class ContentTypeFilter(BaseFilter):
    def __init__(self, type_message: Union[str,list]) -> None:
        self.type_message = type_message
    async def __call__(self, message: Message) -> bool:  
        if isinstance(self.type_message, str):
            return message.content_type == self.type_message
        else:
            return message.content_type in self.type_message