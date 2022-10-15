from tkinter import *
import customtkinter
import numpy as np
import random

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'


class Tic_Tac_Toe():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.iconbitmap("icon.ico")
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)
        self.window.eval('tk::PlaceWindow . center')


        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

        self.canvas.config(width=size_of_board,height=size_of_board)


    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def display_gameover(self):
        
        dispWidth = 800
        dispHeight = 600

        self.canvas.config(width=dispWidth,height=dispHeight)

        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(dispWidth / 2, dispHeight / 4, font="cmr 50 bold", fill=color, text=text, width=dispWidth)

        score_text = 'Scores \n'
        self.canvas.create_text(dispWidth / 2, 4 * dispHeight / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text, width=dispWidth)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O)  : ' + str(self.O_score) + '\n'
        score_text += 'Tie                 : ' + str(self.tie_score)
        self.canvas.create_text(dispWidth / 2, 10 * dispHeight / 16, font="cmr 30 bold", fill=Green_color,
                                text=score_text,width=dispWidth)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(dispWidth / 2, 14 * dispHeight / 16, font="cmr 20 bold", fill="gray",
                                text=score_text,width=dispWidth)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover





    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns

            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False







class Tic_Tac_ToeVSComputer():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.iconbitmap("icon.ico")
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)
        self.window.eval('tk::PlaceWindow . center')


        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

        self.computerChance()

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

        self.canvas.config(width=size_of_board,height=size_of_board)


        if(self.player_X_turns==True):
            self.computerChance()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------
    def computerChance(self):
        # if not self.is_grid_occupied(logical_position):


        if not self.reset_board:
            if self.player_X_turns:
                myrandomindex = []

                for idx in range(0,3):
                    for idj in range(0,3):
                        if(self.board_status[idx][idj]==0):
                            myrandomindex.append((idx,idj))


                myrandomposition = random.choice(myrandomindex)

                logical_position = np.array([myrandomposition[0],myrandomposition[1]], dtype=int)


                self.draw_X(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = -1
                self.player_X_turns = not self.player_X_turns

            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False




    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def display_gameover(self):
        
        dispWidth = 800
        dispHeight = 600

        self.canvas.config(width=dispWidth,height=dispHeight)

        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Computer (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(dispWidth / 2, dispHeight / 4, font="cmr 50 bold", fill=color, text=text, width=dispWidth)

        score_text = 'Scores \n'
        self.canvas.create_text(dispWidth / 2, 4 * dispHeight / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text, width=dispWidth)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O)  : ' + str(self.O_score) + '\n'
        score_text += 'Tie                 : ' + str(self.tie_score)
        self.canvas.create_text(dispWidth / 2, 10 * dispHeight / 16, font="cmr 30 bold", fill=Green_color,
                                text=score_text,width=dispWidth)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(dispWidth / 2, 14 * dispHeight / 16, font="cmr 20 bold", fill="gray",
                                text=score_text,width=dispWidth)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover





    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)


        if not self.reset_board:
            if self.player_X_turns:
                self.computerChance()
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns

            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False







class Mainmenu:

    def __init__(self):

        menuWidth = 500
        menuHeight = 500

        geoString = str(menuWidth) + 'x' + str(menuHeight)

        global app
        app = customtkinter.CTk()  # create CTk window like you do with the Tk window
        app.title('Tic-Tac-Toe')
        app.geometry(geoString)

        app.iconbitmap("icon.ico")

        app.eval('tk::PlaceWindow %s center' % app.winfo_toplevel())

        button = customtkinter.CTkButton(master=app, text="VS Player", command=self.play_with_player)
        button.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER, height=50)

        button = customtkinter.CTkButton(master=app, text="VS Computer", command=self.play_with_computer)
        button.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER, height=50)

        button = customtkinter.CTkButton(master=app, text="Exit", command=self.exit_function)
        button.place(relx=0.5, rely=0.8, anchor=customtkinter.CENTER,height=50)
        button.click_animation()

        headLabel = customtkinter.CTkLabel(text="Tic Tac Toe",text_font="cmr 40 bold")
        headLabel.place(relx=0.5,rely=0.2,anchor=customtkinter.CENTER)


        app.mainloop()
    
    def exit_function(self):
        exit()

    def play_with_player(self):
        # print("button pressed")
        app.destroy()
        game_instance = Tic_Tac_Toe()
        game_instance.mainloop()

    def play_with_computer(self):
        app.destroy()
        game_instance = Tic_Tac_ToeVSComputer()
        game_instance.mainloop()


    def mainloop(self):
        self.window.mainloop()

    def click(self, event):
        pass


menu_instance = Mainmenu()

