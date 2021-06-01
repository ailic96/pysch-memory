import random
from tkinter import *
import tkinter as tk
import csv

def file_to_list(path):
    '''
    Turns a .txt file with a word list into a Python list
    '''

    list = []

    with open(path, mode='r', encoding='utf-8') as file_reader:
        for row in file_reader:
            list.append(row.rstrip('\n'))   # Clear new line at the end of each word
    # Randomize list items 
    random.shuffle(list)
    return list



def return_correct():
    '''
    Returns 'T' if 'True' button is clicked
    '''

    global user_input
    user_input = 'T' 
    print(user_input)



def return_false():
    '''
    Returns 'N' if "False" button is clicked.
    '''

    global user_input
    user_input = 'N'
    print(user_input)



def game(list_complete_rand, correct_words, false_words, color):
    '''
    Game logic
    '''

    step_counter = 0
    score = 0
    # Iterate through a list of random words
    for word in list_complete_rand:

        # Initialize a window with random words
        window_ingame = tk.Tk()
        window_ingame.title('PySch')
        window_ingame.eval('tk::PlaceWindow . center')

        window_ingame.geometry("500x100")

        frame_game = Frame(window_ingame, bg=color)
        frame_game.pack(fill=tk.X)

        label_steps = tk.Label(frame_game, text='You have ' + str(5 - step_counter) + ' more attempts.', fg='blue', bg=color, font=('Arial',10))
        label_steps.pack(anchor=N)
        label_score = tk.Label(frame_game, text='Score: ' + str(score), bg=color, font=('Arial',10))
        label_score.pack(anchor=NW)

        label_word = tk.Label(frame_game, text=word, fg='black', bg=color, font=('Arial',15))
        label_word.place(x=25, y=25, anchor="center")
        label_word.pack()

        # Game controlling buttons
        button_true = tk.Button(frame_game, text='True', width=15, font=('Arial', 13), command=lambda: [return_correct(), window_ingame.after(1, window_ingame.destroy)])
        button_true.pack(side=LEFT)
        button_false = tk.Button(frame_game, text='False',width=15, font=('Arial', 13),  command=lambda: [return_false(), window_ingame.after(1, window_ingame.destroy)])
        button_false.pack(side=RIGHT)
        
        window_ingame.mainloop()
        
        print('Score:', score)
        print('Current word:', word)

        if word in correct_words and user_input == 'T':
            score += 1
            print('Correct!')
        elif word in false_words and user_input == 'N':
            score  += 1
            print('Correct!')
        else:
            print('Wrong!')
        
        step_counter += 1

        # Grant 5 attempts for each group of words
        if step_counter > 4:
            print('Score:', score)
            return score
   


def gui(list_complete_rand, list_correct, list_false, color):
    '''
    Initial game GUI
    '''

    # Initialize game window
    window = tk.Tk()
    window.eval('tk::PlaceWindow . center')
    window.title('PySch')

    frame = Frame(window, bg='green', width='80')
    frame.pack(fill=tk.X)

    label_title = tk.Label(master=frame, text = 'PySch Game', bg='green', font=('Arial bold',25))
    label_title.pack()

    instructions_str = '''In front of you is a list of words with a certain background color. 
    Your task is to memorize the words and determine if each of suggested words which you will face
    was present in this list of words.
    '''

    label_instructions = tk.Label(frame, text = instructions_str, bg = 'green', font=('Arial',13))
    label_instructions.pack()

    for item in list_correct:
        label_word = tk.Label(frame, text=item, fg='black', width='80', bg=color, font=('Arial',15))
        label_word.place(x=25, y=25, anchor="center")
        label_word.pack()

    # Start game button
    button_next = tk.Button(text='Next', anchor=tk.S, width=15, font=('Arial', 13), command=window.destroy)
    button_next.pack(side=RIGHT)
        
    window.mainloop()

    # Return game color results respectively
    return game(list_complete_rand, list_correct, list_false, color)



def gui_score(part_one, part_two):
    '''
    GUI which shows previoius game results
    '''

    # Initialize score window
    window_results = tk.Tk()
    window_results.title('PySch')
    window_results.eval('tk::PlaceWindow . center')
    window_results.geometry("500x250")

    frame = Frame(window_results, bg = 'green')
    frame.pack(fill=tk.X)

    total_score = part_one + part_two

    label_title = tk.Label(master=frame, text = 'Scores:', bg='green', font=('Arial bold',25))
    label_title.pack()

    # File writer
    with open('results.txt', 'a') as output_file:
        write = csv.writer(output_file, delimiter = ',', lineterminator='\n')
        write.writerow([part_one, part_two, total_score])

    # File reader
    with open('results.txt', 'r') as read_file:
        reader = csv.reader(read_file, delimiter=',')

        reader = list(reader)      
        reader = reader[-5:]  

        # Display a list of results
        for item in reader:
            data = 'White words: ' + str(item[0]) + ' Orange words: ' + str(item[1]) + ' Total: ' + str(item[2])

            label_word = tk.Label(frame, text=data, fg='black', width='80', bg='green', font=('Arial',15))
            label_word.place(x=25, y=25, anchor="center")
            label_word.pack()
    
    # Quit button
    button_quit = tk.Button(text='Exit Game', anchor=tk.S, width=15, font=('Arial', 13), command=window_results.destroy)
    button_quit.pack(side=BOTTOM)
    window_results.mainloop()



def main(): 
    '''
    Main function
    '''

    list_complete = file_to_list('words.txt')
    #list_complete = ['sretan', 'cvijet','sunce','pčela','zavjesa','gitara', 'računalo', 'monitor', 'program', 'zvučnik']
    list_white = list_complete[len(list_complete)//2:]
    list_orange = list_complete[0:len(list_complete)//2]

    # Only 5 words from each set are taken as words which are checked for the player's memory
    list_white = list_white[0:5]
    list_orange = list_orange[-5:]

    # Add three random samples which may, or may not be present in list_white and list_orange
    list_completed_rand = list_complete
    random.shuffle(list_completed_rand)

    list_completed_rand = list_completed_rand[0:3]

    # Concatenate lists for more randomness and add a few words which are not present in w/o lists
    list_selected_rand = list_white + list_orange + list_completed_rand

    # Remove duplicates if they exist
    set_selected_rand = set(list_selected_rand)
    list_selected_rand = list(set_selected_rand)
    random.shuffle(list_selected_rand)

    # Start game
    part_one = gui(list_selected_rand, list_white, list_orange, 'white')
    part_two = gui(list_selected_rand, list_orange, list_white, 'orange')

    gui_score(part_one, part_two)

# main() function call
if __name__ == '__main__':
    main()
