import csv
import os
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox as ms

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

with sqlite3.connect('login_details.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (sapid TEXT NOT NULL ,password TEXT NOT NULL);')
db.commit()
db.close()

with sqlite3.connect('user_details.db') as db1:
    c1 = db1.cursor()

c1.execute(
    'CREATE TABLE IF NOT EXISTS user1(sapid TEXT NOT NULL, name TEXT NOT NULL, course TEXT NOT NULL, stream TEXT NOT NULL, sem TEXT NOT NULL);')
db1.commit()
db1.close()


class main:
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.at = []
        self.to = []
        self.name = StringVar()
        self.course = StringVar()
        self.stream = StringVar()
        self.sem = StringVar()
        self.widgets()

    def widgets(self):

        self.head = Label(self.master, text='LOGIN', font=('Comic Sans MS', 35, 'bold'), pady=10, bg='#c05c7e',
                          padx=20, bd=3, relief='raised')
        self.head.pack(pady=100)
        self.logf = Frame(self.master, padx=10, pady=10, bg='#2d3561')
        Label(self.logf, text='SAP ID: ', font=('Times New Roman', 15, 'italic'), pady=5, padx=5, bg='#f090d9', bd=5,
              relief='raised').grid(sticky=W + E, pady=15, padx=10)
        Entry(self.logf, textvariable=self.username, bd=5, font=('Times New Roman', 15, 'italic'), bg='#fdeaab').grid(
            row=0, column=1)

        Label(self.logf, text='Password: ', font=('Times New Roman', 15, 'italic'), pady=5, padx=5, bg='#f090d9', bd=5,
              relief='raised').grid(sticky=W + E, pady=15, padx=10)
        Entry(self.logf, textvariable=self.password, bd=5, font=('Times New Roman', 15, 'italic'), show='*',
              bg='#fdeaab').grid(row=1,
                                 column=1)

        Button(self.logf, text=' Login ', bd=5, font=('Times New Roman', 15, 'bold'), padx=2, pady=5, bg='#f3826f',
               command=self.login).grid(pady=30)
        Button(self.logf, text=' Create Account ', bd=5, font=('Times New Roman', 15, 'bold'), padx=2, pady=5,
               bg='#f3826f',
               command=self.cr).grid(row=2, column=1, pady=30)
        self.logf.pack(pady=50)

        self.crf = Frame(self.master, padx=10, pady=10, bg='#2d3561')
        Label(self.crf, text='SAP ID: ', font=('Times New Roman', 15, 'italic'), pady=5, padx=5, bg='#f090d9', bd=5,
              relief='raised').grid(sticky=W + E, pady=15, padx=10)
        Entry(self.crf, textvariable=self.n_username, bd=3, font=('Times New Roman', 15, 'italic'), bg='#fdeaab').grid(
            row=0,
            column=1)

        Label(self.crf, text='Password: ', font=('Times New Roman', 15, 'italic'), pady=5, padx=5, bg='#f090d9', bd=5,
              relief='raised').grid(sticky=W + E, pady=15, padx=10)
        Entry(self.crf, textvariable=self.n_password, bd=3, font=('Times New Roman', 15, 'italic'), show='*',
              bg='#fdeaab').grid(
            row=1, column=1)

        Label(self.crf, text='Name: ', font=('Times New Roman', 15, 'italic'), pady=5, padx=5, bg='#f090d9', bd=5,
              relief='raised').grid(sticky=W + E, pady=15, padx=10)
        Entry(self.crf, textvariable=self.name, bd=3, font=('Times New Roman', 15, 'italic'), bg='#fdeaab').grid(
            row=2, column=1)

        Label(self.crf, text='Select Course ', font=('Times New Roman', 15, 'italic'), pady=5, padx=5, bg='#f090d9',
              bd=5,
              relief='raised').grid(sticky=W + E, pady=15, padx=10)
        choices = {'BTech'}
        self.course.set('')
        popupmenu = OptionMenu(self.crf, self.course, *choices)
        popupmenu.config(bg='#fdeaab')
        popupmenu.grid(sticky=W + E, row=3, column=1)

        Label(self.crf, text='Select Stream ', font=('Times New Roman', 15, 'italic'), pady=5, padx=5, bg='#f090d9',
              bd=5,
              relief='raised').grid(sticky=W + E, pady=15, padx=10)
        choices = {'Computer Science'}
        self.course.set('')
        popupmenu = OptionMenu(self.crf, self.stream, *choices)
        popupmenu.config(bg='#fdeaab')
        popupmenu.grid(sticky=W + E, row=4, column=1)

        Label(self.crf, text='Select Semester ', font=('Times New Roman', 15, 'italic'), pady=5, padx=5, bg='#f090d9',
              bd=5,
              relief='raised').grid(sticky=W + E, pady=15, padx=10)
        choices = {'V'}
        self.course.set('')
        popupmenu = OptionMenu(self.crf, self.sem, *choices)
        popupmenu.config(bg='#fdeaab')
        popupmenu.grid(sticky=W + E, row=5, column=1)

        Button(self.crf, text='Create Account', bd=5, font=('Times New Roman', 15, 'bold'), padx=5, pady=5,
               command=self.new_user, bg='#f3826f').grid(pady=30)
        Button(self.crf, text='Go to Login', bd=5, font=('Times New Roman', 15, 'bold'), padx=5, pady=5,
               command=self.log, bg='#f3826f').grid(row=6, column=1, pady=30)

    ############################LOGIN#############################################

    def login(self):
        self.f = open('user.txt', "w+")
        self.f1 = open('userdet.txt', "w+")
        with sqlite3.connect('login_details.db') as db:
            c = db.cursor()

        with sqlite3.connect('user_details.db') as db1:
            c1 = db1.cursor()

        find_user = ('SELECT * FROM user WHERE sapid = ? and password = ?')
        c.execute(find_user, [(self.username.get()), (self.password.get())])
        result = c.fetchall()
        find_user1 = ('SELECT * FROM user1 WHERE sapid = ?')
        c1.execute(find_user1, [(self.username.get())])
        result1 = c1.fetchall()
        self.o1 = result1[0][0]
        self.o2 = result1[0][1]
        self.o3 = result1[0][2]
        self.o4 = result1[0][3]
        self.o5 = result1[0][4]
        if result:
            self.logf.pack_forget()
            self.f.write(self.username.get())
            self.f1.write(self.o1 + "\n" + self.o2 + "\n" + self.o3 + "\n" + self.o4 + "\n" + self.o5)
            self.head.forget()
            self.logf.forget()
            self.openhome()

        else:
            ms.showerror('Try again..', 'SAP ID or Password does not match.')

        self.f.close()
        self.f1.close()

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    ###############################NEW USER#######################################

    def new_user(self):
        with sqlite3.connect('login_details.db') as db:
            c = db.cursor()

        with sqlite3.connect('user_details.db') as db1:
            c1 = db1.cursor()

        subs = ['SE', 'MPMC', 'DAA', 'CG', 'DSP', 'RM', 'PA']
        att = [0, 0, 0, 0, 0, 0, 0]
        tot = [0, 0, 0, 0, 0, 0, 0]
        myDict = {"Subjects": subs, "Attended": att, "Total": tot}
        df = pd.DataFrame(myDict)

        find_user = ('SELECT * FROM user WHERE sapid = ?')
        c.execute(find_user, [(self.username.get())])
        if c.fetchall():
            ms.showerror('Error', 'SAP ID already used.')
            self.widgets()
        else:
            if ((
                    self.n_username.get() or self.n_password.get() or self.name.get() or self.course.get() or self.sem.get() or self.stream.get()) == ''):
                ms.showinfo('Fields empty', 'Please fill in all fields')
                return
            ms.showinfo('Success!', 'Account Created!')
            a = self.n_username.get()
            df.to_csv(str(a) + '.csv', index=False)
            self.log()
        insert = 'INSERT INTO user(sapid,password) VALUES(?,?)'
        c.execute(insert, [(self.n_username.get()), (self.n_password.get())])
        db.commit()

        insert1 = 'INSERT INTO user1(sapid,name,course,stream,sem) VALUES(?,?,?,?,?)'
        c1.execute(insert1, [(self.n_username.get()), (self.name.get()), (self.course.get()), (self.stream.get()),
                             (self.sem.get())])
        db1.commit()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()

    #######################################HOME###################################

    def openhome(self):
        self.home = Frame(self.master, padx=10, pady=10, bg='#2d3561')
        Button(self.home, text=' View\nAttendance ', bd=5, font=('Times New Roman', 15, 'bold'), padx=5, pady=5,
               command=self.view, bg='#f3826f').grid(row=0, column=0, padx=30, pady=100)
        Button(self.home, text=' Add\nAttendance ', bd=5, font=('Times New Roman', 15, 'bold'), padx=5, pady=5,
               command=self.add, bg='#f3826f').grid(row=0, column=1, padx=30, pady=100)
        Button(self.home, text=' Search details ', bd=5, font=('Times New Roman', 15, 'bold'), padx=5,
               pady=5,
               command=self.search, bg='#f3826f').grid(row=1, padx=30, pady=30)
        Button(self.home, text=' Generate pdf ', bd=5, font=('Times New Roman', 15, 'bold'), padx=5,
               pady=5,
               command=self.gen, bg='#f3826f').grid(row=1, column=1, padx=30, pady=30)

        self.home.pack(fill="none", expand=True)

    #######################################BACK BUTTON#############################

    def backv(self):
        self.v.forget()
        self.openhome()

    def backa(self):
        self.a.forget()
        self.openhome()

    def backs(self):
        self.l.forget()
        self.openhome()

    def backs1(self):
        self.l1.forget()
        self.openhome()

    #######################################VIEW ATTENDANCE###########################

    def view(self):
        f = open('user.txt', 'r')
        si = f.read()
        filename = si + '.csv'
        fields = []
        rows = []
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                fields.append(row)
                break
            for row in csvreader:
                rows.append(row)
        self.home.forget()
        self.v = Frame(self.master, padx=10, pady=10, bg='#2d3561')
        Label(self.v, text=fields[0][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'),
              pady=30, bg='#f090d9', bd=5, padx=20).grid(row=0, column=0, sticky=E + W)
        Label(self.v, text=fields[0][1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'),
              pady=30, bg='#f090d9', bd=5, padx=20).grid(row=0, column=1, sticky=E + W)
        Label(self.v, text='  ' + fields[0][2] + '  ', borderwidth=2, relief="raised",
              font=('Times New Roman', 15, 'italic'),
              pady=30, bg='#f090d9', bd=5, padx=20).grid(row=0, column=2, sticky=E + W)
        Label(self.v, text="Percentage", borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'),
              pady=30, bg='#f090d9', bd=5, padx=20).grid(row=0, column=3, sticky=E + W)
        Label(self.v, text="Safe Bunks", borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'),
              pady=30, bg='#f090d9', bd=5, padx=20).grid(row=0, column=4, sticky=E + W)

        Label(self.v, text=rows[0][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=1, column=0, sticky=E + W)
        Label(self.v, text=rows[1][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=2, column=0, sticky=E + W)
        Label(self.v, text=rows[2][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=3, column=0, sticky=E + W)
        Label(self.v, text=rows[3][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=4, column=0, sticky=E + W)
        Label(self.v, text=rows[4][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=5, column=0, sticky=E + W)
        Label(self.v, text=rows[5][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=6, column=0, sticky=E + W)
        Label(self.v, text=rows[6][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=7, column=0, sticky=E + W)

        Label(self.v, text=rows[0][1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=1, column=1, sticky=E + W)
        Label(self.v, text=rows[1][1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=2, column=1, sticky=E + W)
        Label(self.v, text=rows[2][1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=3, column=1, sticky=E + W)
        Label(self.v, text=rows[3][1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=4, column=1, sticky=E + W)
        Label(self.v, text=rows[4][1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=5, column=1, sticky=E + W)
        Label(self.v, text=rows[5][1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=6, column=1, sticky=E + W)
        Label(self.v, text=rows[6][1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=7, column=1, sticky=E + W)

        Label(self.v, text=rows[0][2], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=1, column=2, sticky=E + W)
        Label(self.v, text=rows[1][2], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=2, column=2, sticky=E + W)
        Label(self.v, text=rows[2][2], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=3, column=2, sticky=E + W)
        Label(self.v, text=rows[3][2], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=4, column=2, sticky=E + W)
        Label(self.v, text=rows[4][2], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=5, column=2, sticky=E + W)
        Label(self.v, text=rows[5][2], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=6, column=2, sticky=E + W)
        Label(self.v, text=rows[6][2], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=7, column=2, sticky=E + W)

        a = []
        for i in range(7):
            if (int(rows[i][2]) == 0):
                a.append(0)

            else:
                a.append(round((int(rows[i][1]) / int(rows[i][2]) * 100), 1))

        Label(self.v, text=a[0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=1, column=3, sticky=E + W)
        Label(self.v, text=a[1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=2, column=3, sticky=E + W)
        Label(self.v, text=a[2], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=3, column=3, sticky=E + W)
        Label(self.v, text=a[3], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=4, column=3, sticky=E + W)
        Label(self.v, text=a[4], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=5, column=3, sticky=E + W)
        Label(self.v, text=a[5], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=6, column=3, sticky=E + W)
        Label(self.v, text=a[6], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=7, column=3, sticky=E + W)

        b = []
        for i in range(7):
            co = 0
            if (a[i] <= 80):
                b.append(0)

            else:
                x1 = int(rows[i][1])
                x2 = int(rows[i][2])
                x3 = a[i] / 100
                while (x3 >= 0.8):
                    x2 = x2 + 1
                    co = co + 1
                    x3 = x1 / x2
                b.append(co)

        Label(self.v, text=b[0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=1, column=4, sticky=E + W)
        Label(self.v, text=b[1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=2, column=4, sticky=E + W)
        Label(self.v, text=b[2], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=3, column=4, sticky=E + W)
        Label(self.v, text=b[3], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=4, column=4, sticky=E + W)
        Label(self.v, text=b[4], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=5, column=4, sticky=E + W)
        Label(self.v, text=b[5], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=6, column=4, sticky=E + W)
        Label(self.v, text=b[6], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=7, column=4, sticky=E + W)

        Button(self.v, text=' Back ', bd=5, font=('Times New Roman', 15, 'bold'), padx=5, pady=5,
               command=self.backv, bg='#f3826f').grid(sticky=W, padx=30, pady=50)

        self.v.pack(fill="none", expand=True)

    ##########################################ADD ATTENDANCE#########################################

    def add(self):
        f = open('user.txt', 'r')
        si = f.read()
        filename = si + '.csv'
        fields = []
        rows = []
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                fields.append(row)
                break
            for row in csvreader:
                rows.append(row)
        self.a = Frame(self.master, padx=10, pady=10, bg='#2d3561')

        self.home.pack_forget()

        Label(self.a, text=fields[0][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'),
              bg='#f090d9', bd=5, pady=30, padx=20).grid(row=0, column=0, sticky=E + W)
        Label(self.a, text=fields[0][1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'),
              bg='#f090d9', bd=5, pady=30, padx=20).grid(row=0, column=1, sticky=E + W)
        Label(self.a, text=' ' + fields[0][2] + ' ', borderwidth=2, relief="raised",
              bg='#f090d9', bd=5, font=('Times New Roman', 15, 'italic'),
              pady=30, padx=20).grid(row=0, column=2, sticky=E + W)

        Label(self.a, text=rows[0][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=1, column=0, sticky=E + W)
        Label(self.a, text=rows[1][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=2, column=0, sticky=E + W)
        Label(self.a, text=rows[2][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=3, column=0, sticky=E + W)
        Label(self.a, text=rows[3][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=4, column=0, sticky=E + W)
        Label(self.a, text=rows[4][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=5, column=0, sticky=E + W)
        Label(self.a, text=rows[5][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=6, column=0, sticky=E + W)
        Label(self.a, text=rows[6][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'), pady=30,
              bg='#f090d9', bd=5, padx=20).grid(row=7, column=0, sticky=E + W)

        Button(self.a, text=' Back ', bd=5, font=('Times New Roman', 15, 'bold'), padx=5, pady=5,
               command=self.backa, bg='#f3826f').grid(padx=30, pady=50)
        Button(self.a, text=' Submit ', bd=5, font=('Times New Roman', 15, 'bold'), padx=5, pady=5,
               command=self.submit, bg='#f3826f').grid(column=2, padx=30, pady=50, row=8)

        for i in range(1, 8):
            var = StringVar()
            Entry(self.a, textvariable=var, bd=3, font=('Times New Roman', 15, 'italic'), bg='#fdeaab').grid(row=i,
                                                                                                             column=1,
                                                                                                             padx=5)
            self.at.append(var)

        for i in range(1, 8):
            var = StringVar()
            Entry(self.a, textvariable=var, bd=3, font=('Times New Roman', 15, 'italic'), bg='#fdeaab').grid(row=i,
                                                                                                             column=2,
                                                                                                             padx=5)
            self.to.append(var)

        self.a.pack(fill="none", expand=True)

    def submit(self):
        f = open('user.txt', 'r')
        si = f.read()
        filename = si + '.csv'
        fields = []
        rows = []
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                fields.append(row)
                break
            for row in csvreader:
                rows.append(row)

        for i in range(7):
            if ((self.at[i].get() != '') and (self.to[i].get() != '')):
                if (int(self.at[i].get()) > int(self.to[i].get())):
                    ms.showerror('Error', 'Attended is greater than total')
                    self.a.forget()
                    self.openhome()
                    return

            if ((self.at[i].get() == '') and (self.to[i].get() != '')):
                ms.showerror('Error', 'Fields incomplete')
                self.a.forget()
                self.openhome()
                return

            if ((self.at[i].get() != '') and (self.to[i].get() == '')):
                ms.showerror('Error', 'Fields incomplete')
                self.a.forget()
                self.openhome()
                return

        prat = []
        prto = []
        for i in range(7):
            prat.append(rows[i][1])
            prto.append(rows[i][2])

        for i in range(7):
            if (self.at[i].get() == ''):
                pass
            else:
                o = int(prat[i])
                o += int(self.at[i].get())
                prat[i] = o

        for i in range(7):
            if (self.to[i].get() == ''):
                pass
            else:
                o = int(prto[i])
                o += int(self.to[i].get())
                prto[i] = o

        subs = ['SE', 'MPMC', 'DAA', 'CG', 'DSP', 'RM', 'PA']
        att = []
        tot = []
        for i in range(7):
            att.append(prat[i])
            tot.append(prto[i])
        myDict = {"Subjects": subs, "Attended": att, "Total": tot}
        df = pd.DataFrame(myDict)
        df.to_csv(si + '.csv', index=False)
        self.a.forget()
        self.openhome()

    ############################################SEARCH#################################################

    def search(self):
        f = open('users.txt', 'w+')
        self.home.forget()
        self.l = Frame(self.master, padx=10, pady=10, bg='#2d3561')
        Label(self.l, text="Enter SAP ID: ", borderwidth=2, relief="raised", font=('Times New Roman', 15, 'italic'),
              pady=30, bg='#f090d9', bd=5, padx=20).grid(padx=30, pady=50)
        self.vari = StringVar()
        Entry(self.l, textvariable=self.vari, bd=3, font=('Times New Roman', 15, 'italic'), bg='#fdeaab').grid(row=0,
                                                                                                               column=1,
                                                                                                               padx=30,
                                                                                                               pady=50)

        Button(self.l, text=' Back ', bd=5, font=('Times New Roman', 15, 'bold'), padx=5, pady=5, command=self.backs,
               bg='#f3826f').grid(padx=30, pady=50)
        Button(self.l, text=' Search ', bd=5, font=('Times New Roman', 15, 'bold'), padx=5, pady=5, command=self.su,
               bg='#f3826f').grid(column=1, padx=30, pady=50, row=1)

        self.l.pack(fill="none", expand=True)

    def su(self):
        f = open('users.txt', 'w+')
        f.write(self.vari.get())
        f.close()
        f = open('users.txt', 'r')
        si = f.read()
        with sqlite3.connect('user_details.db') as db1:
            c1 = db1.cursor()
        find_user = ('SELECT * FROM user1 WHERE sapid = ?')
        c1.execute(find_user, [(self.username.get())])
        if c1.fetchall():
            self.su1()

        else:
            ms.showinfo('The account is not registered')
            self.l.forget()
            self.openhome()

    def su1(self):
        f = open('users.txt', 'r')
        si = f.read()
        f1 = open('userdet.txt', 'w+')
        with sqlite3.connect('user_details.db') as db1:
            c1 = db1.cursor()

        find_user1 = ('SELECT * FROM user1 WHERE sapid = ?')
        c1.execute(find_user1, [(self.username.get())])
        result1 = c1.fetchall()
        self.o1 = result1[0][0]
        self.o2 = result1[0][1]
        self.o3 = result1[0][2]
        self.o4 = result1[0][3]
        self.o5 = result1[0][4]
        f1.write(self.o1 + "\n" + self.o2 + "\n" + self.o3 + "\n" + self.o4 + "\n" + self.o5)
        f1.close()
        f1 = open('userdet.txt', 'r')
        a = []
        count = 0
        for row in f1.readlines():
            a.append(row)
            count += 1

        for i in range(count - 1):
            l = len(a[i])
            a[i] = a[i][:l - 1]
        self.l.forget()
        self.l1 = Frame(self.master, padx=10, pady=10, bg='#2d3561')

        Label(self.l1, text='SAP ID: ', font=('Times New Roman', 15, 'italic'),
              pady=30, padx=20, bg='#2d3561', foreground='white').grid(sticky=W)
        Label(self.l1, text=a[0], font=('Times New Roman', 15, 'italic'),
              pady=30, padx=20, bg='#2d3561', foreground='white').grid(row=0, column=1)
        Label(self.l1, text='Name: ', font=('Times New Roman', 15, 'italic'),
              pady=30, padx=20, bg='#2d3561', foreground='white').grid(sticky=W)
        Label(self.l1, text=a[1], font=('Times New Roman', 15, 'italic'),
              pady=30, padx=20, bg='#2d3561', foreground='white').grid(row=1, column=1)
        Label(self.l1, text='Course: ', font=('Times New Roman', 15, 'italic'),
              pady=30, padx=20, bg='#2d3561', foreground='white').grid(sticky=W)
        Label(self.l1, text=a[2], font=('Times New Roman', 15, 'italic'),
              pady=30, padx=20, bg='#2d3561', foreground='white').grid(row=2, column=1)
        Label(self.l1, text='Stream: ', font=('Times New Roman', 15, 'italic'),
              pady=30, padx=20, bg='#2d3561', foreground='white').grid(sticky=W)
        Label(self.l1, text=a[3], font=('Times New Roman', 15, 'italic'),
              pady=30, padx=20, bg='#2d3561', foreground='white').grid(row=3, column=1)
        Label(self.l1, text='Semester: ', font=('Times New Roman', 15, 'italic'),
              pady=30, padx=20, bg='#2d3561', foreground='white').grid(sticky=W)
        Label(self.l1, text=a[4], font=('Times New Roman', 15, 'italic'),
              pady=30, padx=20, bg='#2d3561', foreground='white').grid(row=4, column=1)
        Button(self.l1, text=' Back ', bd=5, font=('Times New Roman', 15, 'bold'), padx=5, pady=5, command=self.backs1,
               bg='#f3826f').grid(padx=30, pady=50)

        self.l1.pack(fill="none", expand=True)

    ###########################################GEN##################################################

    def gen(self):

        # container for the 'Flowable' objects
        elements = []
        f = open('user.txt', 'r')
        si = f.read()
        path = 'D:/Sem 5/SE/MiniProject/.idea'
        nm = "Attendance Report - " + si + ".pdf"
        x = os.path.join(path, nm)
        doc = SimpleDocTemplate(x, pagesize=letter)
        filename = si + '.csv'
        fields = []
        rows = []
        data = []
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)
                break
            for row in csvreader:
                data.append(row)

        t = Table(data)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (2, 0), colors.orange),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        elements.append(t)
        # write the document to disk
        doc.build(elements)
        os.startfile(x)


root = tk.Tk()
root.config(bg='#2d3561')
root.attributes('-fullscreen', True)
root.bind("<Escape>", exit)
main(root)
root.mainloop()
