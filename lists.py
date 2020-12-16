import sqlite3
def create():
    con = sqlite3.connect("onboard1.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS account(id INTEGER PRIMARY KEY,name TEXT,link TEXT, user TEXT, password TEXT,tag TEXT,memo TEXT)")
    con.commit()
    con.close()
    
def viewall():
    con = sqlite3.connect("onboard1.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM account")
    rows = cur.fetchall()
    con.close()
    return rows

def search(name=""):
    con = sqlite3.connect("onboard1.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM account WHERE name=? ",(name,))
    rows = cur.fetchall()
    con.close()
    return rows

def add(name,link,user,password,tag,memo):
    con = sqlite3.connect("onboard1.db")
    cur = con.cursor()
    cur.execute("INSERT INTO account VALUES(NULL,?,?,?,?,?,?)",(name,link,user,password,tag,memo))
    con.commit()
    con.close()
    
def update(ori_name,new_name,link,user,password,tag,memo):
    con = sqlite3.connect("onboard1.db")
    cur = con.cursor()
    cur.execute("UPDATE account SET name=?,link=?,user=?,password=?,tag=?,memo=? WHERE name=?",(new_name,link,user,password,tag,memo,ori_name))
    con.commit()
    con.close()
    
def delete(name):
    con = sqlite3.connect("onboard1.db")
    cur = con.cursor()
    cur.execute("DELETE FROM account WHERE name=?",(name,))
    con.commit()
    con.close()

def deleteAll():
    con = sqlite3.connect("onboard1.db")
    cur = con.cursor()
    cur.execute("DELETE FROM acoount").rowcount
    con.commit()
    con.close()

print(search('insta'))
