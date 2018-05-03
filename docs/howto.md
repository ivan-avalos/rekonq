# Rekonq instructions

You can find more information about how to use the program in the README included
in the root directory.

## Step 1. Board

The board is initialized with both players placed in the opposite corners.

<img src="img/board.png" alt="Rekonq board" />

### Characters:

```
- Blue: Player A
- Red: Player B

(0) . - Empty cell.

(1) * - Cell with cross expansion.
(2) o - Cell with 'X' expansion.

    ^        ^   ^
    |         \ /
 <- * ->       o
    |         / \
    v        v   v

(1) # - Reconquered (permanent) cell with cross expansion.
(2) @ - Reconquered (permanent) cell with 'X' expansion.

    ^        ^   ^
    |         \ /
 <- # ->       @
    |         / \
    v        v   v
```

## Step 2. Expansion

You can use your cells to expand your "kingdom". The direction toward which a cell
can expand is determined by the character of the cell (explained above). You
can expand only one cell toward the correspondent direction. When
you expand a cell, you can decide the character of the new cell ('*' or 'o').

## Step 3. Eat cells

When you eat a cell from the opposite player, you become the perpetual owner
of that cell. That means that the opposite player won't be able to eat it
again, so you become invencible. You can decide the character of your new cell
too ('*' -> '#' and 'o' -> '@' )

## Step 4. Winner

The player with the highest number of cells at the end of the game wins.
