class Board:
    def __init__(self):
        """Creates board instance and puts all pieces into the starting location
        black_pieces - list containing all black pieces
        black_locations - list containing all black piece locations, indexes correspond w/ black_pieces
        white_pieces - list containing all white pieces
        white_locations - list containing all white piece locations, indexes correspond w/ white_pieces
        turn - string that indicates whose turn it is
        won - boolean determining if the board is in a winning state
        winner - string that contains the winning team if the board is in a winning state"""

        # Instance variables containing pieces and their corresponding locations
        self.black_pieces = []
        self.black_locations = []
        self.white_pieces = []
        self.white_locations = []
        self.turn = "White"
        self.won = False
        self.winner = None

        # Adding pawns to board
        for col in range(1,9):
            pawn_black = Pawn((7,col),"Black",self)
            self.black_pieces.append(pawn_black)
            self.black_locations.append(pawn_black.get_location())

            pawn_white = Pawn((2,col),"White",self)
            self.white_pieces.append(pawn_white)
            self.white_locations.append(pawn_white.get_location())

        ## Adding Rooks to Board
        rook_white1 = Rook((1,1),"White",self)
        self.white_pieces.append(rook_white1)
        self.white_locations.append(rook_white1.get_location())

        rook_white2 = Rook((1,8),"White",self)
        self.white_pieces.append(rook_white2)
        self.white_locations.append(rook_white2.get_location())

        rook_black1 = Rook((8,1),"Black",self)
        self.black_pieces.append(rook_black1)
        self.black_locations.append(rook_black1.get_location())

        rook_black2 = Rook((8,8),"Black",self)
        self.black_pieces.append(rook_black2)
        self.black_locations.append(rook_black2.get_location())

        ## Adding Knigts to Board
        knight_white1 = Knight((1,2),"White",self)
        self.white_pieces.append(knight_white1)
        self.white_locations.append(knight_white1.get_location())

        knight_white2 = Knight((1,7),"White",self)
        self.white_pieces.append(knight_white2)
        self.white_locations.append(knight_white2.get_location())

        knight_black1 = Knight((8,2),"Black",self)
        self.black_pieces.append(knight_black1)
        self.black_locations.append(knight_black1.get_location())

        knight_black2 = Knight((8,7),"Black",self)
        self.black_pieces.append(knight_black2)
        self.black_locations.append(knight_black2.get_location())

        ## Adding Bishops to Board
        bishop_white1 = Bishop((1,3),"White",self)
        self.white_pieces.append(bishop_white1)
        self.white_locations.append(bishop_white1.get_location())

        bishop_white2 = Bishop((1,6),"White",self)
        self.white_pieces.append(bishop_white2)
        self.white_locations.append(bishop_white2.get_location())

        bishop_black1 = Bishop((8,3),"Black",self)
        self.black_pieces.append(bishop_black1)
        self.black_locations.append(bishop_black1.get_location())

        bishop_black2 = Bishop((8,6),"Black",self)
        self.black_pieces.append(bishop_black2)
        self.black_locations.append(bishop_black2.get_location())

        ## Adding Queens to Board
        queen_white = Queen((1,4),"White",self)
        self.white_pieces.append(queen_white)
        self.white_locations.append(queen_white.get_location())

        queen_black = Queen((8,4),"Black",self)
        self.black_pieces.append(queen_black)
        self.black_locations.append(queen_black.get_location())

        ## Adding Kings to Board
        king_white = King((1,5),"White",self)
        self.white_pieces.append(king_white)
        self.white_locations.append(king_white.get_location())

        king_black = King((8,5),"Black",self)
        self.black_pieces.append(king_black)
        self.black_locations.append(king_black.get_location())


    def get_white_locations(self):
        """Returns the white_locations instance variables which contain the locations of all white pieces"""
        return self.white_locations


    def get_black_locations(self):
        """Returns the black locations instance variables which contain the locations of all black pieces"""
        return self.black_locations

    def move(self,starting,ending):
        """Function that moves a piece
        starting - string containing starting square of the move
        ending - string containing ending square of the move"""
        # Converts starting and ending squares to (row,col) tuples
        starting = self.convert_input(starting.upper())
        ending = self.convert_input(ending.upper())

        # Decides who's turn and creates team and enemy variables
        if self.turn == "White":
            team_locations = self.white_locations
            team_pieces = self.white_pieces
            enemy_locations = self.black_locations
            enemy_pieces = self.black_pieces
        else:
            enemy_locations = self.white_locations
            enemy_pieces = self.white_pieces
            team_locations = self.black_locations
            team_pieces = self.black_pieces

        # Ensures the starting space has a team piece, if not provide feedback
        if starting in team_locations:
            i = team_locations.index(starting)
            piece = team_pieces[i]

            # Ensures ending space is a valid move, if not provide feedback
            if ending in piece.moves():
                # Changes location of piece
                team_locations[i] = ending
                piece.set_location(ending)
                piece.moved = True

                # Checks to see if there was a capture
                if ending in enemy_locations:
                    j = enemy_locations.index(ending)
                    # If a king was captured, declare the winner
                    if type(enemy_pieces[j]) is King:
                        self.won = True
                        self.winner = self.turn
                    # Deletes captured piece
                    del enemy_locations[j]
                    del enemy_pieces[j]
                # Changes turn
                if self.turn == "White":
                    self.turn = "Black"
                else:
                    self.turn = "White"

            else:
                # Feedback for improper inputs
                print("    Please select a valid move for your piece")
                print()
        else:
            # Feedback for improper inputs
            print("    Please select a valid space that contains a piece of the correct team.")
            print()

    def convert_input(self,location):
        """Converts a user location input to usable form A1 to (1,1)
        location - string that represents a location in the form of A1"""
        # Dictionary of letter to number conversions
        conversions = {"A":1 , "B":2 , "C":3 , "D":4 , "E":5 , "F":6 , "G":7 , "H":8}
        location = location.upper()
        # Finding and returning conversion
        return ((int(location[1]),conversions[location[0]]))


    def __repr__(self):
        """initialize the __repr__ function to display the state of the board"""
        # Ans is the string that will represent the board
        ans = " "
        # Top line of board
        ans += "_"*41
        ans += "\n"

        # Iterating thru each row
        for row in range(8,0,-1):
            # Adding row number for user to see
            ans += str(row)
            # Iterating thru each column
            for col in range(1,9):
                # Adds piece to a location if there is a piece in the location, otherwise adds a blank space
                if (row,col) in self.white_locations:
                    ans += "| " + str(self.white_pieces[self.white_locations.index((row,col))]) + " "
                elif (row,col) in self.black_locations:
                    ans += "| " + str(self.black_pieces[self.black_locations.index((row,col))]) + " "
                else:
                    ans += "|    "
            # Bottom line for each row
            ans += "|\n" + " " + "|____"*8 + "|\n"

        # Adding column labels
        ans += "  "
        for col in ["A","B","C","D","E","F","G","H"]:
            ans += "  " + str(col) + "  "
        # Returns board
        return ans

class Piece():
    """A class representing a chess piece
    location - tuple in (row,col) form representing where the piece is
    team - string representing which team the piece is on, either black or white
    board - the board object that the piece is located on"""

    def __init__(self,location,team,board):
        """Class constructor, see variable descriptions in class docstring"""
        self.location = location
        self.team = team
        self.moved = False
        self.board = board

    def get_location(self):
        """Returns the location instance variable of a piece"""
        return self.location

    def set_location(self,location):
        """Sets the location instance variable of a piece"""
        self.location = location

    def upper_right(self):
        """This function returns all possible moves to the upper right
        (used for bishop and queen)"""
        ##Initializing variables
        ans = []
        space = self.get_location()
        team = self.team
        # gets locations of other pieces on the board
        if team == "White":
            enemy_locations = self.board.get_black_locations()
            team_locations = self.board.get_white_locations()
        else:
            team_locations = self.board.get_black_locations()
            enemy_locations = self.board.get_white_locations()

        # Adding all moves on the upper right diagonal
        row = space[0] + 1
        col = space[1] + 1
        # While location is still on the board
        while row <= 8 and col <= 8:
            current = (row,col)
            # Checking if any pieces in the way
            if current in enemy_locations:
                ans.append(current)
                break
            elif current in team_locations:
                break
            else:
                ans.append(current)
                row += 1
                col += 1
        return ans

    def bottom_right(self):
        """This function returns all possible moves to the bottom right
        (used for bishop and queen)"""
        ##Initializing variables
        ans = []
        space = self.get_location()
        team = self.team
        # gets locations of other pieces on the board
        if team == "White":
            enemy_locations = self.board.get_black_locations()
            team_locations = self.board.get_white_locations()
        else:
            team_locations = self.board.get_black_locations()
            enemy_locations = self.board.get_white_locations()

        # Adding all moves on the lower right diagonal
        row = space[0] - 1
        col = space[1] + 1
        # While space is still on the board
        while row >= 1 and col <= 8:
            current = (row,col)
            # Checks if any pieces are in the way
            if current in enemy_locations:
                ans.append(current)
                break
            elif current in team_locations:
                break
            else:
                ans.append(current)
                row -= 1
                col += 1
        return ans

    def bottom_left(self):
        """This function returns all possible moves to the bottom left
        (used for bishop and queen)"""
        ##Initializing variables
        ans = []
        space = self.get_location()
        team = self.team
        # gets locations of other pieces on the board
        if team == "White":
            enemy_locations = self.board.get_black_locations()
            team_locations = self.board.get_white_locations()
        else:
            team_locations = self.board.get_black_locations()
            enemy_locations = self.board.get_white_locations()

        # Adding all moves on the bottom left diagonal
        row = space[0] - 1
        col = space[1] - 1
        # While piece is on the board
        while row >= 1 and col >= 1:
            current = (row,col)
            # Checks if any pieces are in the way
            if current in enemy_locations:
                ans.append(current)
                break
            elif current in team_locations:
                break
            else:
                ans.append(current)
                row -= 1
                col -= 1
        return ans

    def upper_left(self):
        """This function returns all possible moves to the upper left
        (used for bishop and queen)"""
        # Initializing variables
        ans = []
        space = self.get_location()
        team = self.team
        # gets locations of other pieces on the board
        if team == "White":
            enemy_locations = self.board.get_black_locations()
            team_locations = self.board.get_white_locations()
        else:
            team_locations = self.board.get_black_locations()
            enemy_locations = self.board.get_white_locations()

        # Adding all moves on the upper left diagonal
        row = space[0] + 1
        col = space[1] - 1
        # While piece is on the board
        while row <= 8 and col >= 1:
            current = (row,col)
            # Checks if any pieces are in the way
            if current in enemy_locations:
                ans.append(current)
                break
            elif current in team_locations:
                break
            else:
                ans.append(current)
                row += 1
                col -= 1
        return ans

    def upper(self):
        """This function returns all moves above
        (used for rook and queen)"""
        # Initializing variables
        ans = []
        space = self.get_location()
        team = self.team
        # gets locations of other pieces on the board
        if team == "White":
            enemy_locations = self.board.get_black_locations()
            team_locations = self.board.get_white_locations()
        else:
            team_locations = self.board.get_black_locations()
            enemy_locations = self.board.get_white_locations()
        # Adding all moves above piece
        for row in range(space[0] + 1,9):
            option = (row,space[1])
            # Checks if any pieces are in the way
            if option in enemy_locations:
                ans.append(option)
                break
            elif option in team_locations:
                break
            else:
                ans.append(option)
        return ans

    def right(self):
        """This function returns all moves to the right
        (used for rook and queen)"""
        # Initializing variables
        ans = []
        space = self.get_location()
        team = self.team
        # gets locations of other pieces on the board
        if team == "White":
            enemy_locations = self.board.get_black_locations()
            team_locations = self.board.get_white_locations()
        else:
            team_locations = self.board.get_black_locations()
            enemy_locations = self.board.get_white_locations()
        # Adding all valid locations to right
        for col in range(space[1] + 1, 9):
            option = (space[0],col)
            # Checks if any pieces are in the way
            if option in enemy_locations:
                ans.append(option)
                break
            elif option in team_locations:
                break
            else:
                ans.append(option)
        return ans

    def lower(self):
        """This function returns all moves below the piece
        (used for rook and queen)"""
        # Initializing variables
        ans = []
        space = self.get_location()
        team = self.team
        # gets locations of other pieces on the board
        if team == "White":
            enemy_locations = self.board.get_black_locations()
            team_locations = self.board.get_white_locations()
        else:
            team_locations = self.board.get_black_locations()
            enemy_locations = self.board.get_white_locations()
        # Adding all valid spaces below piece
        for row in range(space[0] - 1, -1,-1):
            option = (row,space[1])
            # Checks if any pieces are in the way
            if option in enemy_locations:
                ans.append(option)
                break
            elif option in team_locations:
                break
            else:
                ans.append(option)
        return ans

    def left(self):
        """This function returns all moves to the left
        (used for rook and queen)"""
        # Initializing variables
        ans = []
        space = self.get_location()
        team = self.team
        # gets locations of other pieces on the board
        if team == "White":
            enemy_locations = self.board.get_black_locations()
            team_locations = self.board.get_white_locations()
        else:
            team_locations = self.board.get_black_locations()
            enemy_locations = self.board.get_white_locations()
        # Adding all valid locations to left
        for col in range(space[1] - 1, -1, -1):
            option = (space[0],col)
            # Checks if any pieces are in the way
            if option in enemy_locations:
                ans.append(option)
                break
            elif option in team_locations:
                break
            else:
                ans.append(option)
        return ans

class Pawn(Piece):
    """A class representing a pawn object
    location - tuple in (row,col) form representing where the pawn is
    team - string representing which team the pawn is on, either black or white
    board - the board object that the pawn is located on"""

    def __init__(self,location,team,board):
        """Pawn inherits the superclass Piece constructor"""
        super(Pawn,self).__init__(location,team,board)

    def __repr__(self):
        """Representation for pawn to display piece on board"""
        if self.team == "White":
            return "WP"
        return "BP"

    def get_location(self):
        """Gets the location on the board using the superclass method"""
        return super().get_location()

    def moves(self):
        """This function returns all possible moves a pawn can have"""
        # Initializes moves
        ans = []
        space = self.get_location()
        team = self.team
        # Getting locations of other pieces
        if self.team == "White":
            enemy_locations = self.board.get_black_locations()
            team_locations = self.board.get_white_locations()
            # Locations of moving 1 and 2 spots forward also capturing
            move1 = (space[0] + 1, space[1])
            move2 = (space[0] + 2, space[1])
            capture1 = (space[0] + 1, space[1] + 1)
            capture2 = (space[0] + 1, space[1] - 1)
        else:
            team_locations = self.board.get_black_locations()
            enemy_locations = self.board.get_white_locations()
            # Locations of moving 1 and 2 spots forward also capturing
            move1 = (space[0] - 1, space[1])
            move2 = (space[0] - 2, space[1])
            capture1 = (space[0] - 1, space[1] + 1)
            capture2 = (space[0] - 1, space[1] - 1)

        # Checks if moves are in within the board boundary and there are no pieces in the way
        if (space[0] < 8) and (move1 not in enemy_locations) and (move1 not in team_locations):
            ans.append(move1)
            # Checks if a pawn has already moved, if not they can move 2 spaces
            if (self.moved == False) and (move2 not in enemy_locations) and (move2 not in team_locations):
                ans.append(move2)
        # Checks if a pawn can capture
        if capture1 in enemy_locations:
            ans.append(capture1)
        if capture2 in enemy_locations:
            ans.append(capture2)
        return ans

class Rook(Piece):
    """A class representing a rook object
    location - tuple in (row,col) form representing where the rook is
    team - string representing which team the rook is on, either black or white
    board - the board object that the rook is located on"""

    def __init__(self,location,team,board):
        """Rook inherits superclass Piece constructor"""
        super(Rook,self).__init__(location,team,board)

    def __repr__(self):
        """Representation for rook to display piece on board"""
        if self.team == "White":
            return "WR"
        return "BR"

    def get_location(self):
        """Gets the locations of the piece using superclass"""
        return super().get_location()

    def moves(self):
        """This function returns all possible moves a white rook can have"""
        ##Initializing answer
        ans = []
        # Adding all valid locations
        ans += super().upper()
        ans += super().lower()
        ans += super().left()
        ans += super().right()
        return ans

class Knight(Piece):
    """A class representing a knight object
    location - tuple in (row,col) form representing where the knight is
    team - string representing which team the knight is on, either black or white
    board - the board object that the knight is located on"""

    def __init__(self,location,team,board):
        """Knight inherits superclass Piece constructor"""
        super(Knight,self).__init__(location,team,board)

    def __repr__(self):
        """Displays the game piece"""
        if self.team == "White":
            return "WH"
        return "BH"

    def get_location(self):
        """Uses superclass to get location of piece"""
        return super().get_location()

    def moves(self):
        """This function returns all possible moves a knight can have"""
        ##Initializing variables
        ans = []
        space = self.get_location()
        team = self.team
        # Getting locations of pieces
        if team == "White":
            team_locations = self.board.get_white_locations()
        else:
            team_locations = self.board.get_black_locations()

        # Initializing the 8 possible moves
        move1 = (space[0] + 2,space[1] - 1)
        move2 = (space[0] + 2,space[1] + 1)
        move3 = (space[0] - 2,space[1] - 1)
        move4 = (space[0] - 2,space[1] + 1)
        move5 = (space[0] + 1,space[1] + 2)
        move6 = (space[0] - 1,space[1] + 2)
        move7 = (space[0] + 1,space[1] - 2)
        move8 = (space[0] - 1,space[1] - 2)
        moves = [move1,move2,move3,move4,move5,move6,move7,move8]

        # Looping thru possible moves and adding them if they are valid
        for move in moves:
            # If move is on the board and no teammate is there
            if (1 <= move[0] <= 8) and (1 <= move[1] <= 8) and (move not in team_locations):
                ans.append(move)
        return ans

class Bishop(Piece):
    """A class representing a bishop object
    location - tuple in (row,col) form representing where the piece is
    team - string representing which team the piece is on, either black or white
    board - the board object that the piece is located on"""

    def __init__(self,location,team,board):
        """Bishop inherits superclass Piece constructor"""
        super(Bishop,self).__init__(location,team,board)

    def __repr__(self):
        """Displays the game piece"""
        if self.team == "White":
            return "WB"
        return "BB"

    def get_location(self):
        """Uses superclass Piece to get location"""
        return super().get_location()

    def moves(self):
        """This function returns all possible moves a white bishop can have"""
        ##Initializing variables
        ans = []
        # Adding possible moves
        ans += super().upper_right()
        ans += super().bottom_right()
        ans += super().bottom_left()
        ans += super().upper_left()
        return ans

class Queen(Piece):
    """A class representing a queen object
    location - tuple in (row,col) form representing where the piece is
    team - string representing which team the piece is on, either black or white
    board - the board object that the piece is located on"""

    def __init__(self,location,team,board):
        """Gets constructor from piece superclass"""
        super().__init__(location,team,board)

    def __repr__(self):
        """Represents the piece"""
        if self.team == "White":
            return "WQ"
        return "BQ"

    def get_location(self):
        """Gets location using superclass function"""
        return super().get_location()

    def moves(self):
        """This function returns all possible moves a queen can have"""
        ##Initializing vanswer
        ans = []
        # Adding moves in 8 directions and returning answer
        ans += super().upper_right()
        ans += super().bottom_right()
        ans += super().bottom_left()
        ans += super().upper_left()
        ans += super().upper()
        ans += super().lower()
        ans += super().right()
        ans += super().left()
        return ans

class King(Piece):
    """A class representing a king object
    location - tuple in (row,col) form representing where the piece is
    team - string representing which team the piece is on, either black or white
    board - the board object that the piece is located on"""

    def __init__(self,location,team,board):
        """Inherits the constructor from the superclass"""
        super().__init__(location,team,board)

    def __repr__(self):
        """Displays the king"""
        if self.team == "White":
            return "WK"
        return "BK"

    def get_location(self):
        """Gets the location of the piece using the superclass"""
        return super().get_location()

    def moves(self):
        """This function returns all possible moves a king can have"""
        ##Initializing variables
        ans = []
        space = self.get_location()
        team = self.team
        # Checking the team and getting the team locations
        if self.team == "White":
            team_locations = self.board.get_white_locations()
        else:
            team_locations = self.board.get_black_locations()

        # Initializing the 8 possible moves
        move1 = (space[0] + 1,space[1] + 1)
        move2 = (space[0],space[1] + 1)
        move3 = (space[0] - 1,space[1] + 1)
        move4 = (space[0] - 1,space[1])
        move5 = (space[0] - 1,space[1] - 1)
        move6 = (space[0],space[1] - 1)
        move7 = (space[0] + 1,space[1] - 1)
        move8 = (space[0] + 1,space[1])
        moves = [move1,move2,move3,move4,move5,move6,move7,move8]

        # Looping thru possible moves and adding them if they are valid
        for move in moves:
            # If move is on the board and no teammate is in the move
            if (1 <= move[0] <= 8) and (1 <= move[1] <= 8) and (move not in team_locations):
                ans.append(move)
        return ans

class Menu:
    """A class that creates the menu structure"""

    def __init__(self):
        """The init function that prints the menu structure and the options to the user"""
        # Looping until user quits
        while True:
            #Prints menu and takes user selection
            print("1 Play Chess!\n")
            print("2 Rules of Chess\n")
            print("3 App Instructions\n")
            print("4 Quit Game\n")
            selection = input("Please enter your selection: ")
            print()

            # Checks if selection is valid
            if selection not in ["1","2","3","4"]:
                print("    Please enter a valid choice 1, 2, 3 or 4")
                print()
                continue

            # Plays chess if user specifies
            if selection == "1":
                self.chess()
                continue

            # Displays link to rules if user specifies
            if selection == "2":
                self.rules()
                continue

            # Displays app instructions
            if selection == "3":
                self.instructions()
                continue

            # Quits app
            if selection == "4":
                print("    Thanks for Playing!")
                break


    def chess(self):
        """This function plays a game of chess"""
        # Creates game board
        board = Board()
        # Looping until there is a winner or user chooses to exit
        while True:
            # Displays board
            print(board)
            # Checks if the board is in a winning state
            if board.won == True:
                print("    " + board.winner + " won!")
                print()
                break

            # Takes user input and ensures the input is correct length and checks if the user wants to quit
            print(board.turn + "'s Turn!")
            piece = input("Input location of piece to move (Ex. A1): ")
            # If user wants to quit, quit
            if piece.upper() == "QUIT":
                print()
                print("Thanks for playing!")
                print()
                break
            # Ensures correct length of input adn alphanumeric input
            if (len(piece) != 2) or not piece.isalnum():
                print("Please enter a valid input, like A1")
                continue
            # Ensures first charter is letter and second is number
            if not (piece[0].isalpha() and piece[1].isnumeric()):
                print("Ensure the first character is a letter and the second is a number")
                continue
            # Takes user input and ensures the input is correct length and checks if the user wants to quit
            move = input("Input where to move the piece (Ex. B7): ")
            print()
            # If user wants to quit, quit
            if move.upper() == "QUIT":
                print()
                print("Thanks for playing!")
                print()
                break
            # Ensures correct length of input and alphanumeric input
            if (len(move) != 2) or not move.isalnum():
                print("Please enter a valid input, like B7")
                continue
            # Ensures first character is letter and second is number
            if not (move[0].isalpha() and move[1].isnumeric()):
                print("Ensure the first character is a letter and the second is a number")
                continue
            # Excecutes move
            board.move(piece,move)

    def rules(self):
        """Prints the link to the rules of chess wikipedia page to the screen"""

        print("""    To learn the rules of chess, please visit the following wikipedia page.\n
        https://en.wikipedia.org/wiki/Rules_of_chess""")
        print()

    def instructions(self):
        """Prints instructions of the app to the screen"""

        print("""    1.) Select the Play Chess option on the menu.\n\n
    2.) Indicate the move you would like to make by first inputing the space containing the\n
    piece you would like to move, and then input the space you would like to move it to. An example\n
    opening move would be to first input 'e2' and then input 'e4' to move the pawn from space E2 to E4.\n
    The user will receive feedback if a move is invalid or if an input doesn't make sense, and the user \n
    will be given the opportunity to correct it.\n\n
    3.) Reference 'Piece Keys.txt' for codes to decipher what the pieces mean. \n\n
    4.) There are 3 moves this simulator is not capable of, the first is castling. The second is\n
    en passant. The third is when a pawn reaches the other end it is not replaced with a queen. \n
    There is also no checker for check or checkmate and the king must be captured for the game \n
    to end. Besides this all valid chess moves are possible!\n\n
    5.) At any point in a game, you can type 'quit' in the input to exit the game.\n\n
    6.) Have fun playing chess!""")
        print()

Menu()
