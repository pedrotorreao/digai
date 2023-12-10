from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import hexdigits
from datetime import datetime, date

app = Flask(__name__)
app.config["SECRET_KEY"] = "k@1alsdp%*^&$447HQvam2"
socketio = SocketIO(app)

ROOM_SECRET_LENGTH = 7

rooms = dict()


def generate_unique_secret():
    while True:
        new_secret = ""
        for _ in range(ROOM_SECRET_LENGTH):
            new_secret += random.choice(hexdigits)

        # if secret is unique, break out of the loop and return it;
        # otherwise, keep generating new secrets:
        if new_secret not in rooms:
            break

    return new_secret


@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()

    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        # 1. invalid/empty 'username':
        if not name:
            return render_template(
                "home.html", error="please enter a username", code=code, name=name
            )
        # 2. empty 'room secret':
        if join != False and not code:
            return render_template(
                "home.html",
                error="please enter a valid room secret",
                code=code,
                name=name,
            )

        room_secret = code
        # 3. create a new room and add it to the 'rooms' dictionary:
        if create != False:
            room_secret = generate_unique_secret()
            rooms[room_secret] = {"members": 0, "messages": []}
        # 4. invalid 'room secret' was entered:
        elif code not in rooms:
            return render_template(
                "home.html", error="rooms does not exist", code=code, name=name
            )

        session["room"] = room_secret
        session["name"] = name

        # redirect user to the room selected/created:
        return redirect(url_for("room"))

    return render_template("home.html")


@app.route("/room")
def room():
    room = session.get("room")
    if (room is None) or (session.get("name") is None) or (room not in rooms):
        return redirect(url_for("home"))
    return render_template("room.html", room=room, messages=rooms[room]["messages"])


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")

    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has joined the room"}, to=room)
    rooms[room]["members"] += 1

    print(f"----> {name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")

    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"----> {name} left room {room}")


@socketio.on("message")
def message_handler(data):
    room = session.get("room")

    if room not in rooms:
        return

    # TODO: use a python lib to get the correct Date and add it to the content
    # curr_date = date.today().strftime("%b-%d-%Y")
    # curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    content = {"name": session.get("name"), "message": data["data"]}

    send(content, to=room)
    rooms[room]["messages"].append(content)

    print(f"{session.get('name')} said: {data['data']}")


if __name__ == "__main__":
    socketio.run(app, debug=False)
