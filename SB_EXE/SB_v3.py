#IMPORT RELEVANT MODULES:
import sqlite3 as sql
import pandas as pd
import tkinter as tk
import tabulate as tbl
import pandastable as pt

#CREATE CONNECTION TO DATABASE AND CURSOR FUNCTION:
DB = 'C:/Users/steph/Documents/Python/SB_EXE/SKYRIM_BOOKS.db'
con = sql.connect(DB)
cur = con.cursor()

#FETCH TABLES IN DATABASE:
cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")

#CREATE MAIN SCREEN:
main_screen = tk.Tk()
main_screen.title('Skyrim Books')
width = 845
height = 810
main_screen.geometry(f'{width}x{height}')
frame=tk.Frame(main_screen).pack(fill='both', expand=True, side=tk.TOP)

#CREATE LISTS OF HOUSES AND ROOMS:
houses = ('Tundra Homestead', 'Goldenhills Plantation', 'Breezehome', 'Lakeview Manor', 'Bloodchill Manor', 'Hendraheim')
Houses = tk.StringVar(main_screen, value=houses)
th_rooms = ('Bedroom', 'Basement')
TH_rooms = tk.StringVar(value=th_rooms)
gp_rooms = ('Bedroom', 'Shrine Room (Left)', 'Shrine Room (Right)')
GP_rooms = tk.StringVar(main_screen,  value=gp_rooms)
b_rooms = ('')
B_rooms = tk.StringVar(value=b_rooms)
lm_rooms = ('')
LM_rooms = tk.StringVar(value=lm_rooms)
bm_rooms = ('')
BM_rooms = tk.StringVar(value=bm_rooms)
h_rooms = ('')
H_rooms = tk.StringVar(value=h_rooms)
rooms = (TH_rooms, GP_rooms, B_rooms, LM_rooms, BM_rooms, H_rooms)

#CREATE FUNCTION TO FILL LISTBOX_ROOMS:
def fill_listbox_rooms(*args):
    listbox_rooms.delete(0, tk.END)
    txt.delete(1.0, tk.END)
    idxs=listbox_houses.curselection()
    if len(idxs)==1:
        idx=int(idxs[0])
        Rooms=rooms[idx]
        if idx==0:
            th=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Tundra Homestead'", con)
            tbl_th=tbl.tabulate(th,
                            headers='keys',
                            tablefmt='grid',
                            showindex=False)
            #listbox_rooms.insert(tk.END, th_rooms)
            txt.insert(tk.END, tbl_th)
#POPULATE HOUSES LISTBOX:
lbl_houses=tk.Label(frame, text='Select House:').pack(expand=True, side=tk.TOP)
listbox_houses=tk.Listbox(frame,
                          listvariable=Houses,
                          bg='white',
                          font='Ariel',
                          fg='black')
listbox_houses.pack(expand=True, side=tk.TOP)
listbox_houses.bind('<<ListboxSelect>>', fill_listbox_rooms)
lbl_rooms=tk.Label(frame, text='Select Room:').pack(side=tk.TOP)
listbox_rooms=tk.Listbox(frame,
                          bg='white',
                          font='Ariel',
                          fg='black')
listbox_rooms.pack(expand=True, side=tk.TOP)
txt=tk.Text(frame)
###CREATE & FORMAT TABLE FOR ALL HOUSES:
##all_houses=pd.read_sql_query("SELECT * FROM 'My Books'", con)

##txt_all_houses.insert(tk.END, tbl_all_houses)
txt.pack(fill='both', expand=True, side=tk.TOP)

#LAUNCH DATABASE:
main_screen.mainloop()

#CLOSE DATABASE CONNECTION:
con.close()
        
