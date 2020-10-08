from utils import get_neighbor
import math

###################### bfs
def bfs(maze, max_row, max_col, start, end):
    Q = [[start]]
    visited = set()
    j=0

    while Q:
        j += 1
        path_ls = Q.pop(0) # Q에 노드 대신 노드 history모두 저장
        vertex = path_ls[-1] # 시작
        if vertex == end: # goal이면 끝
            break
        elif vertex not in visited: # goal 아니면 
            visited.add(vertex)     # visit
            for neighbor in get_neighbor(maze, vertex, max_row, max_col): # node expanding
                if neighbor not in visited:
                    new_path = list(path_ls)
                    new_path.append(neighbor) # 기존 path에 neighbor node 추가하여 update
                    Q.append(new_path) # Q 업데이트: 신규 node 포함된 route 
    return path_ls, j

###################### ids
def ids(maze, max_row, max_col, start, end):
    """
    not sure if this code is perfect implementation
    """
    is_goal = False
    j = 0
    for max_depth in range(1000000): 

        # stack에서 나와서
        # expanding할 때 visit(O)
        # stack에 넣을 때 visit(X)
        stack = [[start]]
        visited = set()
        while stack:
            path_ls = stack.pop() # 현재까지 route
            depth = len(path_ls) # 현재까지 move (depth를 move횟수로 정의)
            vertex = path_ls[-1]
            if vertex == end:
                is_goal = True
                break
            elif (vertex not in visited) and (depth <= max_depth): # node expanding하려면 max depth보다 작아야 함
                visited.add(vertex)
                j+=1
                for neighbor in get_neighbor(maze, vertex, max_row, max_col):
                    if neighbor not in visited:
                        new_path = list(path_ls)
                        new_path.append(neighbor)
                        stack.append(new_path)
        if is_goal:
            return path_ls, j

###################### gbfs
def _get_distance(last_node, target_node):
    i, j = last_node
    x, y = target_node
    return math.sqrt((i-x)**2 + (j-y)**2)

def _sort_Q(Q, end):
    """
    현재 노드에서 end노드까지 직선거리에 따라 오름차순으로 Q를 정렬
    
    Arguments
    - Q: route history를 tuple 형태로 저장
    ---
    eg,
    [[(0, 2), (1, 2), (1, 3)], [(0, 2), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]]

    Variable
    - resort: (path index, path distance)
    ---
    eg.
    [(0, 0.0), (1, 8.94427190999916), (2, 10.04987562112089), (3, 1.4142135623730951)]

    """
    resort = []
    for i, path_ls in enumerate(Q):
        last_node = path_ls[-1]
        dist = _get_distance(last_node, end)
        resort.append((i, dist))
    resort = sorted(resort, key=lambda x: x[1]) # 거리 가장 작은 게 맨 앞으로
    resort = [i[0] for i in resort] # sort된 idx만 추출
    return [Q[i] for i in resort] # 가장 작은 순으로 path_ls 정렬(거리 오름차순)

def gbfs(maze, max_row, max_col, start, end):
    Q = [[start]]
    visited = set()
    j=0
    while Q:
        path_ls = Q.pop(0) # Q에 노드 대신 노드 history모두 저장
        vertex = path_ls[-1] # 시작
        if vertex == end: # goal이면 끝
            break
        elif vertex not in visited: # goal 아니면 
            visited.add(vertex)     # visit
            j+=1
            for neighbor in get_neighbor(maze, vertex, max_row, max_col): # node expanding
                if neighbor not in visited:
                    new_path = list(path_ls)
                    new_path.append(neighbor) # 기존 path에 neighbor node 추가하여 update
                    Q.append(new_path) # Q 업데이트: 신규 node 포함된 route 
                    Q = _sort_Q(Q, end) # priority Queue by h(n)
    return path_ls, j

###################### A_star
def _get_distance(last_node, target_node):
    i, j = last_node
    x, y = target_node
    return math.sqrt((i-x)**2 + (j-y)**2)

def sort_Q2(Q, start, end):
    """
    (현재 노드에서 end노드까지 직선거리 + 시작점에서 현재 노드까지 거리) 따라 오름차순으로 Q를 정렬
    """
    resort = []
    for i, path_ls in enumerate(Q):
        last_node = path_ls[-1]
        dist1 = _get_distance(last_node, end) # h(n)
        dist2 = _get_distance(last_node, start)# g(n)
        dist = dist1 + dist2 #f(n) = g(n) + h(n)
        resort.append((i, dist))
    resort = sorted(resort, key=lambda x: x[1]) # 거리 가장 작은 게 맨 앞으로
    resort = [i[0] for i in resort] # sort된 idx만 추출
    return [Q[i] for i in resort] # 가장 작은 순으로 path_ls 정렬(거리 오름차순)

def a_star(maze, max_row, max_col, start, end):
    Q = [[start]]
    visited = set()
    j=0
    while Q:
        path_ls = Q.pop(0) # Q에 노드 대신 노드 history모두 저장
        vertex = path_ls[-1] # 시작
        if vertex == end: # goal이면 끝
            break
        elif vertex not in visited: # goal 아니면 
            visited.add(vertex)     # visit
            j+=1
            for neighbor in get_neighbor(maze, vertex, max_row, max_col): # node expanding
                if neighbor not in visited:
                    new_path = list(path_ls)
                    new_path.append(neighbor) # 기존 path에 neighbor node 추가하여 update
                    Q.append(new_path) # Q 업데이트: 신규 node 포함된 route 
                    Q = sort_Q2(Q, start, end) # g(n)+h(n)에 따라 Q sort
    return path_ls, j
