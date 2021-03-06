from Menu import LoadMenu
from src.parser import *

if __name__ == '__main__':
    print("hello")
    load_menu = LoadMenu()
    cfg = load_menu.load_cfg()
    print(cfg)
    '''cfg = CFG()
    parse_file(cfg, "test.txt")
    print(cfg)'''
