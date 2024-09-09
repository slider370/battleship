
def shipLocations(LOCATIONS, SHIP_STATUS, MISSES, MISSTOTAL, END_GAME, board, LOCATION_TRANSLATION, CHOICE_HISTORY, name, check):
    try:
        with open('ships.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                ship = line.strip().split(', ')
                if len(ship) == 2:
                    LOCATIONS.update({"SHIP2": ship})
                elif len(ship) == 3:
                    LOCATIONS.update({"SHIP3": ship})
                elif len(ship) == 4:
                    LOCATIONS.update({"SHIP4": ship})
                elif len(ship) == 5:
                    LOCATIONS.update({"SHIP5": ship})
                elif len(ship) == 6:
                    LOCATIONS.update({"SHIP6": ship})
        return LOCATIONS
    except FileNotFoundError:
        print("ships.txt file not found.")
        status = gameOver(1, '', SHIP_STATUS, MISSES, MISSTOTAL, board, LOCATIONS, CHOICE_HISTORY, LOCATION_TRANSLATION, name);
        if status == True:
            check[0] = True;
            return;

def printBoard(board, SHIP_STATUS, MISSES ,MISSTOTAL, final, SHIP_LOCATIONS, CHOICE_HISTORY, LOCATION_TRANSLATION):

    if final == 1:
        for ship, location in SHIP_LOCATIONS.items():
            for spot in location:
                if spot not in CHOICE_HISTORY:
                    row = int(LOCATION_TRANSLATION[spot[0]])
                    column = int(spot[1:])
                    board[row][column] = "?"
                     
    for row in board:
        for num in row:
            print(num +5*" ", end="");
        print()
        print("-"*65)
        print()
    print(f"MISSES:{MISSES[0]} out of {MISSTOTAL}")
    print("SHIPS SUNK: ", end="")
    for ship in SHIP_STATUS:
        if SHIP_STATUS[ship] == False:
            print(ship, " ", end="");
    

    print()

def playerChoice(name, guess, SHIP_STATUS, MISSES, MISSTOTAL):

    while True:
        guess = input(f"{name}, choose a location to shoot (EX: B1, J10, etc): ")

        if guess.upper() == "quit".upper():
            return guess;
        
        if (len(guess) > 3) or (len(guess) < 2):
            print(f"Invalid Guess. Try Again {name}")
            continue;

        if len(guess) == 2:
            row = guess[0].upper();
            column = guess[1];
            if not (row.isalpha() and row in "ABCDEFGHIJ" and column.isdigit() and (1 <= int(column) <= 10)):
                print(f"Invalid Guess. Try Again {name}.")
                continue;

        if len(guess) == 3:
            row = guess[0];
            column = guess[1:];
            if not (row.isalpha() and row in "ABCDEFGHIJ" and column.isdigit() and (1 <= int(column) <= 10)):
                print(f"Invalid Guess. Try Again {name}.")
                continue;
        return guess;

def checkChoice(GUESS, CHOICE_HISTORY,LOCATION_TRANSLATION, SHIP_STATUS, SHIP_LOCATIONS, board, name, MISSTOTAL, MISSES):
    HIT = False;
    MISS = False;
    if GUESS in CHOICE_HISTORY:
        print("This guess is a repeat. Try Again.")
        return;
    else:
        CHOICE_HISTORY.add(GUESS);

    for ship, spot in SHIP_LOCATIONS.items():
        if GUESS in spot:
            row = LOCATION_TRANSLATION[GUESS[0]]
            column = int(GUESS[1:])
            board[row][column] = "X";
            print(GUESS, "WAS A HIT.")
            HIT = True;

            if set(spot).issubset(CHOICE_HISTORY):
                print(ship, "SUNK");
                SHIP_STATUS[ship] = False;
                return;
            return;

    if HIT == False:
        MISS = True;
        row = LOCATION_TRANSLATION[GUESS[0]]
        column = int(GUESS[1:])
        board[row][column] = "M"
        print(GUESS, "WAS A MISS")
        MISSES[0] +=1;
        return;

def gameOver(FILEREADIN, guess, SHIP_STATUS, MISSES, MISSTOTAL, board, SHIP_LOCATIONS, CHOICE_HISTORY, LOCATION_TRANSLATION, name):
    SINK_COUNT = 0;

    if FILEREADIN == 1:
        print(f"{name}, ships.txt has failed to load")
        print("----------ENDING GAME DUE TO SHIPS.TXT NOT FOUND----------")
        END_GAME = True;
        return True;

    if MISSES[0] == MISSTOTAL:
        print(f"You have reached the Maximum Misses. GAME OVER {name.upper()}")
        END_GAME = True;
        print("Here is all the places you missed, indicated by a ?")
        printBoard(board, SHIP_STATUS, MISSES ,MISSTOTAL, 1, SHIP_LOCATIONS, CHOICE_HISTORY, LOCATION_TRANSLATION)
        return True;
    if guess.upper() == "QUIT":
        print(f"----------STOPPING THE GAME, QUIT REQUESTED BY {name}----------")
        END_GAME = True;
        return True;
    
    for x in SHIP_STATUS.values():
        if x == False:
            SINK_COUNT+=1
        if SINK_COUNT == 5:
            printBoard(board, SHIP_STATUS, MISSES ,MISSTOTAL, 0, SHIP_LOCATIONS, CHOICE_HISTORY, LOCATION_TRANSLATION)
            print(f"----------ALL SHIPS SUNK, CONGRATULATIONS {name.upper()}!----------")
            END_GAME = True;
            return True;
    END_GAME = False;
    return False;

def main():
    MISSTOTAL = 20;
    MISSES = [0];
    SHIP_STATUS = {
    "SHIP2": True,
    "SHIP3": True,
    "SHIP4": True,
    "SHIP5": True,
    "SHIP6": True
    }
    END_GAME = False;
    CHOICE_HISTORY = set()

    SHIP_LOCATIONS = {}

    LOCATION_TRANSLATION = {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
        "E": 5,
        "F": 6,
        "G": 7,
        "H": 8,
        "I": 9,
        "J": 10
    }

    board = [
        [" ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        ["A", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
        ["B", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
        ["C", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
        ["D", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
        ["E", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
        ["F", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
        ["G", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
        ["H", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
        ["I", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
        ["J", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]
    ]
 
    name = input("Enter your name: ");
    print(f"----------Hello {name}, Welcome to SMS!----------")
    print(f"The goal is to sink all the ships before you have {MISSTOTAL} missed shots.")
    guess = ''
    check = [False]
    shipLocations(SHIP_LOCATIONS, SHIP_STATUS, MISSES, MISSTOTAL, END_GAME, board, LOCATION_TRANSLATION, CHOICE_HISTORY, name, check)

    if check[0] == True:
        END_GAME = True;

    while END_GAME != True:
        if END_GAME == True:
            break;
        printBoard(board, SHIP_STATUS, MISSES ,MISSTOTAL, 0, SHIP_LOCATIONS, CHOICE_HISTORY, LOCATION_TRANSLATION);
        guess = playerChoice(name, guess, SHIP_STATUS, MISSES, MISSTOTAL)
        END_GAME = gameOver(0, guess, SHIP_STATUS, MISSES, MISSTOTAL, board, SHIP_LOCATIONS, CHOICE_HISTORY, LOCATION_TRANSLATION, name)
        if END_GAME == True:
            break;
        checkChoice(guess, CHOICE_HISTORY,LOCATION_TRANSLATION, SHIP_STATUS, SHIP_LOCATIONS, board, name, MISSTOTAL, MISSES)
        END_GAME = gameOver(0, guess, SHIP_STATUS, MISSES, MISSTOTAL, board, SHIP_LOCATIONS, CHOICE_HISTORY, LOCATION_TRANSLATION, name)


main();


