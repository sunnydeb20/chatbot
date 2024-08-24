from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

def signin():
    username = user.get()
    password = code.get()

    if username == 'admin' and password == '12341234':
       Screen=Toplevel(root)
       Screen.title('App')
       Screen.geometry('925x500+300+200')
       Screen.config(bg="white")

       Label(Screen, text='Hello Everyone!', bg='#fff',font=('calibri(Body)',50,'bold')).pack(expand=True)

    elif username!='admin' and password!='12341234':
        messagebox.showerror("Invalid","Invalid username and password") 

    elif password!="12341234":
        messagebox.showerror("Invalid","Invalid password") 

    elif username!= 'admin':
        messagebox.showerror("Invalid","Invalid username" )

def signup():
    messagebox.showinfo("Sign Up", "Sign up functionality not implemented yet!")

img = PhotoImage(file='robot.jpg')
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='sign in', fg='#57a1f7', bg='white', font=('microsoft yahei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')

user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('microsoft yahei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_enter_code(e):
    code.delete(0, 'end')

def on_leave_code(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('microsoft yahei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'password')
code.bind('<FocusIn>', on_enter_code)
code.bind('<FocusOut>', on_leave_code)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

Button(frame, width=39, pady=7, text='sign in', bg='#57a1f8', fg='white', border=0 , command=signin).place(x=35, y=204)

Label(frame, text='Dont have an account?', fg='black', bg='white', font=('microsoft yahei UI Light', 9)).place(x=75, y=270)

sign_up = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=signup)
sign_up.place(x=215, y=270)

root.mainloop()
