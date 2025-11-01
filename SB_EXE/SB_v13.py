#IMPORT RELEVANT MODULES:
import sqlite3 as sql
import pandas as pd
import tkinter as tk
import tabulate as tbl
import sys

#CREATE CONNECTION TO DATABASE AND CURSOR FUNCTION:
DB = 'C:/Users/steph/Documents/Python/SB_EXE/SKYRIM_BOOKS.db'
con = sql.connect(DB)
cur = con.cursor()

#FETCH TABLES IN DATABASE:
cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")

#CREATE LISTS OF HOUSES AND ROOMS:
houses = ('All Houses', 'Tundra Homestead', 'Goldenhills Plantation', 'Breezehome', 'Lakeview Manor', 'Bloodchill Manor', 'Hendraheim', 'Honeyside')
all_rooms = ('All Rooms')
th_rooms = ('All Rooms', 'Bedroom', 'Basement')
gp_rooms = ('All Rooms', 'Bedroom', 'Shrine Room (Left)', 'Shrine Room (Right)')
b_rooms = ('All Rooms', 'Living Room', 'Alchemy Laboratory')
lm_rooms = ('Master Bedroom')
bm_rooms = ('All Rooms', 'Master Bedroom (Floor 1)', 'Master Bedroom (Floor 2)', 'Child Room')
h_rooms = ('All Rooms', 'Bedroom (Left)', 'Bedroom (Right)', 'Dining Area')
hs_rooms = ('All Rooms', 'Bedroom', 'Basement')

#CREATE LAUNCH FUNCTION:
def mm():
    root=tk.Tk()
    root.title('Skyrim Books')
    screen_width=int(root.winfo_screenwidth())
    screen_height=int(root.winfo_screenheight())
    width = screen_width * 0.56
    height = root.winfo_screenheight()* 0.4
    root.geometry("%dx%d" % (width, height))
    root.columnconfigure(2, weight=2)
    app=main_win(root)
    root.mainloop()

#CREATE MAIN WINDOW:
class main_win:
    def __init__(self, master):
        self.master=master
        self.frame=tk.Frame(self.master)
        self.frame.grid(row=0, column=0, sticky='news')
        Houses = tk.StringVar(self.frame, value=houses)
        #sys.stdout=clear_win()
        #CREATE HOUSE'S LISTBOX AND LABEL:
        self.lbl_houses=tk.Label(self.frame, text='Select House:')
        self.lbl_houses.grid(row=0, column=0, sticky='ew')
        self.listbox_houses=tk.Listbox(self.frame, listvariable=Houses, bg='white', font='Ariel', fg='black')
        self.listbox_houses.grid(row=1, column=0, sticky='ew')
        self.listbox_houses.bind('<<ListboxSelect>>', self.fill_listbox_rooms)
        #CREATE ROOM'S LISTBOX AND LABEL:
        self.lbl_rooms=tk.Label(self.frame, text='Select Room:')
        self.lbl_rooms.grid(row=0, column=1, sticky='ew')
        self.listbox_rooms=tk.Listbox(self.frame, bg='white', font='Ariel', fg='black', exportselection=False)
        self.listbox_rooms.grid(row=1, column=1, sticky='ew')
        #CREATE TEXTBOX FOR TABLES:
        self.txt=tk.Text(self.frame)
        self.txt.grid(row=0, column=2, rowspan=5, columnspan=2, sticky='news')
        #CREATE SEARCH BAR AND BUTTON WIDGET:
        self.searchstring = tk.StringVar()
        self.searchbar=tk.Entry(self.frame, textvariable=self.searchstring)
        self.searchbar.grid(row=5, column=2, sticky='news')
        self.searchbar.bind('<Return>', self.search)
        self.btn_search=tk.Button(self.frame, text='Search', command=self.search)
        self.btn_search.grid(row=5, column=3, sticky='news')
        #CREATE BUTTONS FOR ALL HOUSES SCREEN:
        self.btn_clr_ah=tk.Button(self.frame, text="Clear", command=lambda:[self.clear_ah(), self.btn_clr_ah.grid_forget()])
        self.btn_ahas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.all_house_skill(), self.btn_ahas.grid_forget()])
        self.btn_ahasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.all_house_spell(), self.btn_ahasp.grid_forget()])
        self.btn_ahareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.all_house_reg(), self.btn_ahareg.grid_forget()])
    
    def search(self, *event):
        self.txt.delete(1.0, tk.END)
        all_books=pd.read_sql_query('SELECT * FROM "My Books"', con)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        result=all_books.loc[all_books['Title'].str.contains(self.searchstring.get(), na=False, case=False)]
        result_dis=result[['Title', 'House', 'Room', 'Skill Book', 'Spell Tome']]
        #self.txt.insert(tk.END, result_dis)
        #sys.stdout=write()
        self.txt.insert(tk.END, result_dis.to_markdown(index=False))
        #print(result_dis.to_markdown(index=False))

    def fill_listbox_rooms(self, *args):
        sys.stdout=self.forget_btns()
        self.listbox_rooms.delete(0, tk.END)
        self.txt.delete(1.0, tk.END)
        idxs=self.listbox_houses.curselection()
        if len(idxs)==1:
            idx=int(idxs[0])
            if idx==0:
                sys.stdout=self.forget_btns()
                self.txt.delete(1.0, tk.END)
                self.listbox_rooms.delete(0, tk.END)
                self.listbox_rooms.insert(tk.END, 'All Rooms')
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_all_rooms)

    def fill_table_all_rooms(self, *args):         
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                sys.stdout=self.forget_btns()
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=5, column=3, sticky='news')
                self.btn_ahas.grid(row=2, column=0, columnspan=2, sticky='ew')
                self.btn_ahasp.grid(row=3, column=0, columnspan=2, sticky='ew')
                self.btn_ahareg.grid(row=4, column=0, columnspan=2, sticky='ew')
                all_h=pd.read_sql_query('SELECT * FROM "My Books"', con)
                pd.set_option('display.max_columns', None)
                pd.set_option('display.max_rows', None)
                all_h_dis=all_h[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, all_h_dis)

    def forget_btns(self):
        lst=self.frame.winfo_children()
        for item in lst:
            if isinstance(item, tk.Button):
                item.grid_forget()

    def write(self, s):
        self.txt.insert(tk.END, s)

#THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM:
    def clear_ah(*args):
        sys.stdout=fill_table_all_rooms()

#LAUNCH DATABASE:
if __name__ == '__main__':
    mm()

#CLOSE DATABASE CONNECTION:
con.close()
