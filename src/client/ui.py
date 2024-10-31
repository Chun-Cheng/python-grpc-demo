import curses
import time
import api as api
import db as db

current_user = None
run = True

# Function to draw the sign-up screen
def signup_screen(stdscr: curses.window) -> bool:
    global current_user
    stdscr.clear()
    stdscr.addstr("Sign Up\n")
    stdscr.addstr("Enter your username: ")
    curses.echo()
    username = stdscr.getstr().decode('utf-8')
    curses.noecho()
    # operations
    api.signup(username)
    current_user = username
    return True

# Function to draw the user selection screen
def user_selection_screen(stdscr: curses.window) -> None:
    global current_user
    users = db.get_users()
    if len(users) == 1:
        current_user = users[0]
        return

    stdscr.clear()
    stdscr.addstr("Select User\n")
    for i, user in enumerate(users):
        stdscr.addstr(f"({i}) {user}\n")
    stdscr.addstr("(n) New User\n")
    stdscr.addstr("Select an option: ")

    option = stdscr.getch()
    if option == ord('n'):
        signup_screen(stdscr)
    elif ord('0') <= option <= ord('9') and option - ord('0') < len(users):
        current_user = users[option - ord('0')]

# Function to draw the main menu
def main_menu(stdscr: curses.window) -> None:
    global run
    while True:
        stdscr.clear()
        stdscr.addstr(f"Welcome {current_user}\n")
        stdscr.addstr("\n")
        stdscr.addstr("Rooms\n")
        # list rooms
        rooms = api.get_rooms(current_user)[:10]
        if rooms:
            for i in range(len(rooms)):
                stdscr.addstr(f"({i}) {rooms[i]}\n")
        else:
            stdscr.addstr("(empty) \n")
        stdscr.addstr("\n")
        stdscr.addstr("Actions\n")
        stdscr.addstr("(c) Create Room\n")
        stdscr.addstr("(q) Exit\n")
        stdscr.addstr("(s) Sign Up New User\n")
        stdscr.addstr("\n")
        stdscr.addstr("Select an option: ")

        option = stdscr.getch()

        if option == ord('c'):
            create_room(stdscr)
        elif option == ord('q'):
            run = False
            break
        elif option == ord('s'):
            signup_screen(stdscr)
        elif ord('0') <= option <= ord('9') and option - ord('0') < len(rooms):
            enter_room(stdscr, rooms[option - ord('0')])

        time.sleep(0.1)

# Function to create a room
def create_room(stdscr: curses.window) -> None:
    stdscr.clear()
    stdscr.addstr("Create room\n")
    stdscr.addstr("Enter room name: ")
    curses.echo()
    room_name = stdscr.getstr().decode('utf-8')
    curses.noecho()
    api.create_room(room_name, current_user)
    stdscr.addstr(f"Room '{room_name}' created! Press any key to go back.")
    stdscr.getch()

# Function to invite user to a room
def invite_user(stdscr: curses.window, room_name: str) -> None:
    stdscr.clear()
    stdscr.addstr(f"Invite user to {room_name}\n")
    stdscr.addstr("Enter username to invite: ")
    curses.echo()
    username = stdscr.getstr().decode('utf-8')
    curses.noecho()
    api.invite_user(room_name, username)
    stdscr.addstr(f"User '{username}' invited to '{room_name}'. Press any key to go back.")
    stdscr.getch()

# Function to enter a room and send/receive messages
def enter_room(stdscr: curses.window, room_id: str) -> None:
    stdscr.nodelay(True)
    input_buffer = ""
    while True:
        messages = db.get_messages(room_id)

        stdscr.clear()
        stdscr.addstr(f"Room: {room_id}\n")
        stdscr.addstr("\n")
        for message in messages[-10:]:  # Show last 10 messages
            stdscr.addstr(f"{message['author']} ({message['timestamp']})")
            stdscr.addstr(f": {message['text']}\n")

        # Input prompt for new message
        stdscr.addstr(f"\n{'='*30}\n")
        stdscr.addstr("/exit", curses.A_BOLD)
        stdscr.addstr(" to exit the room\n")
        stdscr.addstr("/invite", curses.A_BOLD)
        stdscr.addstr(" to invite a user to the room\n")
        stdscr.addstr(": ")
        stdscr.addstr(input_buffer)
        stdscr.refresh()

        time.sleep(0.1)

        key = stdscr.getch()
        if key == curses.ERR:
            continue
        elif key == 10:  # Enter key
            msg = input_buffer
            input_buffer = ""
            if msg.lower() == '/exit': # TODO: add support for esc key
                stdscr.nodelay(False)
                break
            elif msg.lower() == '/invite':
                stdscr.nodelay(False)
                invite_user(stdscr, room_id)
                stdscr.nodelay(True)
            else:
                # Add message to the room's message list
                api.send_message(room_id, current_user, msg)
        elif key in (8, 127):  # Backspace key
            input_buffer = input_buffer[:-1]
        elif key in (curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN):
            continue  # Ignore arrow keys for now
        else:
            input_buffer += chr(key)

# Main function to run the curses app
def main(stdscr: curses.window) -> None:
    global current_user
    curses.curs_set(0)
    users = db.get_users()
    if users:
        user_selection_screen(stdscr)
    else:
        signup_screen(stdscr)
    while run:
        main_menu(stdscr)

def start() -> None:
    curses.wrapper(main)
