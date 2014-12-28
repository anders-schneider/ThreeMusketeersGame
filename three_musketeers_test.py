import unittest
from three_musketeers import *

left = 'left'
right = 'right'
up = 'up'
down = 'down'
M = 'M'
R = 'R'
_ = '-'


class TestThreeMusketeers(unittest.TestCase):

    def setUp(self):
        set_board([ [_, _, _, M, _],
                    [_, _, R, M, _],
                    [_, R, M, R, _],
                    [_, R, _, _, _],
                    [_, _, _, R, _] ])

    def test_create_board(self):
        create_board()
        self.assertEqual(at((0, 0)), 'R')
        self.assertEqual(at((0, 4)), 'M')

    def test_set_board(self):
        #the set_board function is defined in test file and run automatically
        self.assertEqual(at((0, 0)), '-')
        self.assertEqual(at((1, 2)), 'R')
        self.assertEqual(at((1, 3)), 'M')

    def test_get_board(self):
        self.assertEqual([ [_, _, _, M, _],
                           [_, _, R, M, _],
                           [_, R, M, R, _],
                           [_, R, _, _, _],
                           [_, _, _, R, _] ],
                         get_board())

    def test_string_to_location(self):
        self.assertEqual(string_to_location("A5"), (0, 4))
        self.assertEqual(string_to_location("C2"), (2, 1))

    def test_location_to_string(self):
        self.assertEqual(location_to_string((4,1)), "E2")
        self.assertEqual(location_to_string((2,0)), "C1")

    def test_at(self):
        self.assertEqual(at((0, 0)), '-')
        self.assertEqual(at((1, 2)), 'R')
        self.assertEqual(at((1, 4)), '-')

    def test_all_locations(self):
        self.assertEqual(all_locations()[0], (0, 0))
        self.assertEqual(all_locations()[7], (1, 2))
        self.assertEqual(all_locations()[20], (4, 0))

    def test_adjacent_location(self):
        self.assertEqual(adjacent_location((3, 2), right), (3, 3))
        self.assertEqual(adjacent_location((0, 2), down), (1, 2))
        self.assertEqual(adjacent_location((1, 1), up), (0, 1))

    def test_is_legal_move_by_musketeer(self):
        self.assertEqual(is_legal_move_by_musketeer((0, 3), up), False)
        self.assertEqual(is_legal_move_by_musketeer((1, 3), left), True)
        self.assertEqual(is_legal_move_by_musketeer((2, 2), down), False)

    def test_is_legal_move_by_enemy(self):
        self.assertEqual(is_legal_move_by_enemy((1, 2), right), False)
        self.assertEqual(is_legal_move_by_enemy((1, 2), up), True)
        self.assertEqual(is_legal_move_by_enemy((4, 3), down), False)

    def test_is_legal_move(self):
        self.assertEqual(is_legal_move((1, 2), right), False)
        self.assertEqual(is_legal_move((1, 0), right), False)
        self.assertEqual(is_legal_move((3, 1), left), True)
        self.assertEqual(is_legal_move((2, 2), right), True)

    def test_has_some_legal_move_somewhere(self):
        set_board([ [_, _, _, M, _],
                    [_, R, _, M, _],
                    [_, _, M, _, R],
                    [_, R, _, _, _],
                    [_, _, _, R, _] ] )
        self.assertFalse(has_some_legal_move_somewhere('M'))
        self.assertTrue(has_some_legal_move_somewhere('R'))

    def test_possible_moves_from(self):
        set_board([ [_, _, _, M, R],
                    [_, _, _, M, M],
                    [_, _, R, _, _],
                    [_, _, _, _, _],
                    [_, _, _, _, _] ] )
        self.assertEqual(possible_moves_from((2, 2)), ["up", "down", "left", "right"])
        self.assertEqual(possible_moves_from((1, 3)), [])
        self.assertEqual(possible_moves_from((1, 4)), ["up"])

    def test_can_move_piece_at(self):
        set_board([ [_, _, _, M, R],
                    [_, _, _, M, M],
                    [_, _, R, _, _],
                    [_, _, _, _, _],
                    [_, _, _, _, _] ] )
        self.assertEqual(can_move_piece_at((2, 2)), True)
        self.assertEqual(can_move_piece_at((1, 3)), False)
        self.assertEqual(can_move_piece_at((1, 4)), True)

    def test_is_legal_location(self):
        self.assertEqual(is_legal_location((1, 3)), True)
        self.assertEqual(is_legal_location((5, 3)), False)

    def test_is_within_board(self):
        self.assertEqual(is_within_board((0, 0), up), False)
        self.assertEqual(is_within_board((0, 0), down), True)

    def test_all_possible_moves_for(self):
        set_board([ [_, _, R, M, R],
                    [_, _, _, M, M],
                    [_, _, _, _, _],
                    [_, _, _, _, _],
                    [_, _, _, _, _] ] )
        self.assertEqual(all_possible_moves_for('M'), [((0, 3), "left"),
                                                       ((0, 3), "right"),
                                                       ((1, 4), "up")])
        self.assertEqual(all_possible_moves_for('R'), [((0, 2), "down"),
                                                       ((0, 2), "left")])

    def test_all_locations_for(self):
        set_board([ [_, _, R, M, R],
                    [_, _, _, M, M],
                    [_, _, _, _, _],
                    [_, _, _, _, _],
                    [_, _, _, _, _] ] )
        self.assertEqual(all_locations_for(M), [(0, 3), (1, 3), (1, 4)])
        self.assertEqual(all_locations_for(R), [(0, 2), (0, 4)])

    def test_make_move(self):
        set_board([ [_, _, R, M, R],
                    [_, _, _, M, M],
                    [_, _, _, _, _],
                    [_, _, _, _, _],
                    [_, _, _, _, _] ])
        make_move((0, 2), "down")
        self.assertEqual(get_board(),
                  [ [_, _, _, M, R],
                    [_, _, R, M, M],
                    [_, _, _, _, _],
                    [_, _, _, _, _],
                    [_, _, _, _, _] ])

    def test_choose_computer_move(self):
        self.assertEqual(choose_computer_move(M), ((2,2),'left'))
        self.assertEqual(choose_computer_move(R), ((2,3),'right'))

    def test_is_enemy_win(self):
        set_board([ [_, _, R, M, R],
                    [_, _, _, M, M],
                    [_, _, _, _, _],
                    [_, _, _, _, _],
                    [_, _, _, _, _] ])
        self.assertEqual(is_enemy_win(), False)

        set_board([ [_, _, R, M, R],
                    [_, _, _, M, _],
                    [_, _, _, M, _],
                    [_, _, _, _, _],
                    [_, _, _, _, _] ])
        self.assertEqual(is_enemy_win(), True)


unittest.main()
