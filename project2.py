import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 1111

class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #find if there are two or one person in the chat
        try:
            self.sock.connect((host, port))
        except:
            print("You are the first person in the chat. Please wait for another person... ")
            self.sock.bind((HOST, PORT))
            self.sock.listen()
            client, address = self.sock.accept()
            self.sock = client

        messages = tkinter.Tk()
        messages.withdraw()

        #pop up to input your name
        self.name = simpledialog.askstring("Name", "Please choose a name", parent=messages)

        self.gui_done = False
        self.running = True

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        self.gui()

    #create front end
    def gui(self):
        self.win = tkinter.Tk()
        #give the background color
        self.win.configure(bg="#98FB98")

        self.label = tkinter.Label(self.win, text="Chat:", bg="#98FB98")
        self.label.config(font=("Times New Roman", 14, "bold"))
        self.label.pack(padx=20, pady=5)

        #text box with text history
        self.text_box = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_box.pack(padx=20, pady=5)

        #so that the user can not put text in the text history
        self.text_box.config(state='disabled')

        #message label
        self.message_label = tkinter.Label(self.win, text="Message:", bg="#98FB98")
        self.message_label.config(font=("Times New Roman", 14, "bold"))
        self.message_label.pack(padx=20, pady=5)

        #input area
        self.input = tkinter.Text(self.win, height=3)
        self.input.pack(padx=20, pady=5)

        #send button
        self.send_button = tkinter.Button(self.win, text="Send", bg="#D8BFD8", command=self.write)
        self.send_button.config(font=("Times New Roman", 14, "bold"))
        self.send_button.pack(padx=20, pady=5)

        #end gui
        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.name}: {self.input.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input.delete('1.0', 'end')
    
        #this is here so that both of the chat histories are updated
        self.text_box.config(state='normal')
        self.text_box.insert('end', message)
        self.text_box.yview('end')
        self.text_box.config(state='disabled')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NAMES':
                    self.sock.send(self.name.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_box.config(state='normal')
                        self.text_box.insert('end', message)
                        self.text_box.yview('end')
                        self.text_box.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("error")
                self.sock.close()
                break

client = Client(HOST, PORT)
	
