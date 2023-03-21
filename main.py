import random
from datetime import datetime
import matplotlib.pyplot as plt
import pyodbc

server_name = 'localhost'
database_name = 'game_database'
user_name = 'sa'
password = '3541'

connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server_name};DATABASE={database_name};UID={user_name};PWD={password}'
conn = pyodbc.connect(connection_string)


username = ""
password = ""
ID = ""


def sing():
    global right_pass
    global username
    global password
    global cursor

    while True:
        global ID
        if right_pass > 0:
            print(f"""***** STONE *-* PAPER *-* SCISSORS *****
                            WELCOME TO THE GAME

            1. Sing in
            2. Sing up.
            3. Exit game.

            """)

            info = input("Select your operation: ")
            if info == "1":
                username = input("Username: ")
                password = input("Password: ")
                cursor.execute("SELECT * FROM userpas WHERE username=? AND password=?", (username, password))
                result = cursor.fetchone()

                if result:
                    print("Logged in as", username)
                    ID = cursor.execute("SELECT id FROM userpas WHERE username = ?", (username,)).fetchone()[0]
                    return True
                else:
                    print("Please check your username and password!")
                    right_pass = right_pass - 1
                    continue

            if info == "2":
                username = input("Username: ")
                password = input("Password: ")

                cursor.execute("SELECT * FROM userpas WHERE username=?", (username,))

                if cursor.fetchone() is not None:
                    print("Please enter different username:")
                else:
                    cursor.execute("INSERT INTO userpas(username, password) VALUES (?, ?)", (username, password))
                    conn.commit()
                    print("Your account created!")

            if info == "3":
                print("Have a nice day.")
                right_pass = 0
                break
        else:
            print("Due to incorrect entry, restart the game.")
            right_pass = 0
            break


def analysis():
    global username
    while True:
        print("""**** DATA ANALYSIS ****

        1. Show my max. point?
        2. Show my min. Point?
        3. Show my score list with a bar graph.
        4. Show my score list with a line chart.
        5. Back to game screen.

        """)

        da = input("Enter your operation: ")
        if da == "1":
            b = cursor.execute(f"SELECT MAX(score) from scores where id= ?", (ID,)).fetchone()[0]
            print(f"Your max. score is {b}")
            continue

        elif da == "2":
            b = cursor.execute(f"SELECT MIN(score) from scores where id= ?", (ID,)).fetchone()[0]
            print(f"Your min. score is {b}")
            continue

        elif da == "3":
            cursor.execute(f"SELECT date, score FROM scores WHERE id = ?", (ID,))
            rows = cursor.fetchall()

            dates = [row[0] for row in rows]
            scores = [row[1] for row in rows]

            plt.bar(dates, scores)
            plt.title("Score Distribution")
            plt.xlabel("Date")
            plt.ylabel("Score")
            plt.show()
            continue

        elif da == "4":
            cursor.execute(f"SELECT date, score FROM scores WHERE id = ?", (ID,))
            rows = cursor.fetchall()

            dates = [row[0] for row in rows]
            scores = [row[1] for row in rows]

            plt.plot(dates, scores)
            plt.title("Score Distribution")
            plt.xlabel("Date")
            plt.ylabel("Score")
            plt.show()
            continue

        elif da == "5":
            break
        else:
            print("Invalid input. Please enter a valid operation number.")
            continue


def gameplay():
    global score
    global right
    global last_score
    global right_pass
    while True:
        if right > 0:
            print(f"""
                    Please select,
                    1: for Stone, 2: for Paper, 3: for Scissors
                    Press 'q' for main menu.

                    Your current score is: {score}
                    Your current right point is: {right}
                                                """)

            gamer_select = input(": ")
            if gamer_select == "q":
                break

            elif gamer_select == "1":

                game_tools = ("Stone", "Paper", "Scissors")
                game_tool = random.choice(game_tools)

                if game_tool == "Stone":
                    print("System selected Stone, DRAW!")

                elif game_tool == "Paper":
                    print("System selected Paper, LOSS!")
                    right = right - 1

                elif game_tool == "Scissors":
                    print("System selected Scissors, WON!")
                    score = score + 1

                else:
                    print("Please enter 1, 2 or 3!")
                    continue

            elif gamer_select == "2":

                game_tools = ("Stone", "Paper", "Scissors")
                game_tool = random.choice(game_tools)

                if game_tool == "Stone":
                    print("System selected Stone, WON!")
                    score = score + 1

                elif game_tool == "Paper":
                    print("System selected Paper, DRAW!")

                elif game_tool == "Scissors":
                    print("System selected Scissors, LOSS!")
                    right = right - 1

                else:
                    print("Please enter 1, 2 or 3!")
                    continue

            elif gamer_select == "3":

                game_tools = ("Stone", "Paper", "Scissors")
                game_tool = random.choice(game_tools)

                if game_tool == "Stone":
                    print("System selected Stone, LOSS!")
                    right = right - 1

                elif game_tool == "Paper":
                    print("System selected Paper, WON!")
                    score = score + 1

                elif game_tool == "Scissors":
                    print("System selected Scissors, DRAW!")

                else:
                    print("Please enter 1, 2 or 3!")
                    continue
        else:
            last_score = score
            print(f"You used to all rights point"
                  f"Loss: {last_score} point! Restarting the game.")
            right_pass = 0
            break


def save():
    global right
    global score
    global username
    global password
    global ID
    global cursor

    if score > 0:
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")

        row = cursor.execute("SELECT count(id) FROM scores WHERE id=?", ID,).fetchone()[0]
        cursor.execute(f"INSERT INTO scores (id, game, date, score) VALUES (?, ?, ?, ?)", (ID, f"game_{row + 1}", now, score))
        conn.commit()
        print(f"Your {score} points were saved in the database.")

        score = 0
        right = 3

    else:
        print("You cannot save 0 points but the game is restarting.")

        score = 0
        right = 3


def show_score():
    global cursor
    global username
    global ID

    result1 = cursor.execute("SELECT count(id) FROM scores WHERE id = ?", (ID,)).fetchone()[0]
    if result1 > 0:
        for i in range(1, result1 + 1):
            r1 = "game_" + str(i)
            result2 = cursor.execute(f"SELECT score FROM scores WHERE game = ? and id = ?", (r1, ID,)).fetchone()
            if result2:
                score1 = result2[0]
                print(f"Your {i} score is: {score1}")
    else:
        print("No scores found.")


def delete():
    global username
    global ID
    cursor.execute(f"DELETE FROM scores WHERE id = ?", (ID,))
    conn.commit()
    print("Your all data has been deleted.")


right = 3
right_pass = 3
last_score = 0
score = 0
cursor = conn.cursor()
"----- MAIN GAME CODES -----"
while True:

    sing()

    if right_pass > 0:

        while True:
            if right > 0:

                print(f"""***** STONE *-* PAPER *-* SCISSORS *****

                1. Start Game.
                2. Back to login screen.
                3. Show my score?
                4. Save my score, and restart the game!

                7. Open analysis panel.
                9. Clean my database!

                You have three right, dont forget!

                                                                    """)
                log = input("Enter your operation: ")

                if log == "1":
                    gameplay()

                elif log == "2":
                    print("Login out!")
                    break

                elif log == "3":
                    show_score()

                elif log == "4":
                    save()

                elif log == "7":
                    analysis()

                elif log == "9":
                    delete()

                else:
                    print("Please enter 1, 2, 3 or 4!")
                    continue

            else:
                print("your right is 0 and all your scores are deleted! Please start the game again!")
                break

    else:
        conn.close()
        break
