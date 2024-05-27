import tkinter as tk 
from tkinter import filedialog as fd
from tkinter import colorchooser as cc
from xml.dom.minidom import parseString

class Menu():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x400")
        
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.view_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.view_menu)
        self.view_menu.add_command(label="New File", command=self.pick_file)
        self.view_menu.add_command(label="Parse File", command=self.parse)
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Theme_changer", command=self.change_theme)

        self.input_string_label = tk.Label(self.root, text="Enter a string: ")
        self.input_string = tk.Entry(self.root)
        self.input_submit = tk.Button(self.root, text="Check", command=self.input_check)
        self.input_string_label.pack()
        self.input_string.pack()
        self.input_submit.pack()

        self.root.mainloop()

    def change_theme(self):
        self.color = cc.askcolor()
        self.input_string_label.config(bg=self.color[1])
        self.instruct_label.config(bg=self.color[1])
        self.automata_label.config(bg=self.color[1])
        self.result_label.config(bg=self.color[1])
        self.root.configure(bg=self.color[1])

    def pick_file(self):
        file = fd.askopenfile(defaultextension='.xml' ,filetypes=[('XML files', '*.xml*')])
        if file:
           self.data = file.read()

    def parse(self):
        self.parse_xml(self.data)
        self.automata = self.parse_xml(self.data)
        self.instruct_label = tk.Label(self.root, text='automata instructions:')
        self.automata_label = tk.Label(self.root, text=f'{self.automata}')
        self.automata_label.config(anchor=tk.CENTER)
        self.instruct_label.pack()
        self.automata_label.pack()
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def parse_xml(self, xml_string):
        dom = parseString(xml_string)
        automata = {}
        automata['alphabet'] = [alphabet.getAttribute('letter') for alphabet in dom.getElementsByTagName('alphabet')]
        automata['states'] = [state.getAttribute('name') for state in dom.getElementsByTagName('state')]
        automata['initial'] = dom.getElementsByTagName('initialState')[0].getAttribute('name')
        automata['final'] = [state.getAttribute('name') for state in dom.getElementsByTagName('finalstate')]
        automata['transitions'] = {(trans.getAttribute('source'), trans.getAttribute('label')): trans.getAttribute('destination') for trans in dom.getElementsByTagName('transition')}
        return automata

    def is_valid_string(self, automata, string):
        current_state = automata['initial'] # Starting from our initial 
        for letter in string:
            if (current_state, letter) in automata['transitions']: # Checking if the transition is available
                current_state = automata['transitions'][(current_state, letter)]
            else: # If the transition was not available we return false
                return False
        return current_state in automata['final'] # Checking if we are in the final state
     
    def input_check(self):
        self.string = self.input_string.get()
        self.is_valid_string(self.automata, self.string) 
        if self.is_valid_string(self.automata, self.string):
            self.result_label.config(text="String is accepted.", fg="green")        
        else: 
            self.result_label.config(text="String is not accepted", fg="red")

if __name__ == "__main__":
    Menu()
