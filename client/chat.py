import asyncio
from pyodide.http import pyfetch
import json


def get_element(element_id):
    return js.document.getElementById(element_id)


# Загружает новые сообщения с сервера и отображает их
async def load_messages():
    result = await fetch(f"/messages?chat={chat.value}&login={login.value}", method="GET")
    data = await result.json()
    all_messages = data["messages"]  # Берем список сообщений из ответа сервера
    messages.innerHTML = ""  # Очищаем окно с сообщениями
    for message in all_messages:
        append_message(message)
    set_timeout(1, load_messages)  # Запускаем загрузку заново через секунду


# Добавляет новое сообщение в список сообщений
def append_message(message):
    # Создаем HTML-элемент представляющий сообщение
    item = js.document.createElement("li")  # li - это HTML-тег для элемента списка
    item.className = "list-group-item"
    item.innerHTML = f'[<b>{message["sender"]}</b>]: <span>{message["text"]}</span><span class="badge text-bg-light text-secondary">{message["time"]}</span>'
    messages.prepend(item)


# Вызывается при клике на send_message
async def send_message_click(e):
    # Отправляем запрос
    await fetch(f"/message?chat={chat.value}&sender={login.value}&text={message_text.value}", method="GET")
    # Очищаем поле
    message_text.value = ""


async def get_members_click(e):
    result = await fetch(f"/members?chat={chat.value}&login={login.value}", method="GET")
    data = await result.json()
    all_members = data["members"]
    members.innerHTML = ""
    for member in all_members:
        append_member(member)


def append_member(member):
    item = js.document.createElement("li")
    item.className = "list-group-item"
    item.innerHTML = f'<span>{member}</span>'
    members.prepend(item)


async def fetch(url, method, payload=None):
    kwargs = {
        "method": method
    }
    if method == "POST":
        kwargs["body"] = json.dumps(payload)
        kwargs["headers"] = {"Content-Type": "application/json"}
    return await pyfetch(url, **kwargs)


def set_timeout(delay, callback):
    def sync():
        asyncio.get_running_loop().run_until_complete(callback())

    asyncio.get_running_loop().call_later(delay, sync)


# Находим элементы интерфейса по их ID
chat = get_element("chat")
login = get_element("login")
messages = get_element("messages")
members = get_element("members")
message_text = get_element("message_text")

# Устанавливаем действие при клике
send_message = get_element("send_message")
send_message.onclick = send_message_click
members_btn = get_element("membersBtn")
members_btn.onclick = get_members_click
load_messages()
