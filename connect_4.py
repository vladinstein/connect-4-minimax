import tkinter as tk
from tkinter import Canvas

class Connect_4:
    def __init__(self):
        # https://stackoverflow.com/questions/12791501/why-does-this-code-for-initializing-a-list-of-lists-apparently-link-the-lists-to
        self.board = [[j for j in range(7)] for _ in range(6)]
        self.pl_move = 'pl_1'
        self.pl_not_move = 'pl_2'
        self.pl_1_color = 'red'
        self.pl_2_color = 'yellow'
        self.pl_1_col_hover = "#FF7F7F"
        self.pl_2_col_hover = "#FFFD8F"
        self.depth = 5
        self.vs_comp = True
        self.pl_comp = "pl_1"
        self.pl_human = "pl_2"
        
    def check_win(self):
        for i in range(6):
            for j in range(7):
                if j < 4:
                    # Check victory in a row
                    if self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3]:
                        return self.board[i][j], [[i, j], [i, j+1], [i, j+2], [i, j+3]]
                    # Check victory diagonal top to bottom
                    if (i > 2 and 
                        self.board[i][j] == self.board[i-1][j+1] == self.board[i-2][j+2] == self.board[i-3][j+3]):
                        return self.board[i][j], [[i, j], [i-1, j+1], [i-2, j+2],[i-3, j+3]]
                if i < 3:
                    # Check victory in a column
                    if (isinstance(self.board[i][j], str) and 
                        self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j]):
                        return self.board[i][j], [[i, j], [i+1, j], [i+2, j], [i+3, j]]
                    # Check victory diagonal bottom to top
                    if (j < 4 and 
                        self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3]):
                        return self.board[i][j], [[i, j], [i+1, j+1], [i+2, j+2], [i+3, j+3]]
        return None, None

    def handle_click(self, event):
        # Get the x coordinate of the click and make the move according to that coordinate.
        # 0-100 is move in column 0, 100-200 is move in column 2 e t.c.
        j = event.x // int(width/7)
        self.make_move_player(j)
        self.switch_turns()
        if game.vs_comp == True:
            move, _ = self.minimax(self.pl_comp, self.depth)
            print(move)
            print("hi")
            self.make_move_player(move)
            self.switch_turns()
        victory, coordinates = self.check_win()
        if victory == "pl_1" or victory == "pl_2":
            # List for drawing winning circles.
            winning_cirscles = [_ for _ in range(4)]
            # Draw white circles on top of the winning line.
            for coord in coordinates:
                i, j = coord[0], coord[1]
                for x in range(4):
                    winning_cirscles[x] = canvas.create_oval(width / 28 + width * j / 7 - width/200, 
                                                             height / 24 + height * i / 6, 
                                                             width * 7.5 / 70 + width * j / 7 - width/200,
                                                             height * 7.5 / 60 + height * i / 6, width = 3, 
                                                             fill="white",  tag="victory")
            for j in range(7):
                for i in range(6):
                    # Unbind all the buttons if the game is over.
                    canvas.tag_unbind(circles[i][j], "<Button-1>")
                    # Change hovering color to white if the game is over.
                    canvas.itemconfig("empty", activefill="white")
            return

    def make_move_player(self, move):
        # Make a move and make changes to the visual representation.
        for i in reversed(range(6)):
            if isinstance(self.board[i][move], int):
                # Save the move.
                self.board[i][move] = self.pl_move
                # Change visuals accordingly.
                canvas.itemconfig(circles[i][move], fill=self.pl_1_color if self.pl_move == "pl_1" else 
                                  self.pl_2_color, activefill=self.pl_1_color if self.pl_move == "pl_1" else 
                                  self.pl_2_color, tag="filled")
                # Switch hovering color to next player's.
                canvas.itemconfig("empty", activefill=self.pl_2_col_hover if self.pl_move == "pl_1" else 
                                  self.pl_1_col_hover)
                return
                
    def switch_turns(self):
        self.pl_move, self.pl_not_move = self.pl_not_move, self.pl_move

    def find_available(self):
        # This function returns "j" coordinate of all available moves.
        # Are we going to need the "i" coordinate later?
        available_moves = []
        for j in range(7):
            for i in reversed(range(6)):
                if isinstance(self.board[i][j], int):
                    available_moves.append([i, j])
                    break
        return available_moves
    
    def calculate_heuristic(self, number):
        return 1 << 4 * number
    
    def find_line_of_four(self):
        score = 0
        for i in range(6):
            for j in range(7):
                if j < 4:
                    # Check 4 in a row horizontally
                    if self.pl_comp in self.board[i][j:j+4] and self.pl_human not in self.board[i][j:j+4]:
                        number = self.board[i][j:j+4].count(self.pl_comp)
                        score += self.calculate_heuristic(number)
                    elif self.pl_human in self.board[i][j:j+4] and self.pl_comp not in self.board[i][j:j+4]:
                        number = self.board[i][j:j+4].count(self.pl_human)
                        score -= self.calculate_heuristic(number)
                    # Check 4 in a row diagonal top to bottom
                    if i > 2:
                        top_to_bottom = [self.board[i][j], self.board[i-1][j+1], 
                                        self.board[i-2][j+2], self.board[i-3][j+3]]
                        if self.pl_comp in top_to_bottom and self.pl_human not in top_to_bottom:
                            number = top_to_bottom.count(self.pl_comp)
                            score += self.calculate_heuristic(number)
                        elif self.pl_human in top_to_bottom and self.pl_comp not in top_to_bottom:
                            number = top_to_bottom.count(self.pl_human)
                            score -= self.calculate_heuristic(number)              
                if i < 3:
                    # Check 4 in a row in a column
                    column = [self.board[i][j], self.board[i+1][j], 
                              self.board[i+2][j], self.board[i+3][j]]
                    if self.pl_comp in column and self.pl_human not in column:
                        number = column.count(self.pl_comp)
                        score += self.calculate_heuristic(number)
                    elif self.pl_human in column and self.pl_comp not in column:
                        number = column.count(self.pl_human)
                        score -= self.calculate_heuristic(number)
                    # Check 4 in a row diagonal bottom to top
                    if j < 4:
                        bottom_to_top = [self.board[i][j], self.board[i+1][j+1], 
                                         self.board[i+2][j+2], self.board[i+3][j+3]]
                        if self.pl_comp in bottom_to_top and self.pl_human not in bottom_to_top:
                            number = bottom_to_top.count(self.pl_comp)
                            score += self.calculate_heuristic(number)
                        elif self.pl_human in bottom_to_top and self.pl_comp not in bottom_to_top:
                            number = bottom_to_top.count(self.pl_human)
                            score -= self.calculate_heuristic(number)
        return score
    
    def minimax(self, player, depth):
        # Minimax.
        # Find available moves.
        available_moves = self.find_available()
        # See if there's a winner or if it's a draw.
        winner, _ = self.check_win()
        if winner == self.pl_comp:
            return None, 10000
        elif winner == self.pl_human:
            return None, - 10000
        elif available_moves == []:
            return None, 0
        # If reached the depth, use heuristic.
        depth -= 1
        move_scores = {}
        # Add heuristic here
        if depth == 0:
            value = self.find_line_of_four()
            return None, value
        else:
            for move in available_moves:
                self.board[move[0]][move[1]] = player
                if player == self.pl_comp:
                    result = self.minimax(self.pl_human, depth)
                    move_scores[move[1]] = result[1]
                else:
                    result = self.minimax(self.pl_comp, depth)
                    move_scores[move[1]] = result[1]
                self.board[move[0]][move[1]] = move[1]
        # Calculation for choosing the move with the best score. 
        if player == self.pl_comp:
            maximize = - 100000
            for i in move_scores:
                if move_scores[i] > maximize:
                    maximize = move_scores[i]
                    max_index = i
        else:
            maximize = 100000
            for i in move_scores:
                if move_scores[i] < maximize:
                    maximize = move_scores[i]
                    max_index = i
        return max_index, maximize
              
game = Connect_4()

window = tk.Tk()
width = 700
height = 600
window.geometry(f"{width}x{height}")
window.title("Connect 4")
window.resizable(False, False)

canvas = Canvas(width=width, height=height, bg="blue")
canvas.pack()
# List of lists for saving circle visual objects.
circles = [[j for j in range(7)] for _ in range(6)]
# Loops for drawing all the circles.
for j in range(7):
    for i in range(6):
        circles[i][j] = canvas.create_oval(width / 140 + width * j / 7 , height / 120 + height * i / 6,
                                           width * 9 / 70 + width * j / 7, height * 3 / 20 + height * i / 6, 
                                           width = 3, fill="white", activefill=game.pl_1_col_hover,  tag="empty")
        if game.vs_comp == False or game.vs_comp == True and game.pl_comp == "pl_2":
            # On click on each button, run handle_click method.
            canvas.tag_bind(circles[i][j], "<Button-1>", game.handle_click)

if game.vs_comp == True and game.pl_comp == "pl_1":
    value, _ = game.minimax(game.pl_comp, game.depth)
    game.make_move_player(value)
    game.switch_turns()
    for j in range(7):
        for i in range(6):
            canvas.tag_bind(circles[i][j], "<Button-1>", game.handle_click)

window.mainloop()
