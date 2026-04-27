import logging
import tkinter as tk

log = logging.getLogger(__name__)


def on_key_press(event):
    log.info("Key Pressed: keysym='%s', keycode='%s', char='%s'", event.keysym, event.keycode, event.char)

def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    root = tk.Tk()
    root.title("Key Listener for Slide Passer")
    root.geometry("400x200")

    label = tk.Label(root, text="Click here, then press buttons on your slide passer.\nCheck the terminal for output.", font=("Arial", 12))
    label.pack(expand=True)

    root.bind("<Key>", on_key_press)

    log.info("Listening for key presses... (Press Ctrl+C in terminal or close window to stop)")
    root.mainloop()

if __name__ == "__main__":
    main()
