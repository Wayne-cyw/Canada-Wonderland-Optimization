from pick import pick
import curses
import time

def ascii_art():
    """
    Prints the ASCII art of the application name and waits for 2.5 seconds.
    """
    print('''
__        __              _           _                 _ 
\ \      / /__  _ __   __| | ___ _ __| | __ _ _ __   __| |
 \ \ /\ / / _ \| '_ \ / _` |/ _ \ '__| |/ _` | '_ \ / _` |
  \ V  V / (_) | | | | (_| |  __/ |  | | (_| | | | | (_| |
  _\_/\_/ \___/|_| |_|\__,_|\___|_|  |_|\__,_|_| |_|\__,_|
 / _ \ _ __ | |_(_)_ __ ___ (_)______ _| |_(_) ___  _ __  
| | | | '_ \| __| | '_ ` _ \| |_  / _` | __| |/ _ \| '_ \ 
| |_| | |_) | |_| | | | | | | |/ / (_| | |_| | (_) | | | |
 \___/| .__/ \__|_|_| |_| |_|_/___\__,_|\__|_|\___/|_| |_|
|  _ \|_|__ ___   __ _ _ __ __ _ _ __ ___                 
| |_) | '__/ _ \ / _` | '__/ _` | '_ ` _ \                
|  __/| | | (_) | (_| | | | (_| | | | | | |               
|_|   |_|  \___/ \__, |_|  \__,_|_| |_| |_|               
                 |___/                                    
    ''')
    time.sleep(2.5)

def select_rides_2(*columns: list) -> list:
    """
    Allows the user to select rides from multiple columns using a curses-based menu.
    each column should be a list, it should be a sorted base on the area of wonderland
    """
    COL_WIDTH = 25

    def _menu(stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # highlighted
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # selected

        title = "Select the rides you want to visit"

        cur_col, cur_row = 0, 0
        selected = set()  # stores (col_idx, row_idx) tuples where row_idx is 0-based into items (col[1:])

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, title, curses.A_BOLD)
            stdscr.addstr(2, 0, "Arrow keys: navigate  |  SPACE: select  |  ENTER: confirm")

            for ci, col in enumerate(columns):
                x = ci * COL_WIDTH + 2
                col_title = str(col[0])[:COL_WIDTH - 1]
                stdscr.addstr(4, x, col_title, curses.A_UNDERLINE | curses.A_BOLD)
                for ri, item in enumerate(col[1:]):
                    y = ri + 5
                    is_highlighted = (ci == cur_col and ri == cur_row)
                    is_selected = (ci, ri) in selected
                    prefix = "[x] " if is_selected else "[ ] "
                    text = (prefix + str(item))[:COL_WIDTH - 1]

                    if is_highlighted:
                        stdscr.addstr(y, x, text, curses.color_pair(1))
                    elif is_selected:
                        stdscr.addstr(y, x, text, curses.color_pair(2))
                    else:
                        stdscr.addstr(y, x, text)

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP:
                cur_row = max(0, cur_row - 1)
            elif key == curses.KEY_DOWN:
                cur_row = min(len(columns[cur_col]) - 2, cur_row + 1)
            elif key == curses.KEY_LEFT:
                cur_col = max(0, cur_col - 1)
                cur_row = min(cur_row, len(columns[cur_col]) - 2)
            elif key == curses.KEY_RIGHT:
                cur_col = min(len(columns) - 1, cur_col + 1)
                cur_row = min(cur_row, len(columns[cur_col]) - 2)
            elif key == ord(' '):
                pair = (cur_col, cur_row)
                if pair in selected:
                    selected.discard(pair)
                else:
                    selected.add(pair)
            elif key in (curses.KEY_ENTER, ord('\n'), ord('\r')):
                return [columns[ci][ri + 1] for ci, ri in sorted(selected)]

    return curses.wrapper(_menu)


def select_rides(options: list) -> list:
    """
    do not use this function
    this is replaced by select_rides_2, which is more user-friendly and visually appealing, but this function is still here for testing purposes
    """
    title = 'Please choose the rides you want to visit (press SPACE to mark, ENTER to continue): '
    selected = pick(options, title, indicator='>', multiselect=True, min_selection_count=1)
    return [selected[i][0] for i in range(len(selected))]
        
    
if __name__ == "__main__":
    ascii_art()
    print(select_rides_2(['Group A', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'], ['Group B', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's'], ['Group C', 'u', 'v', 'w', 'x', 'y', 'z']))