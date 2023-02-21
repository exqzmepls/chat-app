from typing import Optional

from server.chat import Chat


class Server:
    def __init__(self):
        self.__chats = []

    def get_chat(self, name: str) -> Optional[Chat]:
        for chat in self.__chats:
            chat_name = chat.get_name()
            if chat_name == name:
                return chat
        return None

    def add_chat(self, name: str) -> bool:
        for chat in self.__chats:
            chat_name = chat.get_name()
            if chat_name == name:
                return False

        new_chat = Chat(name)
        self.__chats.append(new_chat)
        return True
