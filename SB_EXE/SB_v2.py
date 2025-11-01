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
main_screen=tk.Tk()
main_screen.title('Skyrim Books')
width=845
height=main_screen.winfo_screenheight()
main_screen.geometry(f'{width}x{height}')
frame=tk.Frame(main_screen).pack(fill='both', expand=True, side=tk.TOP)
#frame_bot=tk.Frame(main_screen).pack(fill='both', expand=True, side=tk.BOTTOM)
lbl_houses=tk.Label(frame, text='Select House:').pack(side=tk.TOP)
listbox_houses=tk.Listbox(frame,
                          bg='white',
                          font='Ariel',
                          fg='black')
listbox_houses.insert(1, 'All Houses')
listbox_houses.insert(2, 'Tundra Homestead')
listbox_houses.insert(3, 'Breezehome')
listbox_houses.insert(4, 'Goldenhills Plantation')
listbox_houses.insert(5, 'Lakeview Manor')
listbox_houses.insert(6, 'Bloodchill Manor')
listbox_houses.insert(7, 'Hendraheim')
listbox_houses.pack(side=tk.TOP)
listbox_houses=tk.Listbox(frame,
                          bg='white',
                          font='Ariel',
                          fg='black')
lbl_rooms=tk.Label(frame, text='Select Room:').pack(side=tk.TOP)
listbox_rooms=tk.Listbox(frame,
                         bg='white',
                         font='Ariel',
                         fg='black')
listbox_rooms.pack(side=tk.TOP)
#CREATE & FORMAT TABLE FOR ALL HOUSES:
all_houses=pd.read_sql_query("SELECT * FROM 'My Books'", con)
tbl_all_houses=tbl.tabulate(all_houses,
                            headers='keys',
                            tablefmt='grid',
                            showindex=False)
txt_all_houses=tk.Text(frame)
txt_all_houses.insert(tk.END, tbl_all_houses)
txt_all_houses.pack(fill='both', expand=True, side=tk.TOP)

#LAUNCH DATABASE:
main_screen.mainloop()

#CLOSE DATABASE CONNECTION:
con.close()
        
