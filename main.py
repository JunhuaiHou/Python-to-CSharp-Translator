import tkinter as tk
from tkinter import filedialog, messagebox, Text
from tkinter import font
from api.gpt_client import query_chatgpt, load_api_key
from openai import OpenAI


def insert_code(text):
    code.config(state='normal')
    code.delete('1.0', tk.END)
    code.insert(tk.END, text)
    code.config(state='disabled')
    root.update()


def load_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            with open(file_path, 'r') as file:
                insert_code(file.read())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")


def translate_and_save(client):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    code_to_translate = code.get('1.0', tk.END)
    insert_code('Translating....')
    response = query_chatgpt(client, code_to_translate)
    translated_code = response.choices[0].message.content

    if file_path:
        if translated_code == 'Please load valid Python code.':
            insert_code(translated_code)
        else:
            try:
                with open(file_path, 'w') as file:
                    file.write(translated_code)
                    insert_code(f'Translation complete. Saved at {file.name}.')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Python C# Translator")
    x = int((root.winfo_screenwidth() / 2) - (750 / 2))
    y = int((root.winfo_screenheight() / 2) - (600 / 2))
    root.geometry(f'+{x}+{y}')

    api_key = load_api_key()
    client = OpenAI(api_key=api_key)

    title = tk.Label(root, text="Python C# Translator", font=font.Font(family='Helvetica', size=16, weight='bold'))
    title.pack(pady=(10, 0), anchor='center')

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    code = Text(frame, height=30, width=75)
    code.config(state='disabled')
    code.pack()

    load = tk.Button(frame, text="Load Code", command=load_file, font=font.Font(family='Helvetica', size=16, weight='bold'))
    load.pack(side=tk.LEFT)

    save = tk.Button(frame, text="Translate and Export", command=lambda: translate_and_save(client), font=font.Font(family='Helvetica', size=16, weight='bold'))
    save.pack(side=tk.RIGHT)

    root.mainloop()
