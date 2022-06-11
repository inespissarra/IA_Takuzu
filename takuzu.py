# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 84:
# 99261 Juliana Marcelino
# 99236 Inês Pissarra

import sys
from search import (
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

    def __init__(self, board):
        self.board = board
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
        pass

    def __str__(self):
        s = ""
        for i in self.board:
            line = [str(element) for element in i]
            s += " ".join(line)
            s+="\n"
        return s

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def get_size(self):
        return self.size

    def set_number(self, row: int, col: int, number: int):
        self.board[row][col] = number
        pass

    def duplicate(self):
        new_board = Board(self.size)
        for i in self.board:
            new_board.board += [i.copy()]
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

        return b

    # TODO: outros metodos da classe

def restr(board: Board, row: int, col: int, value: int):
    return rest1(board, row, col, value)

def rest1(board: Board, row: int, col: int, value: int):
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

def rest2(board: Board, row: int, col: int, value: int):
    pass
def rest3():
    pass
def rest4():
    pass

class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        l = []
        board = state.get_board()
        n = board.get_size()
        for i in range(n):
            for j in range(n):
                if board.get_number(i, j) == 2:
                    if restr(board, i, j, 0):
                        l += [(i, j, 0)]
                    if restr(board, i, j, 1):
                        l += [(i, j, 1)]
        return l

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        if action in self.actions(state):
            actual_board = state.get_board()
            next_board = actual_board.duplicate()
            next_board.set_number(action[0], action[1], action[2])
            new_state = TakuzuState(next_board)
            return new_state

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        n = state.get_board().get_size()
        for i in range(n):
            for j in range(n):
                if state.get_board().get_number(i, j) == 2:
                    return False
        return True
        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance_from_stdin()

    print("Initial:\n", board, sep="")
    problem = Takuzu(board)
    # Imprimir valores adjacentes
    goal_node = depth_first_tree_search(problem)
    print("Is goal?", problem.goal_test(goal_node.state))
    print(problem.actions(problem.initial))
    print("Solution:\n", board, sep="")
    print("Solution:\n", goal_node.state.board, sep="")
    pass
