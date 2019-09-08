import pytest

import robot_sim


@pytest.mark.parametrize("x,y", [('1', 3), (7, 2), (-1, 2), (None, list)])
def test_invalid_pos(x, y):
    robot = robot_sim.Robot()
    assert robot.validate(x, y) is False


@pytest.mark.parametrize("x,y", [(0, 0), (2, 3), (4, 4)])
def test_valid_pos(x, y):
    robot = robot_sim.Robot()
    assert robot.validate(x, y) is True


@pytest.mark.parametrize("x,y,orientation", [(0, 0, "north"), (3, 4, "west"), (4, 4, "south"), (2, 1, "east")])
def test_valid_place(x, y, orientation):
    robot = robot_sim.Robot()
    robot.place(x, y, orientation)
    assert (robot.x_pos, robot.y_pos, robot.orientation) == (x, y, orientation.lower())


@pytest.mark.parametrize("x,y,orientation", [(-1, 0, "north"), (10, 4, "west"), (4, 4, "fake")])
def test_invalid_place(x, y, orientation):
    robot = robot_sim.Robot()
    robot.place(0, 0, "north")
    robot.place(x, y, orientation)
    assert (robot.x_pos, robot.y_pos, robot.orientation) == (0, 0, "north")


@pytest.mark.parametrize("x,y,orientation,expected", [(0, 0, "north", (0, 2, "north")), (2, 3, "east", (4, 3, "east"))])
def test_move(x, y, orientation, expected):
    robot = robot_sim.Robot()
    robot.place(x, y, orientation)
    robot.move()
    robot.move()
    assert (robot.x_pos, robot.y_pos, robot.orientation) == expected


@pytest.mark.parametrize("starting,expected", [("north", "west"), ("south", "east"), ("east", "north")])
def test_left(starting, expected):
    robot = robot_sim.Robot()
    robot.place(0, 0, starting)
    robot.left()
    assert robot.orientation == expected


@pytest.mark.parametrize("starting,expected", [("north", "east"), ("south", "west"), ("east", "south")])
def test_right(starting, expected):
    robot = robot_sim.Robot()
    robot.place(0, 0, starting)
    robot.right()
    assert robot.orientation == expected


@pytest.mark.parametrize("bad_command", ["0", "None", "Bad command", r"{}, \r"])
def test_bad_commands(bad_command):
    robot = robot_sim.Robot()
    assert robot.input_parser(bad_command) == "Oops, try again"


@pytest.mark.parametrize("x,y,orientation", [(4, 4, "north"), (0, 3, "west"), (4, 2, "east"), (0, 0, "south")])
def test_off_grid(x, y, orientation):
    robot = robot_sim.Robot()
    robot.place(x, y, orientation)
    assert robot.move() == "Sorry, don't want to fall off!"


def test_multi_place():
    robot = robot_sim.Robot()
    robot.place(3, 3, "east")
    robot.place(4, 2, "north")
    robot.place(2, 1, "bad orientation")
    assert (robot.x_pos, robot.y_pos, robot.orientation) == (4, 2, "north")


###############################
# Tests given as part of task #
###############################
def test_scenario_1():
    robot = robot_sim.Robot()
    robot.input_parser("PLACE 0,0,NORTH")
    robot.input_parser("MOVE")
    assert robot.input_parser("REPORT") == (0, 1, "NORTH")


def test_scenario_2():
    robot = robot_sim.Robot()
    robot.input_parser("PLACE 0,0,NORTH")
    robot.input_parser("LEFT")
    assert robot.input_parser("REPORT") == (0, 0, "WEST")


def test_scenario_3():
    robot = robot_sim.Robot()
    robot.input_parser("PLACE 1,2,EAST")
    robot.input_parser("MOVE")
    robot.input_parser("MOVE")
    robot.input_parser("LEFT")
    robot.input_parser("MOVE")
    assert robot.input_parser("REPORT") == (3, 3, "NORTH")
