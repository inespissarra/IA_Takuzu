# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 84:
# 99261 Juliana Marcelino
# 99236 Inês Pissarra

import sys
import numpy as np
from search import (
    InstrumentedProblem,
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

class TakuzuState:
    state_id = 0

    def __init__(self, board, next_actions):
        self.board = board
        self.next_actions = next_actions
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def get_board(self):
        return self.board

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, n):
        self.size = n
        self.board = []
        self.num_rows = []
        self.num_cols = []

    def __str__(self):
        s = ""
        for i in range(self.size):
            line = [str(element) for element in self.board[i]]
            s += "\t".join(line)
            s+="\n"
        return s

    def row_quantity(self):
        quantity = []
        for i in range(self.size):
            zero, one, two = 0, 0, 0
            for j in range(self.size):
                if self.board[i][j] == 0:
                    zero += 1
                elif self.board[i][j] == 1:
                    one += 1
                else:
                    two += 1
            quantity += [[zero, one, two]]
        return quantity

    def col_quantity(self):
        quantity = []
        for i in range(self.size):
            zero, one, two = 0, 0, 0
            for j in range(self.size):
                if self.board[j][i] == 0:
                    zero += 1
                elif self.board[j][i] == 1:
                    one += 1
                else:
                    two += 1
            quantity += [[zero, one, two]]
        return quantity
       
    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def get_size(self):
        return self.size

    def set_number(self, row: int, col: int, number: int):
        self.board[row][col] = number
        self.num_rows[row][number] += 1
        self.num_rows[row][2] -= 1
        self.num_cols[col][number] += 1
        self.num_cols[col][2] -= 1

    def duplicate(self):
        new_board = Board(self.size)
        for i in self.board:
            new_board.board += [i.copy()]
        for i in self.num_cols:
            new_board.num_cols += [i.copy()]
        for i in self.num_rows:
            new_board.num_rows += [i.copy()]
        return new_board

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if row + 1 >= self.size:
            x = None
        else:
            x = self.board[row + 1][col]
        if row - 1 < 0:
            y = None
        else:
            y = self.board[row - 1][col]
    
        return (x, y)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col - 1 < 0:
            x = None
        else:
            x = self.board[row][col - 1]
        if col + 1 >= self.size:
            y = None
        else:
            y = self.board[row][col + 1]
        return (x, y)
            

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        from sys import stdin
        n = int(stdin.readline())

        b = Board(n)

        for i in range(n):
            row = stdin.readline()
            line = [int(element) for element in row.split("\t")]
            b.board += [line]

        b.num_rows = b.row_quantity()
        b.num_cols = b.col_quantity()

        return b


# restrições
def restr(board: Board, row: int, col: int, value: int):
    return rest1(board, row, col, value) and rest2(board, row, col, value) and rest3(board, row, col, value) and rest4(board, row, col, value)

def rest1(board: Board, row: int, col: int, value: int):
    return (board.num_cols[col][value] + 1) <= np.ceil(board.size/2) and (board.num_rows[row][value] + 1) <= np.ceil(board.size/2)

def rest2(board: Board, row: int, col: int, value: int):
    down, up, left, right = 0, 0, 0, 0
    (adj_down, adj_up) = board.adjacent_vertical_numbers(row, col)
    (adj_left, adj_right) = board.adjacent_horizontal_numbers(row, col)
    if isinstance(adj_down, int) and (adj_down == value):
        down += 1
        (adj_dd, trash) = board.adjacent_vertical_numbers(row + 1, col)
        if isinstance(adj_dd, int) and (adj_dd == adj_down):
            down +=1 
    if isinstance(adj_up, int) and (adj_up == value):
        up += 1
        (trash, adj_uu) = board.adjacent_vertical_numbers(row - 1, col)
        if isinstance(adj_uu, int) and (adj_uu == adj_up):
            up += 1
    if isinstance(adj_left, int) and (adj_left == value):
        left += 1
        (adj_ll, trash) = board.adjacent_horizontal_numbers(row, col - 1)
        if isinstance(adj_ll, int) and (adj_ll == adj_left):
            left += 1
    if isinstance(adj_right, int) and (adj_right == value):
        right += 1
        (trash, adj_rr) = board.adjacent_horizontal_numbers(row, col + 1)
        if isinstance(adj_rr, int) and (adj_rr == adj_right):
            right += 1

    return down < 2 and up < 2 and right < 2 and left < 2 and (up == 0 or down == 0) and (left == 0 or right == 0)

def rest3(b: Board, row: int, col: int, value: int):
    if b.num_rows[row][2]==1:
        size = b.get_size()
        for i in range(size):
            if b.num_rows[i][2]==0:
                count = 0
                for j in range(size):
                    if (b.get_number(row, j) ==b.get_number(i, j)) or (j == col and value == b.get_number(i, j)):
                        count += 1
                    else:
                        break
                if count == size:
                    return False
    return True

def rest4(b: Board, row: int, col: int, value: int):
    if b.num_cols[col][2]==1:
        size = b.get_size()
        for i in range(size):
            if b.num_cols[i][2]==0:
                count = 0
                for j in range(size):
                    if (b.get_number(j, col) == b.get_number(j, i)) or (j == row and value == b.get_number(j, i)):
                        count += 1
                    else:
                        break
                if count == size:
                    return False
    return True


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        next_actions = self.prop_rest_init(board)
        self.initial = TakuzuState(board, next_actions)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        if isinstance(state.next_actions, list) and state.next_actions != []:
            return state.next_actions
        elif isinstance(state.next_actions, list):
            board = state.get_board()
            n = board.get_size()
            
            for i in range(n): 
                if board.num_rows[i][2]!=0:
                    for j in range(n):
                        if board.get_number(i, j) == 2:
                            return [(i, j, 0), (i, j, 1)]
        else:
            return []
    
    def pos_actions(self, board: Board, row: int, col: int):
        l = []
        if restr(board, row, col, 0):
            l += [(row, col, 0)]
        if restr(board, row, col, 1):
            l += [(row, col, 1)]

        return l

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        actual_board = state.get_board()
        next_board = actual_board.duplicate()
        next_board.set_number(action[0], action[1], action[2])
        
        next_actions = self.prop_rest(next_board, [action])

        new_state = TakuzuState(next_board, next_actions)
        return new_state

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        n = state.get_board().get_size()
        for i in range(n):
            if state.get_board().num_rows[i][2] != 0:
                return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        h = 0
        for line in node.state.board.num_rows:
            h += line[2]
        
        return h

    def prop_rest_init(self, board: Board):
        n = board.size
        alt = []
        for i in range(n):
            if board.num_cols[i][2]!=0:
                for j in range(n):
                    if board.get_number(i, j) == 2:
                        a = self.pos_actions(board, i, j)
                        if len(a)==1:
                            board.set_number(a[0][0], a[0][1], a[0][2])
                            alt += a
        return self.prop_rest(board, alt)

    def prop_rest(self, board: Board, alt: list):
        while alt!=[]:
            next_actions = []
            next = alt.pop()
            if board.num_cols[next[1]][2]!=0:
                for i in range(board.size):
                    if board.get_number(i, next[1]) == 2:
                        a = self.pos_actions(board, i, next[1])
                        if len(a)==0:
                            return None
                        elif len(a)==1:
                            board.set_number(a[0][0], a[0][1], a[0][2])
                            alt += a
                        else:
                            next_actions = a
            if board.num_rows[next[0]][2]!=0:
                for j in range(board.size):
                    if board.get_number(next[0], j) == 2:
                        a = self.pos_actions(board, next[0], j)
                        if len(a)==0:
                            return None
                        elif len(a)==1:
                            board.set_number(a[0][0], a[0][1], a[0][2])
                            alt += a
                        else:
                            next_actions = a
        return next_actions
                


if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)

    problem = InstrumentedProblem(problem)
    
    #goal_node = greedy_search(problem)
    #goal_node = breadth_first_tree_search(problem)
    goal_node = depth_first_tree_search(problem)
    #goal_node = astar_search(problem)
    #print("gerados:", problem.states)
    #print("expandidos:", problem.succs)
    print(goal_node.state.board, sep="", end = "")