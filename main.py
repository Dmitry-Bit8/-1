import tkinter as tk

from app import PhoneBookApp # type: ignore


def main():
    root = tk.Tk()
    app = PhoneBookApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
