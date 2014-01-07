"""START NEW GAME"""
from xmn import damas

if __name__ == "__main__":
    damas = damas.game()
    damas.game_play(damas.strategy_input, damas.strategy_input)
