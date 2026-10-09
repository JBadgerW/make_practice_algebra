"""Run mathsheet.py in a pseudo-terminal, type keys, and print the screen.

Needs the pyte terminal emulator (pip install pyte). Run from literal_sequence/:
    python3 tests/screen_test.py 80 24 ":mix all:1\\r" wait3 @ "za" wait1 @
Arguments after the size: a key string (escapes like \\r \\x04 allowed),
"waitN" to let the app work for N seconds, or "@" to print the screen.
Set TT=vt100 to test a terminal without colors.
"""
import fcntl, os, pty, select, struct, sys, termios, time
import pyte

cols, rows, steps = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3:]
pid, fd = pty.fork()
if pid == 0:
    os.environ["TERM"] = os.environ.get("TT", "xterm-256color")
    os.execvp("python3", ["python3", "mathsheet.py", "--seed", "12"])
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
class Screen(pyte.Screen):
    """pyte lacks SU/SD (CSI S, CSI T), which ncurses uses on xterm to shift lines."""
    def _scroll(self, n, down):
        top, bottom = self.margins or (0, self.lines - 1)
        y, x = self.cursor.y, self.cursor.x
        self.cursor.y = top if down else bottom
        for _ in range(n or 1):
            self.reverse_index() if down else self.index()
        self.cursor.y, self.cursor.x = y, x
    def scroll_up(self, n=1, *args, **kwargs):
        self._scroll(n, False)
    def scroll_down(self, n=1, *args, **kwargs):
        self._scroll(n, True)
pyte.Stream.csi = dict(pyte.Stream.csi, S="scroll_up", T="scroll_down")

screen = Screen(cols, rows)
stream = pyte.ByteStream(screen)

def pump(t):
    end = time.time() + t
    while time.time() < end:
        if select.select([fd], [], [], 0.05)[0]:
            try:
                stream.feed(os.read(fd, 65536))
            except OSError:
                return

pump(1.0)
for s in steps:
    if s == "@":
        print("+" + "-" * cols + "+")
        for line in screen.display:
            print("|" + line + "|")
        print("+" + "-" * cols + "+")
    elif s.startswith("wait"):
        pump(float(s[4:]))
    else:
        os.write(fd, s.encode().decode("unicode_escape").encode())
        pump(0.4)
try:
    os.kill(pid, 9)
except OSError:
    pass
