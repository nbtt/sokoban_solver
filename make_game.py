# Usage:
# space: toggle pen up/pen down. default is pen up (green)
# arrow key (up/down/left/right) to move
# press number key to change the pen:
# 0: ground or nothing
# 1: wall
# 2: box
# 3: goal
# 4: box on goal
# 5: player
# 6: player on goal
# Enter: Save and exit

from os import system
from pynput import keyboard as K

def print_game():
    global is_pen_down, color_pre_down, color_pre_up, color_post, pen_x, pen_y, n_row, n_col
    system('cls')
    for i in range(n_row):
        if i != pen_x:
            print("".join(game[i]))
        else:
            print("".join(game[i][:pen_y]), 
                color_pre_down if is_pen_down else color_pre_up, game[i][pen_y], color_post, 
                "".join([] if pen_y == n_col - 1 else game[i][pen_y + 1:]), sep='')

def on_press(k):
    global is_pen_down, pen_x, pen_y, pen, pen_idx, game
    try:
        key_char = k.char
        if len(key_char) == 1 and '0' <= key_char <= '6':
            pen_idx = int(key_char)
    except AttributeError:
        if k == K.Key.up:
            if pen_x > 0:
                pen_x -= 1
        elif k == K.Key.down:
            if pen_x < n_row - 1:
                pen_x += 1
        elif k == K.Key.left:
            if pen_y > 0:
                pen_y -= 1
        elif k == K.Key.right:
            if pen_y < n_col - 1:
                pen_y += 1
        elif k == K.Key.space:
            is_pen_down = not is_pen_down
        elif k == K.Key.enter:
            f = open(file_name, 'w')
            f.write(str(n_row) + '\n' + str(n_col) + '\n')
            for i in range(n_row):
                f.write("".join(game[i]) + '\n')
            f.close()
            return False

    if is_pen_down:
        game[pen_x][pen_y] = pen[pen_idx]

    print_game()

if __name__ == "__main__":
    # _: ground or out of board
    # @: wall
    # +: box
    # o: goal
    # *: box on goal
    # i: player
    # $: player on goal
    global color_pre_up, color_pre_down, color_post, pen_x, pen_y, n_row, n_col, game
    pen = "_@+o*i$"
    is_pen_down = False
    pen_x = 0
    pen_y = 0
    pen_idx = 0
    color_pre_up = '\33[42m'
    color_pre_down = '\33[43m'
    color_post = '\33[0m'
    file_name = 'game_input.txt'
    n_row = int(input("Number of rows: "))
    n_col = int(input("Number of columns: "))

    game = []
    for _ in range(n_row):
        game.append(['_' for _ in range(n_col)])
    
    print_game()
 
    with K.Listener(on_press=on_press, suppress=True) as listener:
        listener.join()