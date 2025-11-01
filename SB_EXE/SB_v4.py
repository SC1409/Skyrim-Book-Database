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
width = 1000
height = 810
main_screen.geometry(f'{width}x{height}')
frame=tk.Frame(main_screen).pack(fill='both', expand=True, side=tk.TOP)

#CREATE LISTS OF HOUSES AND ROOMS:
houses = ('All Houses', 'Tundra Homestead', 'Goldenhills Plantation', 'Breezehome', 'Lakeview Manor', 'Bloodchill Manor', 'Hendraheim', 'Honeyside')
Houses = tk.StringVar(main_screen, value=houses)
th_rooms = ('All Rooms', 'Bedroom', 'Basement')
gp_rooms = ('All Rooms', 'Bedroom', 'Shrine Room (Left)', 'Shrine Room (Right)')
b_rooms = ('All Rooms', 'Living Room', 'Alchemy Laboratory')
lm_rooms = ('Master Bedroom')
bm_rooms = ('All Rooms', 'Master Bedroom (Floor 1)', 'Master Bedroom (Floor 2)', "Children's Room")
h_rooms = ('All Rooms', 'Bedroom (Left)', 'Bedroom (Right)', 'Dining Area')
hs_rooms = ('All Rooms', 'Bedroom', 'Basement')

#CREATE FUNCTION TO FILL LISTBOX_ROOMS:
def fill_listbox_rooms(*args):
    listbox_rooms.delete(0, tk.END)
    txt.delete(1.0, tk.END)
    idxs=listbox_houses.curselection()
    if len(idxs)==1:
        idx=int(idxs[0])
        if idx==0:
            all_h=pd.read_sql_query("SELECT * FROM 'My Books'", con)
            tbl_all_h=tbl.tabulate(all_h,
                                   headers='keys',
                                   tablefmt='grid',
                                   showindex=False)
            txt.insert(tk.END, tbl_all_h)
        if idx==1:
            th=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Tundra Homestead'", con)
            tbl_th=tbl.tabulate(th,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            for room in th_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.insert(tk.END, tbl_th)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_th_rooms)
        if idx==2:
            gp=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Goldenhills Plantation'", con)
            tbl_gp=tbl.tabulate(gp,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            for room in gp_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.insert(tk.END, tbl_gp)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_gp_rooms)
        if idx==3:
            b=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Breezehome'", con)
            tbl_b=tbl.tabulate(b,
                               headers='keys',
                               tablefmt='grid',
                               showindex=False)
            for room in b_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.insert(tk.END, tbl_b)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_b_rooms)
        if idx==4:
            lm=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Lakeview Manor'", con)
            tbl_lm=tbl.tabulate(lm,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            for room in lm_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.insert(tk.END, tbl_lm)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_lm_rooms)

#CREATE FUNCTION TO FILL TABLE FOR TUNDRA HOMESTEAD:
def fill_table_th_rooms(*args):           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            listbox_rooms.delete(0, tk.END)
            for room in th_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.delete(1.0, tk.END)
            th=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Tundra Homestead'", con)
            tbl_th=tbl.tabulate(th,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            txt.insert(tk.END, tbl_th)
        if idx_room==1:
            txt.delete(1.0, tk.END)
            th_bedroom=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Tundra Homestead' AND Room = 'Bedroom'", con)
            tbl_th_bedroom=tbl.tabulate(th_bedroom,
                                        headers='keys',
                                        tablefmt='grid',
                                        showindex=False)
            txt.insert(tk.END, tbl_th_bedroom)
        if idx_room==2:
            txt.delete(1.0, tk.END)
            th_basement=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Tundra Homestead' AND Room = 'Basement'", con)
            tbl_th_basement=tbl.tabulate(th_basement,
                                        headers='keys',
                                        tablefmt='grid',
                                        showindex=False)
            txt.insert(tk.END, tbl_th_basement)

#CREATE FUNCTION TO FILL TABLE FOR GOLDENHILLS PLANTATION:
def fill_table_gp_rooms(*args):           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            listbox_rooms.delete(0, tk.END)
            for room in gp_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.delete(1.0, tk.END)
            gp=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Goldenhills Plantation'", con)
            tbl_gp=tbl.tabulate(gp,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            txt.insert(tk.END, tbl_gp)
        if idx_room==1:
            txt.delete(1.0, tk.END)
            gp_bedroom=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Goldenhills Plantation' AND Room = 'Bedroom'", con)
            tbl_gp_bedroom=tbl.tabulate(gp_bedroom,
                                        headers='keys',
                                        tablefmt='grid',
                                        showindex=False)
            txt.insert(tk.END, tbl_gp_bedroom)
        if idx_room==2:
            txt.delete(1.0, tk.END)
            gp_srl=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Goldenhills Plantation' AND Room = 'Shrine Room (Left)'", con)
            tbl_gp_srl=tbl.tabulate(gp_srl,
                                    headers='keys',
                                    tablefmt='grid',
                                    showindex=False)
            txt.insert(tk.END, tbl_gp_srl)
        if idx_room==3:
            txt.delete(1.0, tk.END)
            gp_srr=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Goldenhills Plantation' AND Room = 'Shrine Room (Right)'", con)
            tbl_gp_srr=tbl.tabulate(gp_srr,
                                    headers='keys',
                                    tablefmt='grid',
                                    showindex=False)
            txt.insert(tk.END, tbl_gp_srr)
            
#CREATE FUNCTION TO FILL TABLE FOR BREEZEHOME:
def fill_table_b_rooms(*args):           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            listbox_rooms.delete(0, tk.END)
            for room in b_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.delete(1.0, tk.END)
            b=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Breezehome'", con)
            tbl_b=tbl.tabulate(b,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            txt.insert(tk.END, tbl_b)
        if idx_room==1:
            txt.delete(1.0, tk.END)
            b_living=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Breezehome' AND Room = 'Living Room'", con)
            tbl_b_living=tbl.tabulate(b_living,
                                      headers='keys',
                                      tablefmt='grid',
                                      showindex=False)
            txt.insert(tk.END, tbl_b_living)
        if idx_room==2:
            txt.delete(1.0, tk.END)
            b_lab=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Breezehome' AND Room = 'Alchemy Laboratory'", con)
            tbl_b_lab=tbl.tabulate(b_lab,
                                   headers='keys',
                                   tablefmt='grid',
                                   showindex=False)
            txt.insert(tk.END, tbl_b_lab)

#CREATE FUNCTION TO FILL TABLE FOR LAKEVIEW MANOR:
def fill_table_lm_rooms(*args):           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            listbox_rooms.delete(0, tk.END)
            for room in lm_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.delete(1.0, tk.END)
            lm=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Lakeview Manor'", con)
            tbl_lm=tbl.tabulate(lm,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            txt.insert(tk.END, tbl_lm)
        
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
                         fg='black',
                         exportselection=False)
listbox_rooms.pack(expand=True, side=tk.TOP)
txt=tk.Text(frame)
###CREATE & FORMAT TABLE FOR ALL HOUSES:
##

##txt_all_houses.insert(tk.END, tbl_all_houses)
txt.pack(fill='both', expand=True, side=tk.TOP)

#LAUNCH DATABASE:
main_screen.mainloop()

#CLOSE DATABASE CONNECTION:
con.close()
        
