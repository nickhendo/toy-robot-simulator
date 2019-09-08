import re
import logging

from tabulate import tabulate

logging.basicConfig(level=logging.DEBUG)


class Robot(object):
    def __init__(self):  # , x_pos, y_pos, orientation):
        self.x_pos = None
        self.y_pos = None
        self.orientation = None
        self.placed = False
        self.directions = ["north", "east", "south", "west"]
        self.board_size = (5, 5)
        self.callable_methods = {
            'move': self.move,
            'left': self.left,
            'right': self.right,
            'report': self.report,
            'show': self.show,
        }

    def call_method(self, command):
        if None in (self.x_pos, self.y_pos, self.orientation):
            print("Sorry, please PLACE the Robot before calling other commands. For help type HELP.")
            return False
        return self.callable_methods[command]()

    def validate(self, x_pos, y_pos):
        return x_pos in range(self.board_size[0]) and y_pos in range(self.board_size[1])

    def place(self, x_pos, y_pos, orientation):
        if not self.validate(x_pos, y_pos):
            logging.warning(f"{x_pos, y_pos} not valid")
            return False
        # if not self.board.on_board(x_pos, y_pos):
        #     return False
        if orientation not in self.directions:
            logging.warning(f"{orientation} not valid")
            return False
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.orientation = orientation
        return True

    def left(self):
        direction_pos = self.directions.index(self.orientation)
        new_direction_pos = (direction_pos - 1) % 4
        self.orientation = self.directions[new_direction_pos]

    def right(self):
        direction_pos = self.directions.index(self.orientation)
        new_direction_pos = (direction_pos + 1) % 4
        self.orientation = self.directions[new_direction_pos]

    def move(self):
        facing = self.orientation.lower()
        new_x_pos = self.x_pos
        new_y_pos = self.y_pos
        if facing == 'north':
            new_y_pos += 1
        elif facing == 'south':
            new_y_pos -= 1
        elif facing == 'east':
            new_x_pos += 1
        elif facing == 'west':
            new_x_pos -= 1
        else:
            raise AttributeError(f"{facing} not a valid orientation")
        if self.validate(new_x_pos, new_y_pos):
            self.x_pos = new_x_pos
            self.y_pos = new_y_pos
        else:
            print('Sorry, don\'t want to fall off!')

    def report(self):
        print(self.x_pos, self.y_pos, self.orientation)
        return self.x_pos, self.y_pos, self.orientation

    def show(self):
        grid = [[None for _ in range(self.board_size[0])] for _ in range(self.board_size[1])]
        grid[self.board_size[1] - 1 - self.y_pos][self.x_pos] = self.orientation[0].upper()
        print(tabulate(grid, tablefmt='grid'))


def print_help():
    print("""Welcome to the Toy Robot Simulator, brought to you by NewsCorp!
This revolutionary new game allows you to control a virtual toy robot on a 5x5 grid. The accepted commands are:
      - PLACE X,Y,F     (Place the robot in position (X, Y) facing F (North, East, South or West)
      - MOVE            (Move the robot forward on the grid by one space)
      - LEFT            (Rotate the robot 90 degrees to the left (counter-clockwise)
      - RIGHT           (Rotate the robot 90 degrees to the right (clockwise)
      - REPORT          (This will return the current coordinated of the robot, and its orientation)
      - SHOW            (Show the robot location on a grid)
      - HELP            (Show this help dialog)
      - EXIT            (Exit the simulator)""")


def main():
    print_help()
    robert = Robot()
    while True:
        command = input("Command: ")

        # PLACE command
        place_pattern = r'^PLACE\s+(\d),(\d),(NORTH|EAST|SOUTH|WEST)\s*$'
        place_result = re.search(place_pattern, command, re.IGNORECASE)
        if place_result:
            x_pos, y_pos, orientation = place_result.groups()
            robert.place(int(x_pos), int(y_pos), orientation.lower())
            continue

        # Robot commands
        pattern = r'^(MOVE|LEFT|RIGHT|REPORT|SHOW)\s*$'
        result = re.search(pattern, command, re.IGNORECASE)
        if result:
            robert.call_method(result.group(1).lower())
            continue

        # EXIT command
        exit_pattern = r'^EXIT\s*$'
        exit_result = re.search(exit_pattern, command, re.IGNORECASE)
        if exit_result:
            print("Hope you had a great time playing!")
            break

        # HELP command
        help_pattern = r'^HELP\s*$'
        help_result = re.search(help_pattern, command, re.IGNORECASE)
        if help_result:
            print_help()
            continue

        print('Oops, try again')


if __name__ == '__main__':
    main()
    print('Exiting...')
