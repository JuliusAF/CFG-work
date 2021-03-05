# CFG-work

I'm playing around with parsing context free grammars, checking for correctness, and then hopefully implementing different parsing techniques on them.

### CFG format:

- Terminal variables are composed of single lowercase letters
- Non-terminals may be any single capital letter followed by any amount of numbers
- LHS and RHS are divided by '->'
- Multiple production rules for a single non-terminal may either be separated by a new line, or by '|'
- Whitespaces are ignored
