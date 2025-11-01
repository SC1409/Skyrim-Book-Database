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
houses = ['All Houses', 'Tundra Homestead', 'Goldenhills Plantation', 'Breezehome', 'Lakeview Manor', 'Bloodchill Manor', 'Hendraheim', 'Honeyside']
all_rooms = ['All Rooms']
th_rooms = ['All Rooms', 'Bedroom', 'Basement']
gp_rooms = ['All Rooms', 'Bedroom', 'Shrine Room (Left)', 'Shrine Room (Right)']
b_rooms = ['All Rooms', 'Living Room', 'Alchemy Laboratory']
lm_rooms = ['Master Bedroom']
bm_rooms = ['All Rooms', 'Master Bedroom (Floor 1)', 'Master Bedroom (Floor 2)', 'Child Room']
h_rooms = ['All Rooms', 'Bedroom (Left)', 'Bedroom (Right)', 'Dining Area']
hs_rooms = ['All Rooms', 'Bedroom', 'Basement']
list_binary_skill = ('Yes', 'No')
list_binary_spell = ('Yes', 'No')
houses_addbook = ['Tundra Homestead', 'Goldenhills Plantation', 'Breezehome', 'Lakeview Manor', 'Bloodchill Manor', 'Hendraheim', 'Honeyside']
th_rooms_addbook = ['Bedroom', 'Basement']
gp_rooms_addbook = ['Bedroom', 'Shrine Room (Left)', 'Shrine Room (Right)']
b_rooms_addbook = ['Living Room', 'Alchemy Laboratory']
lm_rooms_addbook = ['Master Bedroom']
bm_rooms_addbook = ['Master Bedroom (Floor 1)', 'Master Bedroom (Floor 2)', 'Child Room']
h_rooms_addbook = ['Bedroom (Left)', 'Bedroom (Right)', 'Dining Area']
hs_rooms_addbook = ['Bedroom', 'Basement']

#CREATE LAUNCH FUNCTION:
def mm():
    root=tk.Tk()
    root.title('Skyrim Books')
    app=main_win(root)
    root.mainloop()

#CREATE MAIN WINDOW:
class main_win:
    def __init__(self, master):
        self.master=master
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.frame=tk.Frame(self.master)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)
        self.frame.rowconfigure(5, weight=1)
        self.frame.rowconfigure(6, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.grid(row=0, column=0, sticky='news')
        Houses = tk.StringVar(self.frame, value=houses)
        self.forget_btns()
        self.men_txt=tk.Menu(self.frame, tearoff=0)
        self.men_txt.add_command(label='Copy')
        self.men_txt.entryconfigure('Copy', command=self.txt_c2c)
        self.men_search=tk.Menu(self.frame, tearoff=0)
        self.men_search.add_command(label='Copy')
        self.men_search.add_command(label='Paste')
        self.men_search.entryconfigure('Copy', command=self.search_c2c)
        self.men_search.entryconfigure('Paste', command=self.search_pfc)
        self.menubar=tk.Menu(self.master)
        self.menubar_settings=tk.Menu(self.menubar, tearoff=0)
        self.menubar_settings.add_command(label='Add House', command=self.open_addhouse)
        self.menubar.add_cascade(label='Settings', menu=self.menubar_settings)
        self.master.config(menu=self.menubar)
        #CREATE HOUSE'S LISTBOX AND LABEL:
        self.lbl_houses=tk.Label(self.frame, text='Select House:')
        self.lbl_houses.grid(row=1, column=0, sticky='ew')
        self.listbox_houses=tk.Listbox(self.frame, listvariable=Houses, bg='white', font='Ariel', fg='black', exportselection=False)
        self.listbox_houses.grid(row=2, column=0, sticky='ew')
        self.listbox_houses.bind('<<ListboxSelect>>', self.fill_listbox_rooms)
        #CREATE ROOM'S LISTBOX AND LABEL:
        self.lbl_rooms=tk.Label(self.frame, text='Select Room:')
        self.lbl_rooms.grid(row=1, column=1, sticky='ew')
        self.listbox_rooms=tk.Listbox(self.frame, bg='white', font='Ariel', fg='black', exportselection=False)
        self.listbox_rooms.grid(row=2, column=1, sticky='ew')
        #CREATE TEXTBOX FOR TABLES:
        self.txt=tk.Text(self.frame, width=125, state=tk.DISABLED)
        self.txt.grid(row=1, column=2, rowspan=5, columnspan=2, sticky='news')
        self.txt.bind('<Key>', lambda e: "break")
        self.txt.bind('<Button-3>', self.txt_do_popup)
        #CREATE SEARCH BAR AND BUTTON WIDGET:
        self.searchstring = tk.StringVar()
        self.searchbar=tk.Entry(self.frame, textvariable=self.searchstring)
        self.searchbar.grid(row=6, column=2, columnspan=2, sticky='news')
        self.searchbar.bind('<Return>', self.search)
        self.searchbar.bind('<Button-3>', self.search_do_popup)
        self.btn_search=tk.Button(self.frame, text='Search', command=self.search)
        self.btn_search.grid(row=6, column=3, sticky='nes')
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
        #CREATE BUTTONS FOR BREEZEHOME, ALL ROOMS:
        self.btn_clr_b=tk.Button(self.frame, text="Clear", command=lambda:[self.clear_b(), self.btn_clr_b.grid_forget()])
        self.btn_baras=tk.Button(self.frame, text="Skill Books", command=lambda:[self.bar_skill(), self.btn_baras.pack_forget()])
        self.btn_barasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.bar_spell(), self.btn_barasp.grid_forget()])
        self.btn_barareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.bar_reg(), self.btn_barareg.grid_forget()])
        #CREATE BUTTONS FOR BREEZEHOME, LIVING ROOM:
        self.btn_blivas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.bliv_skill(), self.btn_blivas.pack_forget()])
        self.btn_blivasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.bliv_spell(), self.btn_blivasp.grid_forget()])
        self.btn_blivareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.bliv_reg(), self.btn_blivareg.grid_forget()])
        #CREATE BUTTONS FOR BREEZEHOME, ALCHEMY LAB:
        self.btn_blabas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.blab_skill(), self.btn_blabas.pack_forget()])
        self.btn_blabasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.blab_spell(), self.btn_blabasp.grid_forget()])
        self.btn_blabareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.blab_reg(), self.btn_blabareg.grid_forget()])
        #CREATE BUTTONS FOR LAKEVIEW MANOR, MASTER BEDROOM:
        self.btn_clr_lm=tk.Button(self.frame, text="Clear", command=lambda:[self.clear_lm(), self.btn_clr_lm.grid_forget()])
        self.btn_lmas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.lm_skill(), self.btn_lmas.grid_forget()])
        self.btn_lmasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.lm_spell(), self.btn_lmasp.grid_forget()])
        self.btn_lmareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.lm_reg(), self.btn_lmareg.grid_forget()])
        #CREATE BUTTONS FOR BLOODCHILL MANOR, ALL ROOMS:
        self.btn_clr_bm=tk.Button(self.frame, text="Clear", command=lambda:[self.clear_bm(), self.btn_clr_bm.grid_forget()])
        self.btn_bmaras=tk.Button(self.frame, text="Skill Books", command=lambda:[self.bmar_skill(), self.btn_bmaras.grid_forget()])
        self.btn_bmarasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.bmar_spell(), self.btn_bmarasp.grid_forget()])
        self.btn_bmarareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.bmar_reg(), self.btn_bmarareg.grid_forget()])
        #CREATE BUTTONS FOR BLOODCHILL MANOR, MASTER BEDROOM FLOOR 1:
        self.btn_bmmb1as=tk.Button(self.frame, text="Skill Books", command=lambda:[self.bmmb1_skill(), self.btn_bmmb1as.pack_forget()])
        self.btn_bmmb1asp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.bmmb1_spell(), self.btn_bmmb1asp.grid_forget()])
        self.btn_bmmb1areg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.bmmb1_reg(), self.btn_bmmb1areg.grid_forget()])
        #CREATE BUTTONS FOR BLOODCHILL MANOR, MASTER BEDROOM FLOOR 2:
        self.btn_bmmb2as=tk.Button(self.frame, text="Skill Books", command=lambda:[self.bmmb2_skill(), self.btn_bmmb2as.pack_forget()])
        self.btn_bmmb2asp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.bmmb2_spell(), self.btn_bmmb2asp.grid_forget()])
        self.btn_bmmb2areg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.bmmb2_reg(), self.btn_bmmb2areg.grid_forget()])
        #CREATE BUTTONS FOR BLOODCHILL MANOR, CHILD ROOM:
        self.btn_bmcras=tk.Button(self.frame, text="Skill Books", command=lambda:[self.bmcr_skill(), self.btn_bmcras.pack_forget()])
        self.btn_bmcrasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.bmcr_spell(), self.btn_bmcrasp.grid_forget()])
        self.btn_bmcrareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.bmcr_reg(), self.btn_bmcrareg.grid_forget()])
        #CREATE BUTTONS FOR HENDRAHEIM, ALL ROOMS:
        self.btn_clr_h=tk.Button(self.frame, text="Clear", command=lambda:[self.clear_h(), self.btn_clr_h.grid_forget()])
        self.btn_haras=tk.Button(self.frame, text="Skill Books", command=lambda:[self.har_skill(), self.btn_haras.pack_forget()])
        self.btn_harasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.har_spell(), self.btn_harasp.grid_forget()])
        self.btn_harareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.har_reg(), self.btn_harareg.grid_forget()])
        #CREATE BUTTONS FOR HENDRAHEIM, BEDROOM LEFT:
        self.btn_hbrlas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.hbrl_skill(), self.btn_hbrlas.pack_forget()])
        self.btn_hbrlasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.hbrl_spell(), self.btn_hbrlasp.grid_forget()])
        self.btn_hbrlareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.hbrl_reg(), self.btn_hbrlareg.grid_forget()])
        #CREATE BUTTONS FOR HENDRAHEIM, BEDROOM RIGHT:
        self.btn_hbrras=tk.Button(self.frame, text="Skill Books", command=lambda:[self.hbrr_skill(), self.btn_hbrras.pack_forget()])
        self.btn_hbrrasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.hbrr_spell(), self.btn_hbrrasp.grid_forget()])
        self.btn_hbrrareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.hbrr_reg(), self.btn_hbrrareg.grid_forget()])
        #CREATE BUTTONS FOR HENDRAHEIM, DINING AREA:
        self.btn_hdaas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.hda_skill(), self.btn_hdaas.pack_forget()])
        self.btn_hdaasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.hda_spell(), self.btn_hdaasp.grid_forget()])
        self.btn_hdaareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.hda_reg(), self.btn_hdaareg.grid_forget()])
        #CREATE BUTTONS FOR HONEYSIDE, ALL ROOMS:
        self.btn_clr_hs=tk.Button(self.frame, text="Clear", command=lambda:[self.clear_hs(), self.btn_clr_h.grid_forget()])
        self.btn_hsaras=tk.Button(self.frame, text="Skill Books", command=lambda:[self.hsar_skill(), self.btn_hsaras.pack_forget()])
        self.btn_hsarasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.hsar_spell(), self.btn_hsarasp.grid_forget()])
        self.btn_hsarareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.hsar_reg(), self.btn_hsarareg.grid_forget()])
        #CREATE BUTTONS FOR HONEYSIDE, BEDROOM:
        self.btn_hsbras=tk.Button(self.frame, text="Skill Books", command=lambda:[self.hsbr_skill(), self.btn_hsbras.pack_forget()])
        self.btn_hsbrasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.hsbr_spell(), self.btn_hsbrasp.grid_forget()])
        self.btn_hsbrareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.hsbr_reg(), self.btn_hsbrareg.grid_forget()])
        #CREATE BUTTONS FOR HONEYSIDE, BASEMENT:
        self.btn_hsbaas=tk.Button(self.frame, text="Skill Books", command=lambda:[self.hsba_skill(), self.btn_hsbaas.pack_forget()])
        self.btn_hsbaasp=tk.Button(self.frame, text="Spell Tomes", command=lambda:[self.hsba_spell(), self.btn_hsbaasp.grid_forget()])
        self.btn_hsbaareg=tk.Button(self.frame, text="Regular Books", command=lambda:[self.hsba_reg(), self.btn_hsbaareg.grid_forget()])
        #CREATE BUTTON TO OPEN 'ADD BOOK' WINDOW:
        self.btn_open_addbook=tk.Button(self.frame, text='Add Book', command=self.open_addbook)
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        #CREATE BUTTON TO OPEN 'MOVE BOOK' WINDOW:
        self.btn_open_movebook=tk.Button(self.frame, text='Move Book', command=self.open_movebook)
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        #CREATE BUTTON TO OPEN 'DELETE BOOK' WINDOW:
        self.btn_open_delbook=tk.Button(self.frame, text='Delete Book', command=self.open_delbook)
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')

    def txt_do_popup(self, event):
        try:
            self.men_txt.tk_popup(event.x_root, event.y_root)
        finally:
            self.men_txt.grab_release()

    def search_do_popup(self, event):
        try:
            self.men_search.tk_popup(event.x_root, event.y_root)
        finally:
            self.men_search.grab_release()

    def txt_c2c(self, *args):
        try:
            selected_txt = self.txt.selection_get()         
            self.master.clipboard_clear()
            self.master.clipboard_append(selected_txt)
        except tk.TclError:
            return

    def search_c2c(self, *args):
        try:
            selected_txt = self.searchbar.selection_get()
            self.master.clipboard_clear()
            self.master.clipboard_append(selected_txt)
            self.master.update()
        except tk.TclError:
            return
        
    def search_pfc(self, *args):
        try:
            content=self.master.clipboard_get()
            self.searchbar.insert(tk.END, content)
        except tk.TclError:
            return

    def txt_activate(self, *args):
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        
    #CREATE SEARCH FUNCTION:
    def search(self, *event):
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        all_books=pd.read_sql_query('SELECT * FROM "My Books"', con)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        result=all_books.loc[all_books['Title'].str.contains(self.searchstring.get(), na=False, case=False)]
        result_dis=result[['Title', 'House', 'Room', 'Skill Book', 'Spell Tome']]
        self.txt.insert(tk.END, result_dis.to_markdown(index=False))
        result_dis_sort=result_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, result_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, result_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)

    #CREATE FUNCTION TO DELETE ALL BUTTONS:
    def forget_btns(self):
        lst=self.frame.winfo_children()
        for item in lst:
            if isinstance(item, tk.Button):
                item.grid_forget()
                
    #CREATE FUNCTION TO OPEN 'ADD BOOK' WINDOW:
    def open_addbook(self):
        self.newWindow=tk.Toplevel(self.master)
        self.app=addbook_win(self.newWindow)

    #CREATE FUNCTION TO OPEN 'MOVE BOOK' WINDOW:
    def open_movebook(self):
        self.newWindow=tk.Toplevel(self.master)
        self.app=movebook_win(self.newWindow)

    #CREATE FUNCTION TO OPEN 'DELETE BOOK' WINDOW:
    def open_delbook(self):
        self.newWindow=tk.Toplevel(self.master)
        self.app=delbook_win(self.newWindow)

    #CREATE FUNCTION TO OPEN 'ADD HOUSE' WINDOW:
    def open_addhouse(self):
        self.newWindow=tk.Toplevel(self.master)
        self.app=self.addhouse_win(self.newWindow)
        
    #CREATE FUNCTION TO FILL LISTBOX_ROOMS:
    def fill_listbox_rooms(self, *args):
        self.forget_btns()
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.listbox_rooms.delete(0, tk.END)
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.txt.config(state=tk.DISABLED)
        idxs=self.listbox_houses.curselection()
        if len(idxs)==1:
            idx=int(idxs[0])
            if idx==0:
                self.forget_btns()
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.listbox_rooms.insert(tk.END, 'All Rooms')
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_all_rooms)
            if idx==1:
                self.forget_btns()
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                for room in th_rooms:
                    self.listbox_rooms.insert(tk.END, room)
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_th_rooms)
            if idx==2:
                self.forget_btns()
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                for room in gp_rooms:
                    self.listbox_rooms.insert(tk.END, room)
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_gp_rooms)
            if idx==3:
                self.forget_btns()
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                for room in b_rooms:
                    self.listbox_rooms.insert(tk.END, room)
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_b_rooms)
            if idx==4:
                self.forget_btns()
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.listbox_rooms.insert(tk.END, 'Master Bedroom')
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_lm_rooms)
            if idx==5:
                self.forget_btns()
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                for room in bm_rooms:
                    self.listbox_rooms.insert(tk.END, room)
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_bm_rooms)
            if idx==6:
                self.forget_btns()
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                for room in h_rooms:
                    self.listbox_rooms.insert(tk.END, room)
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_h_rooms)
            if idx==7:
                self.forget_btns()
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                for room in hs_rooms:
                    self.listbox_rooms.insert(tk.END, room)
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_hs_rooms)
                
#############################################CREATE FUNCTIONS FOR ALL HOUSES########################################  
    #CREATE FUNCTION TO FILL TXT WITH TABLE FOR ALL ROOMS IN ALL HOUSES:
    def fill_table_all_rooms(self, *args):         
        self.forget_btns()
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_ahas.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_ahasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_ahareg.grid(row=5, column=0, columnspan=2, sticky='news')
                all_h=pd.read_sql_query('SELECT * FROM "My Books"', con)
                pd.set_option('display.max_rows', None)
                all_h_dis=all_h[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, all_h_dis.to_markdown(index=False))
                all_h_dis_sort=all_h_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, all_h_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, all_h_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
                
    #THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM IN ALL HOUSES:
    def clear_ah(self, *args):
        self.fill_table_all_rooms()

    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL HOUSES:
    def all_house_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_ah.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_ahasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_ahareg.grid(row=5, column=0, columnspan=2, sticky='news')
        all_h_skill=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Skill Book" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        all_h_skill_dis=all_h_skill[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, all_h_skill_dis.to_markdown(index=False))
        all_h_skill_dis_sort=all_h_skill_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, all_h_skill_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, all_h_skill_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL HOUSES:
    def all_house_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_ah.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_ahas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_ahareg.grid(row=5, column=0, columnspan=2, sticky='news')
        all_h_spell=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Spell Tome" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        all_h_spell_dis=all_h_spell[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, all_h_spell_dis.to_markdown(index=False))
        all_h_spell_dis_sort=all_h_spell_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, all_h_spell_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, all_h_spell_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL HOUSES:
    def all_house_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_ah.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_ahas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_ahasp.grid(row=5, column=0, columnspan=2, sticky='news')
        all_h_reg=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Spell Tome" = "No" AND "Skill Book" = "No"', con)
        pd.set_option('display.max_rows', None)
        all_h_reg_dis=all_h_reg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, all_h_reg_dis.to_markdown(index=False))
        all_h_reg_dis_sort=all_h_reg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, all_h_reg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, all_h_reg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
###########################################CREATE FUNCTIONS FOR TUNDRA HOMESTEAD#####################################
    #CREATE FUNCTION TO FILL TXT WITH TABLE FOR ALL ROOMS IN TUNDRA HOMESTEAD:
    def fill_table_th_rooms(self, *args):            
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_tharas.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_tharasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_tharareg.grid(row=5, column=0, columnspan=2, sticky='news')
                thar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead"', con)
                thar_dis=thar[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, thar_dis.to_markdown(index=False))
                thar_dis_sort=thar_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thar_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thar_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==1:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_thbras.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_thbrasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_thbrareg.grid(row=5, column=0, columnspan=2, sticky='news')
                thbr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND Room = "Bedroom"', con)
                pd.set_option('display.max_rows', None)
                thbr_dis=thbr[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, thbr_dis.to_markdown(index=False))
                thbr_dis_sort=thbr_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbr_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbr_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==2:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_thbaas.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_thbaasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_thbaareg.grid(row=5, column=0, columnspan=2, sticky='news')
                thba=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND Room = "Basement"', con)
                thba_dis=thba[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, thba_dis.to_markdown(index=False))
                thba_dis_sort=thba_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thba_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thba_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
    #THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM IN TUNDRA HOMESTEAD:
    def clear_th(self, *args):
        self.fill_table_th_rooms()

    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN TUNDRA HOMESTEAD:
    def thar_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_th.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_tharasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_tharareg.grid(row=5, column=0, columnspan=2, sticky='news')
        tharas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        tharas_dis=tharas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, tharas_dis.to_markdown(index=False))
        tharas_dis_sort=tharas_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, tharas_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, tharas_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN TUNDRA HOMESTEAD:
    def thar_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_th.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_tharas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_tharareg.grid(row=5, column=0, columnspan=2, sticky='news')
        tharasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        tharasp_dis=tharasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, tharasp_dis.to_markdown(index=False))
        tharasp_dis_sort=tharasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, tharasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, tharasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)

    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN TUNDRA HOMESTEAD:
    def thar_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_th.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_tharas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_tharasp.grid(row=5, column=0, columnspan=2, sticky='news')
        tharareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
        pd.set_option('display.max_rows', None)
        tharareg_dis=tharareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, tharareg_dis.to_markdown(index=False))
        tharareg_dis_sort=tharareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, tharareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, tharareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM IN TUNDRA HOMESTEAD:
    def thbr_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_th.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_thbrasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_thbrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        thbras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        thbras_dis=thbras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbras_dis.to_markdown(index=False))    
        thbras_dis_sort=thbras_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbras_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbras_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM IN TUNDRA HOMESTEAD:
    def thbr_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_th.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_thbras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_thbrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        thbrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        thbrasp_dis=thbrasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbrasp_dis.to_markdown(index=False))
        thbrasp_dis_sort=thbrasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbrasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbrasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM IN TUNDRA HOMESTEAD:
    def thbr_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_th.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_thbras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_thbrasp.grid(row=5, column=0, columnspan=2, sticky='news')
        thbrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        thbrareg_dis=thbrareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbrareg_dis.to_markdown(index=False))
        thbrareg_dis_sort=thbrareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbrareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbrareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BASEMENT IN TUNDRA HOMESTEAD:
    def thba_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_th.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_thbaasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_thbaareg.grid(row=5, column=0, columnspan=2, sticky='news')
        thbaas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Skill Book" = "Yes" AND Room = "Basement"', con)
        pd.set_option('display.max_rows', None)
        thbaas_dis=thbaas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbaas_dis.to_markdown(index=False))
        thbaas_dis_sort=thbaas_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbaas_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbaas_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BASEMENT IN TUNDRA HOMESTEAD:
    def thba_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_th.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_thbaas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_thbaareg.grid(row=5, column=0, columnspan=2, sticky='news')
        thbaasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "Yes" AND Room = "Basement"', con)
        pd.set_option('display.max_rows', None)
        thbaasp_dis=thbaasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbaasp_dis.to_markdown(index=False))
        thbaasp_dis_sort=thbaasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbaasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbaasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BASEMENT IN TUNDRA HOMESTEAD:
    def thba_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_th.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_thbaas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_thbaasp.grid(row=5, column=0, columnspan=2, sticky='news')
        thbaareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Tundra Homestead" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Basement"', con)
        pd.set_option('display.max_rows', None)
        thbaareg_dis=thbaareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, thbaareg_dis.to_markdown(index=False))
        thbaareg_dis_sort=thbaareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbaareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, thbaareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
###########################################CREATE FUNCTIONS FOR GOLDENHILLS PLANTATION#####################################       
    #CREATE FUNCTION TO FILL TXT WITH TABLE FOR ALL ROOMS IN GOLDENHILLS PLANTATION:    
    def fill_table_gp_rooms(self, *args):           
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_gparas.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_gparasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_gparareg.grid(row=5, column=0, columnspan=2, sticky='news')
                gpar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation"', con)
                pd.set_option('display.max_rows', None)
                gpar_dis=gpar[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, gpar_dis.to_markdown(index=False))
                gpar_dis_sort=gpar_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpar_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpar_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==1:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_gpbras.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_gpbrasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_gpbrareg.grid(row=5, column=0, columnspan=2, sticky='news')
                gpbr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND Room = "Bedroom"', con)
                pd.set_option('display.max_rows', None)
                gpbr_dis=gpbr[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, gpbr_dis.to_markdown(index=False))
                gpbr_dis_sort=gpbr_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpbr_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpbr_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==2:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_gpsrlas.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_gpsrlasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_gpsrlareg.grid(row=5, column=0, columnspan=2, sticky='news')
                gpsrl=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND Room = "Shrine Room (Left)"', con)
                pd.set_option('display.max_rows', None)
                gpsrl_dis=gpsrl[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, gpsrl_dis.to_markdown(index=False))
                gpsrl_dis_sort=gpsrl_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrl_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrl_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==3:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_gpsrras.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_gpsrrasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_gpsrrareg.grid(row=5, column=0, columnspan=2, sticky='news')
                gpsrr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND Room = "Shrine Room (Right)"', con)
                pd.set_option('display.max_rows', None)
                gpsrr_dis=gpsrr[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, gpsrr_dis.to_markdown(index=False))
                gpsrr_dis_sort=gpsrr_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrr_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrr_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
                
    #THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM IN GOLDENHILLS PLANTATION:
    def clear_gp(self, *args):
        self.fill_table_gp_rooms()

    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN GOLDENHILLS PLANTATION:
    def gpar_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gparasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gparareg.grid(row=5, column=0, columnspan=2, sticky='news')
        gparas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        gparas_dis=gparas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gparas_dis.to_markdown(index=False))
        gparas_dis_sort=gparas_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gparas_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gparas_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN GOLDENHILLS PLANTATION:
    def gpar_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gparas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gparareg.grid(row=5, column=0, columnspan=2, sticky='news')
        gparasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        gparasp_dis=gparasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gparasp_dis.to_markdown(index=False))
        gparasp_dis_sort=gparasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gparasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gparasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN GOLDENHILLS PLANTATION:
    def gpar_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gparas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gparasp.grid(row=5, column=0, columnspan=2, sticky='news')
        gparareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
        pd.set_option('display.max_rows', None)
        gparareg_dis=gparareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gparareg_dis.to_markdown(index=False))
        gparareg_dis_sort=gparasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gparareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gparareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM IN GOLDENHILLS PLANTATION:
    def gpbr_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gpbrasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gpbrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        gpbras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        gpbras_dis=gpbras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpbras_dis.to_markdown(index=False))
        gpbras_dis_sort=gpbras_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpbras_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpbras_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM IN GOLDENHILLS PLANTATION:
    def gpbr_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gpbras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gpbrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        gpbrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        gpbrasp_dis=gpbrasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpbrasp_dis.to_markdown(index=False))
        gpbrasp_dis_sort=gpbrasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpbrasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpbrasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM IN GOLDENHILLS PLANTATION:
    def gpbr_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gpbras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gpbrasp.grid(row=5, column=0, columnspan=2, sticky='news')
        gpbrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        gpbrareg_dis=gpbrareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpbrareg_dis.to_markdown(index=False))
        gpbrareg_dis_sort=gpbrareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpbrareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpbrareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN SHRINE ROOM LEFT IN GOLDENHILLS PLANTATION:
    def gpsrl_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gpsrlasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gpsrlareg.grid(row=5, column=0, columnspan=2, sticky='news')
        gpsrlas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes" AND Room = "Shrine Room (Left)"', con)
        pd.set_option('display.max_rows', None)
        gpsrlas_dis=gpsrlas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrlas_dis.to_markdown(index=False))
        gpsrlas_dis_sort=gpsrlas_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrlas_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrlas_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN SHRINE ROOM LEFT IN GOLDENHILLS PLANTATION:
    def gpsrl_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gpsrlas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gpsrlareg.grid(row=5, column=0, columnspan=2, sticky='news')
        gpsrlasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes" AND Room = "Shrine Room (Left)"', con)
        pd.set_option('display.max_rows', None)
        gpsrlasp_dis=gpsrlasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrlasp_dis.to_markdown(index=False))
        gpsrlasp_dis_sort=gpsrlasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrlasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrlasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN SHRINE ROOM LEFT IN GOLDENHILLS PLANTATION:
    def gpsrl_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gpsrlas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gpsrlasp.grid(row=5, column=0, columnspan=2, sticky='news')
        gpsrlareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Shrine Room (Left)"', con)
        pd.set_option('display.max_rows', None)
        gpsrlareg_dis=gpsrlareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrlareg_dis.to_markdown(index=False))
        gpsrlareg_dis_sort=gpsrlareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrlareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrlareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN SHRINE ROOM RIGHT IN GOLDENHILLS PLANTATION:
    def gpsrr_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gpsrrasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gpsrrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        gpsrras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Skill Book" = "Yes" AND Room = "Shrine Room (Right)"', con)
        pd.set_option('display.max_rows', None)
        gpsrras_dis=gpsrras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrras_dis.to_markdown(index=False))
        gpsrras_dis_sort=gpsrras_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrras_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrras_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN SHRINE ROOM RIGHT IN GOLDENHILLS PLANTATION:
    def gpsrr_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gpsrras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gpsrrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        gpsrrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "Yes" AND Room = "Shrine Room (Right)"', con)
        pd.set_option('display.max_rows', None)
        gpsrrasp_dis=gpsrrasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrrasp_dis.to_markdown(index=False))
        gpsrrasp_dis_sort=gpsrrasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrrasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrrasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN SHRINE ROOM RIGHT IN GOLDENHILLS PLANTATION:
    def gpsrr_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_gp.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_gpsrras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_gpsrrasp.grid(row=5, column=0, columnspan=2, sticky='news')
        gpsrrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Goldenhills Plantation" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Shrine Room (Right)"', con)
        pd.set_option('display.max_rows', None)
        gpsrrareg_dis=gpsrrareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, gpsrrareg_dis.to_markdown(index=False))
        gpsrrareg_dis_sort=gpsrrareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrrareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, gpsrrareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
#############################################CREATE FUNCTIONS FOR BREEZEHOME########################################
    #CREATE FUNCTION TO FILL TXT WITH TABLE FOR ALL ROOMS IN BREEZEHOME:    
    def fill_table_b_rooms(self, *args):           
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_baras.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_barasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_barareg.grid(row=5, column=0, columnspan=2, sticky='news')
                bar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome"', con)
                pd.set_option('display.max_rows', None)
                bar_dis=bar[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, bar_dis.to_markdown(index=False))
                bar_dis_sort=bar_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bar_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bar_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==1:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_blivas.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_blivasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_blivareg.grid(row=5, column=0, columnspan=2, sticky='news')
                bliv=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND Room = "Living Room"', con)
                pd.set_option('display.max_rows', None)
                bliv_dis=bliv[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, bliv_dis.to_markdown(index=False))
                bliv_dis_sort=bliv_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bliv_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bliv_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==2:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_blabas.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_blabasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_blabareg.grid(row=5, column=0, columnspan=2, sticky='news')
                blab=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND Room = "Alchemy Lab"', con)
                pd.set_option('display.max_rows', None)
                blab_dis=blab[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, blab_dis.to_markdown(index=False))
                blab_dis_sort=blab_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blab_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blab_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
                
    #THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM IN BREEZEHOME:
    def clear_b(self, *args):
        self.fill_table_b_rooms()

    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN BREEZEHOME:
    def bar_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_b.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_barasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_barareg.grid(row=5, column=0, columnspan=2, sticky='news')
        baras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Skill Book" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        baras_dis=baras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, baras_dis.to_markdown(index=False))
        baras_dis_sort=baras_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, baras_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, baras_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN BREEZEHOME:
    def bar_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_b.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_baras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_barareg.grid(row=5, column=0, columnspan=2, sticky='news')
        barasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        barasp_dis=barasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, barasp_dis.to_markdown(index=False))
        barasp_dis_sort=barasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, barasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, barasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN BREEZEHOME:
    def bar_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_b.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_baras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_barasp.grid(row=5, column=0, columnspan=2, sticky='news')
        barareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
        pd.set_option('display.max_rows', None)
        barareg_dis=barareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, barareg_dis.to_markdown(index=False))
        barareg_dis_sort=barareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, barareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, barareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE LIVING ROOM IN BREEZEHOME:
    def bliv_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_b.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_blivasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_blivareg.grid(row=5, column=0, columnspan=2, sticky='news')
        blivas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Skill Book" = "Yes" AND Room = "Living Room"', con)
        pd.set_option('display.max_rows', None)
        blivas_dis=blivas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, blivas_dis.to_markdown(index=False))
        blivas_dis_sort=blivas_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blivas_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blivas_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE LIVING ROOM IN BREEZEHOME:
    def bliv_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_b.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_blivas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_blivareg.grid(row=5, column=0, columnspan=2, sticky='news')
        blivasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "Yes" AND Room = "Living Room"', con)
        pd.set_option('display.max_rows', None)
        blivasp_dis=blivasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, blivasp_dis.to_markdown(index=False))
        blivasp_dis_sort=blivasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blivasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blivasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE LIVING ROOM IN BREEZEHOME:
    def bliv_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_b.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_blivas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_blivasp.grid(row=5, column=0, columnspan=2, sticky='news')
        blivareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Living Room"', con)
        pd.set_option('display.max_rows', None)
        blivareg_dis=blivareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, blivareg_dis.to_markdown(index=False))
        blivareg_dis_sort=blivareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blivareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blivareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE ALCHEMY LAB IN BREEZEHOME:
    def blab_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_b.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_blabasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_blabareg.grid(row=5, column=0, columnspan=2, sticky='news')
        blabas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Skill Book" = "Yes" AND Room = "Alchemy Lab"', con)
        pd.set_option('display.max_rows', None)
        blabas_dis=blabas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, blabas_dis.to_markdown(index=False))
        blabas_dis_sort=blabas_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blabas_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blabas_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE ALCHEMY LAB IN BREEZEHOME:
    def blab_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_b.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_blabas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_blabareg.grid(row=5, column=0, columnspan=2, sticky='news')
        blabasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "Yes" AND Room = "Alchemy Lab"', con)
        pd.set_option('display.max_rows', None)
        blabasp_dis=blabasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, blabasp_dis.to_markdown(index=False))
        blabasp_dis_sort=blabasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blabasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blabasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE ALCHEMY LAB IN BREEZEHOME:
    def blab_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_b.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_blabas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_blabasp.grid(row=5, column=0, columnspan=2, sticky='news')
        blabareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Breezehome" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Alchemy Lab"', con)
        pd.set_option('display.max_rows', None)
        blabareg_dis=blabareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, blabareg_dis.to_markdown(index=False))
        blabareg_dis_sort=blabareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blabareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, blabareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
##########################################CREATE FUNCTIONS FOR LAKEVIEW MANOR#######################################
    #CREATE FUNCTION TO FILL TXT WITH TABLE FOR ALL ROOMS IN LAKEVIEW MANOR:    
    def fill_table_lm_rooms(self, *args):           
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_lmas.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_lmasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_lmareg.grid(row=5, column=0, columnspan=2, sticky='news')
                lm=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Lakeview Manor"', con)
                pd.set_option('display.max_rows', None)
                lm_dis=lm[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, lm_dis.to_markdown(index=False))            
                lm_dis_sort=lm_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, lm_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, lm_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
                
    #THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM IN LAKEVIEW MANOR:
    def clear_lm(self, *args):
        self.fill_table_lm_rooms()

    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN LAKEVIEW MANOR:
    def lm_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_lm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_lmasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_lmareg.grid(row=5, column=0, columnspan=2, sticky='news')
        lmas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Lakeview Manor" AND "Skill Book" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        lmas_dis=lmas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, lmas_dis.to_markdown(index=False))
        lmas_dis_sort=lmas_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, lmas_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, lmas_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)

    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN LAKEVIEW MANOR:
    def lm_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_lm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_lmas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_lmareg.grid(row=5, column=0, columnspan=2, sticky='news')
        lmasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Lakeview Manor" AND "Spell Tome" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        lmasp_dis=lmasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, lmasp_dis.to_markdown(index=False))
        lmasp_dis_sort=lmasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, lmasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, lmasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN LAKEVIEW MANOR:
    def lm_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_lm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_lmas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_lmasp.grid(row=5, column=0, columnspan=2, sticky='news')
        lmareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Lakeview Manor" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
        pd.set_option('display.max_rows', None)
        lmareg_dis=lmareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, lmareg_dis.to_markdown(index=False))
        lmareg_dis_sort=lmareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, lmareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, lmareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
#########################################CREATE FUNCTIONS FOR BLOODCHILL MANOR######################################
    #CREATE FUNCTION TO FILL TXT WITH TABLE FOR ALL ROOMS IN BLOODCHILL MANOR:    
    def fill_table_bm_rooms(self, *args):           
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_bmaras.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_bmarasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_bmarareg.grid(row=5, column=0, columnspan=2, sticky='news')
                bmar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor"', con)
                pd.set_option('display.max_rows', None)
                bmar_dis=bmar[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, bmar_dis.to_markdown(index=False))
                bmar_dis_sort=bmar_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmar_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmar_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==1:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_bmmb1as.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_bmmb1asp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_bmmb1areg.grid(row=5, column=0, columnspan=2, sticky='news')
                bmmb1=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND Room = "Master Bedroom (Floor 1)"', con)
                pd.set_option('display.max_rows', None)
                bmmb1_dis=bmmb1[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, bmmb1_dis.to_markdown(index=False))
                bmmb1_dis_sort=bmmb1_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb1_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb1_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==2:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_bmmb2as.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_bmmb2asp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_bmmb2areg.grid(row=5, column=0, columnspan=2, sticky='news')
                bmmb2=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND Room = "Master Bedroom (Floor 2)"', con)
                pd.set_option('display.max_rows', None)
                bmmb2_dis=bmmb2[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, bmmb2_dis.to_markdown(index=False))
                bmmb2_dis_sort=bmmb2_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb2_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb2_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==3:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_bmcras.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_bmcrasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_bmcrareg.grid(row=5, column=0, columnspan=2, sticky='news')
                bmcr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND Room = "Child Room"', con)
                pd.set_option('display.max_rows', None)
                bmcr_dis=bmcr[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, bmcr_dis.to_markdown(index=False))
                bmcr_dis_sort=bmcr_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmcr_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmcr_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
                
    #THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM IN IN BLOODCHILL MANOR:
    def clear_bm(self, *args):
        self.fill_table_bm_rooms()

    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN BLOODCHILL MANOR:
    def bmar_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_bmarasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_bmarareg.grid(row=5, column=0, columnspan=2, sticky='news')
        bmaras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Skill Book" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        bmaras_dis=bmaras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmaras_dis.to_markdown(index=False))
        bmaras_dis_sort=bmaras_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmaras_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmaras_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN BLOODCHILL MANOR:
    def bmar_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_bmaras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_bmarareg.grid(row=5, column=0, columnspan=2, sticky='news')
        bmarasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        bmarasp_dis=bmarasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmarasp_dis.to_markdown(index=False))
        bmarasp_dis_sort=bmarasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmarasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmarasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN BLOODCHILL MANOR:
    def bmar_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_bmaras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_bmarasp.grid(row=5, column=0, columnspan=2, sticky='news')
        bmarareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
        pd.set_option('display.max_rows', None)
        bmarareg_dis=bmarareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmarareg_dis.to_markdown(index=False))
        bmarareg_dis_sort=bmarareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmarareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmarareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN MASTER BEDROOM FLOOR 1 IN BLOODCHILL MANOR:
    def bmmb1_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_bmmb1asp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_bmmb1areg.grid(row=5, column=0, columnspan=2, sticky='news')
        bmmb1as=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Skill Book" = "Yes" AND Room = "Master Bedroom (Floor 1)"', con)
        pd.set_option('display.max_rows', None)
        bmmb1as_dis=bmmb1as[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmmb1as_dis.to_markdown(index=False))
        bmmb1as_dis_sort=bmmb1as_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb1as_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb1as_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN MASTER BEDROOM FLOOR 1 IN BLOODCHILL MANOR:
    def bmmb1_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_bmmb1as.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_bmmb1areg.grid(row=5, column=0, columnspan=2, sticky='news')
        bmmb1asp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "Yes" AND Room = "Master Bedroom (Floor 1)"', con)
        pd.set_option('display.max_rows', None)
        bmmb1asp_dis=bmmb1asp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmmb1asp_dis.to_markdown(index=False))
        bmmb1asp_dis_sort=bmmb1asp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb1asp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb1asp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN MASTER BEDROOM FLOOR 1 IN BLOODCHILL MANOR:
    def bmmb1_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_bmmb1as.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_bmmb1asp.grid(row=5, column=0, columnspan=2, sticky='news')
        bmmb1areg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Master Bedroom (Floor 1)"', con)
        pd.set_option('display.max_rows', None)
        bmmb1areg_dis=bmmb1areg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmmb1areg_dis.to_markdown(index=False))
        bmmb1areg_dis_sort=bmmb1areg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb1areg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb1areg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN MASTER BEDROOM FLOOR 2 IN BLOODCHILL MANOR:
    def bmmb2_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=1, column=0, columnspan=2, sticky='ew')
        self.btn_bmmb2asp.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.btn_bmmb2areg.grid(row=3, column=0, columnspan=2, sticky='news')
        bmmb2as=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Skill Book" = "Yes" AND Room = "Master Bedroom (Floor 2)"', con)
        pd.set_option('display.max_rows', None)
        bmmb2as_dis=bmmb2as[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmmb2as_dis.to_markdown(index=False))
        bmmb2as_dis_sort=bmmb2as_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb2as_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb2as_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
         
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN MASTER BEDROOM FLOOR 2 IN BLOODCHILL MANOR:
    def bmmb2_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_bmmb2as.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_bmmb2areg.grid(row=5, column=0, columnspan=2, sticky='news')
        bmmb2asp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "Yes" AND Room = "Master Bedroom (Floor 2)"', con)
        pd.set_option('display.max_rows', None)
        bmmb2asp_dis=bmmb2asp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmmb2asp_dis.to_markdown(index=False))
        bmmb2asp_dis_sort=bmmb2asp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb2asp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb2asp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
         
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN MASTER BEDROOM FLOOR 2 IN BLOODCHILL MANOR:
    def bmmb2_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_bmmb2as.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_bmmb2asp.grid(row=5, column=0, columnspan=2, sticky='news')
        bmmb2areg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Master Bedroom (Floor 2)"', con)
        pd.set_option('display.max_rows', None)
        bmmb2areg_dis=bmmb2areg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmmb2areg_dis.to_markdown(index=False))
        bmmb2areg_dis_sort=bmmb2areg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb2areg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmmb2areg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN CHILD ROOM IN BLOODCHILL MANOR:
    def bmcr_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_bmcrasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_bmcrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        bmcras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Skill Book" = "Yes" AND Room = "Child Room"', con)
        pd.set_option('display.max_rows', None)
        bmcras_dis=bmcras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmcras_dis.to_markdown(index=False))
        bmcras_dis_sort=bmcras_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmcras_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmcras_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN CHILD ROOM IN BLOODCHILL MANOR:
    def bmcr_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_bmcras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_bmcrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        bmcrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "Yes" AND Room = "Child Room"', con)
        pd.set_option('display.max_rows', None)
        bmcrasp_dis=bmcrasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmcrasp_dis.to_markdown(index=False))
        bmcrasp_dis_sort=bmcrasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmcrasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmcrasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN CHILD ROOM IN BLOODCHILL MANOR:
    def bmcr_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_bm.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_bmcras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_bmcrasp.grid(row=5, column=0, columnspan=2, sticky='news')
        bmcrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Bloodchill Manor" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Child Room"', con)
        pd.set_option('display.max_rows', None)
        bmcrareg_dis=bmcrareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, bmcrareg_dis.to_markdown(index=False))
        bmcrareg_dis_sort=bmcrareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmcrareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, bmcrareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
###############################################CREATE FUNCTIONS FOR HENDRAHEIM######################################
    #CREATE FUNCTION TO FILL TXT WITH TABLE FOR ALL ROOMS IN HENDRAHEIM:    
    def fill_table_h_rooms(self, *args):           
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_haras.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_harasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_harareg.grid(row=5, column=0, columnspan=2, sticky='news')
                har=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim"', con)
                pd.set_option('display.max_rows', None)
                har_dis=har[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, har_dis.to_markdown(index=False))
                har_dis_sort=har_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, har_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, har_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==1:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_hbrlas.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_hbrlasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_hbrlareg.grid(row=5, column=0, columnspan=2, sticky='news')
                hbrl=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND Room = "Bedroom (Left)"', con)
                pd.set_option('display.max_rows', None)
                hbrl_dis=hbrl[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, hbrl_dis.to_markdown(index=False))
                hbrl_dis_sort=hbrl_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrl_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrl_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==2:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_hbrras.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_hbrrasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_hbrrareg.grid(row=5, column=0, columnspan=2, sticky='news')
                hbrr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND Room = "Bedroom (Right)"', con)
                pd.set_option('display.max_rows', None)
                hbrr_dis=hbrr[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, hbrr_dis.to_markdown(index=False))
                hbrr_dis_sort=hbrr_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrr_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrr_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==3:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_hdaas.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_hdaasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_hdaareg.grid(row=5, column=0, columnspan=2, sticky='news')
                hda=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND Room = "Dining Area"', con)
                pd.set_option('display.max_rows', None)
                hda_dis=hda[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, hda_dis.to_markdown(index=False))                
                hda_dis_sort=hda_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hda_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hda_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
                
    #THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM IN HENDRAHEIM:
    def clear_h(self, *args):
        self.fill_table_h_rooms()

    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN HENDRAHEIM:
    def har_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_harasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_harareg.grid(row=5, column=0, columnspan=2, sticky='news')
        haras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Skill Book" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        haras_dis=haras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, haras_dis.to_markdown(index=False))
        haras_dis_sort=haras_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, haras_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, haras_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN HENDRAHEIM:
    def har_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_haras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_harareg.grid(row=5, column=0, columnspan=2, sticky='news')
        harasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        harasp_dis=harasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, harasp_dis.to_markdown(index=False))
        harasp_dis_sort=harasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, harasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, harasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN HENDRAHEIM:
    def har_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_haras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_harasp.grid(row=5, column=0, columnspan=2, sticky='news')
        harareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
        pd.set_option('display.max_rows', None)
        harareg_dis=harareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, harareg_dis.to_markdown(index=False))
        harareg_dis_sort=harareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, harareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, harareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM (LEFT) IN HENDRAHEIM:
    def hbrl_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hbrlasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hbrlareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hbrlas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Skill Book" = "Yes" AND Room = "Bedroom (Left)"', con)
        pd.set_option('display.max_rows', None)
        hbrlas_dis=hbrlas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hbrlas_dis.to_markdown(index=False))
        hbrlas_dis_sort=hbrlas_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrlas_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrlas_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM (LEFT) IN HENDRAHEIM:
    def hbrl_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hbrlas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hbrlareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hbrlasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "Yes" AND Room = "Bedroom (Left)"', con)
        pd.set_option('display.max_rows', None)
        hbrlasp_dis=hbrlasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hbrlasp_dis.to_markdown(index=False))
        hbrlasp_dis_sort=hbrlasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrlasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrlasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM (LEFT) IN HENDRAHEIM:
    def hbrl_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hbrlas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hbrlasp.grid(row=5, column=0, columnspan=2, sticky='news')
        hbrlareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom (Left)"', con)
        pd.set_option('display.max_rows', None)
        hbrlareg_dis=hbrlareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hbrlareg_dis.to_markdown(index=False))
        hbrlareg_dis_sort=hbrlareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrlareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrlareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM (RIGHT) IN HENDRAHEIM:
    def hbrr_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hbrrasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hbrrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hbrras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Skill Book" = "Yes" AND Room = "Bedroom (Right)"', con)
        pd.set_option('display.max_rows', None)
        hbrras_dis=hbrras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hbrras_dis.to_markdown(index=False))
        hbrras_dis_sort=hbrras_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrras_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrras_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM (RIGHT) IN HENDRAHEIM:
    def hbrr_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hbrras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hbrrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hbrrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "Yes" AND Room = "Bedroom (Right)"', con)
        pd.set_option('display.max_rows', None)
        hbrrasp_dis=hbrrasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hbrrasp_dis.to_markdown(index=False))
        hbrrasp_dis_sort=hbrrasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrrasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrrasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM (RIGHT) IN HENDRAHEIM:
    def hbrr_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hbrras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hbrrasp.grid(row=5, column=0, columnspan=2, sticky='news')
        hbrrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom (Right)"', con)
        pd.set_option('display.max_rows', None)
        hbrrareg_dis=hbrrareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hbrrareg_dis.to_markdown(index=False))
        hbrrareg_dis_sort=hbrrareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrrareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hbrrareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE DINING AREA IN HENDRAHEIM:
    def hda_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hdaasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hdaareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hdaas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Skill Book" = "Yes" AND Room = "Dining Area"', con)
        pd.set_option('display.max_rows', None)
        hdaas_dis=hdaas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hdaas_dis.to_markdown(index=False))
        hdaas_dis_sort=hdaas_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hdaas_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hdaas_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE DINING AREA IN HENDRAHEIM:
    def hda_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hdaas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hdaareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hdaasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "Yes" AND Room = "Dining Area"', con)
        pd.set_option('display.max_rows', None)
        hdaasp_dis=hdaasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hdaasp_dis.to_markdown(index=False))
        hdaasp_dis_sort=hdaasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hdaasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hdaasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE DINING AREA IN HENDRAHEIM:
    def hda_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_h.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hdaas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hdaasp.grid(row=5, column=0, columnspan=2, sticky='news')
        hdaareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Hendraheim" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Dining Area"', con)
        pd.set_option('display.max_rows', None)
        hdaareg_dis=hdaareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hdaareg_dis.to_markdown(index=False))
        hdaareg_dis_sort=hdaareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hdaareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hdaareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
###############################################CREATE FUNCTIONS FOR HONEYSIDE########################################
    #CREATE FUNCTION TO FILL TXT WITH TABLE FOR ALL ROOMS IN HONEYSIDE:    
    def fill_table_hs_rooms(self, *args):            
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_hsaras.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_hsarasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_hsarareg.grid(row=5, column=0, columnspan=2, sticky='news')
                hsar=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside"', con)
                pd.set_option('display.max_rows', None)
                hsar_dis=hsar[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, hsar_dis.to_markdown(index=False))
                hsar_dis_sort=hsar_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsar_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsar_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==1:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_hsbras.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_hsbrasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_hsbrareg.grid(row=5, column=0, columnspan=2, sticky='news')
                hsbr=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND Room = "Bedroom"', con)
                pd.set_option('display.max_rows', None)
                hsbr_dis=hsbr[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, hsbr_dis.to_markdown(index=False))
                hsbr_dis_sort=hsbr_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbr_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbr_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
            if idx_room==2:
                self.forget_btns()
                self.txt.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_search.grid(row=6, column=3, sticky='nes')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_hsbaas.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_hsbaasp.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_hsbaareg.grid(row=5, column=0, columnspan=2, sticky='news')
                hsba=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND Room = "Basement"', con)
                pd.set_option('display.max_rows', None)
                hsba_dis=hsba[['Title', 'House', 'Room']]
                self.txt.insert(tk.END, hsba_dis.to_markdown(index=False))
                hsba_dis_sort=hsba_dis.sort_values('Title')
                self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsba_dis_sort.to_markdown(index=False))])
                self.btn_title_abc.grid(row=6, column=0, sticky='news')
                self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsba_dis.to_markdown(index=False))])
                self.btn_title_ind.grid(row=6, column=1, sticky='news')
                self.txt.config(state=tk.DISABLED)
                
    #THIS FUNCTION RESETS THE TABLE TO ITS UNFILTERED FORM IN HONEYSIDE:
    def clear_hs(self, *args):
        self.fill_table_hs_rooms()
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN ALL ROOMS IN HONEYSIDE:
    def hsar_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_hs.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hsarasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hsarareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hsaras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Skill Book" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        hsaras_dis=hsaras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hsaras_dis.to_markdown(index=False))    
        hsaras_dis_sort=hsaras_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsaras_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsaras_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN ALL ROOMS IN HONEYSIDE:
    def hsar_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_hs.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hsaras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hsarareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hsarasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "Yes"', con)
        pd.set_option('display.max_rows', None)
        hsarasp_dis=hsarasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hsarasp_dis.to_markdown(index=False))
        hsarasp_dis_sort=hsarasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsarasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsarasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN ALL ROOMS IN HONEYSIDE:
    def hsar_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_hs.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hsaras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hsarasp.grid(row=5, column=0, columnspan=2, sticky='news')
        hsarareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "No" AND "Skill Book" = "No"', con)
        pd.set_option('display.max_rows', None)
        hsarareg_dis=hsarareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hsarareg_dis.to_markdown(index=False))
        hsarareg_dis_sort=hsarareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsarareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsarareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BEDROOM IN HONEYSIDE:
    def hsbr_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_hs.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hsbrasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hsbrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hsbras=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Skill Book" = "Yes" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        hsbras_dis=hsbras[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hsbras_dis.to_markdown(index=False))  
        hsbras_dis_sort=hsbras_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbras_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbras_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BEDROOM IN HONEYSIDE:
    def hsbr_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_hs.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hsbras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hsbrareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hsbrasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "Yes" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        hsbrasp_dis=hsbrasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hsbrasp_dis.to_markdown(index=False))
        hsbrasp_dis_sort=hsbrasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbrasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbrasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BEDROOM IN HONEYSIDE:
    def hsbr_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_hs.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hsbras.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hsbrasp.grid(row=5, column=0, columnspan=2, sticky='news')
        hsbrareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Bedroom"', con)
        pd.set_option('display.max_rows', None)
        hsbrareg_dis=hsbrareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hsbrareg_dis.to_markdown(index=False))
        hsbrareg_dis_sort=hsbrareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbrareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[sself.txt_activate(), self.txt.insert(tk.END, hsbrareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SKILL BOOKS IN THE BASEMENT IN HONEYSIDE:
    def hsba_skill(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_hs.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hsbaasp.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hsbaareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hsbaas=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Skill Book" = "Yes" AND Room = "Basement"', con)
        pd.set_option('display.max_rows', None)
        hsbaas_dis=hsbaas[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hsbaas_dis.to_markdown(index=False))
        hsbaas_dis_sort=hsbaas_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbaas_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbaas_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS FOR SPELL TOMES IN THE BASEMENT IN HONEYSIDE:
    def hsba_spell(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_hs.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hsbaas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hsbaareg.grid(row=5, column=0, columnspan=2, sticky='news')
        hsbaasp=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "Yes" AND Room = "Basement"', con)
        pd.set_option('display.max_rows', None)
        hsbaasp_dis=hsbaasp[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hsbaasp_dis.to_markdown(index=False))
        hsbaasp_dis_sort=hsbaasp_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbaasp_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbaasp_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)
        
    #THIS FUNCTION IS BUTTON ACTIVATED AND FILTERS OUT ALL SKILL BOOKS AND SPELL TOMES IN THE BASEMENT IN HONEYSIDE:
    def hsba_reg(self, *args):
        self.forget_btns()
        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)
        self.btn_search.grid(row=6, column=3, sticky='nes')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.btn_clr_hs.grid(row=3, column=0, columnspan=2, sticky='news')
        self.btn_hsbaas.grid(row=4, column=0, columnspan=2, sticky='news')
        self.btn_hsbaasp.grid(row=5, column=0, columnspan=2, sticky='news')
        hsbaareg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House = "Honeyside" AND "Spell Tome" = "No" AND "Skill Book" = "No" AND Room = "Basement"', con)
        pd.set_option('display.max_rows', None)
        hsbaareg_dis=hsbaareg[['Title', 'House', 'Room']]
        self.txt.insert(tk.END, hsbaareg_dis.to_markdown(index=False))
        hsbaareg_dis_sort=hsbaareg_dis.sort_values('Title')
        self.btn_title_abc=tk.Button(self.frame, text='Sort Alphabetically', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbaareg_dis_sort.to_markdown(index=False))])
        self.btn_title_abc.grid(row=6, column=0, sticky='news')
        self.btn_title_ind=tk.Button(self.frame, text='Sort by Index', command=lambda:[self.txt_activate(), self.txt.insert(tk.END, hsbaareg_dis.to_markdown(index=False))])
        self.btn_title_ind.grid(row=6, column=1, sticky='news')
        self.txt.config(state=tk.DISABLED)


    def addhouse_win(self, *args):
        self.addhouse_screen=tk.Toplevel(self.master)
        self.addhouse_screen.title('Add House')
        self.frame=tk.Frame(self.addhouse_screen)
        self.frame.grid(row=0, column=0, sticky='news')
        self.lbl_add_house=tk.Label(self.frame, text='Add House:')
        self.lbl_add_house.grid(row=0, column=0, columnspan=3, sticky='ew')
        self.new_house = tk.StringVar()
        self.addhouse_bar=tk.Entry(self.frame, textvariable=self.new_house)
        self.addhouse_bar.grid(row=1, column=0, columnspan=2, sticky='ew')
        self.btn_addhouse=tk.Button(self.frame, text='Add House', command=lambda: [self.addhouse(), self.addhouse_screen.destroy()])
        self.btn_addhouse.grid(row=1, column=2, columnspan=1, sticky='ew')

    def addhouse(self, *args):
        NEW_HOUSE=self.new_house.get()
        houses.append(NEW_HOUSE)
        self.listbox_houses.delete(0, tk.END)
        self.listbox_houses.insert(tk.END, houses)
##        addbook_win.listbox_houses.delete(0, tk.END)
##        addbook_win.listbox_houses.insert(tk.END, houses_addbook)
#CREATE 'ADD BOOK' WINDOW:
class addbook_win:
    def __init__(self, master):
        self.master=master
        self.master.title('Add Book')
        self.frame=tk.Frame(self.master)
        self.frame.grid(row=0, column=0, sticky='news')
        #CREATE BOX AND LABEL FOR ADDING TITLE:
        self.lbl_addbook_title=tk.Label(self.frame, text='Enter Title:')
        self.lbl_addbook_title.grid(row=0, column=0, sticky='ew')
        self.title=tk.StringVar()
        self.add_title=tk.Entry(self.frame, textvariable=self.title)
        self.add_title.grid(row=0, column=1, columnspan=3, sticky='news')
        #CREATE LISTBOX AND LABEL FOR HOUSES TO SELECT:
        Houses_addbook = tk.StringVar(self.frame, value=houses_addbook)
        self.lbl_houses=tk.Label(self.frame, text='Select House:')
        self.lbl_houses.grid(row=1, column=0, sticky='ew')
        self.listbox_houses=tk.Listbox(self.frame, listvariable=Houses_addbook, bg='white', font='Ariel', fg='black')
        self.listbox_houses.grid(row=1, column=1, sticky='ew')
        self.listbox_houses.bind('<<ListboxSelect>>', self.select_house_addbook)
        #CREATE LISTBOX AND LABEL FOR ROOMS TO SELECT:
        self.lbl_rooms=tk.Label(self.frame, text='Select Room:')
        self.lbl_rooms.grid(row=1, column=2, sticky='ew')
        self.listbox_rooms=tk.Listbox(self.frame, bg='white', font='Ariel', fg='black', exportselection=False)
        self.listbox_rooms.grid(row=1, column=3, sticky='ew')
        #CREATE LISTBOX AND LABEL FOR YES/NO OPTION FOR SKILL BOOKS:
        self.lbl_skill=tk.Label(self.frame, text='Skill Book:')
        self.lbl_skill.grid(row=2, column=0, sticky='ew')
        self.lbsk=tk.StringVar(self.frame, value=list_binary_skill)
        self.listbox_skill=tk.Listbox(self.frame, listvariable=self.lbsk, bg='white', font='Ariel', fg='black', exportselection=False)
        self.listbox_skill.grid(row=2, column=1, sticky='ew')
        #CREATE LISTBOX AND LABEL FOR YES/NO OPTION FOR SPELL TOMES:
        self.lbl_spell=tk.Label(self.frame, text='Spell Book:')
        self.lbl_spell.grid(row=2, column=2, sticky='ew')
        self.lbsp=tk.StringVar(self.frame, value=list_binary_spell)
        self.listbox_spell=tk.Listbox(self.frame, listvariable=self.lbsp, bg='white', font='Ariel', fg='black', exportselection=False)
        self.listbox_spell.grid(row=2, column=3, sticky='ew')
        #CREATE BUTTON TO ADD BOOK:
        self.btn_addbook=tk.Button(self.frame, text='Add Book', command=lambda: [self.addbook(), self.master.destroy()])
        self.btn_addbook.grid(row=3, column=0, columnspan=4, sticky='ew')

     #CREATE FUNCTION TO FILL LISTBOX_ROOMS:
    def select_house_addbook(self, *args):
        self.listbox_rooms.delete(0, tk.END)
        idxs=self.listbox_houses.curselection()
        if len(idxs)==1:
            idx=int(idxs[0])
            if idx==0:
                for room in th_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)
            if idx==1:
                for room in gp_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)
            if idx==2:
                for room in b_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)
            if idx==3:
                self.listbox_rooms.insert(tk.END, 'Master Bedroom')
            if idx==4:
                for room in bm_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)
            if idx==5:
                for room in h_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)
            if idx==6:
                for room in hs_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)

    #CREATE FUNCTION TO ADD BOOK TO DATABASE:
    def addbook(self, *args):
        TITLE=self.title.get()
        idxs_house=self.listbox_houses.curselection()
        HOUSE=self.listbox_houses.get(first=idxs_house)
        idxs_room=self.listbox_rooms.curselection()
        ROOM=self.listbox_rooms.get(first=idxs_room)
        idxs_skill=self.listbox_skill.curselection()
        SKILL=self.listbox_skill.get(first=idxs_skill)
        idxs_spell=self.listbox_spell.curselection()
        SPELL=self.listbox_spell.get(first=idxs_spell)
        check='SELECT "ID" FROM "My Books" where Title = ? LIMIT 1'
        cur.execute(check, (TITLE,))
        if cur.fetchone():
            self.warn_message=tk.Toplevel()
            self.warn_message.title('WARNING!')
            self.warn_frame=tk.Frame(self.warn_message)
            self.warn_frame.grid(row=0, column=0, sticky='news')
            self.lbl_warn=tk.Label(self.warn_frame, text='A book with this title already exists')
            self.lbl_warn.grid(row=0, column=0, sticky='news')
            self.btn_back=tk.Button(self.warn_frame, text='Return', command=self.warn_message.destroy)
            self.btn_back.grid(row=1, column=0, sticky='news')
        else: 
            cur.execute('INSERT INTO "My Books" ("Title", "House", "Room", "Skill Book", "Spell Tome") VALUES (?, ?, ?, ?, ?)', (TITLE, HOUSE, ROOM, SKILL, SPELL))
            con.commit()

#Title=()
class movebook_win:
    def __init__(self, master):
        self.master=master
        self.master.title('Move Book')
        self.frame=tk.Frame(self.master)
        self.frame.grid(row=0, column=0, sticky='news')
        all_books=pd.read_sql_query('SELECT * FROM "My Books"', con)
        self.lbl_select_title=tk.Label(self.frame, text='Select Book:')
        self.lbl_select_title.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.listbox_title=tk.Listbox(self.frame, bg='white', font='Ariel', fg='black', exportselection=False)
        self.listbox_title.grid(row=1, column=0, columnspan=2, sticky='news')
        for title in all_books["Title"]:
            self.listbox_title.insert(tk.END, title)
        #CREATE LISTBOX AND LABEL FOR HOUSES TO SELECT:
        Houses = tk.StringVar(self.frame, value=houses_addbook)
        self.lbl_houses=tk.Label(self.frame, text='Select House:')
        self.lbl_houses.grid(row=2, column=0, sticky='ew')
        self.listbox_houses=tk.Listbox(self.frame, listvariable=Houses, bg='white', font='Ariel', fg='black')
        self.listbox_houses.grid(row=3, column=0, sticky='ew')
        self.listbox_houses.bind('<<ListboxSelect>>', self.select_house_movebook)
        #CREATE LISTBOX AND LABEL FOR ROOMS TO SELECT:
        self.lbl_rooms=tk.Label(self.frame, text='Select Room:')
        self.lbl_rooms.grid(row=2, column=1, sticky='ew')
        self.listbox_rooms=tk.Listbox(self.frame, bg='white', font='Ariel', fg='black', exportselection=False)
        self.listbox_rooms.grid(row=3, column=1, sticky='ew')
        #CREATE LISTBOX AND LABEL FOR YES/NO OPTION FOR SKILL BOOKS:
        self.lbl_skill=tk.Label(self.frame, text='Skill Book:')
        self.lbl_skill.grid(row=4, column=0, sticky='ew')
        self.lbsk=tk.StringVar(self.frame, value=list_binary_skill)
        self.listbox_skill=tk.Listbox(self.frame, listvariable=self.lbsk, bg='white', font='Ariel', fg='black', exportselection=False)
        self.listbox_skill.grid(row=5, column=0, sticky='ew')
        #CREATE LISTBOX AND LABEL FOR YES/NO OPTION FOR SPELL TOMES:
        self.lbl_spell=tk.Label(self.frame, text='Spell Book:')
        self.lbl_spell.grid(row=4, column=1, sticky='ew')
        self.lbsp=tk.StringVar(self.frame, value=list_binary_spell)
        self.listbox_spell=tk.Listbox(self.frame, listvariable=self.lbsp, bg='white', font='Ariel', fg='black', exportselection=False)
        self.listbox_spell.grid(row=5, column=1, sticky='ew')
        #CREATE BUTTON TO MOVE BOOK:
        self.btn_movebook=tk.Button(self.frame, text='Move Book', command=lambda: [self.movebook(), self.master.destroy()])
        self.btn_movebook.grid(row=6, column=0, columnspan=2, sticky='ew')

    def select_house_movebook(self, *args):
        self.listbox_rooms.delete(0, tk.END)
        idxs=self.listbox_houses.curselection()
        if len(idxs)==1:
            idx=int(idxs[0])
            if idx==0:
                for room in th_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)
            if idx==1:
                for room in gp_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)
            if idx==2:
                for room in b_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)
            if idx==3:
                self.listbox_rooms.insert(tk.END, 'Master Bedroom')
            if idx==4:
                for room in bm_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)
            if idx==5:
                for room in h_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)
            if idx==6:
                for room in hs_rooms_addbook:
                    self.listbox_rooms.insert(tk.END, room)

    def movebook(self, *args):
        idxs_title=self.listbox_title.curselection()
        for idx in idxs_title:
            TITLE=self.listbox_title.get(idx)
        idxs_house=self.listbox_houses.curselection()
        HOUSE=self.listbox_houses.get(first=idxs_house)
        idxs_room=self.listbox_rooms.curselection()
        ROOM=self.listbox_rooms.get(first=idxs_room)
        idxs_skill=self.listbox_skill.curselection()
        SKILL=self.listbox_skill.get(first=idxs_skill)
        idxs_spell=self.listbox_spell.curselection()
        SPELL=self.listbox_spell.get(first=idxs_spell)
        update='UPDATE "My Books" SET House=?, Room=?, "Skill Book"=?, "Spell Tome"=? WHERE Title=?'
        cur.execute(update, (HOUSE, ROOM, SKILL, SPELL, TITLE))
        con.commit()

class delbook_win:
    def __init__(self, master):
        self.master=master
        self.master.title('Delete Book')
        self.frame=tk.Frame(self.master)
        self.frame.grid(row=0, column=0, sticky='news')
        all_books=pd.read_sql_query('SELECT * FROM "My Books"', con)
        self.lbl_select_title=tk.Label(self.frame, text='Select Book:')
        self.lbl_select_title.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.listbox_title=tk.Listbox(self.frame, bg='white', font='Ariel', fg='black', exportselection=False, width=32)
        self.listbox_title.grid(row=1, column=0, sticky='news')
        for title in all_books["Title"]:
            self.listbox_title.insert(tk.END, title)
        #CREATE BUTTON TO DELETE BOOK:
        self.btn_delbook=tk.Button(self.frame, text='Delete Book', command=lambda: [self.delbook(), self.master.destroy()])
        self.btn_delbook.grid(row=2, column=0, columnspan=2, sticky='ew')

    def delbook(self, *args):
        idxs_title=self.listbox_title.curselection()
        all_books=pd.read_sql_query('SELECT * FROM "My Books"', con)
        for tit in idxs_title:
            TITLE=self.listbox_title.get(tit)
        delete='DELETE FROM "My Books" WHERE "Title"=?'
        cur.execute(delete, (TITLE,))
        con.commit()
        
#LAUNCH DATABASE:
if __name__ == '__main__':
    mm()

#CLOSE DATABASE CONNECTION:
con.commit()
con.close()
