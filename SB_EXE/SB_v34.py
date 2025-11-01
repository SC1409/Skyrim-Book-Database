#IMPORT RELEVANT MODULES:
import sqlite3 as sql
import pandas as pd
import tkinter as tk
from tkinter import ttk, font
import sys
import os
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

#CREATE CONNECTION TO DATABASE AND CURSOR FUNCTION:
DB = 'C:/Users/steph/Documents/Python/SB_EXE/SKYRIM_BOOKS.db'
con = sql.connect(DB)
cur = con.cursor()

#FETCH TABLES IN DATABASE:
cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")

#OPEN LISTS OF HOUSES AND ROOMS:
with open('C:/Users/steph/Documents/Python/SB_EXE/main_lists/lists_main_houses.txt', 'r') as file_houses_main:
    houses_main=file_houses_main.readline().rstrip('\n')

with open('C:/Users/steph/Documents/Python/SB_EXE/add_move_lists/lists_addmove_houses.txt', 'r') as file_houses_add_move:
    houses_add_move=file_houses_add_move.readline().rstrip('\n')

allrooms_main = []
file_all_rooms_main = open('C:/Users/steph/Documents/Python/SB_EXE/main_lists/lists_main_allrooms.txt', 'r+')
for line in file_all_rooms_main:
    allrooms_main.append(line.strip('\n'))
    
allrooms_add_move = []
file_all_rooms_add_move = open('C:/Users/steph/Documents/Python/SB_EXE/add_move_lists/lists_addmove_allrooms.txt', 'r+')
for line in file_all_rooms_add_move:
    allrooms_add_move.append(line.strip('\n'))

list_binary_skill = ('Yes', 'No')
list_binary_spell = ('Yes', 'No')

FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

#FUNCTION TO LOAD CUSTOM FONTS FOR PROGRAM,TAKEN FROM:
#https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
#IN COMPLIANCE WITH DIGSBY LICENSE PARAGRAPH 3, THE LIST OF CHANGES IS AS FOLLOWS:
#1) MOVED THE SOURCE OF THE FUNCTION FROM THE MIDDLE TO JUST ABOVE THIS LIST
#2) MOVED AND IMPLEMENTED THE FOLLOWING INSTRUCTIONS - # This function is written for Python 2.x. For 3.x, you
    # have to convert the isinstance checks to bytes and str
#3) REMOVED SOME EMPTY LInews
    
def loadfont(fontpath, private=True, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.

    `private`     if True, other processes cannot see this font, and this
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts

    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

    '''
    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or unicode')
    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)

#ADD CUSTOM FONTS FOR PROGRAM:
font_tbl_path='C:\\Users\\steph\\Documents\\Python\\SB_EXE\\15_SkyrimBooks_Handwritten_Bold.ttf'
loadfont(font_tbl_path)
font_btns_path='C:\\Users\\steph\\Documents\\Python\\SB_EXE\\9_Futura_Condensed.ttf'
loadfont(font_btns_path)
font_headers_path='C:\\Users\\steph\\Documents\\Python\\SB_EXE\\13_SkyrimBooks_Gaelic.ttf'
loadfont(font_headers_path)
font_listboxes_path='C:\\Users\\steph\\Documents\\Python\\SB_EXE\\5_Futura_CondensedLight.ttf'
loadfont(font_listboxes_path)

#CREATE LAUNCH FUNCTION:
def mm():
    root=tk.Tk()
    root.title('Skyrim Books')
    app=main_win(root)
    root.mainloop()

#CREATE MAIN WINDOW:
class main_win:
    def __init__(self, master):
        #CREATE MAIN WINDOW AND FRAME:
        self.master=master
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        #self.master.resizable(False, False)
        self.frame=tk.Frame(self.master, bg='black')
        self.frame.grid(row=0, column=0, sticky='news')
        #CONFIGURE ROWS TO ALLOW FOR EXPANSION WHEN FULL SCREEN:
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
        #GET LIST OF HOUSES:
        Houses_main = tk.StringVar(self.frame, value=houses_main.split(','))
        #APPLY FUNCTION TO REMOVE ALL BUTTONS FROM SCREEN:
        self.forget_btns()
        #CREATE RIGHT CLICK MENU FOR TEXTBOX:
        self.men_tree=tk.Menu(self.frame, tearoff=0)
        self.men_tree.add_command(label='Copy')
        self.men_tree.entryconfigure('Copy', command=self.tree_c2c)
        #CREATE RIGHT CLICK MENU FOR SEARCHBAR
        self.men_search=tk.Menu(self.frame, tearoff=0)
        self.men_search.add_command(label='Copy')
        self.men_search.add_command(label='Paste')
        self.men_search.entryconfigure('Copy', command=self.search_c2c)
        self.men_search.entryconfigure('Paste', command=self.search_pfc)
        #CREATE MENUBAR FOR MAIN SCREEN:
        self.menubar=tk.Menu(self.master)
        self.menubar_settings=tk.Menu(self.menubar, tearoff=0)
        self.menubar_settings.add_command(label='Add House', command=self.open_addhouse)
        self.menubar.add_cascade(label='Settings', menu=self.menubar_settings)
        self.master.config(menu=self.menubar)
        #CREATE HOUSE'S LISTBOX AND LABEL:
        self.lbl_houses=tk.Label(self.frame, text='Select House:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_houses.grid(row=1, column=0, sticky='ew')
        self.listbox_houses=tk.Listbox(self.frame, listvariable=Houses_main, bg='black', fg='white', exportselection=False, width=20, height=5, highlightbackground="white", highlightthickness=1)
        self.listbox_houses.config(font=('Futura CondensedLight',15))
        self.listbox_houses.grid(row=2, column=0, sticky='ew')
        self.listbox_houses.bind('<<ListboxSelect>>', self.fill_listbox_rooms)
        #CREATE ROOM'S LISTBOX AND LABEL:
        self.lbl_rooms=tk.Label(self.frame, text='Select Room:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_rooms.grid(row=1, column=1, sticky='ew')
        self.listbox_rooms=tk.Listbox(self.frame, bg='black', fg='white', exportselection=False, width=20, height=5, highlightbackground="white", highlightthickness=1)
        self.listbox_rooms.config(font=('Futura CondensedLight',15))
        self.listbox_rooms.grid(row=2, column=1, sticky='ew')
        #CREATE TREEVIEW FOR TABLES:
        self.tree=ttk.Treeview(self.frame)
        self.style_tree=ttk.Style()
        self.style_tree.theme_use('clam')
        self.style_tree.configure('Treeview.Heading', font='SkyrimBooks_Gaelic', background='#E1C78C')
        self.style_tree.configure('Treeview', font='SkyrimBooks_Handwritten_Bold', borderwidth=0, background='#E1C78C', fieldbackground='#E1C78C')
        self.tree.grid(row=1, column=2, rowspan=5, columnspan=2, sticky='news')
        self.tree.bind('<Button-3>', self.tree_do_popup)
        #CREATE SEARCH BAR AND BUTTON WIDGETS:
        self.searchstring = tk.StringVar()
        self.searchbar=tk.Entry(self.frame, textvariable=self.searchstring, font='SkyrimBooks_Handwritten_Bold', borderwidth=0, bg='#E1C78C', fg='black')
        self.searchbar.grid(row=6, column=2, columnspan=2, sticky='news')
        self.searchbar.bind('<Button-3>', self.search_do_popup)
        self.searchbar.bind('<Return>', self.search)
        self.btn_search=tk.Button(self.frame, text='Search', command=self.search, font=('Futura Condensed',15), bg='black', fg='white', highlightbackground="white", highlightthickness=1)
        self.btn_search.grid(row=6, column=0, columnspan=2, sticky='news')
        #CREATE BUTTON TO OPEN 'ADD BOOK' WINDOW:
        self.btn_open_addbook=tk.Button(self.frame, text='Add Book', command=self.open_addbook, font=('Futura Condensed',15), bg='black', fg='white', highlightbackground="white", highlightthickness=1)
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        #CREATE BUTTON TO OPEN 'MOVE BOOK' WINDOW:
        self.btn_open_movebook=tk.Button(self.frame, text='Move Book', command=self.open_movebook, font=('Futura Condensed',15), bg='black', fg='white', highlightbackground="white", highlightthickness=1)
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        #CREATE BUTTON TO OPEN 'DELETE BOOK' WINDOW:
        self.btn_open_delbook=tk.Button(self.frame, text='Delete Book', command=self.open_delbook, font=('Futura Condensed',15), bg='black', fg='white', highlightbackground="white", highlightthickness=1)
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        
    #CREATE FUNCTION TO DELETE ALL BUTTONS:
    def forget_btns(self, *args):
        lst=self.frame.winfo_children()
        for item in lst:
            if isinstance(item, tk.Button):
                item.grid_forget()

    #CREATE FUNCTION TO COPY TEXT FROM TEXTBOX TO CLIPBOARD:
    def tree_c2c(self, *args):
        try:
            selected_txt = self.tree.selection_get()         
            self.master.clipboard_clear()
            self.master.clipboard_append(selected_txt)
        except tk.TclError:
            return

    #CREATE FUNCTION TO COPY TEXT FROM SEARCHBAR TO CLIPBOARD:
    def search_c2c(self, *args):
        try:
            selected_txt = self.searchbar.selection_get()
            self.master.clipboard_clear()
            self.master.clipboard_append(selected_txt)
            self.master.update()
        except tk.TclError:
            return
        
    #CREATE FUNCTION TO PASTE TEXT INTO SEARCHBAR FROM CLIPBOARD:
    def search_pfc(self, *args):
        try:
            content=self.master.clipboard_get()
            self.searchbar.insert(tk.END, content)
        except tk.TclError:
            return

    #CREATE FUNCTION TO OPEN 'ADD HOUSE' WINDOW:
    def open_addhouse(self, *args):
        self.newWindow=tk.Toplevel(self.master)
        self.app=self.addhouse_win(self.newWindow)

    #CREATE FUNCTION TO OPEN RIGHT CLICK MENU FOR TEXTBOX:
    def tree_do_popup(self, event):
        try:
            self.men_tree.tk_popup(event.x_root, event.y_root)
        finally:
            self.men_tree.grab_release()

    #CREATE FUNCTION TO OPEN RIGHT CLICK MENU FOR SEARCHBAR:
    def search_do_popup(self, event):
        try:
            self.men_search.tk_popup(event.x_root, event.y_root)
        finally:
            self.men_search.grab_release()

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
        
    #CREATE FILTER FOR SKILL BOOKS IN ALL HOUSES:
    def all_skill(self, *args):
        self.tree.delete(*self.tree.get_children())
        query_skill=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Skill Book" = "Yes"', con)
        headers=list(query_skill)
        rowlabels=query_skill['ID'].tolist()
        self.tree['columns']=headers
        self.tree['displaycolumns']=('Title', 'House', 'Room')
        self.tree.column('#0', stretch='NO', minwidth=0, width=0)
        self.tree.column('#1', stretch='YES', width=300, anchor=tk.CENTER)
        self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
        self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
        count=len(query_skill)
        for col in headers:
            self.tree.column(col)
            self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
        for i in range(count):
            self.tree.insert('', i, text=rowlabels[i], values=query_skill.iloc[i,:].tolist())

    #CREATE FILTER FOR SPELL TOMES IN ALL HOUSES:        
    def all_spell(self, *args):
        self.tree.delete(*self.tree.get_children())
        query_spell=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Spell Tome" = "Yes"', con)
        headers=list(query_spell)
        rowlabels=query_spell['ID'].tolist()
        self.tree['columns']=headers
        self.tree['displaycolumns']=('Title', 'House', 'Room')
        self.tree.column('#0', stretch='NO', minwidth=0, width=0)
        self.tree.column('#1', stretch='YES', minwidth=300, width=300, anchor=tk.CENTER)
        self.tree.column('#2', stretch='YES', minwidth=250, width=250, anchor=tk.CENTER)
        self.tree.column('#3', stretch='YES', minwidth=250, width=250, anchor=tk.CENTER)
        count=len(query_spell)
        for col in headers:
            self.tree.column(col)
            self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
        for i in range(count):
            self.tree.insert('', i, text=rowlabels[i], values=query_spell.iloc[i,:].tolist())

    #CREATE FILTER FOR REGULAR BOOKS IN ALL HOUSES: 
    def all_reg(self, *args):
        self.tree.delete(*self.tree.get_children())
        query_reg=pd.read_sql_query('SELECT * FROM "My Books" WHERE "Skill Book" = "No" AND "Spell Tome" = "No"', con)
        headers=list(query_reg)
        rowlabels=query_reg['ID'].tolist()
        self.tree['columns']=headers
        self.tree['displaycolumns']=('Title', 'House', 'Room')
        self.tree.column('#0', stretch='NO', minwidth=0, width=0)
        self.tree.column('#1', stretch='YES', minwidth=0, width=300, anchor=tk.CENTER)
        self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
        self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
        count=len(query_reg)
        for col in headers:
            self.tree.column(col)
            self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
        for i in range(count):
            self.tree.insert('', i, text=rowlabels[i], values=query_reg.iloc[i,:].tolist())

    #CREATE FILTER FOR SKILL BOOKS IN ALL ROOMS IN GIVEN HOUSE:
    def all_room_skill(self, *args):
        self.tree.delete(*self.tree.get_children())
        idxs_house = self.listbox_houses.curselection()
        HOUSE = self.listbox_houses.get(first=idxs_house)
        query_skill=pd.read_sql_query('SELECT * FROM "My Books" WHERE House=? AND "Skill Book" = "Yes"', con, params=(HOUSE,))
        headers=list(query_skill)
        rowlabels=query_skill['ID'].tolist()
        self.tree['columns']=headers
        self.tree['displaycolumns']=('Title', 'House', 'Room')
        self.tree.column('#0', stretch='NO', minwidth=0, width=0)
        self.tree.column('#1', stretch='YES', minwidth=0, width=300, anchor=tk.CENTER)
        self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
        self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
        count=len(query_skill)
        for col in headers:
            self.tree.column(col)
            self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
        for i in range(count):
            self.tree.insert('', i, text=rowlabels[i], values=query_skill.iloc[i,:].tolist())

    #CREATE FILTER FOR SPELL TOMES IN ALL ROOMS IN GIVEN HOUSE:
    def all_room_spell(self, *args):
        self.tree.delete(*self.tree.get_children())
        idxs_house = self.listbox_houses.curselection()
        HOUSE = self.listbox_houses.get(first=idxs_house)
        query_spell=pd.read_sql_query('SELECT * FROM "My Books" WHERE House=? AND "Spell Tome" = "Yes"', con, params=(HOUSE,))
        headers=list(query_spell)
        rowlabels=query_spell['ID'].tolist()
        self.tree['columns']=headers
        self.tree['displaycolumns']=('Title', 'House', 'Room')
        self.tree.column('#0', stretch='NO', minwidth=0, width=0)
        self.tree.column('#1', stretch='YES', minwidth=0, width=300, anchor=tk.CENTER)
        self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
        self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
        count=len(query_spell)
        for col in headers:
            self.tree.column(col)
            self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
        for i in range(count):
            self.tree.insert('', i, text=rowlabels[i], values=query_spell.iloc[i,:].tolist())

    #CREATE FILTER FOR REGULAR BOOKS IN ALL ROOMS IN GIVEN HOUSE:
    def all_room_reg(self, *args):
        self.tree.delete(*self.tree.get_children())
        idxs_house = self.listbox_houses.curselection()
        HOUSE = self.listbox_houses.get(first=idxs_house)
        query_reg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House=? AND "Skill Book" = "No" AND "Spell Tome" = "No"', con, params=(HOUSE,))
        headers=list(query_reg)
        rowlabels=query_reg['ID'].tolist()
        self.tree['columns']=headers
        self.tree['displaycolumns']=('Title', 'House', 'Room')
        self.tree.column('#0', stretch='NO', minwidth=0, width=0)
        self.tree.column('#1', stretch='YES', minwidth=0, width=300, anchor=tk.CENTER)
        self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
        self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
        count=len(query_reg)
        for col in headers:
            self.tree.column(col)
            self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
        for i in range(count):
            self.tree.insert('', i, text=rowlabels[i], values=query_reg.iloc[i,:].tolist())
            
    #CREATE FILTER FOR SKILL BOOKS IN ALL ROOMS IN GIVEN ROOM OF GIVEN HOUSE:
    def room_skill(self, *args):
        self.tree.delete(*self.tree.get_children())
        idxs_house = self.listbox_houses.curselection()
        HOUSE = self.listbox_houses.get(first=idxs_house)
        idxs_rooms = self.listbox_rooms.curselection()
        ROOM=self.listbox_rooms.get(first=idxs_rooms)
        query_skill=pd.read_sql_query('SELECT * FROM "My Books" WHERE House=? AND Room=? AND "Skill Book" = "Yes"', con, params=(HOUSE, ROOM))
        headers=list(query_skill)
        rowlabels=query_skill['ID'].tolist()
        self.tree['columns']=headers
        self.tree['displaycolumns']=('Title', 'House', 'Room')
        self.tree.column('#0', stretch='NO', minwidth=0, width=0)
        self.tree.column('#1', stretch='YES', minwidth=0, width=300, anchor=tk.CENTER)
        self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
        self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
        count=len(query_skill)
        for col in headers:
            self.tree.column(col)
            self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
        for i in range(count):
            self.tree.insert('', i, text=rowlabels[i], values=query_skill.iloc[i,:].tolist())

    #CREATE FILTER FOR SPELL TOMES IN ALL ROOMS IN GIVEN ROOM OF GIVEN HOUSE:
    def room_spell(self, *args):
        self.tree.delete(*self.tree.get_children())
        idxs_house = self.listbox_houses.curselection()
        HOUSE = self.listbox_houses.get(first=idxs_house)
        idxs_rooms = self.listbox_rooms.curselection()
        ROOM=self.listbox_rooms.get(first=idxs_rooms)
        query_spell=pd.read_sql_query('SELECT * FROM "My Books" WHERE House=? AND Room=? AND "Spell Tome" = "Yes"', con, params=(HOUSE, ROOM))
        headers=list(query_spell)
        rowlabels=query_spell['ID'].tolist()
        self.tree['columns']=headers
        self.tree['displaycolumns']=('Title', 'House', 'Room')
        self.tree.column('#0', stretch='NO', minwidth=0, width=0)
        self.tree.column('#1', stretch='YES', minwidth=0, width=300, anchor=tk.CENTER)
        self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
        self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
        count=len(query_spell)
        for col in headers:
            self.tree.column(col)
            self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
        for i in range(count):
            self.tree.insert('', i, text=rowlabels[i], values=query_spell.iloc[i,:].tolist())

    #CREATE FILTER FOR REGULAR BOOKS IN ALL ROOMS IN GIVEN ROOM OF GIVEN HOUSE:
    def room_reg(self, *args):
        self.tree.delete(*self.tree.get_children())
        idxs_house = self.listbox_houses.curselection()
        HOUSE = self.listbox_houses.get(first=idxs_house)
        idxs_rooms = self.listbox_rooms.curselection()
        ROOM=self.listbox_rooms.get(first=idxs_rooms)
        query_reg=pd.read_sql_query('SELECT * FROM "My Books" WHERE House=? AND Room=? AND "Skill Book" = "No" AND "Spell Tome" = "No"', con, params=(HOUSE, ROOM))
        headers=list(query_reg)
        rowlabels=query_reg['ID'].tolist()
        self.tree['columns']=headers
        self.tree['displaycolumns']=('Title', 'House', 'Room')
        self.tree.column('#0', stretch='NO', minwidth=0, width=0)
        self.tree.column('#1', stretch='YES', minwidth=0, width=300, anchor=tk.CENTER)
        self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
        self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
        count=len(query_reg)
        for col in headers:
            self.tree.column(col)
            self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
        for i in range(count):
            self.tree.insert('', i, text=rowlabels[i], values=query_reg.iloc[i,:].tolist())

    #CREATE FUNCTION TO SORT COLUMNS OF TREE:
    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
        #REARRANGE ITEMS IN SORTED POSITIONS:
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        #REVERSE SORT ON NEXT CLICK:
        tv.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(tv, _col, not reverse))

    #CREATE FUNCTION TO RESTART PROGRAM ON COMMAND:
    def restart(self):
            os.execv(sys.executable, ['python'] + sys.argv)

    #CREATE FUNCTION TO OPEN 'ADD HOUSE' WINDOW:
    def addhouse_win(self, *args):
        #CREATE FRAME AND SET TITLE OF WINDOW:
        self.newWindow.title('Add House')
        self.newWindow.resizable(False, False)
        self.frame_addhouse=tk.Frame(self.newWindow, bg='black')
        self.frame_addhouse.grid(row=0, column=0, sticky='news')
        #CREATE STRING VARIABLES FOR LISTBOXES:
        self.new_house = tk.StringVar()
        self.room_one = tk.StringVar()
        self.room_two = tk.StringVar()
        self.room_three = tk.StringVar()
        self.room_four = tk.StringVar()
        #CREATE LABEL AND TEXTBOX FOR NEW HOUSE NAME:
        self.lbl_add_house=tk.Label(self.frame_addhouse, text='Add House:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_add_house.grid(row=0, column=0, columnspan=3, sticky='ew')
        self.addhouse_bar=tk.Entry(self.frame_addhouse, textvariable=self.new_house, font=('Futura CondensedLight',15), bg='black', fg='white', insertbackground='white')
        self.addhouse_bar.grid(row=1, column=0, columnspan=3, sticky='ew')
        #CREATE LABEL AND TEXTBOX FOR ROOM 1 NAME:
        self.lbl_add_room1=tk.Label(self.frame_addhouse, text='Add First Room:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_add_room1.grid(row=2, column=0, columnspan=3, sticky='ew')
        self.addroom1_bar=tk.Entry(self.frame_addhouse, textvariable=self.room_one, font=('Futura CondensedLight',15), bg='black', fg='white', insertbackground='white')
        self.addroom1_bar.grid(row=3, column=0, columnspan=3, sticky='ew')
        #CREATE LABEL AND TEXTBOX FOR ROOM 2 NAME:
        self.lbl_add_room2=tk.Label(self.frame_addhouse, text='Add Second Room:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_add_room2.grid(row=4, column=0, columnspan=3, sticky='ew')
        self.addroom2_bar=tk.Entry(self.frame_addhouse, textvariable=self.room_two, font=('Futura CondensedLight',15), bg='black', fg='white', insertbackground='white')
        self.addroom2_bar.grid(row=5, column=0, columnspan=3, sticky='ew')
        #CREATE LABEL AND TEXTBOX FOR ROOM 3 NAME:
        self.lbl_add_room3=tk.Label(self.frame_addhouse, text='Add Third Room:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_add_room3.grid(row=6, column=0, columnspan=3, sticky='ew')
        self.addroom3_bar=tk.Entry(self.frame_addhouse, textvariable=self.room_three, font=('Futura CondensedLight',15), bg='black', fg='white', insertbackground='white')
        self.addroom3_bar.grid(row=7, column=0, columnspan=3, sticky='ew')
        #CREATE LABEL AND TEXTBOX FOR ROOM 4 NAME:
        self.lbl_add_room4=tk.Label(self.frame_addhouse, text='Add Fourth Room:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_add_room4.grid(row=8, column=0, columnspan=3, sticky='ew')
        self.addroom4_bar=tk.Entry(self.frame_addhouse, textvariable=self.room_four, font=('Futura CondensedLight',15), bg='black', fg='white', insertbackground='white')
        self.addroom4_bar.grid(row=9, column=0, columnspan=3, sticky='ew')
        #CREATE BUTTON TO EXECUTE COMMAND:
        self.btn_addhouse=tk.Button(self.frame_addhouse, text='Add House', command=lambda: [self.addhouse(), self.newWindow.destroy()], font=('Futura Condensed',15), bg='black', fg='white')
        self.btn_addhouse.grid(row=10, column=0, columnspan=3, sticky='ew')
    
    #CREATE FUNCTION TO ADD NEW HOUSES AND ROOMS AS SELECTABLE OPTIONS:
    def addhouse(self, *args):
        #GET NEW HOUSE AND ROOM NAMES:
        NEW_HOUSE=self.new_house.get()
        ROOM_ONE=self.room_one.get()
        ROOM_TWO=self.room_two.get()
        ROOM_THREE=self.room_three.get()
        ROOM_FOUR=self.room_four.get()
        #OPEN FILES TO WRITE NEW HOUSE NAME INTO FILES:
        with open('C:/Users/steph/Documents/Python/SB_EXE/main_lists/lists_main_houses.txt', 'r+') as file_houses_main:
            houses_main=file_houses_main.readline().rstrip('\n')
            file_houses_main.write(','+(NEW_HOUSE))
        with open('C:/Users/steph/Documents/Python/SB_EXE/add_move_lists/lists_addmove_houses.txt', 'r+') as file_houses_add_move:
            houses_add_move=file_houses_add_move.readline().rstrip('\n')
            if houses_add_move == '':
                file_houses_add_move.write((NEW_HOUSE))
            else:
                file_houses_add_move.write(','+(NEW_HOUSE))
        #OPEN FILES TO WRITE NEW ROOMS INTO LIST FOR MAIN WINDOW:
        with open('C:/Users/steph/Documents/Python/SB_EXE/main_lists/lists_main_allrooms.txt', 'a+') as file_all_rooms_main:
            file_all_rooms_main.write('\nAll Rooms')
            if ROOM_ONE == '':
                pass
            else:
                file_all_rooms_main.write(','+ROOM_ONE)
            if ROOM_TWO == '':
                pass
            else:
                file_all_rooms_main.write(','+ROOM_TWO)
            if ROOM_THREE == '':
                pass
            else:
                file_all_rooms_main.write(','+ROOM_THREE)
            if ROOM_FOUR == '':
                pass
            else:
                file_all_rooms_main.write(','+ROOM_FOUR)
        #OPEN FILES TO WRITE NEW ROOMS INTO LIST FOR ADD BOOK/MOVE BOOK WINDOWS:
        with open('C:/Users/steph/Documents/Python/SB_EXE/add_move_lists/lists_addmove_allrooms.txt', 'a+') as file_all_rooms_add_move:
            all_rooms_add_move=file_all_rooms_add_move.readlinews()
            if all_rooms_add_move== '':
                if ROOM_ONE == '':
                    pass
                else:
                    file_all_rooms_add_move.write((ROOM_ONE))
                if ROOM_TWO == '':
                    pass
                else:
                    file_all_rooms_add_move.write(','+(ROOM_TWO))
                if ROOM_THREE == '':
                    pass
                else:
                    file_all_rooms_add_move.write(','+(ROOM_THREE))
                if ROOM_FOUR == '':
                    pass
                else:
                    file_all_rooms_add_move.write(','+(ROOM_FOUR))
            else:
                if ROOM_ONE == '':
                    pass
                else:  
                    file_all_rooms_add_move.write('\n'+(ROOM_ONE))
                if ROOM_TWO == '':
                    pass
                else:
                    file_all_rooms_add_move.write(','+(ROOM_TWO))
                if ROOM_THREE == '':
                    pass
                else:
                    file_all_rooms_add_move.write(','+(ROOM_THREE))
                if ROOM_FOUR == '':
                    pass
                else:
                    file_all_rooms_add_move.write(','+(ROOM_FOUR))
        #RESTART THE PROGRAM FOR CHANGES TO TAKE EFFECT:
        self.restart()
        
    #CREATE SEARCH FUNCTION:
    def search(self, *event):
        self.tree.delete(*self.tree.get_children())
        self.btn_search.grid(row=6, column=0, columnspan=2, sticky='news')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        all_books=pd.read_sql_query('SELECT * FROM "My Books"', con)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        result=all_books.loc[all_books['Title'].str.contains(self.searchstring.get(), na=False, case=False)]
        headers=list(result)
        rowlabels=result['ID'].tolist()
        self.tree['columns']=headers
        self.tree['displaycolumns']=('Title', 'House', 'Room', 'Skill Book', 'Spell Tome')
        self.tree.column('#0', stretch='NO', minwidth=0, width=0)
        self.tree.column('#1', stretch='YES', minwidth=0, width=300, anchor=tk.CENTER)
        self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
        self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
        self.tree.column('#4', stretch='YES', anchor=tk.CENTER, width=100)
        self.tree.column('#5', stretch='YES', anchor=tk.CENTER, width=100)
        count=len(result)
        for col in headers:
            self.tree.column(col)
            self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
        for i in range(count):
            self.tree.insert('', i, text=rowlabels[i], values=result.iloc[i,:].tolist())

    #CREATE FUNCTION TO FILL LISTBOX_ROOMS:
    def fill_listbox_rooms(self, *args):
        self.forget_btns()
        self.tree.delete(*self.tree.get_children())
        self.style_tree.configure('Treeview', background='#E1C78C', fieldbackground='#E1C78C')
        self.btn_search.grid(row=6, column=0, columnspan=2, sticky='news')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.listbox_rooms.delete(0, tk.END)
        self.indxs=self.listbox_houses.curselection()
        if len(self.indxs)==1:
            indx=int(self.indxs[0])
            if indx==0:
                self.forget_btns()
                self.btn_search.grid(row=6, column=0, columnspan=2, sticky='news')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.listbox_rooms.insert(tk.END, 'All Rooms')
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table_all_rooms)
            elif indx>0:
                self.forget_btns()
                self.btn_search.grid(row=6, column=0, columnspan=2, sticky='news')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                for room in allrooms_main[indx].split(','):
                    self.listbox_rooms.insert(tk.END, room)
                self.listbox_rooms.bind('<<ListboxSelect>>', self.fill_table)

    #CREATE FUNCTION TO FILL TREE FOR ALL ROOMS IN ALL HOUSES:
    def fill_table_all_rooms(self, *args):         
        self.forget_btns()
        self.btn_search.grid(row=6, column=0, columnspan=2, sticky='news')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        idxs_rooms=self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                self.forget_btns()
                self.tree.delete(*self.tree.get_children())
                self.btn_search.grid(row=6, column=0, columnspan=2, sticky='news')
                self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
                self.btn_open_movebook.grid(row=0, column=2, sticky='news')
                self.btn_open_delbook.grid(row=0, column=3, sticky='news')
                self.btn_all_skill=tk.Button(self.frame, text='Skill Books', command=self.all_skill, font=('Futura Condensed',15), bg='black', fg='white')
                self.btn_all_skill.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_all_spell=tk.Button(self.frame, text='Spell Tomes', command=self.all_spell, font=('Futura Condensed',15), bg='black', fg='white')
                self.btn_all_spell.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_all_reg=tk.Button(self.frame, text='Spell Tomes', command=self.all_reg, font=('Futura Condensed',15), bg='black', fg='white')
                self.btn_all_reg.grid(row=5, column=0, columnspan=2, sticky='news')
                query=pd.read_sql_query('SELECT * FROM "My Books"', con)
                headers=list(query)
                rowlabels=query['ID'].tolist()
                self.tree['columns']=headers
                self.tree['displaycolumns']=('Title', 'House', 'Room')
                self.tree.column('#0', stretch='NO', minwidth=0, width=0)
                self.tree.column('#1', stretch='YES', minwidth=0, width=300, anchor=tk.CENTER)
                self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
                self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
                count=len(query)
                for col in headers:
                    self.tree.column(col)
                    self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
                for i in range(count):
                    self.tree.insert('', i, text=rowlabels[i], values=query.iloc[i,:].tolist())
            
    #CREATE FUNCTION TO FILL TREE FOR ALL ROOMS OF GIVEN HOUSE AND GIVEN ROOM OF GIVEN HOUSE:
    def fill_table(self, *args):
        self.forget_btns()
        self.btn_search.grid(row=6, column=0, columnspan=2, sticky='news')
        self.btn_open_addbook.grid(row=0, column=0, columnspan=2, sticky='news')
        self.btn_open_movebook.grid(row=0, column=2, sticky='news')
        self.btn_open_delbook.grid(row=0, column=3, sticky='news')
        self.tree.delete(*self.tree.get_children())
        idxs_house = self.listbox_houses.curselection()
        HOUSE = self.listbox_houses.get(first=idxs_house)
        idxs_rooms = self.listbox_rooms.curselection()
        if len(idxs_rooms)==1:
            idx_room=int(idxs_rooms[0])
            if idx_room==0:
                HOUSE = self.listbox_houses.get(first=idxs_house)
                ROOM = self.listbox_rooms.get(first=idx_room)
                query = pd.read_sql_query('SELECT * FROM "My Books" WHERE House=?', con, params=(HOUSE,))
                headers=list(query)
                rowlabels=query['ID'].tolist()
                self.tree['columns']=headers
                self.tree['displaycolumns']=('Title', 'House', 'Room')
                self.tree.column('#0', stretch='NO', minwidth=0, width=0)
                self.tree.column('#1', stretch='YES', minwidth=0, width=300, anchor=tk.CENTER)
                self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
                self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
                count=len(query)
                for col in headers:
                    self.tree.column(col)
                    self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
                for i in range(count):
                    self.tree.insert('', i, text=rowlabels[i], values=query.iloc[i,:].tolist())
                self.btn_all_room_skill=tk.Button(self.frame, text='Skill Books', command=self.all_room_skill, font=('Futura Condensed',15), bg='black', fg='white')
                self.btn_all_room_skill.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_all_room_spell=tk.Button(self.frame, text='Spell Tomes', command=self.all_room_spell, font=('Futura Condensed',15), bg='black', fg='white')
                self.btn_all_room_spell.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_all_room_reg=tk.Button(self.frame, text='Regular Books', command=self.all_room_reg, font=('Futura Condensed',15), bg='black', fg='white')
                self.btn_all_room_reg.grid(row=5, column=0, columnspan=2, sticky='news')
            elif idx_room>0:
                HOUSE = self.listbox_houses.get(first=idxs_house)
                ROOM = self.listbox_rooms.get(first=idx_room)
                query = pd.read_sql_query('SELECT * FROM "My Books" WHERE House=? AND Room=?', con, params=(HOUSE, ROOM,))
                headers=list(query)
                rowlabels=query['ID'].tolist()
                self.tree['columns']=headers
                self.tree['displaycolumns']=('Title', 'House', 'Room')
                self.tree.column('#0', stretch='NO', minwidth=0, width=0)
                self.tree.column('#1', stretch='YES', minwidth=0, width=300, anchor=tk.CENTER)
                self.tree.column('#2', stretch='YES', width=250, anchor=tk.CENTER)
                self.tree.column('#3', stretch='YES', anchor=tk.CENTER)
                count=len(query)
                for col in headers:
                    self.tree.column(col)
                    self.tree.heading(col, text=col, command=lambda _col=col:self.treeview_sort_column(self.tree, _col, False))
                for i in range(count):
                    self.tree.insert('', i, text=rowlabels[i], values=query.iloc[i,:].tolist())
                self.btn_room_skill=tk.Button(self.frame, text='Skill Books', command=self.room_skill, font=('Futura Condensed',15), bg='black', fg='white')
                self.btn_room_skill.grid(row=3, column=0, columnspan=2, sticky='news')
                self.btn_room_spell=tk.Button(self.frame, text='Spell Tomes', command=self.room_spell, font=('Futura Condensed',15), bg='black', fg='white')
                self.btn_room_spell.grid(row=4, column=0, columnspan=2, sticky='news')
                self.btn_room_reg=tk.Button(self.frame, text='Regular Books', command=self.room_reg, font=('Futura Condensed',15), bg='black', fg='white')
                self.btn_room_reg.grid(row=5, column=0, columnspan=2, sticky='news')

#CREATE 'ADD BOOK' WINDOW:
class addbook_win:
    def __init__(self, master):
        self.master=master
        self.master.resizable(False, False)
        self.master.title('Add Book')
        self.frame=tk.Frame(self.master, bg='black')
        self.frame.grid(row=0, column=0, sticky='news')
        #CREATE BOX AND LABEL FOR ADDING TITLE:
        self.lbl_addbook_title=tk.Label(self.frame, text='Enter Title:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_addbook_title.grid(row=0, column=0, sticky='ew')
        self.title=tk.StringVar()
        self.add_title=tk.Entry(self.frame, textvariable=self.title, font=('Futura CondensedLight',15), bg='black', fg='white')
        self.add_title.grid(row=0, column=1, columnspan=3, sticky='news')
        #CREATE LISTBOX AND LABEL FOR HOUSES TO SELECT:
        Houses_add_move = tk.StringVar(self.frame, value=houses_add_move.split(','))
        self.lbl_houses=tk.Label(self.frame, text='Select House:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_houses.grid(row=1, column=0, sticky='ew')
        self.listbox_houses=tk.Listbox(self.frame, listvariable=Houses_add_move, bg='black', fg='white', width=20, height=4)
        self.listbox_houses.config(font=('Futura CondensedLight',15))
        self.listbox_houses.grid(row=1, column=1, sticky='ew')
        self.listbox_houses.bind('<<ListboxSelect>>', self.select_house_addbook)
        #CREATE LISTBOX AND LABEL FOR ROOMS TO SELECT:
        self.lbl_rooms=tk.Label(self.frame, text='Select Room:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_rooms.grid(row=1, column=2, sticky='ew')
        self.listbox_rooms=tk.Listbox(self.frame, bg='black', fg='white', exportselection=False, width=20, height=4)
        self.listbox_rooms.config(font=('Futura CondensedLight',15))
        self.listbox_rooms.grid(row=1, column=3, sticky='ew')
        #CREATE LISTBOX AND LABEL FOR YES/NO OPTION FOR SKILL BOOKS:
        self.lbl_skill=tk.Label(self.frame, text='Skill Book:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_skill.grid(row=2, column=0, sticky='ew')
        self.lbsk=tk.StringVar(self.frame, value=list_binary_skill)
        self.listbox_skill=tk.Listbox(self.frame, listvariable=self.lbsk, bg='black', fg='white', exportselection=False, height=2)
        self.listbox_skill.config(font=('Futura CondensedLight',15))
        self.listbox_skill.grid(row=2, column=1, sticky='ew')
        #CREATE LISTBOX AND LABEL FOR YES/NO OPTION FOR SPELL TOMES:
        self.lbl_spell=tk.Label(self.frame, text='Spell Book:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_spell.grid(row=2, column=2, sticky='ew')
        self.lbsp=tk.StringVar(self.frame, value=list_binary_spell)
        self.listbox_spell=tk.Listbox(self.frame, listvariable=self.lbsp, bg='black', fg='white', exportselection=False, height=2)
        self.listbox_spell.config(font=('Futura CondensedLight',15))
        self.listbox_spell.grid(row=2, column=3, sticky='ew')
        #CREATE BUTTON TO ADD BOOK:
        self.btn_addbook=tk.Button(self.frame, text='Add Book', command=lambda: [self.addbook(), self.master.destroy()], font=('Futura Condensed',15), bg='black', fg='white')
        self.btn_addbook.grid(row=3, column=0, columnspan=4, sticky='ew')

    #CREATE FUNCTION TO FILL LISTBOX_ROOMS:
    def select_house_addbook(self, *args):
        self.listbox_rooms.delete(0, tk.END)
        self.indxs=self.listbox_houses.curselection()
        if len(self.indxs)==1:
            indx=int(self.indxs[0])
            for room in allrooms_add_move[indx].split(','):
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
            self.lbl_warn=tk.Label(self.warn_frame, text='A book with this title already exists', font=('Futura CondensedLight',15), bg='black', fg='white')
            self.lbl_warn.grid(row=0, column=0, sticky='news')
            self.btn_back=tk.Button(self.warn_frame, text='Return', command=self.warn_message.destroy, font=('Futura Condensed',15), bg='black', fg='white')
            self.btn_back.grid(row=1, column=0, sticky='news')
        else: 
            cur.execute('INSERT INTO "My Books" ("Title", "House", "Room", "Skill Book", "Spell Tome") VALUES (?, ?, ?, ?, ?)', (TITLE, HOUSE, ROOM, SKILL, SPELL))
            con.commit()

class movebook_win:
    def __init__(self, master):
        self.master=master
        self.master.title('Move Book')
        self.master.resizable(False, False)
        self.frame=tk.Frame(self.master)
        self.frame.grid(row=0, column=0, sticky='news')
        all_books=pd.read_sql_query('SELECT * FROM "My Books"', con)
        self.lbl_select_title=tk.Label(self.frame, text='Select Book:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_select_title.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.listbox_title=tk.Listbox(self.frame, bg='black', fg='white', exportselection=False)
        self.listbox_title.config(font=('Futura CondensedLight',15))
        self.listbox_title.grid(row=1, column=0, columnspan=2, sticky='news')
        for title in all_books["Title"].sort_values():
            self.listbox_title.insert(tk.END, title)
        #CREATE LISTBOX AND LABEL FOR HOUSES TO SELECT:
        Houses_add_move = tk.StringVar(self.frame, value=houses_add_move.split(','))
        self.lbl_houses=tk.Label(self.frame, text='Select House:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_houses.grid(row=2, column=0, sticky='ew')
        self.listbox_houses=tk.Listbox(self.frame, listvariable=Houses_add_move, bg='black', fg='white', width=20, height=4)
        self.listbox_houses.config(font=('Futura CondensedLight',15))
        self.listbox_houses.grid(row=3, column=0, sticky='ew')
        self.listbox_houses.bind('<<ListboxSelect>>', self.select_house_movebook)
        #CREATE LISTBOX AND LABEL FOR ROOMS TO SELECT:
        self.lbl_rooms=tk.Label(self.frame, text='Select Room:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_rooms.grid(row=2, column=1, sticky='ew')
        self.listbox_rooms=tk.Listbox(self.frame, bg='black', fg='white', exportselection=False, width=20, height=4)
        self.listbox_rooms.config(font=('Futura CondensedLight',15))
        self.listbox_rooms.grid(row=3, column=1, sticky='ew')
        #CREATE LISTBOX AND LABEL FOR YES/NO OPTION FOR SKILL BOOKS:
        self.lbl_skill=tk.Label(self.frame, text='Skill Book:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_skill.grid(row=4, column=0, sticky='ew')
        self.lbsk=tk.StringVar(self.frame, value=list_binary_skill)
        self.listbox_skill=tk.Listbox(self.frame, listvariable=self.lbsk, bg='black', fg='white', exportselection=False, height=2)
        self.listbox_skill.config(font=('Futura CondensedLight',15))
        self.listbox_skill.grid(row=5, column=0, sticky='ew')
        #CREATE LISTBOX AND LABEL FOR YES/NO OPTION FOR SPELL TOMES:
        self.lbl_spell=tk.Label(self.frame, text='Spell Book:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_spell.grid(row=4, column=1, sticky='ew')
        self.lbsp=tk.StringVar(self.frame, value=list_binary_spell)
        self.listbox_spell=tk.Listbox(self.frame, listvariable=self.lbsp, bg='black', fg='white', exportselection=False, height=2)
        self.listbox_spell.config(font=('Futura CondensedLight',15))
        self.listbox_spell.grid(row=5, column=1, sticky='ew')
        #CREATE BUTTON TO MOVE BOOK:
        self.btn_movebook=tk.Button(self.frame, text='Move Book', command=lambda: [self.movebook(), self.master.destroy()], font=('Futura Condensed',15), bg='black', fg='white')
        self.btn_movebook.grid(row=6, column=0, columnspan=2, sticky='ew')

    def select_house_movebook(self, *args):
        self.listbox_rooms.delete(0, tk.END)
        self.indxs=self.listbox_houses.curselection()
        if len(self.indxs)==1:
            indx=int(self.indxs[0])
            for room in allrooms_add_move[indx].split(','):
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
        self.master.resizable(False, False)
        self.frame=tk.Frame(self.master)
        self.frame.grid(row=0, column=0, sticky='news')
        all_books=pd.read_sql_query('SELECT * FROM "My Books"', con)
        self.lbl_select_title=tk.Label(self.frame, text='Select Book:', font=('Futura Condensed',15), bg='black', fg='white')
        self.lbl_select_title.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.listbox_title=tk.Listbox(self.frame, bg='black', fg='white', exportselection=False, width=42)
        self.listbox_title.config(font=('Futura CondensedLight',15))
        self.listbox_title.grid(row=1, column=0, sticky='news')
        for title in all_books["Title"].sort_values():
            self.listbox_title.insert(tk.END, title)
        #CREATE BUTTON TO DELETE BOOK:
        self.btn_delbook=tk.Button(self.frame, text='Delete Book', command=lambda: [self.delbook(), self.master.destroy()], font=('Futura Condensed',15), bg='black', fg='white')
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
