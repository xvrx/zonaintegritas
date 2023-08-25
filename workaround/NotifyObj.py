# set_icon_and_title.py
# https://www.devdungeon.com/content/gui-programming-python-tkinter
from tkinter import Tk, PhotoImage, Label ,X,Button, Entry, INSERT
import os


cwd = os.getcwd()
iconPath = fr'{cwd}\djponline\monke.png'
print(f'{cwd}\djponline\monke.png')

class DisplayCaptcha():
    def __init__(self, picName, stageLev):
        self.retainedValue = ''
        self.picName = picName
        self.stageLev = stageLev

    def runAttempt(self) :
        root = Tk()
        # get full desktop window size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Make window (w x h)300x150 and place at position (35% of screen width,35% of height)
        root.geometry(f"300x150+{int((35/100)*screen_width)}+{int((35/100)*screen_height)}")

        # set window icon - Image path provided as first command line arg. PNG format
        root.iconphoto(root, PhotoImage(file=iconPath)) 
        root.title("Bruh Moment!")


        #! displaying text => import Label from Tkinter first ================================================

        # Some of the packing options:
        # - fill: tells the widget to expand to take up any extra space (X, Y, or BOTH)
        # - padx/pady: outter padding
        # - ipadx/ipady: inner padding
        # - side: which side to stack from. Default is TOP (to bottom)

        my_text = Label(root, 
        text=f'captcha ({self.stageLev}) entry :', 
        bg="orange",
        fg="purple"
        )

        # display image

        img = PhotoImage(file=self.picName)

        my_image = Label(root, image=img)
        my_image.pack()


        my_text.pack(fill=X, padx=0, ipady=0)  # Pack from right to left
        # label2.pack(fill=Y, padx=25, ipady=15, side=RIGHT)

        #! Input Catpcha ================================================
        entry = Entry(root, justify='center',fg='black')
        entry.pack(fill=X)

        # Specifying character position in entry
        # - END: After last character of entry widget
        # - ANCHOR: The beginning of the current selection
        # - INSERT: Current text cursor position
        # - "@x": Mouse coordinates

        # Insert some default text
        def focusIn () :
            entry.delete('0', 'end')

        entry.insert(INSERT, 'type here...')
        entry.bind("<FocusIn>", lambda args: focusIn()  )
        entry.bind("<FocusOut>", lambda args: entry.insert(INSERT, 'type here...'))


        #! Submit  ================================================
        # Print the contents of entry widget to console
        def submitCaptcha(event):
            self.retainedValue = entry.get()
            root.destroy()

        def clickSubmit():
            # print(entry.get())
            self.retainedValue = entry.get()
            root.destroy()

        root.bind("<Return>", submitCaptcha)

        # Create a button that will print the contents of the entry
        button = Button(root, text='Submit', command=clickSubmit)
        button.pack()
        # focus entry / textbox on launch
        entry.focus_set()

        def onClose():
            print('window closed!')
            root.destroy()
            
        root.protocol("WM_DELETE_WINDOW", onClose)

        root.resizable(False, False)

        root.mainloop()
        print(self.retainedValue)
        return self.retainedValue
