import sqlite3
def create():
    con = sqlite3.connect("onboard3.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS account(id INTEGER PRIMARY KEY,password TEXT)")
    con.commit()
    con.close()
    
def viewall():
    con = sqlite3.connect("onboard3.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM account")
    rows = cur.fetchall()
    con.close()
    return rows

def search(password=""):
    con = sqlite3.connect("onboard3.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM account WHERE password=? ",(password,))
    rows = cur.fetchall()
    con.close()
    return rows

def add(password):
    con = sqlite3.connect("onboard3.db")
    cur = con.cursor()
    cur.execute("INSERT INTO account VALUES(NULL,?)", (password,))
    con.commit()
    con.close()
    
def update(ori_password, new_password):
    con = sqlite3.connect("onboard3.db")
    cur = con.cursor()
    cur.execute("UPDATE account SET password=? WHERE password=?",(new_password, ori_password))
    con.commit()
    con.close()
    
def delete(name):
    con = sqlite3.connect("onboard3.db")
    cur = con.cursor()
    cur.execute("DELETE FROM account WHERE password=?",(password,))
    con.commit()
    con.close()

def deleteAll():
    con = sqlite3.connect("onboard3.db")
    cur = con.cursor()
    cur.execute("DELETE FROM acoount").rowcount
    con.commit()
    con.close()

print(viewall())
