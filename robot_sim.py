import re

from tabulate import tabulate


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
        """Converts a string to a class method and calls it

        Takes in a command as string, and calls the associated class method according to self.callable_methods

        Args:
            command: method to call as a string

        Returns:
            The result from the method that is called, or a message indicating the robot hasn't been placed yet
        """
        if None in (self.x_pos, self.y_pos, self.orientation):  # Check if robot already has co-ords
            return "Sorry, please PLACE the Robot before calling other commands. For help, type HELP."
        return self.callable_methods[command]()

    def validate(self, x_pos, y_pos):
        """Checks that co-ordinates are valid on the board

        Takes in x and y co-ordinates and checks that they are within the specified self.board_size

        Args:
            x_pos: integer x co-ordinate for the robot
            y_pos: integer y co-ordinate for the robot

        Returns:
            True or False depending on whether the supplied co-ordinates are valid
        """
        return x_pos in range(self.board_size[0]) and y_pos in range(self.board_size[1])

    def place(self, x_pos, y_pos, orientation):
        """Place the robot at a specific point on the board with a given orientation

        Takes in co-ordinates and sets the robot co-ordinates and orientation if they are valid

        Args:
            x_pos: integer x co-ordinate for the robot
            y_pos: integer y co-ordinate for the robot
            orientation: lowercase orientation of either north, east, south or west

        Returns:
            None if placed successfully, otherwise returns a string showing either the co-ordinates are not valid,
            or that the orientation is not valid
        """
        if not self.validate(x_pos, y_pos):
            return f"{x_pos, y_pos} not valid"
        if orientation not in self.directions:
            return f"{orientation} not valid"
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.orientation = orientation

    def left(self):
        """Rotate the robot 90 degrees to the left

        Sets the new orientation after rotating 90 degrees to the left. The next orientation after turning left, is one
        index less in self.directions, than the index of the current orientation. Taking '% 4' of the new index ensures
        that the index wraps when taking the orientation of -1. i.e. -1 % 4 is 3, so the orientation to the left of
        North, will be West.

        Returns:
            None

        """
        direction_pos = self.directions.index(self.orientation)
        new_direction_pos = (direction_pos - 1) % 4  # Left orientation is the index
        self.orientation = self.directions[new_direction_pos]

    def right(self):
        """Rotate the robot 90 degrees to the right

        Sets the new orientation after rotating 90 degrees to the right. The next orientation after turning right, is
        one index higher in self.directions, than the index of the current orientation. Taking '% 4' of the new index
        ensures that the index wraps when taking the 5th orientation. i.e. 5 % 4 is 0, so the orientation to the right
        of West, will be North.

        Returns:
            None

        """
        direction_pos = self.directions.index(self.orientation)
        new_direction_pos = (direction_pos + 1) % 4
        self.orientation = self.directions[new_direction_pos]

    def move(self):
        """Move the robot forward one space

        Adds/subtracts 1 to the x or y position of the robot, depending on its orientation

        Returns:
            None if moved successfully, returns a message if the move would send the robot off the edge.
        """
        # Find the current orientation and calculate the next position based off of it
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

        # If the new position is valid, set the co-ordinates to the new position
        if self.validate(new_x_pos, new_y_pos):
            self.x_pos = new_x_pos
            self.y_pos = new_y_pos
        else:
            return 'Sorry, don\'t want to fall off!'

    def report(self):
        """Return the co-ordinates and the orientation of the robot

        Returns:
            The x and y co-ordinates and the orientation in uppercase
        """
        return self.x_pos, self.y_pos, self.orientation.upper()

    def show(self):
        """Show the robot on the grid

        Returns:
            A tabulate string with the first letter of the orientation, located in the grid to show the robots position
        """
        grid = [[None for _ in range(self.board_size[0])] for _ in range(self.board_size[1])]
        grid[self.board_size[1] - 1 - self.y_pos][self.x_pos] = self.orientation[0].upper()
        return tabulate(grid, tablefmt='grid')

    def input_parser(self, command):
        """Parse the given command and perform actions accordingly

        Takes in the command, and performs the relevant logic

        Args:
            command: A string of the desired command

        Returns:
              None if the command was a PLACE command, otherwise the relevant return of the called command is returned.
              If a relevant command is not found, a string asking to try again, is returned.
        """
        # PLACE command
        # Check if the command is a PLACE command. If so, retrieve the co-ordinates and orientation to pass
        place_pattern = r'^PLACE\s+(\d),(\d),(NORTH|EAST|SOUTH|WEST)\s*$'
        place_result = re.search(place_pattern, command, re.IGNORECASE)
        if place_result:
            x_pos, y_pos, orientation = place_result.groups()
            self.place(int(x_pos), int(y_pos), orientation.lower())
            return

        # Robot commands
        # Check if the command is one of the remaining commands and calls the relevant method
        pattern = r'^(MOVE|LEFT|RIGHT|REPORT|SHOW)\s*$'
        result = re.search(pattern, command, re.IGNORECASE)
        if result:
            return self.call_method(result.group(1).lower())

        return 'Oops, try again'


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

        # EXIT command
        # Exit the program if EXIT is entered
        exit_pattern = r'^EXIT\s*$'
        exit_result = re.search(exit_pattern, command, re.IGNORECASE)
        if exit_result:
            print("Hope you had a great time playing!")
            break

        # HELP command
        # Show the HELP dialog if HELP is given as a command
        help_pattern = r'^HELP\s*$'
        help_result = re.search(help_pattern, command, re.IGNORECASE)
        if help_result:
            print_help()
            continue

        # Parse the command
        output = robert.input_parser(command)
        if output:
            print(output)  # If the command returns a string, print it


if __name__ == '__main__':
    main()
    print('Exiting...')
