import time
import threading
import os
from tkinter import Tk, Frame, Text, Scrollbar, INSERT, FLAT, LEFT, RIGHT, Y, VERTICAL


SLEEP_TIME = 0.5


"""
Note-taking app that stays always on top. Auto-saves. 

Can only run one instance from one folder.
"""


class TextObserver(object):
    """
    Observes App.text every SLEEP_TIME seconds and updates 'topnote' file's contents.

    Runs on a separate thread.
    """
    def __init__(self, text):
        self.text = text
        self.on = True

    def run(self):

        old_content = ''
        while self.on:
            content = self.text.get('1.0', 'end-1c')

            if old_content != content:
                with open('topnote', 'w') as f:
                    f.write(content)

                old_content = content

            time.sleep(SLEEP_TIME)


class App(object):
    """
    """
    def __init__(self, master):
        self.master = master

        # Open contents of 'topnote' file
        try:
            with open('topnote', 'r') as f:
                contents = f.read()
        except FileNotFoundError:
            contents = ''

        # Create main Frame
        self.frame = Frame(self.master)
        self.frame.config(relief=FLAT)
        self.frame.pack(expand=True, fill='both')

        # Create Scroller
        self.scroller = Scrollbar(self.frame, orient=VERTICAL)
        self.scroller.pack(side=RIGHT, fill=Y)

        # Create Text container
        self.text = Text(self.frame, wrap=None, undo=True, yscrollcommand=self.scroller.set)
        self.text.config(height=20, width=40)
        self.text.insert(INSERT, contents)
        self.text.pack(side=LEFT, expand=1, fill='both')
        self.text.focus_set()
        self.text.config(bg='#4c4f54', bd=0, fg='#edeeef', insertbackground='#edeeef', padx=5, pady=5)

        # Attach Scroller to Text Y
        self.scroller.config(command=self.text.yview)

        # Start TextObserver thread
        self.to = TextObserver(self.text)
        self.observer_thread = threading.Thread(target=self.to.run)
        self.observer_thread.start()

        self.scroller.pack_forget()  # TODO: Remove

    def crash(self, e=None):
        """
        Test crashes
        """
        raise IndexError

    def quit(self):
        """
        Makes sure thread is stopped before quitting
        """
        self.to.on = False
        root.destroy()


# ASSURES ONLY ONE INSTANCE RUNS FROM FOLDER

try:
    open('open', 'r').read()  # We use a file to check if an instance is already running.


except FileNotFoundError:
    open('open', 'w').write('')

    try:
        # Create and config master Widget
        root = Tk()
        root.title("TopNote")
        root.config(relief=FLAT)
        root.attributes('-topmost', 'true')
        root.iconbitmap('icon.ico')

        a = App(root)
        root.protocol('WM_DELETE_WINDOW', a.quit)
        root.mainloop()

    finally:
        # In case of crashes, we make sure the 'open' file is removed before quitting.
        os.remove('open')
