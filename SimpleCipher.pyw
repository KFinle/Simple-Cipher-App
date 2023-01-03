# Name: Khris Finley
# Date: Dec 6, 2021
# App Name: Updated Cipher
# Description: Encodes or decodes a message based on a given shift factor. Sends encoded message to the clipboard for easy storage elsewhere.

import string
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

# Using full character set including empty space
CHARACTER_SET = string.ascii_lowercase + string.ascii_uppercase + string.digits + " "+ string.punctuation

# Copy output to clipboard
def clipboard_copy(message):
    window.clipboard_clear()
    window.clipboard_append(message)
    messagebox.showinfo("Hooray!", "Output message saved to clipboard!")

# Press enter to submit, esc to clear and reset focus 
def key_handler(event:Event):
    if event.keysym == "Return":
        cipher_click()
    elif event.keysym == "Escape":
        clear_click()
        
# Clear
def clear_click():
    shift_factor.set("")
    input_text.set("")
    output_text.set("")
    shift_factor_entry.focus()

# Entry Validation for Extended Caesar Mode
def entry_validation_mode_1():
    global keycheck
        # Entry check
    if shift_factor.get() == "":
        messagebox.showerror("ERROR", "Must enter a shift factor!")
        return
    elif input_text.get() == "":
        messagebox.showerror("ERROR", "Must enter a message!")
        return
    try:
        keycheck = int(shift_factor.get())
    except:
        messagebox.showerror("Error", "Shift factor must be a number!")
        return

# Used to convert password to numbers based on CHARACTER SET indices
def key_to_num(key):
    return ([CHARACTER_SET.find(i) for i in key])

# cycle through the list of characters
def cycle_inc(index,lst):
    if index == len(lst) - 1:
        index = 0
    else:
        index += 1
    return(index)

# Shifts the current letter 
def shift(letter, value):
    current_letter_value = CHARACTER_SET.find(letter)
    end_value = current_letter_value + value
    return(cycle_get(CHARACTER_SET, end_value))

# Gets the value to shift a character by 
def cycle_get(lst,index):
    new_index = index % len(lst)
    return(lst[new_index])


# Encode/Decode
def cipher_click():

    # Determine cipher type
    cipher_select = cipher_type.get()
    
    if cipher_select == "Extended Caesar":
        mode = 1

    elif cipher_select == "Polyalphabetic":
        mode = 2

    else:
        messagebox.showerror("ERROR", "Please select a cipher mode!")
        return

    if mode == 1:
        entry_validation_mode_1()
        mode_caesar()
    elif mode == 2:
        mode_poly()

def mode_poly():

    """
    Uses a password as a key rather than a numeric shift factor
    Uses index location of each character in shift password to determine the shift value for each input character
    Loops through the password if the input message is longer than the password

    Example:
    Input message = abcde
    Shift password = abcd (indecies 0,1,2,3 in CHARACTER_SET)
    Encoded text = acege (a+0=a, b+1=c, c+2=e, d+3=g, e+0=e)
    """

    result = ""
    input_message = input_text.get()
    password = shift_factor.get()
    key = key_to_num(password)
    index_of_key = 0
    if option_select.get() == 1:
        for char in input_message:
            result += shift(char, key[index_of_key])
            index_of_key = cycle_inc(index_of_key, key)
        input_text.set("")

    elif option_select.get() == 2:
        for char in input_message:
            result += shift(char,- key[index_of_key])
            index_of_key = cycle_inc(index_of_key, key)
        
    output_text.set(result)
    clipboard_copy(result)
    return

    
def mode_caesar():
    # Variable set
    #key = int(shift_factor.get())
    key = keycheck
    input_message = input_text.get()
    characters = CHARACTER_SET
    n = len(characters)
    shift = (n - key) % n
    if shift == 0:
        messagebox.showwarning("Not so secret", "This shift factor will result in the output message being the same as the input message!")

    # Encode message and erase input
    if option_select.get() == 1:
        message_convert = str.maketrans(characters, characters[shift:]+characters[:shift])
        translated_text = input_message.translate(message_convert)
        output_text.set(translated_text)
        input_text.set("")

    # Decode message, do not erase input
    elif option_select.get() == 2:
        
        shift = -shift
        message_convert = str.maketrans(characters, characters[shift:]+characters[:shift])
        translated_text = input_message.translate(message_convert)
        output_text.set(translated_text)


    # Copy output to clipboard
    clipboard_copy(translated_text)

# Build Window
window = Tk()
window.title('Message Encoder')
window.resizable(width=False, height=False)
window.bind("<Key>", key_handler)
frame = Frame()

# Labels
shift_factor_label = Label(frame, text="Enter your shift factor / password: ")
input_label = Label(frame, text="Enter your message: ")
output_label = Label(frame, text="Output message: ")

# Shift Factor section
shift_factor = Variable()
shift_factor_entry = Entry(frame, width=60, textvariable= shift_factor)
shift_factor_entry.focus()

# Input text section
input_text = Variable()
input_entry = Entry(frame, width=60, textvariable=input_text)

# Output text section
output_text = Variable()
output_entry = Entry(frame, width=60, textvariable=output_text ,state="readonly", cursor="no")

# Buttons
submit_button = Button(text="Submit", command=cipher_click)
clear_button = Button(text="Clear", command=clear_click)

# Cipher Options
cipher_list = ["Extended Caesar", "Polyalphabetic"]
cipher_type = Combobox(frame, values=cipher_list)
cipher_type.set(cipher_list[0])

# Initialize radio buttons, set default value to "Encode"
option_select = IntVar()
option_select.set(1)
encode_radiobutton = Radiobutton(text="Encode", variable= option_select, value= 1)
decode_radiobutton = Radiobutton(text="Decode", variable= option_select, value= 2)

# Pack elements 
frame.pack(padx=10, pady=10)
cipher_type.pack()
shift_factor_label.pack(anchor="w")
shift_factor_entry.pack(pady=(0,5))
input_label.pack(anchor="w")
input_entry.pack(pady=(0,5))
output_label.pack(anchor="w")
output_entry.pack(pady=(0, 10))
encode_radiobutton.pack()
decode_radiobutton.pack()
submit_button.pack(side = "left" ,pady=(0, 5), padx=20)
clear_button.pack(side= "right", pady=(0,5), padx=20)

# Window
window.mainloop()