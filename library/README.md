# The built-in library

This folder is the library that ships with the app. It holds only JSON:

- **Fixed banks**, written problems (`lesson_1-4.json`)
- **Sequences**, ordered steps through banks' types (`literal_by_type.json`)
- **`courses.json`**, the courses and their units

`lesson_1-4.json` and `literal_by_type.json` are written by `gen_sequence.py`,
so change them there, not here.

## Where else problems live

- **Your own library**, `~/Documents/mathsheet-library` by default (`:library DIR`
  in the app changes it). It works the same way: put your banks, sequences, and
  `courses.json` there. A bank or sequence with the same name as one here
  replaces it.
- **Generators**, the banks that draw new problems (literal equations,
  inequalities, systems, ...), are Python code, so they live with the rest of the
  program in `sheets/banks/`. Ask for a new generator as a programming task;
  don't put a `.py` file here or in your own library. A library holds only JSON,
  so a shared folder can never run code.

The MANUAL's *Adding problems* section has the formats.
