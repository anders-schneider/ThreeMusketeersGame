# The Three Musketeers Game
# by Selah Lynch and Anders Schneider

# In all methods,
#   A 'location' is a two-tuple of integers, each in the range 0 to 4.
#        The first integer is the row number, the second is the column number.
#   A 'direction' is one of the strings "up", "down", "left", or "right".
#   A 'board' is a list of 5 lists, each containing 5 strings: "M", "R", or "-".
#        "M" = Musketeer, "R" = Cardinal Richleau's man, "-" = empty.
#        Each list of 5 strings is a "row"
#   A 'player' is one of the strings "M" or "R" (or sometimes "-").
#
# For brevity, Cardinal Richleau's men are referred to as "enemy".
# 'pass' is a no-nothing Python statement. Replace it with actual code.


def create_board():
    global board
    """Creates the initial Three Musketeers board. 'M' represents
    a Musketeer, 'R' represents one of Cardinal Richleau's men,
    and '-' denotes an empty space."""
    m = 'M'
    r = 'R'
    board = [ [r, r, r, r, m],
              [r, r, r, r, r],
              [r, r, m, r, r],
              [r, r, r, r, r],
              [m, r, r, r, r] ]


def set_board(new_board):
    """Replaces the global board with new_board."""
    global board
    board = new_board


def get_board():
    """Just returns the board. Possibly useful for unit tests."""
    return board


def string_to_location(s):
    """Given a two-character string (such as 'A5') return the designated
       location as a 2-tuple (such as (0, 4))."""
    assert s[0] >= 'A' and s[0] <= 'E'
    assert s[1] >= '1' and s[1] <= '5'
    x = ord(s[0])-ord('A')
    y = ord(s[1])-ord('1')
    return x, y


def location_to_string(location):
    """Return the string representation of a location."""
    assert location[0] >= 0 and location[0] <= 4
    assert location[1] >= 0 and location[1] <= 4
    x = chr(location[0] + ord('A'))
    y = chr(location[1] + ord('1'))
    return x + y


def at(location):
    """Returns the contents of the board at the given location."""
    #location defined as (down, across)
    return board[location[0]][location[1]]


def all_locations():
    """Returns a list of all 25 locations on the board."""
    locations_list = [0]*25
    for i in range(5):
        for j in range(5):
            locations_list[5*i + j] = (i, j)
    return locations_list


def adjacent_location(location, direction):
    """Return the location next to the given one, in the given direction.
       Does not check if the location returned is legal on a 5x5 board."""
    (row, column) = location
    if direction == "right":
        column += 1
    if direction == "left":
        column -= 1
    if direction == "down":
        row += 1
    if direction == "up":
        row -= 1
    return row, column


def is_legal_move_by_musketeer(location, direction):
    """Tests if the Musketeer at the location can move in the direction."""
    assert at(location) == 'M'
    return is_within_board(location, direction) and at(adjacent_location(location, direction)) == 'R'


def is_legal_move_by_enemy(location, direction):
    """Tests if the enemy at the location can move in the direction."""
    assert at(location) == 'R'
    return is_within_board(location, direction) and at(adjacent_location(location, direction)) == '-'


def is_legal_move(location, direction):
    """Tests whether it is legal to move the piece at the location
    in the given direction."""
    if at(location) == 'M':
        return is_legal_move_by_musketeer(location, direction)
    elif at(location) == 'R':
        return is_legal_move_by_enemy(location, direction)
    else:
        return False


def has_some_legal_move_somewhere(who):
    """Tests whether a legal move exists for player "who" (which must
    be either 'M' or 'R'). Does not provide any information on where
    the legal move is."""

    return len(all_possible_moves_for(who)) > 0


def possible_moves_from(location):
    """Returns a list of directions ('left', etc.) in which it is legal
       for the player at location to move. If there is no player at
       location, returns the empty list, []."""
    possible_moves = []
    for direction in ["up", "down", "left", "right"]:
        if is_legal_move(location, direction):
            possible_moves.append(direction)
    return possible_moves


def can_move_piece_at(location):
    """Tests whether the player at the location has at least one move available."""
    return len(possible_moves_from(location)) > 0


def is_legal_location(location):
    """Tests if the location is legal on a 5x5 board."""
    is_y_legal = 0 <= location[0] and location[0] <= 4
    is_x_legal = 0 <= location[1] and location[1] <= 4
    return is_y_legal and is_x_legal


def is_within_board(location, direction):
    """Tests if the move stays within the boundaries of the board."""
    test_location = adjacent_location(location, direction)
    return is_legal_location(test_location)


def all_possible_moves_for(player):
    """Returns every possible move for the player ('M' or 'R') as a list
       (location, direction) tuples."""
    list_of_moves = []
    locations_list = all_locations_for(player)
    for location in locations_list:
        if can_move_piece_at(location):
            for move_direction in possible_moves_from(location):
                list_of_moves.append((location, move_direction))
    return list_of_moves


def all_locations_for(who):
    """returns a list of locations"""
    locations_list = []
    for y in range(0, 4+1):
        for x in range(0, 4+1):
            if board[y][x] == who:
                locations_list.append((y, x))
    return locations_list


def make_move(location, direction):
    """Moves the piece in location in the indicated direction."""
    who = at(location)
    my_board = get_board()
    my_board[location[0]][location[1]] = '-'
    new_location = adjacent_location(location, direction)
    my_board[new_location[0]][new_location[1]] = who
    set_board(my_board)


def choose_computer_move(who):
    """The computer chooses a move for a Musketeer (who = 'M') or an
       enemy (who = 'R') and returns it as the tuple (location, direction),
       where a location is a (row, column) tuple as usual."""

    #The strategy for R is to move a piece to the right, if possible
    if who == 'R':
        for move in all_possible_moves_for(who):
            if move[1] == 'right':
                return move

    #The strategy for M is to reject a move if it would result in two M's being in the same row or column
    elif who == 'M':
        for move in all_possible_moves_for(who):

            is_rejected = False
            for ally_location in all_locations_for(who):
                if move[0] == ally_location:
                    continue
                elif adjacent_location(move[0], move[1])[0] == ally_location[0] or adjacent_location(move[0], move[1])[1] == ally_location[1]:
                    is_rejected = True

            if not is_rejected:
                return move

    #If the strategy is impossible to implement, the computer chooses the first move in its list of possible moves
    return all_possible_moves_for(who)[0]


def is_enemy_win():
    """Returns True if all 3 Musketeers are in the same row or column."""
    muskateers = all_locations_for('M')
    y_positions_match = muskateers[0][0] == muskateers[1][0] == muskateers[2][0]
    x_positions_match = muskateers[0][1] == muskateers[1][1] == muskateers[2][1]
    return y_positions_match or x_positions_match


#---------- Communicating with the user ----------

def print_board():
    print "    1  2  3  4  5"
    print "  ---------------"
    ch = "A"
    for i in range(0, 5):
        print ch, "|",
        for j in range(0, 5):
            print board[i][j] + " ",
        print
        ch = chr(ord(ch) + 1)
    print


def print_instructions():
    print
    print """To make a move, enter the location of the piece you want to move,
and the direction you want it to move. Locations are indicated as a
letter (A, B, C, D, or E) followed by an integer (1, 2, 3, 4, or 5).
Directions are indicated as left, right, up, or down (or simply L, R,
U, or D). For example, to move the Musketeer from the top right-hand
corner to the row below, enter 'A5 left' (without quotes).

For convenience in typing, you may use lowercase letters."""
    print


def choose_users_side():
    """Returns 'M' if user is playing Musketeers, 'R' otherwise."""
    user = ""
    while user != 'M' and user != 'R':
        answer = raw_input("Would you like to play Musketeer (M) or enemy (R)? ")
        answer = answer.strip()
        if answer != "":
            user = answer.upper()[0]
    return user


def get_users_move():
    """Gets a legal move from the user, and returns it as a
       (location, direction) tuple."""
    directions = {'L':'left', 'R':'right', 'U':'up', 'D':'down'}
    move = raw_input("Your move? ").upper().replace(' ', '')
    #check if less than 3 characters
    try:
        if move[0] in 'ABCDE' and move[1] in '12345' and move[2] in 'LRUD':
            location = string_to_location(move[0:2])
            direction = directions[move[2]]
            if is_legal_move(location, direction):
                return (location, direction)
    except IndexError:
        pass
    print "Illegal move--'" + move + "'"
    print_instructions()
    return get_users_move()


def move_musketeer(users_side):
    """Gets the Musketeer's move (from either the user or the computer)
       and makes it."""
    if users_side == 'M':
        (location, direction) = get_users_move()
        if at(location) == 'M':
            if is_legal_move(location, direction):
                make_move(location, direction)
                describe_move("Musketeer", location, direction)
        else:
            print "You can't move there!"
            return move_musketeer(users_side)
    else: # Computer plays Musketeer
        (location, direction) = choose_computer_move('M')         
        make_move(location, direction)
        describe_move("Musketeer", location, direction)


def move_enemy(users_side):
    """Gets the enemy's move (from either the user or the computer)
       and makes it."""
    if users_side == 'R':
        (location, direction) = get_users_move()
        if at(location) == 'R':
            if is_legal_move(location, direction):
                make_move(location, direction)
                describe_move("Enemy", location, direction)
        else:
            print "You can't move there!"
            return move_enemy(users_side)
    else: # Computer plays enemy
        (location, direction) = choose_computer_move('R')         
        make_move(location, direction)
        describe_move("Enemy", location, direction)
        return board


def describe_move(who, location, direction):
    """Prints a sentence describing the given move."""
    new_location = adjacent_location(location, direction)
    print who, 'moves', direction, 'from',\
          location_to_string(location), 'to',\
          location_to_string(new_location) + ".\n"


def start():
    """Plays the Three Musketeers Game."""
    users_side = choose_users_side()
    board = create_board()
    print_instructions()
    print_board()
    while True:
        if has_some_legal_move_somewhere('M'):
            board = move_musketeer(users_side)
            print_board()
            if is_enemy_win():
                print "Cardinal Richleau's men win!"
                break
        else:
            print "The Musketeers win!"
            break
        if has_some_legal_move_somewhere('R'):
            board = move_enemy(users_side)
            print_board()
        else:
            print "The Musketeers win!"
            break
