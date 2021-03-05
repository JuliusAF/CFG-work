# CFG-work

I'm playing around with parsing context free grammars, checking for correctness, and then hopefully implementing different parsing techniques on them. Just a way to practice python and learn CFGs for my automata course.

### CFG format

- Terminal variables are composed of single lowercase letters
- Non-terminals may be any single capital letter followed by any amount of numbers
- LHS and RHS are divided by '->'
- Multiple production rules for a single non-terminal may either be separated by a new line, or by '|'
- Whitespaces are ignored

### Functionality

The following is the planned functionality and the 

- The program should take a CFG either through a specified text file containing the entire thing, or it should be able to read a CFG line-by-line through the command line
- The program should store this CFG in some data structure
- The program should then check the CFG for correctness, and alert the user on an error (we'll try to stick with legitimate errors)
- Then I want to implement CFG reduction techniques, such as lambda rule removals, unit production removals, removing useless variables
- Then I want to implement transformation to Chomsky normal form
- Using the hopefully correct Chomsky normal form, I'd like to implement the CYK algorithm
- Lastly I'd like to implement LL parsing, but how can I implement something I do not even understand :). Anyway, if I reach here it'll be LL(1) first.
