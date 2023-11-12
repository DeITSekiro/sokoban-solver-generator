import time
from collections import deque

import numpy as np
import pygame

from .utils import can_move, get_state, is_deadlock, is_solved, print_state


def gbfs(matrix, player_pos, widget=None, visualizer=False):
    print('Greedy Best-First Search')
    initial_state = get_state(matrix)
    shape = matrix.shape
    print_state(initial_state, shape)
    
    def heuristic(state, player_pos):
        # Example heuristic: Manhattan distance between the player and the nearest box
        boxes = np.argwhere(state == '$')
        if not boxes:
            return 0
        distances = [np.abs(player_pos[0] - box[0]) + np.abs(player_pos[1] - box[1]) for box in boxes]
        return min(distances)
    
    seen = {None}
    q = deque([(initial_state, player_pos, 0, '')])
    moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    curr_depth = 0
    direction = {
        (1, 0): 'D',
        (-1, 0): 'U',
        (0, -1): 'L',
        (0, 1): 'R',
    }
    
    while q:
        if widget:
            pygame.event.pump()
        state, pos, depth, path = q.popleft()
        seen.add(state)
        
        for move in moves:
            new_state, _ = can_move(state, shape, pos, move)
            deadlock = is_deadlock(new_state, shape)
            
            if new_state in seen or deadlock:
                continue
            
            # Calculate the heuristic value for the new state
            h_value = heuristic(new_state, pos)
            
            q.append((
                new_state,
                (pos[0] + move[0], pos[1] + move[1]),
                depth + 1,
                path + direction[move],
            ))
            
            if is_solved(new_state):
                print(f'[GBFS] Solution found!\n\n{path + direction[move]}\nDepth {depth + 1}\n')
                if widget and visualizer:
                    widget.solved = True
                    widget.set_text(f'[GBFS] Solution Found!\n{path + direction[move]}', 20)
                    pygame.display.update()
                return path + direction[move], depth + 1
            
            if widget and visualizer:
                widget.set_text(f'[GBFS] Solution Depth: {depth + 1}\n{path + direction[move]}\nHeuristic: {h_value}', 20)
                pygame.display.update()
    
    print(f'[GBFS] Solution not found!\n')
    if widget and visualizer:
        widget.set_text(f'[GBFS] Solution Not Found!\nDepth {depth + 1}', 20)
        pygame.display.update()
    return None, -1 if not q else depth + 1
    print('Greedy Best-First Search')
    initial_state = get_state(matrix)
    shape = matrix.shape
    print_state(initial_state, shape)
    
    def heuristic(state, player_pos):
        # Example heuristic: Manhattan distance between the player and the nearest box
        boxes = np.argwhere(state == '$')
        if not boxes:
            return 0
        distances = [np.abs(player_pos[0] - box[0]) + np.abs(player_pos[1] - box[1]) for box in boxes]
        return min(distances)
    
    seen = {None}
    q = deque([(initial_state, player_pos, 0, '')])
    moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    curr_depth = 0
    direction = {
        (1, 0): 'D',
        (-1, 0): 'U',
        (0, -1): 'L',
        (0, 1): 'R',
    }
    
    while q:
        if widget:
            pygame.event.pump()
        state, pos, depth, path = q.popleft()
        seen.add(state)
        
        for move in moves:
            new_state, _ = can_move(state, shape, pos, move)
            deadlock = is_deadlock(new_state, shape)
            
            if new_state in seen or deadlock:
                continue
            
            q.append((
                new_state,
                (pos[0] + move[0], pos[1] + move[1]),
                depth + 1,
                path + direction[move],
            ))
            
            if is_solved(new_state):
                print(f'[GBFS] Solution found!\n\n{path + direction[move]}\nDepth {depth + 1}\n')
                if widget and visualizer:
                    widget.solved = True
                    widget.set_text(f'[GBFS] Solution Found!\n{path + direction[move]}', 20)
                    pygame.display.update()
                return path + direction[move], depth + 1
            
            if widget and visualizer:
                widget.set_text(f'[GBFS] Solution Depth: {depth + 1}\n{path + direction[move]}', 20)
                pygame.display.update()
    
    print(f'[GBFS] Solution not found!\n')
    if widget and visualizer:
        widget.set_text(f'[GBFS] Solution Not Found!\nDepth {depth + 1}', 20)
        pygame.display.update()
    return None, -1 if not q else depth + 1

def solve_gbfs(puzzle, widget=None, visualizer=False):
    matrix = puzzle
    where = np.where((matrix == '*') | (matrix == '%'))
    player_pos = where[0][0], where[1][0]
    return gbfs(matrix, player_pos, widget, visualizer)

if __name__ == '__main__':
	start = time.time()
	root = solve_gbfs(np.loadtxt('levels/lvl7.dat', dtype='<U1'))
	print(f'Runtime: {time.time() - start} seconds')