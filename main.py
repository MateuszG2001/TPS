import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog

from codec import Codec


def str_to_bitlist(s):
    ords = (ord(c) for c in s)
    shifts = (7, 6, 5, 4, 3, 2, 1, 0)
    return [(o >> shift) & 1 for o in ords for shift in shifts]


def bitlist_to_chars(bl):
    bi = iter(bl)
    bytez = zip(*(bi,) * 8)
    shifts = (7, 6, 5, 4, 3, 2, 1, 0)
    for byte in bytez:
        yield chr(sum(bit << s for bit, s in zip(byte, shifts)))


def bitlist_to_str(bl):
    return ''.join(bitlist_to_chars(bl))


def str_to_binary(s):
    return ' '.join('{0:08b}'.format(ord(x), 'b') for x in s)


def binary_to_str(b):
    string = ''
    for i in range(0, len(b), 9):
        string += chr(int(b[i:i + 9], 2))
    return string


def handle_decoded_to_encoded_button_click(event):
    message = decoded_text.get("1.0", tk.END)
    message = message.replace('\n', '')
    message_bits = str_to_bitlist(message)
    encoded_bits = Codec.encode(message_bits)
    encoded_text.delete("1.0", tk.END)
    encoded_text.insert("1.0", bitlist_to_str(encoded_bits))


def handle_encoded_to_decoded_button_click(event):
    encoded = encoded_text.get("1.0", tk.END)
    encoded = encoded.replace('\n', '')
    encoded_bits = str_to_bitlist(encoded)
    try:
        decoded_bits = Codec.decode(encoded_bits)
    except Exception as e:
        tk.messagebox.showerror("Error", str(e))
    else:
        decoded = bitlist_to_str(decoded_bits)
        decoded_text.delete("1.0", tk.END)
        decoded_text.insert("1.0", decoded)


def handle_decoded_to_binary_button_click(event):
    decoded = decoded_text.get("1.0", tk.END)
    decoded = decoded.replace('\n', '')
    binary = str_to_binary(decoded)
    decoded_binary_text.delete("1.0", tk.END)
    decoded_binary_text.insert("1.0", binary)


def handle_encoded_to_binary_button_click(event):
    encoded = encoded_text.get("1.0", tk.END)
    encoded = encoded.replace('\n', '')
    encoded_binary_text.delete("1.0", tk.END)
    encoded_binary_text.insert("1.0", str_to_binary(encoded))


def handle_binary_to_decoded_button_click(event):
    decoded_binary = decoded_binary_text.get("1.0", tk.END)
    try:
        decoded = binary_to_str(decoded_binary)
    except Exception as e:
        tk.messagebox.showerror("Error", str(e))
    else:
        decoded_text.delete("1.0", tk.END)
        decoded_text.insert("1.0", decoded)


def handle_binary_to_encoded_button_click(event):
    encoded_binary = encoded_binary_text.get("1.0", tk.END)
    try:
        encoded = binary_to_str(encoded_binary)
    except Exception as e:
        tk.messagebox.showerror("Error", str(e))
    else:
        encoded_text.delete("1.0", tk.END)
        encoded_text.insert("1.0", encoded)


def handle_decoded_save_button_click(event):
    filename = tk.filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text documents", "*.txt"), ("All files", "*.*")])
    with open(filename, "w", encoding="utf-16le") as f:
        f.write(decoded_text.get("1.0", tk.END).replace('\n', ''))


def handle_decoded_load_button_click(event):
    filename = tk.filedialog.askopenfilename(defaultextension=".txt",
                                             filetypes=[("Text documents", "*.txt"), ("All files", "*.*")])
    with open(filename, "r", encoding="utf-16le") as f:
        decoded_text.delete("1.0", tk.END)
        decoded_text.insert("1.0", f.read())


def handle_encoded_save_button_click(event):
    filename = tk.filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text documents", "*.txt"), ("All files", "*.*")], )
    with open(filename, "w", encoding="utf-16le") as f:
        f.write(encoded_text.get("1.0", tk.END).replace('\n', ''))


def handle_encoded_load_button_click(event):
    filename = tk.filedialog.askopenfilename(defaultextension=".txt",
                                             filetypes=[("Text documents", "*.txt"), ("All files", "*.*")])
    with open(filename, "r", encoding="utf-16le") as f:
        encoded_text.delete("1.0", tk.END)
        encoded_text.insert("1.0", f.read())


if __name__ == '__main__':
    window = tk.Tk()
    window.title("TPS")

    window.columnconfigure([0, 2], weight=1, minsize=100)
    window.rowconfigure([0, 2], weight=1, minsize=200)

    decoded_frame = tk.Frame(master=window)
    decoded_label = tk.Label(master=decoded_frame, text="Decoded")
    decoded_label.pack(padx=5, pady=5)
    decoded_buttons_frame = tk.Frame(master=decoded_frame)
    decoded_save_button = tk.Button(master=decoded_buttons_frame, text="Save")
    decoded_save_button.bind("<Button-1>", handle_decoded_save_button_click)
    decoded_save_button.pack(padx=5, pady=5, side=tk.LEFT)
    decoded_load_button = tk.Button(master=decoded_buttons_frame, text="Load")
    decoded_load_button.bind("<Button-1>", handle_decoded_load_button_click)
    decoded_load_button.pack(padx=5, pady=5, side=tk.RIGHT)
    decoded_buttons_frame.pack()
    decoded_text = tk.Text(master=decoded_frame, height=16, width=32)
    decoded_text.pack(padx=5, pady=5, fill=tk.BOTH)
    decoded_frame.grid(row=0, column=0, sticky=tk.NSEW)

    decoded_binary_buttons_frame = tk.Frame(master=window)
    binary_to_decoded_button = tk.Button(master=decoded_binary_buttons_frame, text="↑", width=2, height=1)
    binary_to_decoded_button.bind("<Button-1>", handle_binary_to_decoded_button_click)
    decoded_to_binary_button = tk.Button(master=decoded_binary_buttons_frame, text="↓", width=2, height=1)
    decoded_to_binary_button.bind("<Button-1>", handle_decoded_to_binary_button_click)
    binary_to_decoded_button.pack(side=tk.LEFT, padx=5, pady=5)
    decoded_to_binary_button.pack(side=tk.RIGHT, padx=5, pady=5)
    decoded_binary_buttons_frame.grid(row=1, column=0)

    decoded_binary_frame = tk.Frame(master=window)
    decoded_binary_text = tk.Text(master=decoded_binary_frame, height=16, width=32)
    decoded_binary_text.pack(padx=5, pady=5, fill=tk.BOTH)
    decoded_binary_label = tk.Label(master=decoded_binary_frame, text="Binary")
    decoded_binary_label.pack(padx=5, pady=5)
    decoded_binary_frame.grid(row=2, column=0, sticky=tk.NSEW)

    decoded_encoded_buttons_frame = tk.Frame(master=window)
    decoded_to_encoded_button = tk.Button(master=decoded_encoded_buttons_frame, text="→", width=2, height=1)
    decoded_to_encoded_button.bind("<Button-1>", handle_decoded_to_encoded_button_click)
    encoded_to_decoded_button = tk.Button(master=decoded_encoded_buttons_frame, text="←", width=2, height=1)
    encoded_to_decoded_button.bind("<Button-1>", handle_encoded_to_decoded_button_click)
    decoded_to_encoded_button.pack(padx=5, pady=5)
    encoded_to_decoded_button.pack(padx=5, pady=5)
    decoded_encoded_buttons_frame.grid(row=0, column=1)

    encoded_frame = tk.Frame(master=window)
    encoded_label = tk.Label(master=encoded_frame, text="Encoded")
    encoded_label.pack(padx=5, pady=5)
    encoded_buttons_frame = tk.Frame(master=encoded_frame)
    encoded_save_button = tk.Button(master=encoded_buttons_frame, text="Save")
    encoded_save_button.bind("<Button-1>", handle_encoded_save_button_click)
    encoded_save_button.pack(padx=5, pady=5, side=tk.LEFT)
    encoded_load_button = tk.Button(master=encoded_buttons_frame, text="Load")
    encoded_load_button.bind("<Button-1>", handle_encoded_load_button_click)
    encoded_load_button.pack(padx=5, pady=5, side=tk.RIGHT)
    encoded_buttons_frame.pack()
    encoded_text = tk.Text(master=encoded_frame, height=16, width=32)
    encoded_text.pack(padx=5, pady=5, fill=tk.BOTH)
    encoded_frame.grid(row=0, column=2, sticky=tk.NSEW)

    encoded_binary_buttons_frame = tk.Frame(master=window)
    binary_to_encoded_button = tk.Button(master=encoded_binary_buttons_frame, text="↑", width=2, height=1)
    binary_to_encoded_button.bind("<Button-1>", handle_binary_to_encoded_button_click)
    encoded_to_binary_button = tk.Button(master=encoded_binary_buttons_frame, text="↓", width=2, height=1)
    encoded_to_binary_button.bind("<Button-1>", handle_encoded_to_binary_button_click)
    binary_to_encoded_button.pack(side=tk.LEFT, padx=5, pady=5)
    encoded_to_binary_button.pack(side=tk.RIGHT, padx=5, pady=5)
    encoded_binary_buttons_frame.grid(row=1, column=2)

    encoded_binary_frame = tk.Frame(master=window)
    encoded_binary_text = tk.Text(master=encoded_binary_frame, height=16, width=32)
    encoded_binary_text.pack(padx=5, pady=5, fill=tk.BOTH)
    encoded_binary_label = tk.Label(master=encoded_binary_frame, text="Binary")
    encoded_binary_label.pack(padx=5, pady=5)
    encoded_binary_frame.grid(row=2, column=2, sticky=tk.NSEW)

    window.mainloop()
