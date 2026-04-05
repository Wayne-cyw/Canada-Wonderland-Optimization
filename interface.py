from pick import pick
import curses
import time

def ascii_art():
    """
    Displays the ASCII art splash screen for the Wonderland Optimization Program.

    Renders the splash screen using curses, centered in the terminal window,
    then pauses for 2.5 seconds before returning.
    """
    art = [
        r"__        __              _           _                 _ ",
        r"\ \      / /__  _ __   __| | ___ _ __| | __ _ _ __   __| |",
        r" \ \ /\ / / _ \| '_ \ / _` |/ _ \ '__| |/ _` | '_ \ / _` |",
        r"  \ V  V / (_) | | | | (_| |  __/ |  | | (_| | | | | (_| |",
        r"  _\_/\_/ \___/|_| |_|\__,_|\___|_|  |_|\__,_|_| |_|\__,_|",
        r" / _ \ _ __ | |_(_)_ __ ___ (_)______ _| |_(_) ___  _ __  ",
        r"| | | | '_ \| __| | '_ ` _ \| |_  / _` | __| |/ _ \| '_ \ ",
        r"| |_| | |_) | |_| | | | | | | |/ / (_| | |_| | (_) | | | |",
        r" \___/| .__/ \__|_|_| |_| |_|_/___\__,_|\__|_|\___/|_| |_|",
        r"|  _ \|_|__ ___   __ _ _ __ __ _ _ __ ___                 ",
        r"| |_) | '__/ _ \ / _` | '__/ _` | '_ ` _ \                ",
        r"|  __/| | | (_) | (_| | | | (_| | | | | | |               ",
        r"|_|   |_|  \___/ \__, |_|  \__,_|_| |_| |_|               ",
        r"                 |___/                                    ",
    ]

    def _splash(stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        term_h, term_w = stdscr.getmaxyx()
        art_h = len(art)
        art_w = max(len(line) for line in art)
        y_start = max(0, (term_h - art_h) // 2)
        x_start = max(0, (term_w - art_w) // 2)

        stdscr.clear()
        for i, line in enumerate(art):
            stdscr.addstr(y_start + i, x_start, line, curses.A_BOLD | curses.color_pair(1))
        stdscr.refresh()
        time.sleep(2.5)

    curses.wrapper(_splash)

def select_rides_2(*columns: list) -> list:
    """
    Displays an interactive terminal menu for selecting rides across multiple columns.

    Renders a multi-column curses UI where each column represents a zone/area of
    Canada's Wonderland. The first element of each column is treated as the column
    header (zone name); the remaining elements are selectable ride names.

    Controls:
        Arrow keys  — navigate between rides and columns
        SPACE       — toggle selection on the highlighted ride
        ENTER       — confirm all selections and return

    Visual indicators:
        [x]         — ride is selected (shown in green)
        [ ]         — ride is not selected
        Highlighted — current cursor position (white background)

    Args:
        *columns (list): One or more lists, each representing a zone. The first
            element of each list must be the zone/column header (str), and the
            remaining elements are the ride names (str). Columns should be ordered
            by their physical area within the park.

    Returns:
        list: The selected ride names in the order their columns appear
            (left-to-right), then by row position within each column.
    """
    COLS_PER_ROW = 4

    def _menu(stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)  # highlighted
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # selected

        _, term_width = stdscr.getmaxyx()
        COL_WIDTH = max(10, (term_width - 2) // COLS_PER_ROW)

        # Precompute the y offset where each band (row of up to 4 columns) starts.
        # Each band's height = tallest column in that band + 1 (header) + 1 (gap).
        num_bands = (len(columns) + COLS_PER_ROW - 1) // COLS_PER_ROW
        y_starts = []
        y = 4  # first band starts after title (row 0), blank (row 1), hint (row 2), blank (row 3)
        for b in range(num_bands):
            y_starts.append(y)
            band_cols = columns[b * COLS_PER_ROW : (b + 1) * COLS_PER_ROW]
            tallest = max(len(col) - 1 for col in band_cols)
            y += tallest + 2  # +1 for header row, +1 for gap between bands

        title = "Select the rides you want to visit"

        cur_col, cur_row = 0, 0
        selected = set()  # stores (col_idx, row_idx) tuples where row_idx is 0-based into items (col[1:])

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, title, curses.A_BOLD)
            stdscr.addstr(2, 0, "Arrow keys: navigate  |  SPACE: select  |  ENTER: confirm")

            for ci, col in enumerate(columns):
                band = ci // COLS_PER_ROW
                col_in_band = ci % COLS_PER_ROW
                x = col_in_band * COL_WIDTH + 2
                y_base = y_starts[band]

                col_title = str(col[0])[:COL_WIDTH - 1]
                stdscr.addstr(y_base, x, col_title, curses.A_UNDERLINE | curses.A_BOLD)

                for ri, item in enumerate(col[1:]):
                    row_y = y_base + 1 + ri
                    is_highlighted = (ci == cur_col and ri == cur_row)
                    is_selected = (ci, ri) in selected
                    prefix = "[x] " if is_selected else "[ ] "
                    text = (prefix + str(item))[:COL_WIDTH - 1]

                    if is_highlighted:
                        stdscr.addstr(row_y, x, text, curses.color_pair(1))
                    elif is_selected:
                        stdscr.addstr(row_y, x, text, curses.color_pair(2))
                    else:
                        stdscr.addstr(row_y, x, text)

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

def ask_budget() -> int:
    """
    Asks the user for their budget in hours and returns it as an float in minutes.
    """
    title_start = 'Please choose the time you want to visit (ENTER to continue): '
    options = ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00']
    selected_start, index_start = pick(options, title_start, indicator='>')
    title_end = 'Please choose the time you want to leave (ENTER to continue): '
    selected_end, index_end = pick(options[index_start + 1:], title_end, indicator='>')
    start_time = int(selected_start.split(':')[0]) * 60 + int(selected_start.split(':')[1])
    end_time = int(selected_end.split(':')[0]) * 60 + int(selected_end.split(':')[1])
    return start_time, end_time, end_time - start_time
    
        
    
def display_optimal_path(path: tuple) -> None:
    """
    Displays the optimal ride path in a curses screen.

    Shows each ride in visit order, numbered and prefixed with an arrow.
    If the path is empty (no rides fit within the budget), a message is shown
    instead. Waits for the user to press any key before returning.

    Args:
        path (tuple): Ordered ride names as returned by find_optimal_path.
            Pass an empty tuple to display the no-rides message.
    """
    def _display(stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

        stdscr.clear()
        stdscr.addstr(0, 0, "Optimal Path", curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.addstr(1, 0, "─" * 40)

        if not path:
            stdscr.addstr(3, 0, "No rides could be completed within the time budget.")
        else:
            stdscr.addstr(2, 0, f"Rides to visit: {len(path)}", curses.A_BOLD)
            for i, ride in enumerate(path, start=1):
                stdscr.addstr(3 + i, 0, f"  {i}. → {ride}", curses.color_pair(1))

        stdscr.addstr(3 + len(path) + 2, 0, "Press any key to exit.", curses.A_DIM)
        stdscr.refresh()
        stdscr.getch()

    curses.wrapper(_display)


if __name__ == "__main__":
    ascii_art()
    print(select_rides_2(['Group A', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'], ['Group B', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's'], ['Group C', 'u', 'v', 'w', 'x', 'y', 'z']))