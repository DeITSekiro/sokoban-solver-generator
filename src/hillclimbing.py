import time
import numpy as np
import pygame

from .utils import can_move, get_state, is_deadlock, is_solved, print_state

def hill_climbing(matrix, player_pos, widget=None, visualizer=False, max_time=60):
    print('Hill-Climbing Search')
    initial_state = get_state(matrix)
    shape = matrix.shape
    print_state(initial_state, shape)
    
    current_state = initial_state
    current_pos = player_pos
    current_depth = 0
    path = ''
    
    moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    direction = {
        (1, 0): 'D',
        (-1, 0): 'U', 
        (0, -1): 'L',
        (0, 1): 'R',
    }
    
    start_time = time.time()  # Lưu thời gian bắt đầu
    stop_flag = False  # Flag to indicate whether to stop the algorithm
    
    while not stop_flag:
        try:
            if widget:
                pygame.event.pump()

            next_move = None
            for move in moves:
                new_state, _ = can_move(current_state, shape, current_pos, move)
                deadlock = is_deadlock(new_state, shape)
                if new_state is not None and not deadlock:
                    next_move = move
                    break

            if next_move is None:
                print(f'[Hill-Climbing] Solution not found!\n')
                if widget and visualizer:
                    widget.set_text(f'[Hill-Climbing] Solution Not Found!\nDepth {current_depth}', 20)
                    pygame.display.update()
                return (None, -1)

            new_state, player_pos = can_move(current_state, shape, current_pos, next_move)

            if new_state is None:
                continue

            current_state = new_state
            current_depth += 1
            path += direction[next_move]

            if is_solved(current_state):
                print(f'[Hill-Climbing] Solution found!\n\n{path}\nDepth {current_depth}\n')
                if widget and visualizer:
                    widget.solved = True
                    widget.set_text(f'[Hill-Climbing] Solution Found!\n{path}', 20)
                    pygame.display.update()
                return (path, current_depth)

            if widget and visualizer:
                widget.set_text(f'[Hill-Climbing] Solution Depth: {current_depth}\n{path}', 20)
                pygame.display.update()

            # Kiểm tra thời gian và dừng nếu vượt quá giới hạn
            if time.time() - start_time > max_time:
                print(f"[Hill-Climbing] Time limit ({max_time} seconds) exceeded.")
                stop_flag = True

        except KeyboardInterrupt:
            print("Hill-Climbing algorithm interrupted.")
            stop_flag = True  # Set the flag to stop the algorithm


def solve_hill_climbing(puzzle, max_time=60, widget=None, visualizer=False):
    matrix = puzzle
    where = np.where((matrix == '*') | (matrix == '%'))
    player_pos = tuple(np.where((matrix == '*') | (matrix == '%')))
    return hill_climbing(matrix, player_pos, widget, visualizer, max_time)

if __name__ == '__main__':
    start = time.time()
    max_time = 10  # Thời gian tối đa là 60 giây
    root = solve_hill_climbing(np.loadtxt('levels/lvl7.dat', dtype='<U1'), max_time=max_time)
    print(f'Runtime: {time.time() - start} seconds')
