from Menu import LoadMenu
from src.parser import *
from src.chomsky import *


if __name__ == '__main__':
    '''print("hello")
    load_menu = LoadMenu()
    cfg = load_menu.load_cfg()
    print(cfg)
    cfg = CFG()
    parse_file(cfg, "test.txt")
    print(cfg)'''
    var = [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]]
    var2 = 1
    print(solution(var, 1))
