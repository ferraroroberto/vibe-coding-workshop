import tkinter as tk

def on_key_press(event):
    print(f"Key Pressed: keysym='{event.keysym}', keycode='{event.keycode}', char='{event.char}'")

def main():
    root = tk.Tk()
    root.title("Key Listener for Slide Passer")
    root.geometry("400x200")
    
    label = tk.Label(root, text="Click here, then press buttons on your slide passer.\nCheck the terminal for output.", font=("Arial", 12))
    label.pack(expand=True)
    
    # Bind all key presses
    root.bind("<Key>", on_key_press)
    
    print("Listening for key presses... (Press Ctrl+C in terminal or close window to stop)")
    root.mainloop()

if __name__ == "__main__":
    main()
