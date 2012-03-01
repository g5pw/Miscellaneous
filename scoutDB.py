#!/usr/bin/env python
import sqlite3
import sys
import datetime
import curses
import locale

if len(sys.argv) < 2:
    print("Error: Too few arguments.")
    sys.exit(-1)

locale.setlocale(locale.LC_ALL,'')
code = locale.getpreferredencoding()
# Init Database
dbName = sys.argv[1]
conn = sqlite3.connect(dbName)
cur = conn.cursor()

def main(stdscr):
    stdscr.addstr(0,0, "Welcome!\nSelect what to do:")
    stdscr.addch(2,3, 'L', curses.A_BOLD)
    stdscr.addstr(2,4, "ist current scouts")
    stdscr.addch(3,3, 'E')
    stdscr.addch(3,4, 'x', curses.A_BOLD)
    stdscr.addstr(3,5, "it")
    stdscr.hline(5,0, '-', 40)

    while True:
        stdscr.addstr(6,0, "Select choice: ", curses.A_STANDOUT)
        stdscr.refresh()
        choice = stdscr.getch()
        if choice in (ord('l'),ord('L')):
            year = datetime.date.today().year - 11
            cur.execute("SELECT * FROM BasicInfo WHERE birthDate > ?-00-00", (str(year),))
            for row in cur:
                stdscr.clear()
                buf = row[1].ljust(10) + row[0] + "\n"
                stdscr.addstr(buf.encode('utf8'))
            stdscr.refresh()
            stdscr.getch()
        elif choice in (ord('x'),ord('X')):
            return 0
        else:
            stdscr.addstr(6,0, "Invalid choice", curses.A_STANDOUT)
            stdscr.refresh()
            curses.napms(500)


curses.wrapper(main)
