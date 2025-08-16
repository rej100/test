import curses
import random

def main(stdscr):
    # initial settings
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(1)
    win.timeout(100)

    # initial snake and food
    snake_x = sw // 4
    snake_y = sh // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]

    opponent_x = sw * 3 // 4
    opponent_y = sh // 2
    opponent_snake = [
        [opponent_y, opponent_x],
        [opponent_y, opponent_x + 1],
        [opponent_y, opponent_x + 2]
    ]

    food = [sh // 2, sw // 2]
    win.addch(int(food[0]), int(food[1]), curses.ACS_PI)

    # initial direction
    key = curses.KEY_RIGHT
    opponent_key = curses.KEY_LEFT

    score = 0
    opponent_score = 0

    while True:
        next_key = win.getch()
        key = key if next_key == -1 else next_key

        # check if game over
        if (snake[0][0] in [0, sh-1] or
            snake[0][1] in [0, sw-1] or
            snake[0] in snake[1:] or
            snake[0] in opponent_snake):
            curses.endwin()
            print(f"Final Score: You: {score}, Opponent: {opponent_score}")
            quit()

        # Opponent AI: move towards food
        possible_moves = [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]
        if opponent_key == curses.KEY_UP:
            possible_moves.remove(curses.KEY_DOWN)
        elif opponent_key == curses.KEY_DOWN:
            possible_moves.remove(curses.KEY_UP)
        elif opponent_key == curses.KEY_LEFT:
            possible_moves.remove(curses.KEY_RIGHT)
        elif opponent_key == curses.KEY_RIGHT:
            possible_moves.remove(curses.KEY_LEFT)

        best_move = None
        min_dist = float('inf')
        for move in possible_moves:
            temp_head = list(opponent_snake[0])
            if move == curses.KEY_UP: temp_head[0] -= 1
            elif move == curses.KEY_DOWN: temp_head[0] += 1
            elif move == curses.KEY_LEFT: temp_head[1] -= 1
            elif move == curses.KEY_RIGHT: temp_head[1] += 1
            
            dist = abs(temp_head[0] - food[0]) + abs(temp_head[1] - food[1])
            if dist < min_dist:
                min_dist = dist
                best_move = move
        
        if best_move:
            opponent_key = best_move

        opponent_new_head = [opponent_snake[0][0], opponent_snake[0][1]]
        if opponent_key == curses.KEY_DOWN: opponent_new_head[0] += 1
        elif opponent_key == curses.KEY_UP: opponent_new_head[0] -= 1
        elif opponent_key == curses.KEY_LEFT: opponent_new_head[1] -= 1
        elif opponent_key == curses.KEY_RIGHT: opponent_new_head[1] += 1
        opponent_snake.insert(0, opponent_new_head)

        if (opponent_snake[0][0] in [0, sh-1] or
            opponent_snake[0][1] in [0, sw-1] or
            opponent_snake[0] in opponent_snake[1:] or
            opponent_snake[0] in snake):
            curses.endwin()
            print(f"Final Score: You: {score}, Opponent: {opponent_score}")
            quit()

        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        # check if snake eats food
        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                food = nf if nf not in snake and nf not in opponent_snake else None
            win.addch(int(food[0]), int(food[1]), curses.ACS_PI)
        else:
            tail = snake.pop()
            win.addch(int(tail[0]), int(tail[1]), ' ')

        # check if opponent snake eats food
        if opponent_snake[0] == food:
            opponent_score += 1
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                food = nf if nf not in snake and nf not in opponent_snake else None
            win.addch(int(food[0]), int(food[1]), curses.ACS_PI)
        else:
            opponent_tail = opponent_snake.pop()
            win.addch(int(opponent_tail[0]), int(opponent_tail[1]), ' ')

        win.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
        win.addch(int(opponent_snake[0][0]), int(opponent_snake[0][1]), curses.ACS_CKBOARD)
        win.addstr(0, 2, f'Score: {score} ')
        win.addstr(0, sw - 20, f'Opponent: {opponent_score} ')

if __name__ == "__main__":
    curses.wrapper(main)
