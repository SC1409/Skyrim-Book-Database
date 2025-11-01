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
        self.forget_btns()
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
        self.txt=tk.Text(self.frame, width=120)
        self.txt.grid(row=0, column=2, rowspan=5, columnspan=2, sticky='news')
        #CREATE SEARCH BAR AND BUTTON WIDGET:
        self.searchstring = tk.StringVar()
        self.searchbar=tk.Entry(self.frame, textvariable=self.searchstring)
        self.searchbar.grid(row=5, column=2, columnspan=2, sticky='news')
        self.searchbar.bind('<Return>', self.search)
        self.btn_search=tk.Button(self.frame, text='Search', command=self.search)
        self.btn_search.grid(row=5, column=3, sticky='e')
        #CREATE BUTTONS FOR ALL HOUSES SCREEN:
        self.btn_clr_ah=tk.Button(self.frame, text="Clear", command=lambda:[self.clear_ah(), self.btn_clr_ah.grid_forget()])
        self.btn_ahas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.all_house_skill(), self.btn_ahas.grid_forget()])
        self.btn_ahasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.all_house_spell(), self.btn_ahasp.grid_forget()])
        self.btn_ahareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.all_house_reg(), self.btn_ahareg.grid_forget()])
        #CREATE BUTTONS FOR TUNDRA HOMESTEAD, ALL ROOMS:
        self.btn_clr_th=tk.Button(self.frame, text="Clear", command=lambda:[self.clear_th(), self.btn_clr_th.grid_forget()])
        self.btn_tharas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.thar_skill(), self.btn_tharas.pack_forget()])
        self.btn_tharasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.thar_spell(), self.btn_tharasp.grid_forget()])
        self.btn_tharareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.thar_reg(), self.btn_tharareg.grid_forget()])
        #CREATE BUTTONS FOR TUNDRA HOMESTEAD, BEDROOM:
        self.btn_thbras=tk.Button(self.frame, text="Skill Books", command=lambda:[self.thbr_skill(), self.btn_thbras.pack_forget()])
        self.btn_thbrasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.thbr_spell(), self.btn_thbrasp.grid_forget()])
        self.btn_thbrareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.thbr_reg(), self.btn_thbrareg.grid_forget()])
        #CREATE BUTTONS FOR TUNDRA HOMESTEAD, BASEMENT:
        self.btn_thbaas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.thba_skill(), self.btn_thbaas.pack_forget()])
        self.btn_thbaasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.thba_spell(), self.btn_thbaasp.grid_forget()])
        self.btn_thbaareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.thba_reg(), self.btn_thbaareg.grid_forget()])
        #CREATE BUTTONS FOR GOLDENHILLS PLANTATION, ALL ROOMS:
        self.btn_clr_gp=tk.Button(self.frame, text="Clear", command=lambda:[self.clear_gp(), self.btn_clr_gp.grid_forget()])
        self.btn_gparas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.gpar_skill(), self.btn_gparas.pack_forget()])
        self.btn_gparasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.gpar_spell(), self.btn_gparasp.grid_forget()])
        self.btn_gparareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.gpar_reg(), self.btn_gparareg.grid_forget()])
        #CREATE BUTTONS FOR GOLDENHILLS PLANTATION, BEDROOM:
        self.btn_gpbras=tk.Button(self.frame, text="Skill Books", command=lambda:[self.gpbr_skill(), self.btn_gpbras.pack_forget()])
        self.btn_gpbrasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.gpbr_spell(), self.btn_gpbrasp.grid_forget()])
        self.btn_gpbrareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.gpbr_reg(), self.btn_gpbrareg.grid_forget()])
        #CREATE BUTTONS FOR GOLDENHILLS PLANTATION, SHRINE ROOM LEFT:
        self.btn_gpsrlas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.gpsrl_skill(), self.btn_gpsrlas.pack_forget()])
        self.btn_gpsrlasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.gpsrl_spell(), self.btn_gpsrlasp.grid_forget()])
        self.btn_gpsrlareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.gpsrl_reg(), self.btn_gpsrlareg.grid_forget()])
        #CREATE BUTTONS FOR GOLDENHILLS PLANTATION, SHRINE ROOM RIGHT:
        self.btn_gpsrras=tk.Button(self.frame, text="Skill Books", command=lambda:[self.gpsrr_skill(), self.btn_gpsrras.pack_forget()])
        self.btn_gpsrrasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.gpsrr_spell(), self.btn_gpsrrasp.grid_forget()])
        self.btn_gpsrrareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.gpsrr_reg(), self.btn_gpsrrareg.grid_forget()])
    #CREATE SEARCH FUNCTION:
    def search(self, *event):
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        all_books=pd.read_sql_query('SELECT * FROM "My Books"', con)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        result=all_books.loc[all_books['Title'].str.contains(self.searchstring.get(), na=False, case=False)]
        result_dis=result[['Title', 'House', 'Room', 'Skill Book', 'Spell Tome']]
        self.txt.insert(tk.END, result_dis.to_markdown(index=False))
    #CREATE FUNCTION TO DELETE ALL BUTTONS:
    def forget_btns(self):
        lst=self.frame.winfo_children()
        for item in lst:
            if isinstance(item, tk.Button):
                item.grid_forget()
    #CREATE FUNCTION TO FILL LISTBOX_ROOMS:
    def fill_listbox_rooms(self, *args):
        self.forget_btns()
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.listbox_rooms.delete(0, tk.END)
        self.txt.delete(1.0, tk.END)
        idxs=self.listbox_houses.curselection()
        if len(idxs)==1:
            idx=int(idxs[0])
            if idx==0:
                self.forget_btns()
                self.btn_search.grid(row=5, column=3, sticky='e')
                self.txt.delete(1.0, tk.END)
                self.listbox_rooms.delete(0, tk.END)
                self.listbox_rooms.insert(tk.END, 'All Rooms')
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_all_rooms)
            if idx==1:
                self.forget_btns()
                self.btn_search.grid(row=5, column=3, sticky='e')
                self.txt.delete(1.0, tk.END)
                self.listbox_rooms.delete(0, tk.END)
                for room in th_rooms:
                    self.listbox_rooms.insert(tk.END, room)
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_th_rooms)
            if idx==2:
                self.forget_btns()
                self.btn_search.grid(row=5, column=3, sticky='e')
                self.txt.delete(1.0, tk.END)
                self.listbox_rooms.delete(0, tk.END)
                for room in gp_rooms:
                    self.listbox_rooms.insert(tk.END, room)
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_gp_rooms)
#############################################CREATE FUNCTIONS FOR ALL HOUSES########################################  
    #CREATE FUNCTION TO FILL TXT WITH TABLE FOR ALL ROOMS IN ALL HOUSES:
    def fill_table_all_rooms(self, *args):         
        self.forget_btns()
        self.btn_search.grid(row=5, column=3, sticky='e')
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=5, column=3, sticky='e')
                self.btn_ahas.grid(row=2, column=0, columnspan=2, sticky='ew')
                self.btn_ahasp.grid(row=3, column=0, columnspan=2, sticky='ew')
                self.btn_ahareg.grid(row=4, column=0, columnspan=2, sticky='ew')
                all_h=pd.read_sql_query('SELECT * FROM "My Books"', con)
                pd.set_option('display.max_rows', None)
                all_h_dis=all_h[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, all_h_dis.to_markdown(index=False))
    #THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM IN ALL HOUSES:
    def clear_ah(self, *args):
        self.fill_table_all_rooms()
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL HOUSES:
    def all_house_skill(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_ah.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_ahasp.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_ahareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        all_h_skill=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Skill Book" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        all_h_skill_dis=all_h_skill[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, all_h_skill_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL HOUSES:
    def all_house_spell(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_ah.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_ahas.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_ahareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        all_h_spell=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Spell Tome" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        all_h_spell_dis=all_h_spell[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, all_h_spell_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL HOUSES:
    def all_house_reg(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_ah.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_ahas.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_ahasp.grid(row=4, column=0, columnspan=2, sticky='ew')
        all_h_reg=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Spell Tome" = "No" AND "Skill Book" = "No"', con)
        pd.set_option('display.max_rows', None)
        all_h_reg_dis=all_h_reg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, all_h_reg_dis.to_markdown(index=False))
###########################################CREATE FUNCTIONS FOR TUNDRA HOMESTEAD#####################################
    #CREATE FUNCTION TO FILL TXT WITH TABLE FOR ALL ROOMS IN TUNDRA HOMESTEAD:
    def fill_table_th_rooms(self, *args):            
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=5, column=3, sticky='e')
                self.btn_tharas.grid(row=2, column=0, columnspan=2, sticky='ew')
                self.btn_tharasp.grid(row=3, column=0, columnspan=2, sticky='ew')
                self.btn_tharareg.grid(row=4, column=0, columnspan=2, sticky='ew')
                thar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead"', con)
                thar_dis=thar[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, thar_dis.to_markdown(index=False))
            if idx_room==1:
                self.forget_btns()
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=5, column=3, sticky='e')
                thbr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND Room = "Bedroom"', con)
                self.btn_thbras.grid(row=2, column=0, columnspan=2, sticky='ew')
                self.btn_thbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
                self.btn_thbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
                pd.set_option('display.max_rows', None)
                thbr_dis=thbr[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, thbr_dis.to_markdown(index=False))
            if idx_room==2:
                self.forget_btns()
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=5, column=3, sticky='e')
                self.btn_thbaas.grid(row=2, column=0, columnspan=2, sticky='ew')
                self.btn_thbaasp.grid(row=3, column=0, columnspan=2, sticky='ew')
                self.btn_thbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
                thba=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND Room = "Basement"', con)
                thba_dis=thba[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, thba_dis.to_markdown(index=False))
    #THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM IN TUNDRA HOMESTEAD:
    def clear_th(self, *args):
        self.fill_table_th_rooms()
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN TUNDRA HOMESTEAD:
    def thar_skill(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_tharasp.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_tharareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        tharas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        tharas_dis=tharas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, tharas_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN TUNDRA HOMESTEAD:
    def thar_spell(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_tharas.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_tharareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        tharasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        tharasp_dis=tharasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, tharasp_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN TUNDRA HOMESTEAD:
    def thar_reg(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_tharas.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_tharasp.grid(row=4, column=0, columnspan=2, sticky='ew')
        tharareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
        pd.set_option('display.max_rows', None)
        tharareg_dis=tharareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, tharareg_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM IN TUNDRA HOMESTEAD:
    def thbr_skill(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_thbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_thbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        thbras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        thbras_dis=thbras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbras_dis.to_markdown(index=False))    
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM IN TUNDRA HOMESTEAD:
    def thbr_spell(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_thbras.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_thbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        thbrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        thbrasp_dis=thbrasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbrasp_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM IN TUNDRA HOMESTEAD:
    def thbr_reg(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_thbras.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_thbrasp.grid(row=4, column=0, columnspan=2, sticky='ew')
        thbrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        thbrareg_dis=thbrareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbrareg_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BASEMENT IN TUNDRA HOMESTEAD:
    def thba_skill(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_thbaasp.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_thbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        thbaas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes" AND Room = "Basement"', con)
        pd.set_option('display.max_rows', None)
        thbaas_dis=thbaas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbaas_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BASEMENT IN TUNDRA HOMESTEAD:
    def thba_spell(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_thbaas.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_thbaareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        thbaasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes" AND Room = "Basement"', con)
        pd.set_option('display.max_rows', None)
        thbaasp_dis=thbaasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbaasp_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BASEMENT IN TUNDRA HOMESTEAD:
    def thba_reg(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_th.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_thbaas.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_thbaasp.grid(row=4, column=0, columnspan=2, sticky='ew')
        thbaareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Basement"', con)
        pd.set_option('display.max_rows', None)
        thbaareg_dis=thbaareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbaareg_dis.to_markdown(index=False))
###########################################CREATE FUNCTIONS FOR GOLDENHILLS PLANTATION#####################################       
    #CREATE FUNCTION TO FILL TXT WITH TABLE FOR ALL ROOMS IN GOLDENHILLS PLANTATION:    
    def fill_table_gp_rooms(self, *args):           
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=5, column=3, sticky='e')
                self.btn_gparas.grid(row=2, column=0, columnspan=2, sticky='ew')
                self.btn_gparasp.grid(row=3, column=0, columnspan=2, sticky='ew')
                self.btn_gparareg.grid(row=4, column=0, columnspan=2, sticky='ew')
                gpar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation"', con)
                pd.set_option('display.max_rows', None)
                gpar_dis=gpar[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, gpar_dis.to_markdown(index=False))
            if idx_room==1:
                self.forget_btns()
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=5, column=3, sticky='e')
                self.btn_gpbras.grid(row=2, column=0, columnspan=2, sticky='ew')
                self.btn_gpbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
                self.btn_gpbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
                gpbr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND Room = "Bedroom"', con)
                pd.set_option('display.max_rows', None)
                gpbr_dis=gpbr[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, gpbr_dis.to_markdown(index=False))
            if idx_room==2:
                self.forget_btns()
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=5, column=3, sticky='e')
                self.btn_gpsrlas.grid(row=2, column=0, columnspan=2, sticky='ew')
                self.btn_gpsrlasp.grid(row=3, column=0, columnspan=2, sticky='ew')
                self.btn_gpsrlareg.grid(row=4, column=0, columnspan=2, sticky='ew')
                gpsrl=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND Room = "Shrine Room (Left)"', con)
                pd.set_option('display.max_rows', None)
                gpsrl_dis=gpsrl[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, gpsrl_dis.to_markdown(index=False))
            if idx_room==3:
                self.forget_btns()
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=5, column=3, sticky='e')
                self.btn_gpsrras.grid(row=2, column=0, columnspan=2, sticky='ew')
                self.btn_gpsrrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
                self.btn_gpsrrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
                gpsrr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND Room = "Shrine Room (Right)"', con)
                pd.set_option('display.max_rows', None)
                gpsrr_dis=gpsrr[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, gpsrr_dis.to_markdown(index=False))
    #THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM IN GOLDENHILLS PLANTATION:
    def clear_gp(self, *args):
        self.fill_table_gp_rooms()
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN GOLDENHILLS PLANTATION:
    def gpar_skill(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gparasp.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gparareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        gparas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        gparas_dis=gparas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gparas_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN GOLDENHILLS PLANTATION:
    def gpar_spell(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gparas.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gparareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        gparasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        gparasp_dis=gparasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gparasp_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN GOLDENHILLS PLANTATION:
    def gpar_reg(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gparas.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gparasp.grid(row=4, column=0, columnspan=2, sticky='ew')
        gparareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
        pd.set_option('display.max_rows', None)
        gparareg_dis=gparareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gparareg_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM IN GOLDENHILLS PLANTATION:
    def gpbr_skill(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gpbrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gpbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        gpbras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        gpbras_dis=gpbras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpbras_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM IN GOLDENHILLS PLANTATION:
    def gpbr_spell(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gpbras.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gpbrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        gpbrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        gpbrasp_dis=gpbrasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpbrasp_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM IN GOLDENHILLS PLANTATION:
    def gpbr_reg(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gpbras.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gpbrasp.grid(row=4, column=0, columnspan=2, sticky='ew')
        gpbrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        gpbrareg_dis=gpbrareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpbrareg_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN SHRINE ROOM LEFT IN GOLDENHILLS PLANTATION:
    def gpsrl_skill(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrlasp.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrlareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        gpsrlas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes" AND Room = "Shrine Room (Left)"', con)
        pd.set_option('display.max_rows', None)
        gpsrlas_dis=gpsrlas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrlas_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN SHRINE ROOM LEFT IN GOLDENHILLS PLANTATION:
    def gpsrl_spell(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrlas.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrlareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        gpsrlasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes" AND Room = "Shrine Room (Left)"', con)
        pd.set_option('display.max_rows', None)
        gpsrlasp_dis=gpsrlasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrlasp_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN SHRINE ROOM LEFT IN GOLDENHILLS PLANTATION:
    def gpsrl_reg(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrlas.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrlasp.grid(row=4, column=0, columnspan=2, sticky='ew')
        gpsrlareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Shrine Room (Left)"', con)
        pd.set_option('display.max_rows', None)
        gpsrlareg_dis=gpsrlareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrlareg_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN SHRINE ROOM RIGHT IN GOLDENHILLS PLANTATION:
    def gpsrr_skill(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrrasp.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        gpsrras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes" AND Room = "Shrine Room (Right)"', con)
        pd.set_option('display.max_rows', None)
        gpsrras_dis=gpsrras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrras_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN SHRINE ROOM RIGHT IN GOLDENHILLS PLANTATION:
    def gpsrr_spell(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrras.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrrareg.grid(row=4, column=0, columnspan=2, sticky='ew')
        gpsrrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes" AND Room = "Shrine Room (Right)"', con)
        pd.set_option('display.max_rows', None)
        gpsrrasp_dis=gpsrrasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrrasp_dis.to_markdown(index=False))
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN SHRINE ROOM RIGHT IN GOLDENHILLS PLANTATION:
    def gpsrr_reg(self, *args):
        self.forget_btns()
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=5, column=3, sticky='e')
        self.btn_clr_gp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrras.grid(row=3, column=0, columnspan=2, sticky='ew')
        self.btn_gpsrrasp.grid(row=4, column=0, columnspan=2, sticky='ew')
        gpsrrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Shrine Room (Right)"', con)
        pd.set_option('display.max_rows', None)
        gpsrrareg_dis=gpsrrareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrrareg_dis.to_markdown(index=False))
#############################################CREATE FUNCTIONS FOR BREEZEHOME########################################

##########################################CREATE FUNCTIONS FOR LAKEVIEW MANOR#######################################
#LAUNCH DATABASE:
if __name__ == '__main__':
    mm()

#CLOSE DATABASE CONNECTION:
con.close()
