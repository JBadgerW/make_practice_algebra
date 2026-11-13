"""The terminal app (python3 mathsheet.py runs it).

    common.py    the imports every part shares, the constants (rows, settings,
                 help text, hints), and small helpers (paths, Tab completion, prose)
    app.py       App: the state, the caches keyed by revision, change() and undo.
                 App has no curses in it, so tests drive it with keys.
                 It is put together from one mixin per part:
      tree.py      the banks pane: rows, values, counts and settings
      sheet.py     the sheet pane: cursor, selection, and the changes made there
      render.py    the sheet laid out as the page shows it
      files.py     :w, :pre, :present, :open, :e
      commands.py  ex commands and search
      keys.py      every key, in each mode
      info.py      the info box (I)
      find.py      the finder (f): banks and types by a few letters
    screen.py    Screen (curses drawing), and run, the loop; a long key runs in
                 a worker thread (handle)
"""
