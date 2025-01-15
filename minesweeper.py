# echipa F21 , Gingu Alexandra-Gabriela si Stancu Robert-Costin , 424F UPB ETTI , joc de Minesweeper

import tkinter as tk
import random

class Minesweeper:
    def __init__(self, root, size=5, num_mines=5):
        self.size = size
        self.num_mines = num_mines
        self.board = []
        self.revealed = set()
        self.flagged = set()
        self.mines = set()
        self.game_ended = False  # aici am facut o variabila care determina daca jocul s-a terminat sau nu


        # Fereastra principală
        self.root = root
        self.root.title("Minesweeper")
        self.root.geometry("400x400")  # aici am setat dimnesiunile ferestrei
        self.root.resizable(False, False)  # si ne-am asigurat sa nu poata fi redimensionata


        # un frame care ajuta la centrarea jocului
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)


        # crearea grilei
        self.buttons = {}
        for i in range(size):
            for j in range(size):
                button = tk.Button(self.frame, width=4, height=2, command=lambda i=i, j=j: self.reveal(i, j), relief="raised", bg="#d3d3d3", font=("Arial", 10))

                button.bind("<Button-3>", lambda event, i=i, j=j: self.flag(event, i, j))  # click dreapta pentru flag (steag)(optiunea de a bloca casuta)

                button.grid(row=i, column=j, padx=5, pady=5)

                self.buttons[(i, j)] = button



        # functie pentru plasarea minelor
        self.place_mines()


    def place_mines(self):
        while len(self.mines) < self.num_mines:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            self.mines.add((x, y))


    def reveal(self, x, y):
        if self.game_ended:  # daca jocul s-a terminat, nu mai facem nimic
            return


        # daca celula e deja dezvaluita sau are steag, nu facem nimic
        if (x, y) in self.revealed or (x, y) in self.flagged:
            return


        # daca este mina, am explodat si jocul se termina
        if (x, y) in self.mines:
            self.buttons[(x, y)].config(text="X", bg="red", fg="white")
            self.game_over()
            return


        # daca nu este mina, se continua jocul, dezvaluindu-se casuta
        self.revealed.add((x, y))
        adjacent_mines = self.count_adjacent_mines(x, y)
        if adjacent_mines > 0:
            self.buttons[(x, y)].config(text=str(adjacent_mines), bg="lightblue")
        else:
            self.buttons[(x, y)].config(text="0", bg="lightgray")  # adaugam textul "0" pentru celulele fără mine


        # daca nu exista mine adiacente, dezvaluim și vecinii
        if adjacent_mines == 0:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        self.reveal(nx, ny)


        # dupa ce celula este dezvaluita, o facem inaccesibila , exact ca la flag
        self.buttons[(x, y)].config(state="disabled")


        # verificam daca am castigat
        self.check_win()


    def flag(self, event, x, y):
        if self.game_ended:  # daca jocul s-a terminat, nu mai facem nimic
            return


        # click dreapta pentru a marca o celula cu flag
        if (x, y) in self.revealed:
            return
        if (x, y) not in self.flagged:
            self.buttons[(x, y)].config(text="F", fg="blue", bg="yellow")
            self.flagged.add((x, y))
        else:
            self.buttons[(x, y)].config(text="", bg="#d3d3d3")
            self.flagged.remove((x, y))


    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if (nx, ny) in self.mines:
                    count += 1
        return count


    def check_win(self):
        # aici verificam daca toate celulele care nu sunt mine sunt dezvaluite
        if self.game_ended:  # daca jocul s-a terminat deja, nu mai are rost sa verificam
            return


        for i in range(self.size):
            for j in range(self.size):
                if (i, j) not in self.mines and (i, j) not in self.revealed:
                    return  # daca exista celule care nu sunt dezvaluite, continuam jocul


        self.game_won()



    def game_over(self):

        self.game_ended = True
        for (x, y) in self.mines:
            self.buttons[(x, y)].config(text="X", bg="pink", fg="white")
        self.show_message("Game Over")



    def game_won(self):

        self.game_ended = True
        for (x, y) in self.mines:
            self.buttons[(x, y)].config(bg="green", fg="white")
        self.show_message("You Won!")



    def show_message(self, message):   # o functie pentru mesajul de final si blocarea casutelor (fiindca jocul s-a terminat)

        message_box = tk.Toplevel(self.root)

        message_box.title("Game Over")

        label = tk.Label(message_box, text=message, font=("Arial", 12), padx=20, pady=20)
        label.pack()

        button = tk.Button(message_box, text="OK", command=lambda: self.quit_game(message_box))
        button.pack(pady=5)


    def quit_game(self, message_box):

        message_box.destroy()  # inchide fereastra cu mesajul

        self.root.quit()  # opreste programul



if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root, size=5, num_mines=5)
    root.mainloop()
