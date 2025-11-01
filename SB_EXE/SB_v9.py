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

#CREATE MAIN SCREEN:
main_screen = tk.Tk()
main_screen.title('Skyrim Books')
screen_width=int(main_screen.winfo_screenwidth())
screen_height=int(main_screen.winfo_screenheight())
width = screen_width * 0.75
height = main_screen.winfo_screenheight()* 0.4
main_screen.geometry("%dx%d" % (width, height))
main_screen.columnconfigure(2, weight=2)

#CREATE LISTS OF HOUSES AND ROOMS:
houses = ('All Houses', 'Tundra Homestead', 'Goldenhills Plantation', 'Breezehome', 'Lakeview Manor', 'Bloodchill Manor', 'Hendraheim', 'Honeyside')
Houses = tk.StringVar(main_screen, value=houses)
all_rooms = ('All Rooms')
th_rooms = ('All Rooms', 'Bedroom', 'Basement')
gp_rooms = ('All Rooms', 'Bedroom', 'Shrine Room (Left)', 'Shrine Room (Right)')
b_rooms = ('All Rooms', 'Living Room', 'Alchemy Laboratory')
lm_rooms = ('Master Bedroom')
bm_rooms = ('All Rooms', 'Master Bedroom (Floor 1)', 'Master Bedroom (Floor 2)', 'Child Room')
h_rooms = ('All Rooms', 'Bedroom (Left)', 'Bedroom (Right)', 'Dining Area')
hs_rooms = ('All Rooms', 'Bedroom', 'Basement')


#CREATE FUNCTION TO REMOVE BUTTONS:
def forget_btns(main_screen):
    lst=main_screen.winfo_children()
    for item in lst:
        if isinstance(item, tk.Button):
            item.grid_forget()
        
#CREATE FUNCTIONS FOR ALL HOUSES:
def clear_ah(*args):#THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM:
    sys.stdout=fill_table_all_rooms()
    
def fill_table_all_rooms(*args):#THIS FUNCTION PRODUCES THE UNFILTERED TABLE WHEN SELECTED IN LISTBOX 2:         
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            btn_ahas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_ahasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_ahareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            all_h=pd.read_sql_query('SELECT * FROM "My Books"', con)
            sys.stdout=printtotxt()
            print(all_h.to_markdown(index=False))
            
def all_house_skill(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    all_h_skill=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Skill Book" = "Yes"', con)
    btn_clr_ah.grid(row=2, column=0, columnspan=2, sticky='ew')
    btn_ahasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_ahareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    all_h_skill_dis=all_h_skill[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(all_h_skill_dis.to_markdown(index=False))

def all_house_spell(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    all_h_spell=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Spell Tome" = "Yes"', con)
    btn_clr_ah.grid(row=2, column=0, columnspan=2, sticky='ew')
    btn_ahas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_ahareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    all_h_spell_dis=all_h_spell[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(all_h_spell_dis.to_markdown(index=False))

def all_house_reg(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    all_h_reg=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Spell Tome" = "No" AND "Skill Book" = "No"', con)
    btn_clr_ah.grid(row=2, column=0, columnspan=2, sticky='ew')
    btn_ahas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_ahasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    all_h_reg_dis=all_h_reg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(all_h_reg_dis.to_markdown(index=False))
            
#CREATE FUNCTIONS FOR TUNDRA HOMESTEAD:
def fill_table_th_rooms(*args):#THIS FUNCTION PRODUCES THE ALL BOOKS IN TUNDRA HOMESTEAD WHEN SELECTED IN LISTBOX 2:            
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            thar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead"', con)
            btn_tharas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_tharasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_tharareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            thar_dis=thar[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(thar_dis.to_markdown(index=False))
        if idx_room==1:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            thbr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND Room = "Bedroom"', con)
            btn_thbras.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_thbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_thbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            thbr_dis=thar[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(thbr_dis.to_markdown(index=False))
        if idx_room==2:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            thba=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Tundra Homestead' AND Room = 'Basement'", con)
            btn_thbaas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_thbaasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_thbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            thba_dis=thar[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(thba_dis.to_markdown(index=False))

def clear_th(*args):#THIS FUNCTION RESETS THE TABLE TO ALL BOOKS FROM TUNDRA HOMESTEAD:
    sys.stdout=fill_table_th_rooms()

def thar_skill(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    tharas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes"', con)
    btn_tharasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_tharareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    tharas_dis=all_th_skill[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(tharas_dis.to_markdown(index=False))

def thar_spell(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    tharasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes"', con)
    btn_tharas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_tharareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    tharasp_dis=all_h_spell[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(tharasp_dis.to_markdown(index=False))

def thar_reg(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    tharareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
    btn_tharas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_tharasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    tharareg_dis=all_h_reg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(tharareg_dis.to_markdown(index=False))

def thbr_skill(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes" AND Room = "Bedroom"', con)
    btn_thbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbras_dis=all_th_skill[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbras_dis.to_markdown(index=False))

def thbr_spell(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes" AND Room = "Bedroom"', con)
    btn_thbras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbrasp_dis=all_h_spell[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbrasp_dis.to_markdown(index=False))

def thbr_reg(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom"', con)
    btn_thbras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbrasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbrareg_dis=all_h_reg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbrareg_dis.to_markdown(index=False))

def thba_skill(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BASEMENT:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbaas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes" AND Room = "Basement"', con)
    btn_thbaasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbaas_dis=all_th_skill[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbaas_dis.to_markdown(index=False))

def thba_spell(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BASEMENT:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbaasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes" AND Room = "Basement"', con)
    btn_thbaas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbaasp_dis=all_h_spell[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbaasp_dis.to_markdown(index=False))

def thba_reg(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BASEMENT:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbaareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Basement"', con)
    btn_thbaas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbaasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbaareg_dis=all_h_reg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbaareg_dis.to_markdown(index=False))

#CREATE FUNCTION TO FILL TABLE FOR GOLDENHILLS PLANTATION:
def fill_table_gp_rooms(*args):#THIS FUNCTION PRODUCES THE ALL BOOKS IN TUNDRA HOMESTEAD WHEN SELECTED IN LISTBOX 2           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            gpar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation"', con)
            btn_gparas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_gparasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_gparareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            gpar_dis=all_h_reg[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(gpar_dis.to_markdown(index=False))

def clear_gp(*args):#THIS FUNCTION RESETS THE TABLE TO ALL BOOKS FROM GOLDENHILLS PLANTATION IN ALL ROOMS:
    sys.stdout=fill_table_gp_rooms()

def gpar_skill(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    gparas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes"', con)
    btn_gparasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gparareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    gparas_dis=all_th_skill[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gparas_dis.to_markdown(index=False))
    
#START FROM HERE  #START FROM HERE #START FROM HERE #START FROM HERE #START FROM HERE #START FROM HERE #START FROM HERE
#START FROM HERE #START FROM HERE #START FROM HERE #START FROM HERE #START FROM HERE #START FROM HERE #START FROM HERE     

def gpar_spell(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    tharasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes"', con)
    btn_tharas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_tharareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    tharasp_dis=all_h_spell[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(tharasp_dis.to_markdown(index=False))

def thar_reg(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    tharareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
    btn_tharas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_tharasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    tharareg_dis=all_h_reg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(tharareg_dis.to_markdown(index=False))

def thbr_skill(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes" AND Room = "Bedroom"', con)
    btn_thbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbras_dis=all_th_skill[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbras_dis.to_markdown(index=False))

def thbr_spell(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes" AND Room = "Bedroom"', con)
    btn_thbras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbrasp_dis=all_h_spell[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbrasp_dis.to_markdown(index=False))

def thbr_reg(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom"', con)
    btn_thbras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbrasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbrareg_dis=all_h_reg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbrareg_dis.to_markdown(index=False))

def thba_skill(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BASEMENT:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbaas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes" AND Room = "Basement"', con)
    btn_thbaasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbaas_dis=all_th_skill[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbaas_dis.to_markdown(index=False))

def thba_spell(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BASEMENT:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbaasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes" AND Room = "Basement"', con)
    btn_thbaas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbaasp_dis=all_h_spell[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbaasp_dis.to_markdown(index=False))

def thba_reg(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BASEMENT:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbaareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Basement"', con)
    btn_thbaas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbaasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbaareg_dis=all_h_reg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbaareg_dis.to_markdown(index=False))
###############################################FILL LISTBOX_ROOMS###################################################
#CREATE FUNCTION TO FILL LISTBOX_ROOMS:
class printtotxt(object):
    def write(self, s):
        txt.insert(tk.END, s)
        
#CREATE FUNCTION TO PRESENT GUI:
def fill_listbox_rooms(*args):
    sys.stdout=forget_btns(main_screen)
    listbox_rooms.delete(0, tk.END)
    txt.delete(1.0, tk.END)
    txt.grid_forget()
    idxs=listbox_houses.curselection()
    if len(idxs)==1:
        idx=int(idxs[0])
        if idx==0:
            sys.stdout=forget_btns(main_screen)
            txt.grid_forget()
            #all_h_dis=all_h[['Title', 'House', 'Room']]
            listbox_rooms.insert(tk.END, 'All Rooms')
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_all_rooms)
        if idx==1:
            sys.stdout=forget_btns(main_screen)
            txt.grid_forget()
            listbox_rooms.delete(0, tk.END)
            for room in th_rooms:
                listbox_rooms.insert(tk.END, room)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_th_rooms)
        if idx==2:
            sys.stdout=forget_btns(main_screen)
            txt.grid_forget()
            listbox_rooms.delete(0, tk.END)
            for room in gp_rooms:
                listbox_rooms.insert(tk.END, room)
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
##
##
##        if idx_room==1:
##            txt.delete(1.0, tk.END)
##            gp_bedroom=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Goldenhills Plantation' AND Room = 'Bedroom'", con)
##            tbl_gp_bedroom=tbl.tabulate(gp_bedroom,
##                                        headers='keys',
##                                        tablefmt='grid',
##                                        showindex=False)
##            txt.insert(tk.END, tbl_gp_bedroom)
##        if idx_room==2:
##            txt.delete(1.0, tk.END)
##            gp_srl=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Goldenhills Plantation' AND Room = 'Shrine Room (Left)'", con)
##            tbl_gp_srl=tbl.tabulate(gp_srl,
##                                    headers='keys',
##                                    tablefmt='grid',
##                                    showindex=False)
##            txt.insert(tk.END, tbl_gp_srl)
##        if idx_room==3:
##            txt.delete(1.0, tk.END)
##            gp_srr=pd.read_sql_query("SELECT * FROM 'My Books' WHERE House = 'Goldenhills Plantation' AND Room = 'Shrine Room (Right)'", con)
##            tbl_gp_srr=tbl.tabulate(gp_srr,
##                                    headers='keys',
##                                    tablefmt='grid',
##                                    showindex=False)
##            txt.insert(tk.END, tbl_gp_srr)
            
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
lbl_houses=tk.Label(main_screen, text='Select House:')
lbl_houses.grid(row=0, column=0, sticky='ew')
listbox_houses=tk.Listbox(main_screen,
                          listvariable=Houses,
                          bg='white',
                          font='Ariel',
                          fg='black')
listbox_houses.grid(row=1, column=0, sticky='ew')
listbox_houses.bind('<<ListboxSelect>>', fill_listbox_rooms)
#CREATE ROOM'S LISTBOX AND LABEL:
lbl_rooms=tk.Label(main_screen, text='Select Room:')
lbl_rooms.grid(row=0, column=1, sticky='ew')
listbox_rooms=tk.Listbox(main_screen,
                         bg='white',
                         font='Ariel',
                         fg='black',
                         exportselection=False)
listbox_rooms.grid(row=1, column=1, sticky='ew')
#CREATE TEXTBOX FOR TABLES:
txt=tk.Text(main_screen)

#CREATE BUTTONS FOR ALL HOUSES SCREEN:
btn_clr_ah=tk.Button(main_screen, text="Clear", command=lambda:[clear_ah(), btn_clr_ah.grid_forget()])
btn_ahas=tk.Button(main_screen, text="Skill Books", command=lambda:[all_house_skill(), btn_ahas.grid_forget()])
btn_ahasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[all_house_spell(), btn_ahasp.grid_forget()])
btn_ahareg=tk.Button(main_screen, text="Regular Books", command=lambda:[all_house_reg(), btn_ahareg.grid_forget()])

#CREATE BUTTONS FOR TUNDRA HOMESTEAD, ALL ROOMS:
btn_clr_th=tk.Button(main_screen, text="Clear", command=lambda:[clear_th(), btn_clr_th.grid_forget()])
btn_tharas=tk.Button(main_screen, text="Skill Books", command=lambda:[thar_skill(), btn_tharas.pack_forget()])
btn_tharasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[thar_spell(), btn_tharasp.grid_forget()])
btn_tharareg=tk.Button(main_screen, text="Regular Books", command=lambda:[thar_reg(), btn_tharareg.grid_forget()])

#CREATE BUTTONS FOR TUNDRA HOMESTEAD, BEDROOM:
btn_thbras=tk.Button(main_screen, text="Skill Books", command=lambda:[thbr_skill(), btn_thbras.pack_forget()])
btn_thbrasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[thbr_spell(), btn_thbrasp.grid_forget()])
btn_thbrareg=tk.Button(main_screen, text="Regular Books", command=lambda:[thbr_reg(), btn_thbrareg.grid_forget()])

#CREATE BUTTONS FOR TUNDRA HOMESTEAD, BASEMENT:
btn_thbaas=tk.Button(main_screen, text="Skill Books", command=lambda:[thba_skill(), btn_thbaas.pack_forget()])
btn_thbaasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[thba_spell(), btn_thbaasp.grid_forget()])
btn_thbaareg=tk.Button(main_screen, text="Regular Books", command=lambda:[thba_reg(), btn_thbaareg.grid_forget()])

#CREATE BUTTONS FOR GOLDENHILLS PLANTATION, ALL ROOMS:
btn_clr_gp=tk.Button(main_screen, text="Clear", command=lambda:[clear_gp(), btn_clr_gp.grid_forget()])
btn_gparas=tk.Button(main_screen, text="Skill Books", command=lambda:[gpar_skill(), btn_gparas.pack_forget()])
btn_gparasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[gpar_spell(), btn_gparasp.grid_forget()])
btn_gparareg=tk.Button(main_screen, text="Regular Books", command=lambda:[gpar_reg(), btn_gparareg.grid_forget()])
#################################################CREATE WIDGETS#######################################################
##################################################RUN PROGRAM#######################################################
#LAUNCH DATABASE:
main_screen.mainloop()

#CLOSE DATABASE CONNECTION:
con.close()
##################################################RUN PROGRAM#######################################################
