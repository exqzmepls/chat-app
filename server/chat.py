import json
from datetime import datetime


class Chat:
    def __init__(self, name):
        self.__name = name
        self.__members = []
        self.__messages = []
        self.__messages_file = f"{name}.txt"
        with open(self.__messages_file, "w"):
            pass

    def get_name(self):
        return self.__name

    def get_members(self, login):
        member = self.__get_member(login)
        if member is None:
            return []
        result = []
        for m in self.__members:
            result.append(m["login"])
        return result

    def add_member(self, login: str) -> bool:
        if not self.__get_member(login) is None:
            return False
        join_time = datetime.now()
        member = {"login": login, "join_time": join_time}
        self.__members.append(member)
        return True

    def get_messages(self, login):
        member = self.__get_member(login)
        if member is None:
            return []

        result = []
        for message in self.__messages:
            if message["time"] >= member["join_time"]:
                result.append(message)
        return result

    def add_message(self, sender, message_text):
        if self.__get_member(sender) is None:
            return False

        message_time = datetime.now()
        message = {"sender": sender, "time": message_time, "text": message_text}
        self.__messages.append(message)
        self.__save_message(message)
        return True

    def __get_member(self, login):
        for member in self.__members:
            if member["login"] == login:
                return member
        return None

    def __save_message(self, message):
        message_json = json.dumps(message, default=str)
        with open(self.__messages_file, "a") as file:
            file.write(f"{message_json}\n")
