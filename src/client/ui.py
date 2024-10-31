import curses

import api as api
import db as db

current_user = None
run = True

# Function to draw the sign-up screen
def signup_screen(stdscr: curses.window) -> bool:
    global current_user
    stdscr.clear()
    stdscr.addstr("hello~\n")
    stdscr.addstr("Enter your username: ")
    curses.echo()
    username = stdscr.getstr().decode('utf-8')
    curses.noecho()
    # operations
    api.signup(username)
    current_user = username
    return True

# Function to draw the main menu
def main_menu(stdscr: curses.window) -> None:
    global run
    while True:
        stdscr.clear()
        stdscr.addstr(f"Welcome {current_user}\n")
        stdscr.addstr("\n")
        stdscr.addstr("Rooms\n")
        # list rooms
        rooms = api.get_rooms()[:10]
        if rooms:
            for i in range(len(rooms)):
                stdscr.addstr(f"({i}) {rooms[i]}\n")
        else:
            stdscr.addstr("(empty) \n")
        stdscr.addstr("\n")
        stdscr.addstr("Actions\n")
        stdscr.addstr("(c) Create Room\n")
        stdscr.addstr("(q) Exit\n")
        stdscr.addstr("\n")
        stdscr.addstr("Select an option: ")

        option = stdscr.getch()

        if option == ord('c'):
            create_room(stdscr)
        elif option == ord('q'):
            run = False
            break
        elif ord('0') <= option <= ord('9') and option - ord('0') < len(rooms):
            enter_room(stdscr, rooms[option - ord('0')])

# Function to create a room
def create_room(stdscr: curses.window) -> None:
    stdscr.clear()
    stdscr.addstr("Create room\n")
    stdscr.addstr("Enter room name: ")
    curses.echo()
    room_name = stdscr.getstr().decode('utf-8')
    curses.noecho()
    api.create_room(room_name)
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
    while True:
        stdscr.clear()
        stdscr.addstr(f"Room: {room_id}\n")
        stdscr.addstr("Messages:\n")
        
        # Display messages
        messages = db.get_messages(room_id)
        for message in messages[-10:]:  # Show last 10 messages
            stdscr.addstr(message + "\n")

        # Input prompt for new message
        stdscr.addstr("\n====================\n")
        stdscr.addstr("/exit", curses.A_BOLD)
        stdscr.addstr(" to exit the room\n")
        stdscr.addstr("/invite", curses.A_BOLD)
        stdscr.addstr(" to invite a user to the room\n")
        stdscr.addstr(": ")
        curses.echo()
        msg = stdscr.getstr().decode('utf-8')
        curses.noecho()

        if msg.lower() == '/exit':
            break
        elif msg.lower() == '/invite':
            invite_user(stdscr, room_id)
        else:
            # Add message to the room's message list
            api.send_message(room_id, msg)

# Main function to run the curses app
def main(stdscr: curses.window) -> None:
    global current_user
    curses.curs_set(0)
    current_user = db.get_username()
    while run:
        if not current_user:
            if signup_screen(stdscr):
                main_menu(stdscr)
        else:
            main_menu(stdscr)

def start() -> None:
    curses.wrapper(main)
