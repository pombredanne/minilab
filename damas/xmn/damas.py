"""
DAMAS GAME

INSTRUCTIONS
PLAYER1
PLAYER2
"""
from xmn import player

class game:
    """INVENTORY"""
    players = []
    other   = {}
    p_name  = []
    square = 8
    vertical_key   = [x for x in 'ABCDEFGH']
    horizontal_key = [x for x in '12345678']
    
    def __init__(self):
        pass
    
    """CREATION BOARD STRUCTURE"""
    board_key = [v+h for v in vertical_key for h in horizontal_key]
    
    """BOARD EMPTY"""
    board  = dict((n, '.') for n in board_key)
    
    """BOARD VIEW"""
    def view_board(self):
        print '  ' + ''.join(self.horizontal_key)
        
        for keyV in self.vertical_key:
            line = keyV + ' '
            for keyH in self.horizontal_key:
                line += self.board[keyV+keyH]
            print line
    
    """NEW GAME"""
    def new_game(self):
        for keyV in self.vertical_key[0:2]:
            for keyH in self.horizontal_key:
                self.board[keyV+keyH] = self.players[0].initial
    
        for keyV in self.vertical_key[-2:]:
            for keyH in self.horizontal_key:
                self.board[keyV+keyH] = self.players[1].initial
                
    """VERIFY LEGAL MOVE"""
    def legal_move(self, p, initiate, destiny):
        if self.board[initiate] != self.players[p].initial:
            return False
        if self.board[destiny] != '.':
            return False
        
        v = [] #LETTER
        h = [] #NUMBER
        
        v[0] = self.vertical_key.index(initiate[0])
        h[0] = self.horizontal_key.index(initiate[1])
        
        v[1] = self.vertical_key.index(destiny[0])
        h[1] = self.horizontal_key.index(destiny[1])
        
        if abs(v[0] - v[1]) > 3:
            return False 
        return True
    
    """MOVE PIECE"""
    def move_piece(self, p, initiate, destiny):
        if not self.legal_move(p, initiate, destiny):
            raise Exception('ILLEGAL-MOVE')
        v = [], h = []
        
        v[0] = self.vertical_key.index(initiate[0])
        h[0] = self.horizontal_key.index(initiate[1])
        
        v[1] = self.vertical_key.index(destiny[0])
        h[1] = self.horizontal_key.index(destiny[1])
              
        self.board[initiate] = '.'
        self.board[destiny]  = self.players[p].initial
    
    """STRATEGY INPUT"""
    def strategy_input(self, p):
        msg = 'Player %s move:'
        player_name = self.players[p].name
        while True:
            try:
                move = raw_input(msg % player_name).upper().split(',')
                
                if len(move) != 2:
                    raise Exception('I-GIVE-UP')
                
                self.move_piece(p, move[0], move[1])
                return
            except Exception as ex:
                if 'I-GIVE-UP' in ex:
                    ans = raw_input('Are you sure you wanna give up? (s/n) :')
                    if ans == 's':
                        raise Exception('I-GIVE-UP')
                    
                    msg = 'Player %s move:'
                elif 'ILLEGAL-MOVE' in ex:
                    msg = 'You do a illegal move. Player %s try again:'
                else:
                    print ex
        
    
    """GAME PLAY"""
    def game_play(self, player1, player2):
        p1 = player.new(player1, 0, raw_input('Player 1\'s name:').upper())
        p2 = player.new(player2, 1, raw_input('Player 2\'s name:').upper())
        
        self.players = [p1, p2]
        self.other = {0:1, 1:0}
        
        self.new_game()
        self.view_board()
        p = 0
        while True:
            try:
                self.players[p].action(p)
                self.view_board()
                p = self.other[p]
            except Exception as ex:
                if 'I-GIVE-UP' in ex:
                    print 'Player %s winner!' % self.other[p]
                    return
                print ex
