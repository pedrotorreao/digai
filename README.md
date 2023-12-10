### digai

this is just a simple live chat room app.

#### technologies used

- python
- flask
- SocketIO
- javascript
- html
- css

#### how to run

requirements:

- clone repo
- install python
- install flask
- install SocketIO

run locally:

- `python main.py`
- `flask --app main.py run`

make it accessible to others (caution!):

- `flask --app main.py run --host=0.0.0.0`

#### next steps ideas

> functional:

- [ ] use a python date library to serve the correct date instead of `new Date().toLocaleString()`.
- [ ] option to create either public or private rooms
  - [ ] public rooms can be joined at random
  - [ ] private rooms would require the room secret
- [ ] option to choose one of the pre-defined topics for the room
  - [ ] filter public room selection by topic

> styling:

- [ ] make it more responsive

#### docs and links

- [Flask](https://flask.palletsprojects.com/en/2.3.x/quickstart/)
- [python-socketio](https://python-socketio.readthedocs.io/en/stable/intro.html)
