import pymysql as pm
usr='root'
passwrd='root'
hst='localhost'
dbase='quizmgmt'
#==================================================
def create_database():
    try:
        con=pm.connect(user=usr,passwd=passwrd,host=hst)
        qry='Create Database quizmgmt'
        cur=con.cursor()
        cur.execute(qry)
        con.commit()
        print('Database Created Successfully')
    except pm.DatabaseError as e:
        con.rollback()
        print(e)
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()
#create_database()
#==================================================
def Create_Table_quiz():
    try:
        con=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)
        qry="create table quiz\
( qno int primary key,\
qname varchar(600) Not null,\
opta varchar(40) not null,\
optb varchar (40) not null,\
optc varchar(40) not null, \
coropt varchar(40) check (coropt in ('A','B','C')), \
subject varchar(60)check (subject in ('CHEMISTRY','PHYSICS', 'CS','MATHS','ENGLISH')))"
        cur=con.cursor()
        cur.execute(qry)
        con.commit()
        print('TABLE CREATED SUCCESSFULLY')
    except pm.DatabaseError as e:
        con.rollback()
        print(e)
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()
#Create_Table_quiz()
#==================================================
def Create_Table_Student():
    try:
        con=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)#"SID","STUDENT NAME","CRT ANS","WRNG ANS","SUBJECT","TOTAL MARKS"
        qry='''CREATE table student_mst
        ( S_id INT PRIMARY KEY,
        S_Name VARCHAR (600),
        Crt_Ans int (23),
        Wrng_Ans int(23),
        Subject Varchar(34),
        Total_Marks int
        ) '''
        cur=con.cursor()
        cur.execute(qry)
        con.commit()
        print('Student Table created Successfully')
        
    except pm.DatabaseError as e:
        con.rollback()
        print(e)
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()
#Create_Table_Student()


