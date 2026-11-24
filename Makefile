CC = gcc
CFLAGS = -Wall -Wextra -g
PYTHON = python3

all: onepiecedle

onepiecedle: onepiecedle.c jsmn.h
	$(CC) $(CFLAGS) onepiecedle.c -o onepiecedle

run: onepiecedle
	./onepiecedle

character_editor:
	$(PYTHON) character_editor.py

clean:
	rm -f onepiecedle *.o
	rm -rf __pycache__

.PHONY: all run character_editor clean
