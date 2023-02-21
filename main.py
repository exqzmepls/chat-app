from flask import Flask, request, render_template, url_for, redirect, Response

from server.server import Server

app = Flask(__name__, static_folder="./client", template_folder="./client")
server = Server()


@app.route("/")
def hello_page():
    return "main page"


@app.route("/chat")
def chat_page():
    return render_template("chat.html")


@app.route("/create_chat", methods=("GET", "POST"))
def create_chat():
    if request.method == "POST":
        chat_name = request.form["chat"]
        result = server.add_chat(chat_name)
        if result:
            return redirect(url_for("join_chat"))
        return Response("Already exists", status=400)
    return render_template("create.html")


@app.route("/join", methods=("GET", "POST"))
def join_chat():
    if request.method == "POST":
        chat_name = request.form["chat"]
        login = request.form["login"]
        chat = server.get_chat(chat_name)
        if chat is None:
            return Response("No chat", status=400)

        result = chat.add_member(login)
        if result:
            params = {"chat": chat_name, "login": login}
            return redirect(url_for("chat_page", chat=chat_name, login=login))
        return Response("Already member", status=400)

    return render_template("join.html")


@app.route("/messages")
def get_messages():
    chat_name = request.args["chat"]
    chat = server.get_chat(chat_name)
    login = request.args["login"]
    messages = chat.get_messages(login)
    return {"messages": messages}


@app.route("/members")
def get_members():
    chat_name = request.args["chat"]
    chat = server.get_chat(chat_name)
    login = request.args["login"]
    members = chat.get_members(login)
    return {"members": members}


@app.route("/message")
def send_message():
    chat_name = request.args["chat"]
    chat = server.get_chat(chat_name)
    sender = request.args["sender"]
    text = request.args["text"]
    result = chat.add_message(sender, text)
    return {"result": result}


app.run(port=5123)
