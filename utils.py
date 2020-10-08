import itertools
import copy

def read_data(PATH):
    """
    txt file을 읽어서 미로를 list형태로 반환
    """
    maze = []
    with open(PATH) as f:
        for i, l in enumerate(f):
            if i == 0:
                n_maze, _, _ = list(map(int, l.split()))
                continue
            maze.append(l.replace('\n',''))
    maze = [list(i) for i in maze]
    maze = [list(map(int, l)) for l in maze]
    return maze, n_maze

def write_txt(len_, time_, path_, fn):
    """
    output txt 작성하는 함수
    """
    with open(fn, 'w+') as f:
        for l in path_:
            f.write(l)
            f.write('\n')
        f.write('---')
        f.write('\n')
        f.write('length={}'.format(len_))
        f.write('\n')
        f.write('time={}'.format(time_))

def get_neighbor(maze: list, vertex: tuple, max_row: int, max_col: int):
    """
    vertex의 neighbor list 생성
    벽(1)은 neighbor에서 제외
    """
    
    neighbors = []
    i, j = vertex
    #상
    if i-1 > 0:
        if maze[i-1][j] != 1:
            neighbors.append((i-1, j))
    #하
    if i+1 < max_row:
        if maze[i+1][j] != 1:
            neighbors.append((i+1, j))
    #좌
    if j-1 > 0:
        if maze[i][j-1] != 1:
            neighbors.append((i, j-1))
    
    #우
    if j+1 < max_col:
        if maze[i][j+1] != 1:
            neighbors.append((i, j+1))
    
    return neighbors

def get_route(maze: list):
    """
    start부터 key경유하여 goal 포인트까지 모든 경우의 수를 list로 반환

    Return
    ---
    eg.
    [[(0, 2), (1, 0), (3, 4), (5, 5), (11, 2)],
    [(0, 2), (1, 0), (5, 5), (3, 4), (11, 2)],
    [(0, 2), (3, 4), (1, 0), (5, 5), (11, 2)],
    [(0, 2), (3, 4), (5, 5), (1, 0), (11, 2)],
    [(0, 2), (5, 5), (1, 0), (3, 4), (11, 2)],
    [(0, 2), (5, 5), (3, 4), (1, 0), (11, 2)]]
    """
    start, keys, end = _find_start_key_num_goal(maze)

    route = []
    key_permute = list(itertools.permutations(keys))
    for tup in key_permute:
        ls = [start]
        ls.extend(list(tup))
        ls.append(end)
        route.append(ls)
    
    return route

def _find_start_key_num_goal(maze:list):
    """
    start point, key point(list), goal point를 반환 
    
    Return
    ---
    (0, 2), [(5, 3)], (11, 2)

    """
    keys = []
    for i, l in enumerate(maze): # i=row
        for j, val in enumerate(l): # j=column
            if val == 3:
                start = (i, j)
            if val == 6:
                keys.append((i, j))
            if val == 4:
                end = (i, j)
    return start, keys, end

def _convert_maze(maze):
    """
    int형태의 value를 print할 수 있도록 str로 바꿈

    Return
    ---
    eg.
    ['1 1 5 1 1 1 1 1 1 1 1 1',
    '1 5 5 5 5 2 2 2 2 2 2 1',
    '1 5 1 1 5 1 1 1 1 1 2 1',
    '1 5 1 5 5 1 5 5 5 1 2 1',
    '1 5 1 5 1 5 5 1 5 1 2 1',
    '1 5 1 5 1 5 1 1 5 1 1 1',
    '1 5 1 1 1 5 5 1 5 1 2 1',
    '1 5 1 2 1 1 5 1 5 1 2 1',
    '1 5 5 5 5 5 5 1 5 5 5 1',
    '1 1 1 1 1 1 1 1 1 1 5 1',
    '1 2 5 5 5 5 5 5 5 5 5 1',
    '1 1 5 1 1 1 1 1 1 1 1 1']

    """
    return [' '.join([str(i) for i in l]) for l in maze]

def get_length_time(maze, path_ls_ls, j_ls):
    """
    각 경유지 루트에 대한 건을 합쳐서 length와 time 반환

    Variable
    - path_ls_ls: 각 루트에 대한 경유지 path list
    - path_ls: 한 개 루트의 path
    """
    maze_copy = copy.deepcopy(maze)
    start_i, start_j = path_ls_ls[0][0]
    end_i, end_j = path_ls_ls[-1][-1]
    for path_ls in path_ls_ls:
        for i_,j_ in path_ls:
            maze_copy[i_][j_] = 5
    
    # 시작, 끝은 원래 value로 정정
    maze_copy[start_i][start_j] = 3
    maze_copy[end_i][end_j] = 4
    
    length=0
    key_num = 0
    for row in maze_copy:
        for elem in row:
            if elem == 5 or elem == 6:
                length += 1
            if elem == 6:
                key_num += 1
    
    time = sum(j_ls)-key_num              # key는 2번 방문하므로 한번 빼줘야 함
    maze_copy = _convert_maze(maze_copy) # print할 수 있게 변환
    
    return length, time, maze_copy

def find_goal_and_key(maze, search_algo):
    """
    start point, key경유지, goal까지의 모든 경로를 탐색한 후 
    최단 경로 정보를 반환하는 함수

    Return
    - len_: 최단 경로 길이
    - time_: 최단 경로 방문 노드 횟수
    - path_: 최단 경로 
    """
    max_row, max_col = len(maze), len(maze[0])
    route = get_route(maze)
    length = 100000000000000000000000000000; time = 0; answer_path = None;
    
    for r in route:     # 가능한 루트 iterate
        path_ls_ls = [] # 각 루트에 대해 경유지 path list
        j_ls = []       # 각 루트에 대해 경유지까지 모든 방문 node
        start = r[0]    # start node
        p = start
        for q in r[1:]:
            path_ls, j = search_algo(maze, max_row, max_col, start=p, end=q)
            path_ls_ls.append(path_ls)
            j_ls.append(j)
            p = q
        
        # 해당 루트의 length와 time
        path_length, path_time, maze_path = get_length_time(maze, path_ls_ls, j_ls)
        if path_length < length:
            length = path_length
            time = path_time
            answer_path = copy.deepcopy(maze_path)
    
    return length, time, answer_path
