import argparse
from utils import *
from search_algorithm import *

parser = argparse.ArgumentParser()
parser.add_argument('--path', '-p', type=str,
                    help='maze txt file full PATH')
args = parser.parse_args()
PATH = args.path

if __name__ == '__main__':
    maze, n_maze = read_data(PATH)
    for name, algo in [('BFS', bfs), ('IDS', ids), ('GBFS', gbfs), ('A_star', a_star)]:
        len_, time_, path_ = find_goal_and_key(maze, algo)
        fn = 'Maze_{}_{}_output.txt'.format(n_maze, name)
        write_txt(len_, time_, path_, fn)
        print(name)
    print('complete')
