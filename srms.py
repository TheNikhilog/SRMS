import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class std():
    def _init_(self,root):
        self.root = root
        self.root.title("Student Record")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        title = tk.Label(self.root, text="Student Record Management System", bd=4, relief="groove", font=("Arial", 50, "bold"), bg="light gray")
        title.pack(side="top", fill="x")
        
        # Add frame
        addFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(240, 150, 100))
        addFrame.place(width=self.width/3, height=self.height-180, x=50, y=100)

        # Input labels and entries
        labels = ["RollNo:", "Std_Name:", "F_Name:", "Subject:", "CGPA:"]
        self.entries = []
        for i, label in enumerate(labels):
            lbl = tk.Label(addFrame, text=label, background=self.clr(240, 150, 100), fg="white", font=("Arial", 15, "bold"))
            lbl.grid(row=i, column=0, padx=20, pady=20)
            entry = tk.Entry(addFrame, bd=2, width=20, font=("Arial", 15))
            entry.grid(row=i, column=1, padx=10, pady=20)
            self.entries.append(entry)

        # Buttons
        addBtn = tk.Button(addFrame, command=self.insertFun, text="Add Student", width=20, font=("Arial", 20, "bold"), bd=3, relief="raised")
        addBtn.grid(row=5, column=0, padx=30, pady=50, columnspan=2)

        updateBtn = tk.Button(addFrame, command=self.updateFun, text="Update Student", width=20, font=("Arial", 20, "bold"), bd=3, relief="raised")
        updateBtn.grid(row=6, column=0, padx=30, pady=20, columnspan=2)

        # Detail frame
        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(100, 150, 240))
        self.detFrame.place(width=self.width/2 + 60, height=self.height - 180, x=self.width/3 + 100, y=100)

        # Search options
        optLbl = tk.Label(self.detFrame, text="Options:", bg=self.clr(100, 150, 240), fg="white", font=("Arial", 15, "bold"))
        optLbl.grid(row=0, column=0, padx=20, pady=20)
        self.optIn = ttk.Combobox(self.detFrame, width=17, values=("RollNo", "Name", "Subject"), font=("Arial", 15, "bold"))
        self.optIn.set("Select Option")
        self.optIn.grid(row=0, column=1, padx=10, pady=20)

        valLbl = tk.Label(self.detFrame, text="Value:", bg=self.clr(100, 150, 240), fg="white", font=("Arial", 15, "bold"))
        valLbl.grid(row=0, column=2, padx=10, pady=20)
        self.valIn = tk.Entry(self.detFrame, width=18, font=("Arial", 15), bd=2)
        self.valIn.grid(row=0, column=3, padx=10, pady=20)

        # Button frame
        btnFrame = tk.Frame(self.detFrame, bd=4, relief="solid", bg=self.clr(120, 150, 220))
        btnFrame.place(width=self.width/2 + 20, height=70, x=18, y=70)

        srchBtn = tk.Button(btnFrame, command=self.srchFun, text="Search", width=10, bd=2, relief="raised", font=("Arial", 15, "bold"))
        srchBtn.grid(row=0, column=0, padx=35, pady=12)

        delBtn = tk.Button(btnFrame, command=self.delFun, text="Delete", width=10, bd=2, relief="raised", font=("Arial", 15, "bold"))
        delBtn.grid(row=0, column=1, padx=35, pady=12)

        allBtn = tk.Button(btnFrame, command=self.showAll, text="Show_All", width=10, bd=2, relief="raised", font=("Arial", 15, "bold"))
        allBtn.grid(row=0, column=2, padx=35, pady=12)

        # Table for displaying records
        self.tabFun()

    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=5, relief="sunken")
        tabFrame.place(width=self.width/2 + 20, height=370, x=17, y=150)
        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")
        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")
        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set, columns=("rn", "name", "fname", "sub", "grade"))
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        self.table.heading("rn", text="Roll_No")
        self.table.heading("name", text="Std_Name")
        self.table.heading("fname", text="F_Name")
        self.table.heading("sub", text="Subject")
        self.table.heading("grade", text="CGPA")
        self.table["show"] = "headings"
        self.table.column("rn", width=100)
        self.table.column("name", width=150)
        self.table.column("fname", width=150)
        self.table.column("sub", width=120)
        self.table.column("grade", width=80)
        self.table.pack(fill="both", expand=1)

    def insertFun(self):
        rn = self.entries[0].get()
        name = self.entries[1].get()
        fname = self.entries[2].get()
        sub = self.entries[3].get()
        grade = self.entries[4].get()
        if rn and name and fname and sub and grade:
            try:
                self.dbFun()
                self.cur.execute("INSERT INTO stu(rollNo, name, fname, subject, cgpa) VALUES(%s, %s, %s, %s, %s)", (rn, name, fname, sub, grade))
                self.con.commit()
                tk.messagebox.showinfo("Success", f"Student {name} is Registered")
                self.clearFun()
                self.showAll()  # Refresh the table
                self.con.close()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
        else:
            tk.messagebox.showerror("Error", "Please fill all input fields!")

    def updateFun(self):
        rn = self.entries[0].get()
        name = self.entries[1].get()
        fname = self.entries[2].get()
        sub = self.entries[3].get()
        grade = self.entries[4].get()
        if rn and name and fname and sub and grade:
            try:
                self.dbFun()
                self.cur.execute("UPDATE stu SET name=%s, fname=%s, subject=%s, cgpa=%s WHERE rollNo=%s", (name, fname, sub, grade, rn))
                self.con.commit()
                tk.messagebox.showinfo("Success", f"Student {name}'s record updated successfully!")
                self.clearFun()
                self.showAll()  # Refresh the table
                self.con.close()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
        else:
            tk.messagebox.showerror("Error", "Please fill all input fields!")

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="Ritesh@123", database="student")
        self.cur = self.con.cursor()

    def clearFun(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def srchFun(self):
        opt = self.optIn.get()
        val = self.valIn.get()
        try:
            self.dbFun()
            query = f"SELECT * FROM stu WHERE {opt}=%s"
            self.cur.execute(query, val)
            data = self.cur.fetchall()
            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('', tk.END, values=i)
            self.con.close()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")

    def clr(self, r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"

    def delFun(self):
        opt = self.optIn.get()
        val = self.valIn.get()
        try:
            self.dbFun() 
            query = f"DELETE FROM stu WHERE {opt}=%s"
            self.cur.execute(query, val)
            self.con.commit()
            tk.messagebox.showinfo("Success", "Operation was successful!")
            self.showAll()  # Refresh the table
            self.con.close()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")

    def showAll(self):
        try:
            self.dbFun()
            self.cur.execute("SELECT * FROM stu")
            rows = self.cur.fetchall()
            self.table.delete(*self.table.get_children())
            for j in rows:
                self.table.insert('', tk.END, values=j)
            self.con.close()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")

root = tk.Tk()
obj = std(root)
root.mainloop()
