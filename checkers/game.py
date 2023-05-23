import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init() #private constructor 
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None #if there is a selected piece or not selected yet 
        self.board = Board() #instance of the board 
        self.turn = RED
        self.valid_moves = {} #dictionary of open list (forienter ) for next available moves

    def winner(self):
        return self.board.winner()

    def reset(self):  #reset the game state make start again (in case of player is playing against the agent)
        self._init()

    def select(self, row, col):    # select the piece 
        if self.selected:
            result = self._move(row, col)  #awel ma a select ay piece ha3mlha move ll row we column el selected brdu ely na 3ayzo 
            if not result:
                self.selected = None
                self.select(row, col) # htb2a haga zy recursuive function akeeny dost 3la piece tanya aslun mynf3sh ados 3leha ma hy re select el piece
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col): #private move function LEHA MOVE AW LAA check if the piece has a move or not 
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):   #just to change the turns by the color of the piece to make it valid to move
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self): 
        return self.board

    def ai_move(self, board): #ai agent itself to change turn
        self.board = board
        self.change_turn()