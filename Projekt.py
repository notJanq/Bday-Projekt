
import tkinter as tk
from tkinter import ttk
import random
import time

root = tk.Tk() #create window

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#FF00AA")

root.configure(bg="pink")
root.geometry("900x700")
root.title("Alles Gute Zum Gebusrtstag!")

#txt_input = tk.Entry(root, width=24)
#txt_input.place(x=350, y=260)

lbl_title = tk.Label(root, text="Klick dich einf durch:)", bg="lightblue", font=("Times", 12, "bold")) #Text
lbl_title.place(x=1, y=1)


#functions


#def textfield():
    #textfield = txt_input.get() #Textfeld


def next_button():
    global index 
    buttons[index].pack_forget()

    index += 1

    if index < len(buttons):
        buttons[index].pack(pady=20)


current_button = None
current_index = 0

def show_question():
    frage_label = tk.Label(root, text="Liebst du mich?")
    frage_label.place(x=350, y=180)

    eingabe = tk.Entry(root)
    eingabe.place(x=350, y=200)

    def weiter_klicken1():
        frage_label.destroy()
        eingabe.destroy()
        pruef_button.destroy()
        reaction_label.destroy()
        start_game_button()
        
    def check_answer():
        antwort = eingabe.get()

        if antwort.lower() == "ja":
            show_reaction1()
            weiter_button = tk.Button(root, text="Weiter", command=weiter_klicken1)
            weiter_button.place(x=350, y=270)

    # ERST NACH Definition erstellen
    pruef_button = tk.Button(root, text="Antwort prüfen", command=check_answer)
    pruef_button.place(x=350, y=230)
    

def show_reaction1():
    global reaction_label
    reaction_label = tk.Label(root, text="Ich dich auch<33")
    reaction_label.place(x=350, y=100)

def next_button():
    global current_button, current_index

    if current_button:
        current_button.place_forget()

    if current_index < len(buttons):
        current_button = buttons[current_index]
        current_button.place(x=400, y=150)
        current_index += 1
    else:
        show_question() ###

def next_button1():
    show_car_game()
    
def start_game_button():
    start_button = tk.Button(root, text = "Spiel starten", command = next_button1)
    start_button.place(x=400, y=150)


def show_car_game():

    # alte Widgets entfernen
    for widget in root.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(root, width=900, height=700, bg="green")
    canvas.pack()

    # Straße
    canvas.create_rectangle(300, 0, 600, 700, fill="gray")

    # Fahrspuren
    canvas.create_line(400, 0, 400, 700, dash=(20,20), width=4, fill="white")
    canvas.create_line(500, 0, 500, 700, dash=(20,20), width=4, fill="white")

    # Spielerauto
    car = canvas.create_rectangle(430, 600, 470, 650, fill="pink")

    # Timer Anzeige
    timer_text = canvas.create_text(
        800, 40,
        text="Zeit: 30",
        font=("Verdana", 18, "bold"),
        fill="white"
    )

    enemy_cars = []

    speed = 80
    game_running = True
    start_time = time.time()

    # Bewegung
    def move_left(event):
        if game_running:
            canvas.move(car, -40, 0)
            check_grass()

    def move_right(event):
        if game_running:
            canvas.move(car, 40, 0)
            check_grass()

    root.bind("<Left>", move_left)
    root.bind("<Right>", move_right)

    # Prüfen, ob Auto auf Gras fährt
    def check_grass():
        nonlocal game_running
        car_pos = canvas.coords(car)
        # links oder rechts außerhalb der Straße?
        if car_pos[0] < 300 or car_pos[2] > 600:
            canvas.create_text(
                450, 350,
                text="Wohin braski, nicht in Graben fahren 😆\nNeuer Versuch",
                font=("Times", 28)
            )
            game_running = False
            root.after(2000, show_car_game)

    # Gegner erzeugen
    def spawn_enemy():
        if not game_running:
            return
        x_positions = [330, 430, 530]
        x = random.choice(x_positions)
        enemy = canvas.create_rectangle(x, -100, x+40, -50, fill="red")
        enemy_cars.append(enemy)
        root.after(1500, spawn_enemy)

    # Gegner bewegen
    def move_enemies():
        if not game_running:
            return
        for enemy in enemy_cars[:]:
            canvas.move(enemy, 0, speed)
            pos = canvas.coords(enemy)
            if pos[1] > 700:
                canvas.delete(enemy)
                enemy_cars.remove(enemy)
        root.after(50, move_enemies)

    # Kollision prüfen
    def check_collision():
        nonlocal game_running
        if not game_running:
            return
        car_pos = canvas.coords(car)
        for enemy in enemy_cars:
            enemy_pos = canvas.coords(enemy)
            if (car_pos[0] < enemy_pos[2] and
                car_pos[2] > enemy_pos[0] and
                car_pos[1] < enemy_pos[3] and
                car_pos[3] > enemy_pos[1]):
                canvas.create_text(
                    450, 350,
                    text="Bist du sicher bereit für den Verkehr? :P\nVersuchs nochmal",
                    font=("Times", 28)
                )
                game_running = False
                root.after(2000, show_car_game)
                return
        root.after(50, check_collision)

    # Timer prüfen
    def check_timer():
        nonlocal game_running
        if not game_running:
            return
        elapsed = int(time.time() - start_time)
        remaining = 30 - elapsed ###
        canvas.itemconfig(timer_text, text=f"Zeit: {remaining}")
        if remaining <= 0:
            game_running = False
            canvas.create_text(
                450, 300,
                text="YIPPIE! Du bist fr bereit fuers Auto fahren:D",
                font=("Times", 28)
            )
            quiz_screen()
            # Weiter Button zum Beenden des Spiels
            weiter_button = tk.Button(root, text="Weiter", font=("Verdana", 16, "bold"),
                                     command=lambda: canvas.destroy())
            weiter_button.place(x=400, y=400)
            
        root.after(100, check_timer)
                    
        
        return
    # Start Game Loop
    spawn_enemy()
    move_enemies()
    check_collision()
    check_timer()
    
 



#buttons


buttons = [
    tk.Button(root, text = "Klick mich", command = next_button),
    tk.Button(root, text = "Nochmal", command = next_button),
    tk.Button(root, text = "Nochmal:P", command = next_button),
    tk.Button(root, text = "Gut gemacht;)", command = next_button),

]

index = 0

buttons[0].pack(pady=20)

def quiz_screen():
   

    def check_answer(answer):
        if answer == "C":
            result_label.config(text="Richtig!")
            final_screen()
        else:
            result_label.config(text="Leider nicht Nikita, sei ein Goodboy und geh nicht drauf ein")

    

    question_label = tk.Label(root, text="Wie reagiere ich auf provokation von anderen Verkehrsteilnehmern?")
    question_label.pack()

    button_a = tk.Button(root, text="A: Ich spame Lichthupe", command=lambda: check_answer("A"))
    button_a.pack()

    button_b = tk.Button(root, text="B: Ich ueberhole ihn und brems ihn aus", command=lambda: check_answer("B"))
    button_b.pack()

    button_c = tk.Button(root, text="C: Ich gehe nicht drauf ein und fahre wie ein goodboy normal weiter", command=lambda: check_answer("C"))
    button_c.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

def final_screen():
    # Alle alten Widgets entfernen
    for widget in root.winfo_children():
        widget.destroy()

    # Final-Text
    end_label = tk.Label(root, text="SUPI, du bist bereit fürs Erwachsenenleben.\nAlles Gute zum Geburtstag mein Schatz<3",
                         font=("Times", 16), justify="center")
    end_label.pack(pady=50)

    # Optional: Button zum Beenden
    close_btn = tk.Button(root, text="Beenden", font=("Arial", 14), command=root.destroy)
    close_btn.pack(pady=20)

    








#start main event loop
root.mainloop()