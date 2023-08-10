from tkinter import *
from tkinter import ttk
from nltk.corpus import brown
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import sys
import threading
import ttkthemes as td
import pickle
from nltk.corpus import wordnet
import json

root = td.ThemedTk()
style = ttk.Style()
# Global variable to store the timeout id
timeout_id = None
suggestion_labels = []
word_freq_dist = FreqDist(brown.words())  # Calculate word frequency distribution only once

# Custom dictionary set to store user-defined words
custom_dictionary = set()

def save_custom_dictionary():
    with open("custom_dictionary.json", "w", encoding="utf-8") as file:
        json.dump(list(custom_dictionary), file, ensure_ascii=False)
 
       
def load_custom_dictionary():
    try:
        with open("custom_dictionary.json", "r", encoding="utf-8") as file:
            return set(json.load(file))
     
    except FileNotFoundError:
        return set()

def print_custom_dictionary_hover(event):
    print_custom_dictionary()

def print_custom_dictionary():
    # Print the custom dictionary entries to the console
    print("Custom Dictionary:")
    for word in custom_dictionary:
        print(word)

def on_enter(e):
    global timeout_id

    # Cancel any existing timeout
    if timeout_id is not None:
        root.after_cancel(timeout_id)
        timeout_id = None

    button_text = e.widget.cget("text")

    if button_text not in ['Space', 'Print Custom Dictionary']:
        textarea.focus_set()  # Set focus to the text area

    def add_text():
        nonlocal button_text

        if button_text == 'Space':
            current_text = textarea.get(1.0, END)
            current_text = current_text.rstrip('\n')
            words = current_text.split()

            if words and len(words) >= 1:
                previous_word = words[-1].lower()
                custom_dictionary.add(previous_word)  # Add previous word to custom dictionary
                print(f"Adding '{previous_word}' to custom dictionary")
            textarea.insert(INSERT, ' ')
            update_suggestion_labels([])  # Clear suggestions when hovering over 'Space'
            button_text = ''  # Clear button_text after processing 'Space'
        elif button_text == 'Esc':
            root.destroy()
            sys.exit()
        elif button_text == 'Enter':
            textarea.insert(INSERT, '\n')
        elif button_text == 'Tab':
            textarea.insert(INSERT, '\t')
        elif button_text == 'Del':
            textarea.delete(1.0, END)
            update_suggestion_labels([])  # Clear suggestions when hovering over 'DEL'
            button_text = ''
        elif button_text == 'Backs':
            i = textarea.get(1.0, END)
            newtext = i[:-2]
            textarea.delete(1.0, END)
            textarea.insert(INSERT, newtext)
            button_text = ''  # Clear button_text after processing Backs
            update_suggestions()  # Update suggestions after 'Backs' is used
        elif button_text == 'Shift ↑':
            # Update the keyboard layout
            update_keyboard_layout(leftShiftButtons)
        elif button_text == '↑ Shift':
            # Update the keyboard layout
            update_keyboard_layout(buttons)
        elif button_text == 'Caps':
            # Update the keyboard layout
            update_keyboard_layout(capsButtons)
        elif button_text == 'CAPS':
            # Update the keyboard layout
            update_keyboard_layout(buttons)
        elif button_text not in ['Custom', 'Print Custom Dictionary']:
            textarea.insert(INSERT, button_text)

        if button_text not in ['Space', 'Custom', 'Print Custom Dictionary']:
            # Get the current text in the text area
            current_text = textarea.get(1.0, END)

            # Remove the trailing newline character
            current_text = current_text.rstrip('\n')

            # Split the text into words
            words = current_text.split()

            if words:
                # Get the last word from the text area
                last_word = words[-1]
                # Generate word suggestions for the last word
                suggestions = generate_word_suggestions(last_word, num_suggestions=6)

                # Update the suggestions label with the new suggestions
                update_suggestion_labels(suggestions)

    if button_text not in ['Space', 'Custom', 'Print Custom Dictionary']:
        textarea.focus_set()

    timeout_id = root.after(1000, add_text)

    e.widget.config(bg="#ccc", fg="#000")

def update_suggestion_labels(suggestions):
    # Clear existing labels
    for label in suggestion_labels:
        label.destroy()

    # Clear the list of suggestion labels
    suggestion_labels.clear()

    # Create new suggestion labels and display them horizontally
    for i, suggestion in enumerate(suggestions):
        label = ttk.Label(suggestion_frame, text=suggestion, font=('arial', 15, 'bold'), style='TLabel', anchor='w', background='black', foreground='white')
        label.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
        suggestion_labels.append(label)
        label.bind("<Enter>", on_label_enter)
        label.bind("<Leave>", on_label_leave)

def on_label_enter(event):
    label = event.widget
    # Get the current text in the text area
    current_text = textarea.get(1.0, END)

    # Remove the trailing newline character
    current_text = current_text.rstrip('\n')

    # Split the text into words
    words = current_text.split()
    if words and len(words) >= 2:
        previous_word = words[-2].lower()
        custom_dictionary.add(previous_word)  # Add previous word to custom dictionary
        print(f"Adding '{previous_word}' to custom dictionary")
    if words:
        # Remove the last word from the text area
        textarea.delete(1.0, END)
        new_text = ' '.join(words[:-1])

        # Append the label's text to the text area
        new_word = label.cget("text")
        textarea.insert(INSERT, new_text + ' ' + new_word)
        
        # Add the new word to the custom dictionary
        custom_dictionary.add(new_word)
        print(f"Adding '{new_word}' to custom dictionary")

        update_suggestions()
    else:
        # If there are no words, just insert the label's text
        textarea.insert(INSERT, label.cget("text"))

def on_label_leave(event):
    update_suggestion_labels([])  # Clear suggestions when hovering over other labels

def on_leave(e):
    global timeout_id

    # Cancel any existing timeout
    if timeout_id is not None:
        root.after_cancel(timeout_id)
        timeout_id = None

    e.widget.config(background="#333", foreground="#fff")

def handle(e):
    textarea.focus_set()

def select(value):
    if value == 'Space':
        textarea.insert(INSERT, ' ')
    elif value == 'Enter':
        textarea.insert(INSERT, '\n')
    elif value == 'Tab':
        textarea.insert(INSERT, '\t')
    elif value == 'Del':
        textarea.delete(1.0, END)
    elif value == 'Backs':
        i = textarea.get(1.0, END)
        newtext = i[:-2]
        textarea.delete(1.0, END)
        textarea.insert(INSERT, newtext)
    elif value == 'Shift ↑':
        # Update the keyboard layout
        update_keyboard_layout(leftShiftButtons)
    elif value == '↑ Shift':
        # Update the keyboard layout
        update_keyboard_layout(buttons)
    elif value == 'Caps':
        # Update the keyboard layout
        update_keyboard_layout(capsButtons)
    elif value == 'CAPS':
        # Update the keyboard layout
        update_keyboard_layout(buttons)
    else:
        textarea.insert(INSERT, value)
    textarea.focus_set()
def update_keyboard_layout(new_buttons, change_layout=True):
    # Clear existing buttons
    for child in root.winfo_children():
        if isinstance(child, ttk.Button):
            child.destroy()

    # Create new buttons based on the provided layout
    varRow = 3
    varColumn = 0
    for button in new_buttons:
        command = lambda x=button: select(x)
        if button != 'Space':
            btn = ttk.Button(root, text=button, command=command, width=10, padding=(10, 10), style='KeyboardButton.TButton')
            btn.grid(row=varRow, column=varColumn, padx=2, pady=2,sticky='nsew')
        if button == 'Space':
            btn = ttk.Button(root, text=button, command=command, width=30, padding=(10, 10), style='KeyboardButton.TButton')
            btn.grid(row=8, column=0, columnspan=14, padx=2, pady=2)

        varColumn += 1
        if varColumn > 14:
            varColumn = 0
            varRow += 1
        btn.bind("<Button-1>", handle)
        btn.bind("<ButtonRelease-1>", on_enter)
        btn.bind("<Enter>", lambda e: update_keyboard_layout(buttons, False))  # Keep original layout on hover
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    print_custom_dict_button = ttk.Button(root, text="Print Dict", command=print_custom_dictionary, width=12, padding=(10, 10), style='CustomButton.TButton')
    print_custom_dict_button.grid(row=8, column=12, padx=4, pady=4)
    print_custom_dict_button.bind("<Enter>",print_custom_dictionary_hover)  # Bind only on hovering

    custom_dict_button = ttk.Button(root, text="Custom", command=on_custom_dict_button_hover, width=10, padding=(10, 10), style='CustomButton.TButton')
    custom_dict_button.grid(row=8, column=13, padx=4, pady=4)
    custom_dict_button.bind("<Button-1>", handle)
    custom_dict_button.bind("<ButtonRelease-1>", on_enter)
    custom_dict_button.bind("<Enter>", on_enter)
    custom_dict_button.bind("<Leave>", on_leave)
    custom_dict_button.bind("<Enter>", on_custom_dict_button_hover)

    suggestions_label.grid(row=2, column=0, columnspan=15, padx=10, pady=10)


def generate_word_suggestions(input_text, num_suggestions=6):
    suggestions = []

    # Get the first token as the base word
    tokens = word_tokenize(input_text)
    if tokens:
        base_word = tokens[-1].lower()
    else:
        return suggestions

    # First, check for suggestions in the custom dictionary
    custom_suggestions = [word for word in custom_dictionary if word.lower().startswith(base_word)]
    suggestions.extend(custom_suggestions)

    # If there are not enough suggestions from the custom dictionary, use WordNet
    while len(suggestions) < num_suggestions:
        # Filter words from WordNet that start with the base word
        synsets = wordnet.synsets(base_word)
        wordnet_suggestions = set([lemma.name() for synset in synsets for lemma in synset.lemmas()])
        wordnet_suggestions = [word for word in wordnet_suggestions if word.lower().startswith(base_word)]
        wordnet_suggestions = [word for word in wordnet_suggestions if word not in custom_dictionary and word not in suggestions]
        
        if not wordnet_suggestions:
            break
        suggestions.extend(wordnet_suggestions)

    # Select the top 'num_suggestions'
    suggestions = suggestions[:num_suggestions]

    return suggestions
keyboard_color = "black"

def update_keyboard_color():
    for child in root.winfo_children():
        if isinstance(child, ttk.Button):
            child.configure(style=f'KeyboardButton{keyboard_color.capitalize()}.TButton')
        if isinstance(child, Text):
            child.configure(bg=keyboard_color)
        if isinstance(child, ttk.Label):
            child.configure(style=f'TLabel{keyboard_color.capitalize()}.TLabel')

def initial_suggestions():
    # Load the custom dictionary from file
    global custom_dictionary
    custom_dictionary = load_custom_dictionary()
    print_custom_dictionary()

    # Call this function to show initial suggestions when the application starts
    update_suggestions()

def update_suggestions(event=None):
    # Get the current text in the text area
    current_text = textarea.get(1.0, END)

    # Remove the trailing newline character
    current_text = current_text.rstrip('\n')

    # Split the text into words
    words = current_text.split()

    if words:
        # Get the last word from the text area
        last_word = words[-1]
        # Generate word suggestions for the last word
        suggestions = generate_word_suggestions(last_word, num_suggestions=6)

        # Update the suggestions label with the new suggestions
        update_suggestion_labels(suggestions)
    else:
        # No words, so display empty suggestions
        update_suggestion_labels([])

def minimize_window(event=None):
    root.iconify()

def close_window(event=None):
    # Save the custom dictionary to file
    save_custom_dictionary()
    root.quit()
def toggle_keyboard_color():
    global keyboard_color
    if keyboard_color == "black":
        keyboard_color = "blue"
    else:
        keyboard_color = "black"
    update_keyboard_color()

# ... (rest of the code)
def submit_custom_words(words_list):
    for custom_word in words_list:
        if custom_word:
            # Add each custom word to the custom dictionary
            custom_dictionary.add(custom_word)
            print(f"Adding '{custom_word}' to custom dictionary")
    update_suggestions()

def submit_custom_word(event=None):  # Modify the submit_custom_word function to take an optional event argument
  
        custom_words = custom_entry.get("1.0", "end-1c").split()  # Split text by spaces
        for custom_word in custom_words:
           if custom_word:
            # Add each custom word to the custom dictionary
            custom_dictionary.add(custom_word)
            print(f"Adding '{custom_word}' to custom dictionary")
        update_suggestions()
        custom_window.destroy()

def on_custom_dict_button_hover(event):
    global custom_window, custom_entry
    custom_window = Toplevel(root)
    custom_window.title("Custom Dictionary Entry")
    custom_window.geometry("500x200")
    custom_window.resizable(0, 0)

    custom_label = Label(custom_window, text="Enter custom word:", font=('arial', 12))
    custom_label.pack(pady=10)
    custom_entry = Text(custom_window, font=('arial', 12), height=3, width=50)
    custom_entry.pack(pady=5)

   
    custom_entry.bind("<Return>", lambda event: submit_custom_word())

    custom_button = ttk.Button(custom_window, text="Submit", command=submit_custom_word, width=10, padding=(10, 10), style='CustomButton.TButton')
    custom_button.pack(pady=10)
    custom_button.bind("<Return>", lambda event: submit_custom_word())
    custom_button.bind("<Enter>", on_custom_button_hover)  # Bind the new function on hovering
    custom_button.bind("<Leave>", on_custom_button_leave)
    custom_button.bind("<Enter>", submit_custom_word)  

  
def on_custom_button_hover(event):
    custom_button = event.widget
    custom_button.configure(style='CustomButtonHover.TButton')  # Change the style on hovering

def empty_custom_dictionary():
    global custom_dictionary
    custom_dictionary.clear()
    print("Custom dictionary has been emptied.")
def on_custom_button_leave(event):
    custom_button = event.widget
    custom_button.configure(style='CustomButton.TButton')  # Change the style back when leaving
def clear_dictionary(event=None):
    empty_custom_dictionary()
    print_custom_dictionary()

def on_custom_dict_button_leave(event):
    # Clear the text in the popup entry when the mouse leaves the "Submit" button
    custom_entry.delete(0, END)

# root = td.ThemedTk()
# style = ttk.Style()
style.configure('CustomButton.TButton', padding=(6, 6), font=('Arial', 20))  # Original style for the Custom button
style.map('CustomButton.TButton',
          foreground=[('pressed', 'blue'), ('active', 'blue')],
          background=[('pressed', '!disabled', 'orange'), ('active', 'orange')])

style.configure('CustomButtonHover.TButton', padding=(10, 10), font=('Arial', 20), background='yellow', foreground='black')
style.configure('KeyboardButton.TButton', padding=(6, 6), font=('Arial', 20))
style.configure('ShiftButton.TButton', padding=(6, 6), font=('Arial', 20), background='light blue')
style.configure('ShiftEscButton.TButton', padding=(6, 6), font=('Arial', 20), background='red', foreground='white')
style.configure('CapsButton.TButton', padding=(6, 6), font=('Arial', 20), background='light green')
style.configure('CustomButton.TButton', padding=(6, 6), font=('Arial', 20))  # New style for the Custom button
style.map('KeyboardButton.TButton',
          foreground=[('pressed', 'blue'), ('active', 'blue')],
          background=[('pressed', '!disabled', 'orange'), ('active', 'orange')])
root.get_themes()
root.configure(bg="black")
root.title("On Screen Keyboard")
root.set_theme('black')
root.resizable(0, 0)

suggestion_frame = Frame(root, bg="black")
suggestion_frame.grid(row=2, column=0, columnspan=15, padx=10, pady=10)
suggestion_frame.grid_rowconfigure(0, weight=1)  # Set the height of this row to create a gap

textarea = Text(root, font=('arial', 15, 'bold'), height=2, width=110, wrap='word', bd=8, relief=SUNKEN)
textarea.grid(row=1, columnspan=15, padx=10, pady=10)
textarea.focus_set()

buttons = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backs', 'Del',
           'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', '7', '8', '9',
           'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', 'Enter', '4', '5', '6',
           'Shift ↑', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '↑ Shift', '1', '2', '3',
           'Space']

leftShiftButtons = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', 'Backs', 'Del',
                    'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ']', '7', '8', '9',
                    'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', 'Enter', '4', '5', '6',
                    'Shift ↑', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '<', '>', '?', '↑ Shift', '1', '2', '3',
                    'Space']

capsButtons = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backs', 'Del',
               'Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', '7', '8', '9',
               'CAPS', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', 'Enter', '4', '5', '6',
               'Shift ↑', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', '↑ Shift', '1', '2', '3',
               'Space']

varRow = 3
varColumn = 0
for button in buttons:
    command = lambda x=button: select(x)
    if button != 'Space':
        btn = ttk.Button(root, text=button, command=command, width=10, padding=(10, 10), style='KeyboardButton.TButton')
        btn.grid(row=varRow, column=varColumn, padx=2, pady=2,sticky='nsew')
    if button == 'Space':
        btn = ttk.Button(root, text=button, command=command, width=30, padding=(10, 10), style='KeyboardButton.TButton')
        btn.grid(row=8, column=0, columnspan=14, padx=2, pady=2,)


    varColumn += 1
    if varColumn > 14:
        varColumn = 0
        varRow += 1
    btn.bind("<Button-1>", handle)
    btn.bind("<ButtonRelease-1>", on_enter)
    btn.bind("<Enter>", update_suggestions)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

suggestions_label = ttk.Label(root, font=('arial', 15, 'bold'), style='TLabel')

suggestions_label.grid(row=2, column=0, columnspan=15, padx=10, pady=10)
textarea.unbind("<Key>")

# Bind the update_suggestions function to the Key and KeyRelease events
textarea.bind("<Key>", update_suggestions)
textarea.bind("<KeyRelease>", update_suggestions)

# Call the initial_suggestions function
initial_suggestions()

root.protocol("WM_DELETE_WINDOW", close_window)
root.bind("<Escape>", close_window)
root.bind("<Control-KeyPress-m>", minimize_window)
custom_dictionary = load_custom_dictionary()
custom_dict_button = ttk.Button(root, text="Custom", command=on_custom_dict_button_hover, width=16, padding=(10, 10), style='CustomButton.TButton')
# Create a new button for custom dictionary entry
custom_dict_button = ttk.Button(root, text="Custom", command=on_custom_dict_button_hover, width=10, padding=(10, 10), style='CustomButton.TButton')
custom_dict_button.grid(row=8, column=13, padx=4, pady=4)
custom_dict_button.bind("<Button-1>", handle)
custom_dict_button.bind("<ButtonRelease-1>", on_enter)
custom_dict_button.bind("<Enter>", on_enter)
custom_dict_button.bind("<Leave>", on_leave)
custom_dict_button.bind("<Enter>", on_custom_dict_button_hover)

# Add the "Print Custom Dictionary" button to the main application


print_custom_dict_button = ttk.Button(root, text="Print Dict", command=print_custom_dictionary, width=12, padding=(10, 10), style='CustomButton.TButton')
print_custom_dict_button.grid(row=8, column=12, padx=4, pady=4)
print_custom_dict_button.bind("<Enter>",print_custom_dictionary_hover)  # Bind only on hovering

# Run the GUI main loop
root.mainloop()
# from tkinter import *