#0IMPORT RELEVANT MODULES:
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

#CREATE MAIN SCREEN:
main_screen = tk.Tk()
main_screen.title('Skyrim Books')
width = 700
height = 950
main_screen.geometry(f'{width}x{height}')
#frame=tk.Frame(main_screen).pack(fill='both', expand=True, side=tk.TOP)

#CREATE LISTS OF HOUSES AND ROOMS:
houses = ('All Houses', 'Tundra Homestead', 'Goldenhills Plantation', 'Breezehome', 'Lakeview Manor', 'Bloodchill Manor', 'Hendraheim', 'Honeyside')
Houses = tk.StringVar(main_screen, value=houses)
th_rooms = ('All Rooms', 'Bedroom', 'Basement')
gp_rooms = ('All Rooms', 'Bedroom', 'Shrine Room (Left)', 'Shrine Room (Right)')
b_rooms = ('All Rooms', 'Living Room', 'Alchemy Laboratory')
lm_rooms = ('Master Bedroom')
bm_rooms = ('All Rooms', 'Master Bedroom (Floor 1)', 'Master Bedroom (Floor 2)', 'Child Room')
h_rooms = ('All Rooms', 'Bedroom (Left)', 'Bedroom (Right)', 'Dining Area')
hs_rooms = ('All Rooms', 'Bedroom', 'Basement')

###############################################FILL LISTBOX_ROOMS###################################################
#CREATE FUNCTION TO FILL LISTBOX_ROOMS:
class printtotxt(object):
    def write(self, s):
        txt.insert(tk.END, s)
        
#CREATE FUNCTIONS FOR ALL HOUSE FILTERS:
def all_house_skill(*args):
    txt.delete(1.0, tk.END)
    all_h_skill=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Skill Book" = "Yes"', con)
    btn_clr_ah.pack(fill='both', expand=True, side=tk.TOP)
    btn_ahasp.pack(fill='both', expand=True)
    btn_ahareg.pack(fill='both', expand=True)
    all_h_skill_dis=all_h_skill[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(all_h_skill_dis.to_markdown(index=False))

def all_house_spell(*args):
    txt.delete(1.0, tk.END)
    all_h_spell=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Spell Tome" = "Yes"', con)
    btn_clr_ah.pack(fill='both', expand=True, side=tk.TOP)
    btn_ahas.pack(fill='both', expand=True)
    btn_ahareg.pack(fill='both', expand=True)
    all_h_spell_dis=all_h_spell[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(all_h_spell_dis.to_markdown(index=False))

def all_house_reg(*args):
    txt.delete(1.0, tk.END)
    all_h_reg=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Spell Tome" = "No" AND "Skill Book" = "No"', con)
    btn_clr_ah.pack(fill='both', expand=True, side=tk.TOP)
    btn_ahas.pack(fill='both', expand=True)
    btn_ahasp.pack(fill='both', expand=True)
    all_h_reg_dis=all_h_reg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(all_h_reg_dis.to_markdown(index=False))

def clear_ah(*args):
    sys.stdout=fill_listbox_rooms()

#CREATE FUNCTION TO DESTROY BUTTONS:
def destroy_btns(main_screen):
    lst=main_screen.winfo_children()
    for item in lst:
        if isinstance(item, tk.Button):
            item.destroy()
            
#CREATE FUNCTIONS FOR ALL HOUSE FILTERS:
def th_skill(*args):
    txt.delete(1.0, tk.END)
    th_skill=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes"', con)
    #btn_clr_ah.pack(fill='both', expand=True, side=tk.TOP)
    #btn_ahasp.pack(fill='both', expand=True)
    #btn_ahareg.pack(fill='both', expand=True)
    th_skill_dis=all_th_skill[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(th_skill_dis.to_markdown(index=False))

def fill_listbox_rooms(*args):
    listbox_rooms.delete(0, tk.END)
    txt.delete(1.0, tk.END)
    idxs=listbox_houses.curselection()
    if len(idxs)==1:
        idx=int(idxs[0])
        if idx==0:
##            for item in frame.winfo_children():
##                item.destroy()
            btn_ahas.pack(fill='both', expand=True, side=tk.TOP)
            btn_ahasp.pack(fill='both', expand=True)
            btn_ahareg.pack(fill='both', expand=True)
            all_h=pd.read_sql_query("SELECT * FROM 'My Books'", con)
            all_h_dis=all_h[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(all_h_dis.to_markdown(index=False))
        if idx==1:
##            for item in main_screen.winfo_children():
##                item.destroy()
            sys.stdout=destroy_btns(main_screen)
            btn_thas.pack(fill='both', expand=True, side=tk.TOP)
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
            listbox_rooms.insert(tk.END, 'Master Bedroom')
            txt.insert(tk.END, tbl_lm)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_lm_rooms)
        if idx==5:
            bm=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Bloodchill Manor'", con)
            tbl_bm=tbl.tabulate(bm,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            for room in bm_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.insert(tk.END, tbl_bm)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_bm_rooms)
        if idx==6:
            h=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Hendraheim'", con)
            tbl_h=tbl.tabulate(h,
                               headers='keys',
                               tablefmt='grid',
                               showindex=False)
            for room in h_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.insert(tk.END, tbl_h)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_h_rooms)
        if idx==7:
            hs=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Honeyside'", con)
            tbl_hs=tbl.tabulate(hs,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            for room in hs_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.insert(tk.END, tbl_hs)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_hs_rooms)
###############################################FILL LISTBOX_ROOMS###################################################
##################################################FILL TABLES#######################################################
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
            listbox_rooms.insert(tk.END, 'Master Bedroom')
            txt.delete(1.0, tk.END)
            lm=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Lakeview Manor'", con)
            tbl_lm=tbl.tabulate(lm,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            txt.insert(tk.END, tbl_lm)

#CREATE FUNCTION TO FILL TABLE FOR BLOODCHILL MANOR:
def fill_table_bm_rooms(*args):           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            listbox_rooms.delete(0, tk.END)
            for room in bm_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.delete(1.0, tk.END)
            bm=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Bloodchill Manor'", con)
            tbl_bm=tbl.tabulate(bm,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            txt.insert(tk.END, tbl_bm)
        if idx_room==1:
            txt.delete(1.0, tk.END)
            bm_mb1=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Bloodchill Manor' AND Room = 'Master Bedroom (Floor 1)'", con)
            tbl_bm_mb1=tbl.tabulate(bm_mb1,
                                    headers='keys',
                                    tablefmt='grid',
                                    showindex=False)
            txt.insert(tk.END, tbl_bm_mb1)
        if idx_room==2:
            txt.delete(1.0, tk.END)
            bm_mb2=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Bloodchill Manor' AND Room = 'Master Bedroom (Floor 2)'", con)
            tbl_bm_mb2=tbl.tabulate(bm_mb2,
                                    headers='keys',
                                    tablefmt='grid',
                                    showindex=False)
            txt.insert(tk.END, tbl_bm_mb2)
        if idx_room==3:
            txt.delete(1.0, tk.END)
            bm_kidroom=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Bloodchill Manor' AND Room = 'Child Room'", con)
            tbl_bm_kidroom=tbl.tabulate(bm_kidroom,
                                        headers='keys',
                                        tablefmt='grid',
                                        showindex=False)
            txt.insert(tk.END, tbl_bm_kidroom)

#CREATE FUNCTION TO FILL TABLE FOR HENDRAHEIM:
def fill_table_h_rooms(*args):           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            listbox_rooms.delete(0, tk.END)
            for room in h_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.delete(1.0, tk.END)
            h=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Hendraheim'", con)
            tbl_h=tbl.tabulate(h,
                               headers='keys',
                               tablefmt='grid',
                               showindex=False)
            txt.insert(tk.END, tbl_h)
        if idx_room==1:
            txt.delete(1.0, tk.END)
            h_bedrooml=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Hendraheim' AND Room = 'Bedroom (Left)'", con)
            tbl_h_bedrooml=tbl.tabulate(h_bedrooml,
                                       headers='keys',
                                       tablefmt='grid',
                                       showindex=False)
            txt.insert(tk.END, tbl_h_bedrooml)
        if idx_room==2:
            txt.delete(1.0, tk.END)
            h_bedroomr=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Hendraheim' AND Room = 'Bedroom (Right)'", con)
            tbl_h_bedroomr=tbl.tabulate(h_bedroomr,
                                        headers='keys',
                                        tablefmt='grid',
                                        showindex=False)
            txt.insert(tk.END, tbl_h_bedroomr)
        if idx_room==3:
            txt.delete(1.0, tk.END)
            h_dining=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Hendraheim' AND Room = 'Dining Area'", con)
            tbl_h_dining=tbl.tabulate(h_dining,
                                      headers='keys',
                                      tablefmt='grid',
                                      showindex=False)
            txt.insert(tk.END, tbl_h_dining)

#CREATE FUNCTION TO FILL TABLE FOR HONEYSIDE:
def fill_table_hs_rooms(*args):           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            listbox_rooms.delete(0, tk.END)
            for room in hs_rooms:
                listbox_rooms.insert(tk.END, room)
            txt.delete(1.0, tk.END)
            hs=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Honeyside'", con)
            tbl_hs=tbl.tabulate(hs,
                                headers='keys',
                                tablefmt='grid',
                                showindex=False)
            txt.insert(tk.END, tbl_hs)
        if idx_room==1:
            txt.delete(1.0, tk.END)
            hs_bedroom=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Honeyside' AND Room = 'Bedroom'", con)
            tbl_hs_bedroom=tbl.tabulate(hs_bedroom,
                                        headers='keys',
                                        tablefmt='grid',
                                        showindex=False)
            txt.insert(tk.END, tbl_hs_bedroom)
        if idx_room==2:
            txt.delete(1.0, tk.END)
            hs_basement=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Honeyside' AND Room = 'Basement'", con)
            tbl_hs_basement=tbl.tabulate(hs_basement,
                                         headers='keys',
                                         tablefmt='grid',
                                         showindex=False)
            txt.insert(tk.END, tbl_hs_basement)
##################################################FILL TABLES#######################################################
#################################################CREATE WIDGETS#######################################################
#CREATE HOUSE'S LISTBOX AND LABEL:
lbl_houses=tk.Label(main_screen, text='Select House:').pack(expand=True, side=tk.TOP)
listbox_houses=tk.Listbox(main_screen,
                          listvariable=Houses,
                          bg='white',
                          font='Ariel',
                          fg='black')
listbox_houses.pack(expand=True, side=tk.TOP)
listbox_houses.bind('<<ListboxSelect>>', fill_listbox_rooms)
#CREATE ROOM'S LISTBOX AND LABEL:
lbl_rooms=tk.Label(main_screen, text='Select Room:').pack(side=tk.TOP)
listbox_rooms=tk.Listbox(main_screen,
                         bg='white',
                         font='Ariel',
                         fg='black',
                         exportselection=False)
listbox_rooms.pack(expand=True)
#CREATE TEXTBOX FOR TABLES:
txt=tk.Text(main_screen)
txt.pack(fill='both', expand=True, side=tk.BOTTOM)
#CREATE BUTTONS FOR ALL HOUSES SCREEN
btn_ahas=tk.Button(main_screen, text="Skill Books", command=lambda:[all_house_skill(), btn_ahas.pack_forget()])
btn_ahasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[all_house_spell(), btn_ahasp.pack_forget()])
btn_ahareg=tk.Button(main_screen, text="Regular Books", command=lambda:[all_house_reg(), btn_ahasp.pack_forget()])
btn_clr_ah=tk.Button(main_screen, text="Clear", command=lambda:[clear_ah(), btn_clr_ah.pack_forget()])
#CREATE BUTTONS FOR TUNDRA HOMESTEAD SCREEN
btn_thas=tk.Button(main_screen, text="Skill Books", command=lambda:[all_house_skill(), btn_ahas.pack_forget()])
#################################################CREATE WIDGETS#######################################################
##################################################RUN PROGRAM#######################################################
#LAUNCH DATABASE:
main_screen.mainloop()

#CLOSE DATABASE CONNECTION:
con.close()
##################################################RUN PROGRAM#######################################################
