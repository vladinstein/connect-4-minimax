import tkinter as tk
from tkinter import Canvas

class Connect_4:
    def __init__(self):
        # https://stackoverflow.com/questions/12791501/why-does-this-code-for-initializing-a-list-of-lists-apparently-link-the-lists-to
        self.board = [[j for j in range(7)] for _ in range(6)]
        self.circles = [[j for j in range(7)] for _ in range(6)]
        self.pl_move = 'pl_1'
        self.pl_not_move = 'pl_2'
        self.pl_1_color = 'red'
        self.pl_2_color = 'yellow'
        self.pl_1_col_hover = "#FF7F7F"
        self.pl_2_col_hover = "#FFFD8F"
        self.depth = 5
        self.vs_comp = False
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
                    if ((self.board[i][j] == "pl_1" or self.board[i][j] == "pl_2") and 
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
        window.update()
        victory, coordinates = self.check_win()
        if victory == "pl_1" or victory == "pl_2":
            game.draw_a_winning_line(coordinates)
            return
        # Need to check victory for human as well
        if game.vs_comp == True:
            move, _ = self.minimax(self.pl_comp, self.depth)
            self.make_move_player(move)
            self.switch_turns()
        victory, coordinates = self.check_win()
        if victory == "pl_1" or victory == "pl_2":
            game.draw_a_winning_line(coordinates)
            return
        
    def draw_a_winning_line(self, coordinates):
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
                                                            fill=self.pl_1_color if self.pl_move == "pl_1" 
                                                            else self.pl_2_color,  tag="victory")
        for j in range(7):
            for i in range(6):
                # Unbind all the buttons if the game is over.
                canvas.tag_unbind(self.circles[i][j], "<Button-1>")
                # Change hovering color to white if the game is over.
                canvas.itemconfig("empty", activefill="#ADD8E6")

    def make_move_player(self, move):
        # Make a move and make changes to the visual representation.
        for i in reversed(range(6)):
            if self.board[i][move] != "pl_1" and self.board[i][move] != "pl_2":
                # Save the move.
                self.board[i][move] = self.pl_move
                # Change visuals accordingly.
                canvas.itemconfig(self.circles[i][move], fill=self.pl_1_color if self.pl_move == "pl_1" else 
                                  self.pl_2_color, activefill=self.pl_1_color if self.pl_move == "pl_1" else 
                                  self.pl_2_color, tag="filled")
                # Switch hovering color to next player's.
                canvas.itemconfig("empty", activefill=self.pl_2_col_hover if self.pl_move == "pl_1" else 
                                self.pl_1_col_hover)
                if self.vs_comp and self.pl_move == self.pl_human:
                    canvas.itemconfig("empty", activefill="#ADD8E6")
                return
                
    def switch_turns(self):
        self.pl_move, self.pl_not_move = self.pl_not_move, self.pl_move

    def find_available(self):
        # Returns "j" coordinate of all available moves.
        available_moves = []
        for j in range(7):
            for i in reversed(range(6)):
                if self.board[i][j] != "pl_1" and self.board[i][j] != "pl_2":
                    available_moves.append([i, j])
                    break
        return available_moves
    
    def calculate_heuristic(self, number):
        return 1 << 4 * number
    
    def find_line_of_four(self):
        # Finds four-in-a-row with (1-3) pieces of one player and no pieces of the other.
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
                    column = [col[j] for col in self.board[i:i+4]]
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
        # Find available moves.
        available_moves = self.find_available()
        # See if there's a winner or if it's a draw.
        winner, _ = self.check_win()
        if winner == self.pl_comp:
            #https://stackoverflow.com/questions/66053813/minimax-algorithm-for-connect-4-producing-a-losing-move
            return None, 100000 + depth
        elif winner == self.pl_human:
            return None, - 100000 - depth
        elif available_moves == []:
            return None, 0
        # If reached the maximum depth, use heuristic.
        if depth == 0:
            # Calculate position on a board
            value = self.find_line_of_four()
            return None, value
        else:
            # Recursive call of the function for an opposite player.
            depth -= 1
            move_scores = {}
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
            maximize = - 1000000
            for i in move_scores:
                if move_scores[i] > maximize:
                    maximize = move_scores[i]
                    max_index = i
        else:
            maximize = 1000000
            for i in move_scores:
                if move_scores[i] < maximize:
                    maximize = move_scores[i]
                    max_index = i
        return max_index, maximize
    
    def second_menu(self, _):
        # Menu for choosing who moves first.
        canvas.delete("all")
        self.vs_comp = True
        canvas.create_text(width/2,height/4,fill="black",font="Aerial 25 bold",
                    text="First move:")
        first = canvas.create_text(width/2,height/2,fill="darkblue",font="Aerial 25 bold",
                            text="Human", activefill="black")
        second = canvas.create_text(width/2,height*3/4,fill="darkblue",font="Aerial 25 bold",
                            text="Destroyer 1.1", activefill="black")
        canvas.tag_bind(first, "<Button-1>", lambda event: game.third_menu(1, event))
        canvas.tag_bind(second, "<Button-1>", lambda event: game.third_menu(0, event))

    def third_menu(self, first, _):
        # Menu for choosing your color.
        canvas.delete("all")
        if first:
            self.pl_comp, self.pl_human = self.pl_human, self.pl_comp
        canvas.create_text(width/2,height/4,fill="black",font="Aerial 25 bold",
                    text="Pick Your Color:")
        red = canvas.create_text(width/2,height/2,fill="darkblue",font="Aerial 25 bold",
                            text="Red", activefill="black")
        yellow = canvas.create_text(width/2,height*3/4,fill="darkblue",font="Aerial 25 bold",
                            text="Yellow", activefill="black")
        canvas.tag_bind(red, "<Button-1>", lambda event: game.start_game(1, event))
        canvas.tag_bind(yellow, "<Button-1>", lambda event: game.start_game(0, event))

    def start_game(self, color, _):
        canvas.delete("all")
        # Switch colors if needed.
        if color and self.pl_human == "pl_2" or not color and self.pl_human == "pl_1":
            self.pl_1_color, self.pl_2_color = self.pl_2_color, self.pl_1_color
            self.pl_1_col_hover, self.pl_2_col_hover = self.pl_2_col_hover, self.pl_1_col_hover
        # Loops for drawing all the circles.
        for j in range(7):
            for i in range(6):
                self.circles[i][j] = canvas.create_oval(width / 140 + width * j / 7 , height / 120 + height * i / 6,
                                                width * 9 / 70 + width * j / 7, height * 3 / 20 + height * i / 6, 
                                                width = 3, fill="#ADD8E6", activefill=game.pl_1_col_hover,  tag="empty")
                if game.vs_comp == False or game.vs_comp == True and game.pl_comp == "pl_2":
                    # Bind a click on any of the circles to the function.
                    canvas.tag_bind(self.circles[i][j], "<Button-1>", game.handle_click)
        # First move of the computer if needed.
        if game.vs_comp == True and game.pl_comp == "pl_1":
            value, _ = game.minimax(game.pl_comp, game.depth)
            game.make_move_player(value)
            game.switch_turns()
            # Bind a click on any of the circles to the function.
            for j in range(7):
                for i in range(6):
                    canvas.tag_bind(self.circles[i][j], "<Button-1>", game.handle_click)

game = Connect_4()

window = tk.Tk()
width = 700
height = 600
window.geometry(f"{width}x{height}")
window.title("Connect 4")
window.resizable(False, False)

canvas = Canvas(width=width, height=height, bg="blue")
canvas.pack()
# First menu: game vs computer or vs another player.
canvas.create_text(width/2,height/4,fill="black",font="Aerial 25 bold",
                    text="Game Mode:")
vs_human = canvas.create_text(width/2,height/2,fill="darkblue",font="Aerial 25 bold",
                    text="Human VS Human", activefill="black")
vs_ai = canvas.create_text(width/2,height*3/4,fill="darkblue",font="Aerial 25 bold",
                    text="Human VS Destroyer 1.1", activefill="black")
canvas.tag_bind(vs_ai, "<Button-1>", game.second_menu)
canvas.tag_bind(vs_human, "<Button-1>", lambda event: game.start_game(0, event))


window.mainloop()
