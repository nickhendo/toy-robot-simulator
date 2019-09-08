import re
import tabulate
import logging

logging.basicConfig(level=logging.DEBUG)

class Robot(object):
    def __init__(self):  # , x_pos, y_pos, orientation):
        self.x_pos       = None
        self.y_pos       = None
        self.orientation = None
        self.placed      = False
        self.directions  = ["North", "East", "South", "West"]
        # self.board       = Board(5, 5)
        self.board_size  = (5, 5)
        # self.place(x_pos, y_pos, orientation)

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

    def turn(self, side):
        if side.lower() not in ['left', 'right']:
            return False
        increment = 1 if side.lower() == 'right' else -1
        cur = self.directions.index(self.orientation)
        new_cur = (cur + increment) % 4
        self.orientation = self.directions[new_cur]

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


def main():
    print("""Welcome to the Toy Robot Simulator, brought to you by NewsCorp!
This revolutionary new game allows you to control a virtual toy robot on a 5x5 grid. The accepted commands are:
      - PLACE X,Y,F     (Place the robot in position (X, Y) facing F (North, East, South or West)
      - MOVE            (Move the robot forward on the grid by one space)
      - LEFT            (Rotate the robot 90 degrees to the left (counter-clockwise)
      - RIGHT           (Rotate the robot 90 degrees to the right (clockwise)
      - REPORT          (This will return the current coordinated of the robot, and its orientation)
      - EXIT            (Exit the simulator)""")
    robert = Robot()
    while True:
        command = input("Command: ")
        # logging.debug(command)

        # Validate command
        # pattern = '^(PLACE|MOVE|LEFT|RIGHT|REPORT|EXIT)'
        # regex = re.search(pattern, command)
        # if regex is not None:
        #     return True
        # return False

        # Execute command
        
        place_pattern = '^PLACE\s+(\d),(\d),(NORTH|EAST|SOUTH|WEST)\s*$'
        move_pattern = '^MOVE\s*$'
        turn_pattern = '^(LEFT|RIGHT)\s*$'
        report_pattern = '^REPORT\s*$'
        exit_pattern = '^EXIT\s*$'
        help_pattern = '^HELP\s*$'

        # PLACE command
        place_result = re.search(place_pattern, command, re.IGNORECASE)
        if place_result:
            logging.info('PLACE detected')
            logging.debug(place_result.groups())
            x_pos, y_pos, orientation = place_result.groups()
            robert.place(int(x_pos), int(y_pos), orientation)
            continue
        
        # MOVE command
        move_result = re.search(move_pattern, command, re.IGNORECASE)
        if move_result:
            logging.info('MOVE detected')
            robert.move()
            continue

        # LEFT/RIGHT command
        turn_result = re.search(turn_pattern, command, re.IGNORECASE)
        if turn_result:
            logging.info(f'TURN {turn_result.group(1)} detected')
            robert.turn(turn_result.group(1))
            continue

        # REPORT command
        report_result = re.search(report_pattern, command, re.IGNORECASE)
        if report_result:
            logging.info(f'REPORT detected')
            robert.report()
            continue

        # EXIT command
        exit_result = re.search(exit_pattern, command, re.IGNORECASE)
        if exit_result:
            print("Hope you had a great time playing!")
            break

        # HELP command
        help_result = re.search(help_pattern, command, re.IGNORECASE)
        if help_result:
            print("""
      - PLACE X,Y,F     (Place the robot in position (X, Y) facing F (North, East, South or West)
      - MOVE            (Move the robot forward on the grid by one space)
      - LEFT            (Rotate the robot 90 degrees to the left (counter-clockwise)
      - RIGHT           (Rotate the robot 90 degrees to the right (clockwise)
      - REPORT          (This will return the current coordinated of the robot, and its orientation)
      - EXIT            (Exit the simulator)""")
            continue

        print('Oops, try again')


if __name__ == '__main__':
    main()
    print('Exiting...')
