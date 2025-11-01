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
width = screen_width * 0.56
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

####################################DEFINE MAJOR FUNCTIONS##################################
#CREATE FUNCTION TO REMOVE BUTTONS:
def forget_btns(main_screen):
    lst=main_screen.winfo_children()
    for item in lst:
        if isinstance(item, tk.Button):
            item.grid_forget()

#CREATE FUNCTION FOR SEARCHING:
def search(*args):
    keyword=searchstring.get()
    title=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Title" = keyword', con)
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    title_dis=title[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(title_dis.to_markdown(index=False))
                        ######CREATE FUNCTIONS FOR ALL HOUSES######   
#CREATE FUNCTION TO FILL UNFILTERED TABLE:
def fill_table_all_rooms(*args):         
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
            all_h_dis=all_h[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(all_h_dis.to_markdown(index=False))
            
#THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM:
def clear_ah(*args):
    sys.stdout=fill_table_all_rooms()
            
#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS:
def all_house_skill(*args):
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

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES:
def all_house_spell(*args):
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

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES:
def all_house_reg(*args):
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
            
                    ######CREATE FUNCTIONS FOR TUNDRA HOMESTEAD######
#CREATE FUNCTION TO FILL TABLES FOR TUNDRA HOMESTEAD:    
def fill_table_th_rooms(*args):            
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
            thbr_dis=thbr[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(thbr_dis.to_markdown(index=False))
        if idx_room==2:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            thba=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND Room = "Basement"', con)
            btn_thbaas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_thbaasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_thbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            thba_dis=thba[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(thba_dis.to_markdown(index=False))

#THIS FUNCTION RESETS THE TABLE TO ALL BOOKS FROM TUNDRA HOMESTEAD:
def clear_th(*args):
    sys.stdout=fill_table_th_rooms()

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS:
def thar_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    tharas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes"', con)
    btn_tharasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_tharareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    tharas_dis=tharas[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(tharas_dis.to_markdown(index=False))
    
#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS:
def thar_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    tharasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes"', con)
    btn_tharas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_tharareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    tharasp_dis=tharasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(tharasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS:
def thar_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    tharareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
    btn_tharas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_tharasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    tharareg_dis=tharareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(tharareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM:
def thbr_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes" AND Room = "Bedroom"', con)
    btn_thbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbras_dis=thbras[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbras_dis.to_markdown(index=False))
    
#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM:
def thbr_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes" AND Room = "Bedroom"', con)
    btn_thbras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbrasp_dis=thbrasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbrasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM:
def thbr_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom"', con)
    btn_thbras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbrasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbrareg_dis=thbrareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbrareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BASEMENT:
def thba_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbaas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes" AND Room = "Basement"', con)
    btn_thbaasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbaas_dis=thbaas[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbaas_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BASEMENT:
def thba_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbaasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes" AND Room = "Basement"', con)
    btn_thbaas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbaasp_dis=thbaasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbaasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BASEMENT:
def thba_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
    thbaareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Basement"', con)
    btn_thbaas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_thbaasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    thbaareg_dis=thbaareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(thbaareg_dis.to_markdown(index=False))

                    ######CREATE FUNCTIONS FOR GOLDENHILLS PLANTATION######
#CREATE FUNCTION TO FILL TABLES FOR GOLDENHILLS PLANTATION:    
def fill_table_gp_rooms(*args):           
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
            gpar_dis=gpar[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(gpar_dis.to_markdown(index=False))
        if idx_room==1:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            gpbr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND Room = "Bedroom"', con)
            btn_gpbras.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_gpbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_gpbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            gpbr_dis=gpbr[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(gpbr_dis.to_markdown(index=False))
        if idx_room==2:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            gpsrl=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND Room = "Shrine Room (Left)"', con)
            btn_gpsrlas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_gpsrlasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_gpsrlareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            gpsrl_dis=gpsrl[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(gpsrl_dis.to_markdown(index=False))
        if idx_room==3:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            gpsrr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND Room = "Shrine Room (Right)"', con)
            btn_gpsrras.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_gpsrrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_gpsrrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            gpsrr_dis=gpsrr[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(gpsrr_dis.to_markdown(index=False))

#THIS FUNCTION RESETS THE TABLE TO ALL BOOKS FROM GOLDENHILLS PLANTATION IN ALL ROOMS:
def clear_gp(*args):
    sys.stdout=fill_table_gp_rooms()

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN GOLDENHILLS PLANTATION:
def gpar_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gparas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes"', con)
    btn_gparasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gparareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    gparas_dis=gparas[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gparas_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS:
def gpar_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gparasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes"', con)
    btn_gparas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gparareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    gparasp_dis=gparasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gparasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS:
def gpar_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gparareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
    btn_gparas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gparasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    gparareg_dis=gparareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gparareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM:
def gpbr_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gpbras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes" AND Room = "Bedroom"', con)
    btn_gpbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gpbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    gpbras_dis=gpbras[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gpbras_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM:
def gpbr_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gpbrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes" AND Room = "Bedroom"', con)
    btn_gpbras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gpbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    gpbrasp_dis=gpbrasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gpbrasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM:
def gpbr_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gpbrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom"', con)
    btn_gpbras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gpbrasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    gpbrareg_dis=gpbrareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gpbrareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN SHRINE ROOM LEFT:
def gpsrl_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gpsrlas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes" AND Room = "Shrine Room (Left)"', con)
    btn_gpsrlasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gpsrlareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    gpsrlas_dis=gpsrlas[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gpsrlas_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN SHRINE ROOM LEFT:
def gpsrl_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gpsrlasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes" AND Room = "Shrine Room (Left)"', con)
    btn_gpsrlas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gpsrlareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    gpsrlasp_dis=gpsrlasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gpsrlasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN SHRINE ROOM LEFT:
def gpsrl_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gpsrlareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Shrine Room (Left)"', con)
    btn_gpsrlas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gpsrlasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    gpsrlareg_dis=gpsrlareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gpsrlareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN SHRINE ROOM RIGHT:
def gpsrr_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gpsrras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes" AND Room = "Shrine Room (Right)"', con)
    btn_gpsrrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gpsrrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    gpsrras_dis=gpsrras[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gpsrras_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN SHRINE ROOM RIGHT:
def gpsrr_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gpsrrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes" AND Room = "Shrine Room (Right)"', con)
    btn_gpsrras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gpsrrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    gpsrrasp_dis=gpsrrasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gpsrrasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN SHRINE ROOM RIGHT:
def gpsrr_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
    gpsrrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Shrine Room (Right)"', con)
    btn_gpsrras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_gpsrrasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    gpsrrareg_dis=gpsrrareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(gpsrrareg_dis.to_markdown(index=False))

                            ######CREATE FUNCTIONS FOR BREEZEHOME######
#CREATE FUNCTION TO FILL TABLES FOR BREEZEHOME:
def fill_table_b_rooms(*args):           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            bar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome"', con)
            btn_baras.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_barasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_barareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            bar_dis=bar[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(bar_dis.to_markdown(index=False))
        if idx_room==1:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            bliv=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND Room = "Living Room"', con)
            btn_blivas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_blivasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_blivareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            bliv_dis=bliv[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(bliv_dis.to_markdown(index=False))
        if idx_room==2:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            blab=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND Room = "Alchemy Lab"', con)
            btn_blabas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_blabasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_blabareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            blab_dis=blab[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(blab_dis.to_markdown(index=False))

#THIS FUNCTION RESETS THE TABLE TO ALL BOOKS FROM BREEZEHOME IN ALL ROOMS:
def clear_b(*args):
    sys.stdout=fill_table_b_rooms()

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN BREEZEHOME:
def bar_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_b.grid(row=2, column=0, columnspan=2, sticky='ew')
    baras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Skill Book" = "Yes"', con)
    btn_barasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_barareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    baras_dis=baras[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(baras_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS:
def bar_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_b.grid(row=2, column=0, columnspan=2, sticky='ew')
    barasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "Yes"', con)
    btn_baras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_barareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    barasp_dis=barasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(barasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS:
def bar_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_b.grid(row=2, column=0, columnspan=2, sticky='ew')
    barareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
    btn_baras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_barasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    barareg_dis=barareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(barareg_dis.to_markdown(index=False))

def bliv_skill(*args):#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE LIVING ROOM:
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_b.grid(row=2, column=0, columnspan=2, sticky='ew')
    blivas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Skill Book" = "Yes" AND Room = "Living Room"', con)
    btn_blivasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_blivareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    blivas_dis=blivas[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(blivas_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE LIVING ROOM:
def bliv_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_b.grid(row=2, column=0, columnspan=2, sticky='ew')
    blivasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "Yes" AND Room = "Living Room"', con)
    btn_blivas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_blivareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    blivasp_dis=blivasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(blivasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE LIVING ROOM:
def bliv_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_b.grid(row=2, column=0, columnspan=2, sticky='ew')
    blivareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Living Room"', con)
    btn_blivas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_blivasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    blivareg_dis=blivareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(blivareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE ALCHEMY LAB:
def blab_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_b.grid(row=2, column=0, columnspan=2, sticky='ew')
    blabas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Skill Book" = "Yes" AND Room = "Alchemy Lab"', con)
    btn_blabasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_blabareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    blabas_dis=blabas[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(blabas_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE ALCHEMY LAB:
def blab_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_b.grid(row=2, column=0, columnspan=2, sticky='ew')
    blabasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "Yes" AND Room = "Alchemy Lab"', con)
    btn_blabas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_blabareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    blabasp_dis=blabasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(blabasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE ALCHEMY LAB:
def blab_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_b.grid(row=2, column=0, columnspan=2, sticky='ew')
    blabareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Alchemy Lab"', con)
    btn_blabas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_blabasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    blabareg_dis=blabareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(blabareg_dis.to_markdown(index=False))

                            ######CREATE FUNCTIONS FOR LAKEVIEW MANOR######
#CREATE FUNCTION TO FILL TABLE FOR LAKEVIEW MANOR:
def fill_table_lm_rooms(*args):           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            btn_lmas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_lmasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_lmareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            lm=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Lakeview Manor"', con)
            lm_dis=lm[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(lm_dis.to_markdown(index=False))
            
#THIS FUNCTION RESETS THE TABLE TO ALL BOOKS FROM LAKEVIEW MANOR IN ALL ROOMS:
def clear_lm(*args):
    sys.stdout=fill_table_lm_rooms()
            
#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS:
def lm_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    lm_skill=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Lakeview Manor" AND "Skill Book" = "Yes"', con)
    btn_clr_lm.grid(row=2, column=0, columnspan=2, sticky='ew')
    btn_lmasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_lmareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    lm_skill_dis=lm_skill[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(lm_skill_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES:
def lm_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    lm_spell=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Lakeview Manor" AND "Spell Tome" = "Yes"', con)
    btn_clr_lm.grid(row=2, column=0, columnspan=2, sticky='ew')
    btn_lmas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_lmareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    lm_spell_dis=lm_spell[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(lm_spell_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES:
def lm_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    lm_reg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Lakeview Manor" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
    btn_clr_lm.grid(row=2, column=0, columnspan=2, sticky='ew')
    btn_lmas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_lmasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    lm_reg_dis=lm_reg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(lm_reg_dis.to_markdown(index=False))

                         ######CREATE FUNCTIONS FOR BLOODCHILL MANOR######
#CREATE FUNCTION TO FILL TABLE FOR BLOODCHILL MANOR:
def fill_table_bm_rooms(*args):           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            bmar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor"', con)
            btn_bmaras.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_bmarasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_bmarareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            bmar_dis=bmar[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(bmar_dis.to_markdown(index=False))
        if idx_room==1:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            bmmb1=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND Room = "Master Bedroom (Floor 1)"', con)
            btn_bmmb1as.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_bmmb1asp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_bmmb1areg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            bmmb1_dis=bmmb1[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(bmmb1_dis.to_markdown(index=False))
        if idx_room==2:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            bmmb2=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND Room = "Master Bedroom (Floor 2)"', con)
            btn_bmmb2as.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_bmmb2asp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_bmmb2areg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            bmmb2_dis=bmmb2[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(bmmb2_dis.to_markdown(index=False))
        if idx_room==3:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            bmcr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND Room = "Child Room"', con)
            btn_bmcras.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_bmcrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_bmcrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            bmcr_dis=bmcr[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(bmcr_dis.to_markdown(index=False))

#THIS FUNCTION RESETS THE TABLE TO ALL BOOKS FROM BLOODCHILL MANOR IN ALL ROOMS:
def clear_bm(*args):
    sys.stdout=fill_table_bm_rooms()

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN BLOODCHILL MANOR:
def bmar_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmaras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Skill Book" = "Yes"', con)
    btn_bmarasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmarareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmaras_dis=bmaras[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmaras_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN BLOODCHILL MANOR:
def bmar_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmarasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "Yes"', con)
    btn_bmaras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmarareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmarasp_dis=bmarasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmarasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN BLOODCHILL MANOR:
def bmar_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmarareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
    btn_bmaras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmarasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmarareg_dis=bmarareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmarareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN BLOODCHILL MANOR, MASTER BEDROOM FLOOR 1:
def bmmb1_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmmb1as=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Skill Book" = "Yes" AND Room = "Master Bedroom (Floor 1)"', con)
    btn_bmmb1asp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmmb1areg.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmmb1as_dis=bmmb1as[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmmb1as_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN BLOODCHILL MANOR, MASTER BEDROOM FLOOR 1:
def bmmb1_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmmb1asp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "Yes" AND Room = "Master Bedroom (Floor 1)"', con)
    btn_bmmb1as.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmmb1areg.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmmb1asp_dis=bmmb1asp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmmb1asp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN BLOODCHILL MANOR, MASTER BEDROOM FLOOR 1:
def bmmb1_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmmb1areg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Master Bedroom (Floor 1)"', con)
    btn_bmmb1as.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmmb1asp.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmmb1areg_dis=bmmb1areg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmmb1areg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN BLOODCHILL MANOR, MASTER BEDROOM FLOOR 2:
def bmmb2_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmmb2as=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Skill Book" = "Yes" AND Room = "Master Bedroom (Floor 2)"', con)
    btn_bmmb2asp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmmb2areg.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmmb2as_dis=bmmb2as[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmmb2as_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN BLOODCHILL MANOR, MASTER BEDROOM FLOOR 2:
def bmmb2_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmmb2asp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "Yes" AND Room = "Master Bedroom (Floor 2)"', con)
    btn_bmmb2as.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmmb2areg.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmmb2asp_dis=bmmb2asp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmmb2asp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN BLOODCHILL MANOR, MASTER BEDROOM FLOOR 2:
def bmmb2_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmmb2areg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Master Bedroom (Floor 2)"', con)
    btn_bmmb2as.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmmb2asp.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmmb2areg_dis=bmmb2areg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmmb2areg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN BLOODCHILL MANOR, CHILD ROOM:
def bmcr_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmcras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Skill Book" = "Yes" AND Room = "Child Room"', con)
    btn_bmcrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmcrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmcras_dis=bmcras[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmcras_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN BLOODCHILL MANOR, CHILD ROOM:
def bmcr_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmcrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "Yes" AND Room = "Child Room"', con)
    btn_bmcras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmcrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmcrasp_dis=bmcrasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmcrasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN BLOODCHILL MANOR, CHILD ROOM:
def bmcr_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_bm.grid(row=2, column=0, columnspan=2, sticky='ew')
    bmcrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Child Room"', con)
    btn_bmcras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_bmcrasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    bmcrareg_dis=bmcrareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(bmcrareg_dis.to_markdown(index=False))

                        ######CREATE FUNCTIONS FOR HENDRAHEIM######
#CREATE FUNCTION TO FILL TABLE FOR HENDRAHEIM:
def fill_table_h_rooms(*args):           
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            har=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim"', con)
            btn_haras.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_harasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_harareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            har_dis=har[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(har_dis.to_markdown(index=False))
        if idx_room==1:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            hbrl=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND Room = "Bedroom (Left)"', con)
            btn_hbrlas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_hbrlasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_hbrlareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            hbrl_dis=hbrl[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(hbrl_dis.to_markdown(index=False))
        if idx_room==2:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            hbrr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND Room = "Bedroom (Right)"', con)
            btn_hbrras.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_hbrrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_hbrrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            hbrr_dis=hbrr[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(hbrr_dis.to_markdown(index=False))
        if idx_room==3:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            hda=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND Room = "Dining Area"', con)
            btn_hdaas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_hdaasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_hdaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            hda_dis=hda[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(hda_dis.to_markdown(index=False))
            
#THIS FUNCTION RESETS THE TABLE TO ALL BOOKS FROM HENDRAHEIM IN ALL ROOMS:
def clear_h(*args):
    sys.stdout=fill_table_h_rooms()

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN HENDRAHEIM:
def har_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    haras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Skill Book" = "Yes"', con)
    btn_harasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_harareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    haras_dis=haras[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(haras_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN HENDRAHEIM:
def har_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    harasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "Yes"', con)
    btn_haras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_harareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    harasp_dis=harasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(harasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN HENDRAHEIM:
def har_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    harareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
    btn_haras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_harasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    harareg_dis=harareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(harareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM LEFT:
def hbrl_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    hbrlas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Skill Book" = "Yes" AND Room = "Bedroom (Left)"', con)
    btn_hbrlasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hbrlareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hbrlas_dis=hbrlas[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hbrlas_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM LEFT:
def hbrl_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    hbrlasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "Yes" AND Room = "Bedroom (Left)"', con)
    btn_hbrlas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hbrlareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hbrlasp_dis=hbrlasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hbrlasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM LEFT:
def hbrl_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    hbrlareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom (Left)"', con)
    btn_hbrlas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hbrlasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    hbrlareg_dis=hbrlareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hbrlareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM RIGHT:
def hbrr_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    hbrras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Skill Book" = "Yes" AND Room = "Bedroom (Right)"', con)
    btn_hbrrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hbrrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hbrras_dis=hbrras[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hbrras_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM RIGHT:
def hbrr_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    hbrrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "Yes" AND Room = "Bedroom (Right)"', con)
    btn_hbrras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hbrrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hbrrasp_dis=hbrrasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hbrrasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM RIGHT:
def hbrr_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    hbrrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom (Right)"', con)
    btn_hbrras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hbrrasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    hbrrareg_dis=hbrrareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hbrrareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE DINING AREA:
def hda_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    hdaas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Skill Book" = "Yes" AND Room = "Dining Area"', con)
    btn_hdaasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hdaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hdaas_dis=hdaas[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hdaas_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN HENDRAHEIM IN THE DINING AREA:
def hda_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    hdaasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "Yes" AND Room = "Dining Area"', con)
    btn_hdaas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hdaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hdaasp_dis=hdaasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hdaasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN HENDRAHEIMIN THE DINING AREA:
def hda_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_h.grid(row=2, column=0, columnspan=2, sticky='ew')
    hdaareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Dining Area"', con)
    btn_hdaas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hdaasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    hdaareg_dis=hdaareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hdaareg_dis.to_markdown(index=False))

                    ######CREATE FUNCTIONS FOR HONEYSIDE######
#CREATE FUNCTION TO FILL TABLES FOR HONEYSIDE:    
def fill_table_hs_rooms(*args):            
    idxs_rooms=listbox_rooms.curselection()
    if len(idxs_rooms)==1:
        idx_room=int(idxs_rooms[0])
        if idx_room==0:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            hsar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside"', con)
            btn_hsaras.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_hsarasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_hsarareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            hsar_dis=hsar[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(hsar_dis.to_markdown(index=False))
        if idx_room==1:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            hsbr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND Room = "Bedroom"', con)
            btn_hsbras.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_hsbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_hsbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            hsbr_dis=hsbr[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(hsbr_dis.to_markdown(index=False))
        if idx_room==2:
            sys.stdout=forget_btns(main_screen)
            txt.delete(1.0, tk.END)
            hsba=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND Room = "Basement"', con)
            btn_hsbaas.grid(row=2, column=0, columnspan=2, sticky='ew')
            btn_hsbaasp.grid(row=3, column=0, columnspan=2, sticky='ew')
            btn_hsbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
            txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
            hsba_dis=hsba[['Title', 'House', 'Room']]
            sys.stdout=printtotxt()
            print(hsba_dis.to_markdown(index=False))

#THIS FUNCTION RESETS THE TABLE TO ALL BOOKS FROM HONEYSIDE:
def clear_hs(*args):
    sys.stdout=fill_table_hs_rooms()

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS:
def hsar_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_hs.grid(row=2, column=0, columnspan=2, sticky='ew')
    hsaras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Skill Book" = "Yes"', con)
    btn_hsarasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hsarareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hsaras_dis=hsaras[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hsaras_dis.to_markdown(index=False))
    
#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS:
def hsar_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_hs.grid(row=2, column=0, columnspan=2, sticky='ew')
    hsarasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "Yes"', con)
    btn_hsaras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hsarareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hsarasp_dis=hsarasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hsarasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS:
def hsar_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_hs.grid(row=2, column=0, columnspan=2, sticky='ew')
    hsarareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
    btn_hsaras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hsarasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    hsarareg_dis=hsarareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hsarareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM:
def hsbr_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_hs.grid(row=2, column=0, columnspan=2, sticky='ew')
    hsbras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Skill Book" = "Yes" AND Room = "Bedroom"', con)
    btn_hsbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hsbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hsbras_dis=hsbras[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hsbras_dis.to_markdown(index=False))
    
#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM:
def hsbr_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_hs.grid(row=2, column=0, columnspan=2, sticky='ew')
    hsbrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "Yes" AND Room = "Bedroom"', con)
    btn_hsbras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hsbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hsbrasp_dis=hsbrasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hsbrasp_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM:
def hsbr_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_hs.grid(row=2, column=0, columnspan=2, sticky='ew')
    hsbrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom"', con)
    btn_hsbras.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hsbrasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    hsbrareg_dis=hsbrareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hsbrareg_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BASEMENT:
def hsba_skill(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    btn_clr_hs.grid(row=2, column=0, columnspan=2, sticky='ew')
    hsbaas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Skill Book" = "Yes" AND Room = "Basement"', con)
    btn_hsbaasp.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hsbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hsbaas_dis=hsbaas[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hsbaas_dis.to_markdown(index=False))

#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BASEMENT:
def hsba_spell(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_hs.grid(row=2, column=0, columnspan=2, sticky='ew')
    hsbaasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "Yes" AND Room = "Basement"', con)
    btn_hsbaas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hsbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
    hsbaasp_dis=hsbaasp[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hsbaasp_dis.to_markdown(index=False))
    
#THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BASEMENT:
def hsba_reg(*args):
    sys.stdout=forget_btns(main_screen)
    txt.delete(1.0, tk.END)
    txt.grid(row=0, column=2, rowspan=5, sticky='nsew')
    btn_clr_hs.grid(row=2, column=0, columnspan=2, sticky='ew')
    hsbaareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Basement"', con)
    btn_hsbaas.grid(row=3, column=0, columnspan=2, sticky='ew')
    btn_hsbaasp.grid(row=4, column=0, columnspan=2, sticky='ew')
    hsbaareg_dis=hsbaareg[['Title', 'House', 'Room']]
    sys.stdout=printtotxt()
    print(hsbaareg_dis.to_markdown(index=False))
###############################################FILL LISTBOX_ROOMS###################################################
#CREATE FUNCTION TO FILL LISTBOX_ROOMS:
class printtotxt(object):
    def write(self, s):
        txt.insert(tk.END, s)
        
#CREATE FUNCTION TO POPULATE LISTBOX 2:
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
            listbox_rooms.delete(0, tk.END)
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
            sys.stdout=forget_btns(main_screen)
            txt.grid_forget()
            listbox_rooms.delete(0, tk.END)
            for room in b_rooms:
                listbox_rooms.insert(tk.END, room)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_b_rooms)
        if idx==4:
            sys.stdout=forget_btns(main_screen)
            txt.grid_forget()
            listbox_rooms.delete(0, tk.END)
            listbox_rooms.insert(tk.END, 'Master Bedroom')
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_lm_rooms)
        if idx==5:
            sys.stdout=forget_btns(main_screen)
            txt.grid_forget()
            listbox_rooms.delete(0, tk.END)
            for room in bm_rooms:
                listbox_rooms.insert(tk.END, room)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_bm_rooms)
        if idx==6:
            sys.stdout=forget_btns(main_screen)
            txt.grid_forget()
            listbox_rooms.delete(0, tk.END)
            for room in h_rooms:
                listbox_rooms.insert(tk.END, room)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_h_rooms)
        if idx==7:
            sys.stdout=forget_btns(main_screen)
            txt.grid_forget()
            listbox_rooms.delete(0, tk.END)
            for room in hs_rooms:
                listbox_rooms.insert(tk.END, room)
            listbox_rooms.bind('<<ListboxSelect>>', fill_table_hs_rooms)
###############################################FILL LISTBOX_ROOMS###################################################
################################################CREATE WIDGETS######################################################
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

#CREATE BUTTONS FOR GOLDENHILLS PLANTATION, BEDROOM:
btn_gpbras=tk.Button(main_screen, text="Skill Books", command=lambda:[gpbr_skill(), btn_gpbras.pack_forget()])
btn_gpbrasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[gpbr_spell(), btn_gpbrasp.grid_forget()])
btn_gpbrareg=tk.Button(main_screen, text="Regular Books", command=lambda:[gpbr_reg(), btn_gpbrareg.grid_forget()])

#CREATE BUTTONS FOR GOLDENHILLS PLANTATION, SHRINE ROOM LEFT:
btn_gpsrlas=tk.Button(main_screen, text="Skill Books", command=lambda:[gpsrl_skill(), btn_gpsrlas.pack_forget()])
btn_gpsrlasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[gpsrl_spell(), btn_gpsrlasp.grid_forget()])
btn_gpsrlareg=tk.Button(main_screen, text="Regular Books", command=lambda:[gpsrl_reg(), btn_gpsrlareg.grid_forget()])

#CREATE BUTTONS FOR GOLDENHILLS PLANTATION, SHRINE ROOM RIGHT:
btn_gpsrras=tk.Button(main_screen, text="Skill Books", command=lambda:[gpsrr_skill(), btn_gpsrras.pack_forget()])
btn_gpsrrasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[gpsrr_spell(), btn_gpsrrasp.grid_forget()])
btn_gpsrrareg=tk.Button(main_screen, text="Regular Books", command=lambda:[gpsrr_reg(), btn_gpsrrareg.grid_forget()])

#CREATE BUTTONS FOR BREEZEHOME, ALL ROOMS:
btn_clr_b=tk.Button(main_screen, text="Clear", command=lambda:[clear_b(), btn_clr_b.grid_forget()])
btn_baras=tk.Button(main_screen, text="Skill Books", command=lambda:[bar_skill(), btn_baras.pack_forget()])
btn_barasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[bar_spell(), btn_barasp.grid_forget()])
btn_barareg=tk.Button(main_screen, text="Regular Books", command=lambda:[bar_reg(), btn_barareg.grid_forget()])

#CREATE BUTTONS FOR BREEZEHOME, LIVING ROOM:
btn_blivas=tk.Button(main_screen, text="Skill Books", command=lambda:[bliv_skill(), btn_blivas.pack_forget()])
btn_blivasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[bliv_spell(), btn_blivasp.grid_forget()])
btn_blivareg=tk.Button(main_screen, text="Regular Books", command=lambda:[bliv_reg(), btn_blivareg.grid_forget()])

#CREATE BUTTONS FOR BREEZEHOME, ALCHEMY LAB:
btn_blabas=tk.Button(main_screen, text="Skill Books", command=lambda:[blab_skill(), btn_blabas.pack_forget()])
btn_blabasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[blab_spell(), btn_blabasp.grid_forget()])
btn_blabareg=tk.Button(main_screen, text="Regular Books", command=lambda:[blab_reg(), btn_blabareg.grid_forget()])

#CREATE BUTTONS FOR LAKEVIEW MANOR, MASTER BEDROOM:
btn_clr_lm=tk.Button(main_screen, text="Clear", command=lambda:[clear_lm(), btn_clr_lm.grid_forget()])
btn_lmas=tk.Button(main_screen, text="Skill Books", command=lambda:[lm_skill(), btn_lmas.grid_forget()])
btn_lmasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[lm_spell(), btn_lmasp.grid_forget()])
btn_lmareg=tk.Button(main_screen, text="Regular Books", command=lambda:[lm_reg(), btn_lmareg.grid_forget()])

#CREATE BUTTONS FOR BLOODCHILL MANOR, ALL ROOMS:
btn_clr_bm=tk.Button(main_screen, text="Clear", command=lambda:[clear_bm(), btn_clr_bm.grid_forget()])
btn_bmaras=tk.Button(main_screen, text="Skill Books", command=lambda:[bmar_skill(), btn_bmaras.grid_forget()])
btn_bmarasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[bmar_spell(), btn_bmarasp.grid_forget()])
btn_bmarareg=tk.Button(main_screen, text="Regular Books", command=lambda:[bmar_reg(), btn_bmarareg.grid_forget()])

#CREATE BUTTONS FOR BLOODCHILL MANOR, MASTER BEDROOM FLOOR 1:
btn_bmmb1as=tk.Button(main_screen, text="Skill Books", command=lambda:[bmmb1_skill(), btn_bmmb1as.pack_forget()])
btn_bmmb1asp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[bmmb1_spell(), btn_bmmb1asp.grid_forget()])
btn_bmmb1areg=tk.Button(main_screen, text="Regular Books", command=lambda:[bmmb1_reg(), btn_bmmb1areg.grid_forget()])

#CREATE BUTTONS FOR BLOODCHILL MANOR, MASTER BEDROOM FLOOR 2:
btn_bmmb2as=tk.Button(main_screen, text="Skill Books", command=lambda:[bmmb2_skill(), btn_bmmb2as.pack_forget()])
btn_bmmb2asp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[bmmb2_spell(), btn_bmmb2asp.grid_forget()])
btn_bmmb2areg=tk.Button(main_screen, text="Regular Books", command=lambda:[bmmb2_reg(), btn_bmmb2areg.grid_forget()])

#CREATE BUTTONS FOR BLOODCHILL MANOR, CHILD ROOM:
btn_bmcras=tk.Button(main_screen, text="Skill Books", command=lambda:[bmcr_skill(), btn_bmcras.pack_forget()])
btn_bmcrasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[bmcr_spell(), btn_bmcrasp.grid_forget()])
btn_bmcrareg=tk.Button(main_screen, text="Regular Books", command=lambda:[bmcr_reg(), btn_bmcrareg.grid_forget()])

#CREATE BUTTONS FOR HENDRAHEIM, ALL ROOMS:
btn_clr_h=tk.Button(main_screen, text="Clear", command=lambda:[clear_h(), btn_clr_h.grid_forget()])
btn_haras=tk.Button(main_screen, text="Skill Books", command=lambda:[har_skill(), btn_haras.pack_forget()])
btn_harasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[har_spell(), btn_harasp.grid_forget()])
btn_harareg=tk.Button(main_screen, text="Regular Books", command=lambda:[har_reg(), btn_harareg.grid_forget()])

#CREATE BUTTONS FOR HENDRAHEIM, BEDROOM LEFT:
btn_hbrlas=tk.Button(main_screen, text="Skill Books", command=lambda:[hbrl_skill(), btn_hbrlas.pack_forget()])
btn_hbrlasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[hbrl_spell(), btn_hbrlasp.grid_forget()])
btn_hbrlareg=tk.Button(main_screen, text="Regular Books", command=lambda:[hbrl_reg(), btn_hbrlareg.grid_forget()])

#CREATE BUTTONS FOR HENDRAHEIM, BEDROOM RIGHT:
btn_hbrras=tk.Button(main_screen, text="Skill Books", command=lambda:[hbrr_skill(), btn_hbrras.pack_forget()])
btn_hbrrasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[hbrr_spell(), btn_hbrrasp.grid_forget()])
btn_hbrrareg=tk.Button(main_screen, text="Regular Books", command=lambda:[hbrr_reg(), btn_hbrrareg.grid_forget()])

#CREATE BUTTONS FOR HENDRAHEIM, DINING AREA:
btn_hdaas=tk.Button(main_screen, text="Skill Books", command=lambda:[hda_skill(), btn_hdaas.pack_forget()])
btn_hdaasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[hda_spell(), btn_hdaasp.grid_forget()])
btn_hdaareg=tk.Button(main_screen, text="Regular Books", command=lambda:[hda_reg(), btn_hdaareg.grid_forget()])

#CREATE BUTTONS FOR HONEYSIDE, ALL ROOMS:
btn_clr_hs=tk.Button(main_screen, text="Clear", command=lambda:[clear_hs(), btn_clr_h.grid_forget()])
btn_hsaras=tk.Button(main_screen, text="Skill Books", command=lambda:[hsar_skill(), btn_hsaras.pack_forget()])
btn_hsarasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[hsar_spell(), btn_hsarasp.grid_forget()])
btn_hsarareg=tk.Button(main_screen, text="Regular Books", command=lambda:[hsar_reg(), btn_hsarareg.grid_forget()])

#CREATE BUTTONS FOR HONEYSIDE, BEDROOM:
btn_hsbras=tk.Button(main_screen, text="Skill Books", command=lambda:[hsbr_skill(), btn_hsbras.pack_forget()])
btn_hsbrasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[hsbr_spell(), btn_hsbrasp.grid_forget()])
btn_hsbrareg=tk.Button(main_screen, text="Regular Books", command=lambda:[hsbr_reg(), btn_hsbrareg.grid_forget()])

#CREATE BUTTONS FOR HONEYSIDE, BASEMENT:
btn_hsbaas=tk.Button(main_screen, text="Skill Books", command=lambda:[hsba_skill(), btn_hsbaas.pack_forget()])
btn_hsbaasp=tk.Button(main_screen, text="Spell Tomes", command=lambda:[hsba_spell(), btn_hsbaasp.grid_forget()])
btn_hsbaareg=tk.Button(main_screen, text="Regular Books", command=lambda:[hsba_reg(), btn_hsbaareg.grid_forget()])

#CREATE LABEL AND SEARCH BAR WIDGET:
lbl_search=tk.Label(main_screen, text="Search for Title")
lbl_search.grid(row=5, column=0, columnspan=2, sticky='ew')
searchstring = tk.StringVar()
searchbar=tk.Entry(main_screen, textvariable=searchstring)

searchstring.trace('w', search
searchbar.grid(row=5, column=2, sticky='news')
searchbar.bind('<<return>>', search)
#################################################CREATE WIDGETS#####################################################
##################################################RUN PROGRAM#######################################################
#LAUNCH DATABASE:
main_screen.mainloop()

#CLOSE DATABASE CONNECTION:
con.close()
##################################################RUN PROGRAM#######################################################
