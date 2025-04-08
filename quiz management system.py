import pymysql as pm, prettytable as pt,time,sys,setup as sp
from pwinput import *

#================================================================
usr='root'
passwrd='root'
hst='localhost'
dbase='quizmgmt'
d={}
gapvalue=30
#===============================================
'''user=usr,password=passwrd,host=hst,db=dbase'''

def protection(user,passwd):
    global d
    d['1234']='Harshit@1234'
    for k,v in d.items():
        if k==user and v==passwd:
            return True
        else:
            print('='*80)
            print('Given credentials Does not match with Record')
    return False
    
        
#==================================================



def chk_connection():
    mycon= None
    try:
        mycon=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)
    except:
        pass
    if mycon!= None:
        con=True
        #print('Connection Established Successfully.')
        mycon.close()
        return con
        #print('Version :',mycon.version_info)
    else:
        print('\n\n\n')
        print('='*15,'CONNECTION FAILED WITH DATABASE ! WE ARE SORRY FOR THE INCONVIENCE','='*15)
        return False
#chk_connection()





#==================================================
def get_subject_nm(typ):
    print("\n\n"+'='*20+"SUBJECT AVAILABLE WITH THIER CODE"+"="*20)
    
    subject=["CS","PHYSICS","CHEMISTRY","MATHS","ENGLISH"]
    i=0
    x=pt.PrettyTable(["CODE","SUBJECT"])
    for sub in subject:
        x.add_row((i,sub))
        i+=1

    print(x)


    while True:
        print('\nENTER SUBJECT CODE TO '+typ+'OF: ',end='')
        try:
            
            sub_code=int(input())
            if sub_code<i and sub_code>-1:
                    break
            else:
                    print('\t\tENTER CORRECT SUBJECT CODE !\n')
        except ValueError:
            print('\tONLY NUMBERS EXPECTED!')

    return subject[sub_code]
#==================================================
def autogen_Dno():
    id=None
    try:
        mycon=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)
        cur=mycon.cursor()
        qry='SELECT MAX(QNO) FROM QUIZ'
        cur.execute(qry)
        rows=cur.fetchone()
        #print(rows)
        if rows[0]==None:
            id =1
        else:
            id=rows[0]+1
    except pm.DatabaseError as e:
        mycon.rollback()
        print('Database Error : ',e)
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()
        return id
    
        

#==================================================
def insert_many_ques():
    cur=None

    try:
        
        mycon=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)
        cur=mycon.cursor()

        #QUESTION ADDING  TO DATABASE ------------------------------
        print('\t\t\t\t\t\t===================================')
        subject=get_subject_nm("ADD QUESTION ")

        questions=list()
        print('\t\t\t\tMAXIMUM CHARACTER LENGTH FOR QUESTION IS = 600 \n')
        
        while True:
            qno=autogen_Dno()
            print('Question no. :',qno)
            #print(type(qno))
            ques=input('ENTER QUESTION:  ')
            if len(ques)>600:
                print('\tQUESTION LENGTH IS GREATER THAN 600! REDUCE YOUR QUESTION SIZE AND RE-ENTER QUESTION')
                continue
            op1=input('ENTER OPTION A:  ')
            op2=input('ENTER OPTION B:  ')
            op3=input('ENTER OPTION C:  ')
            correct=input('ENTER CORRECT OPTION NUMBER[A-C]:  ')
            qry=f'INSERT INTO QUIZ VALUES ({qno},"{ques}","{op1}","{op2}","{op3}","{correct}","{subject}")'
            cur.execute(qry)
            mycon.commit()
            print('RECORD SAVED SUCCESSFULLY')
            print('\n\t====WISH TO ADD MORE QUESTION ? \n====PRESS [Y/y] TO ADD:',end='')
            choice=input()

            if choice.lower()=='y':
                qno=qno+1
            

            else:
                break
        print('\t\t\t\t\t\t\t\t                 ===============================')
        print('\t\t\t\t\t\t\t\t=================!QUESTION ADDITION SUCCESSFULL!=================')


    except pm.DatabaseError as e:
        if mycon:
            mycon.rollback()
            print('\t\t\t\t\t\t=====!QUESTION ADDITION FAILED!======')
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()

#===================================================
def search_ques():
    cur=None
    
    try:
        print('\n\n==================================================================  SEARCH CONSOLE   ================================================================================')
        mycon=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)
        cur=mycon.cursor()
        try:
            qid=int(input('ENTER QID OF THE QUESTION TO BE SEARCHED: '))
        except ValueError:
            print("\n\t\t=====!  INVALID QID  !  NUMBERS ONLY EXPECTED  !=====")
            return
        
        qry="SELECT * FROM QUIZ WHERE qno=%s"
        cur.execute(qry,qid)

        row_det=cur.fetchall()
        
        if not row_det:
            print('\n====================!NO SUCH QUESTION WITH GIVEN QID EXIST!====================')

        else:
            row=row_det[0]
            print('\t\t\t\t\t\t\t=========================== ')
            print('\t\t\t\t\t\t\t!REQUIRED QUESTION DETAILS!\t')
            print('\t\t\t\t\t\t\t=========================== ')
            print('\nQID: {}\nQUESTION: {}\nOPTION 1: {}\nOPTION 2:{} \nOPTION 3: {}\nCORRECT OPTION: {}\nSUBJECT: {}'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            print('\t\t\t\t\t\t========================================== ')

                
    
    except pm.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()
#insert_many_ques()
#==============================================================================================================================================================================

def update_ques():
    cur=None
    
    try:
        print('==================================================================  UPDATE FORM   ================================================================================')
        mycon=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)
        cur=mycon.cursor()
        try:
            qid=int(input('ENTER QID OF THE QUESTION TO BE EDITED: '))
        except ValueError:
            print("\n\t\t=====!  INVALID QID  !  NUMBERS ONLY EXPECTED  !=====")
            return
        
        qry="SELECT * FROM QUIZ WHERE qno=%s"
        cur.execute(qry,qid)

        row_det=cur.fetchall()
        
        if not row_det:
            print('NO SUCH QUESTION WITH GIVEN QID EXIST')

        else:
            row=row_det[0]
            print('\t\t\t\t\t\t\t=========================== ')
            print('\t\t\t\t\t\t\t!CURRENT QUESTION DETAILS!\t')
            print('\t\t\t\t\t\t\t=========================== ')
            print('\nQID: {}\nQUESTION: {}\nOPTION 1: {}\nOPTION 2:{} \nOPTION 3: {}\nCORRECT OPTION: {}\nSUBJECT: {}'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            print('\t\t\t\t\t\t========================================== ')

            print('\t\t\t\t\t\t!PLEASE ENTER NEW DETAILS OF THIS QUESTION!')
            print('\t\t\t\t\t\t========================================== ')

            while True:
            
                n_ques=input('ENTER NEW QUESTION:  ')
                if len(n_ques)>600:
                    print('\tQUESTION LENGTH IS GREATER THAN 600! REDUCE YOUR QUESTION SIZE AND RE-ENTER QUESTION')
                    continue
                n_op1=input('ENTER OPTION 1:  ')
                n_op2=input('ENTER OPTION 2:  ')
                n_op3=input('ENTER OPTION 3:  ')
                n_correct=input('ENTER CORRECT OPTION NUMBER[A-C]:  ')
                n_subject=input('ENTER NEW SUBJECT NAME: ')
                break

            qry='''UPDATE  QUIZ 
                SET
                QNAME=%s,
                optA=%s,
                optB=%s,
                optC=%s,
                coropt=%s,
                subject=%s
                WHERE QNO=%s
                '''
            cur.execute(qry,(n_ques,n_op1,n_op2,n_op3,n_correct,n_subject,qid))
            mycon.commit()
            print('\n\n===============!QUESTION EDITED SUCCESSFULLY!===========================')
    

    except pm.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()


#update_ques()
#==============================================================================================================================================================================
def delete_ques():
    cur=None

    print('='*188)
    print('\t\t\t\t\t\t\t\t\t\tDELETE FORM')
    print('\t\t\t\t\t\t\t\t\t\t===========')

    ch=True
    print()
    while ch:
        try:
            qid=int(input('\n>>>ENTER QID OF THE QUESTION TO BE DELETED:'))
            ch=False

        except ValueError:
            print('\n\t\t\t\t\t\t\t\t\t!PLEASE ENTER ONLY A VALID QUESTION ID!\n\t\t\t\t\t\t\t\t\t       !ONLY NUMBERS EXCEPTED!')

    try:
        mycon=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)
        cur=mycon.cursor()

        #CHECKING WETHER QID IS PRESENT OR NOT IN DATABASE
        qry="SELECT * FROM QUIZ WHERE QNo=%s"
        cur.execute(qry,qid)

        row_det=cur.fetchall()
        

        if not row_det:  #IF QID IS NOT PRESENT IN THE DB THEN GOES IN THIS BLOCK

            print('\n\n\t\t\t\t\t\t\t\t\t=================================')
            print('\t\t\t\t\t\t\t\t\tNO SUCH RECORD EXIST WITH QID=',qid)
            print('\t\t\t\t\t\t\t\t\t=================================')
            
        else:            #IF QID DOES EXIST
            
            row=row_det[0]
            print('\n\n\t\t\t\t\t\t\t\t\t==========!CURRENT QUESTION RECORD!==========')
            print('QID:  ',qid)
            print('QUESTION:  ',row[1])
            print('OPTION 1:  ',row[2])
            print('OPTION 2:  ',row[3])
            print('OPTION 3:  ',row[4])
            print('CORRECT OPTION:  ',row[5])
            print('SUBJECT:  ',row[6])

            time.sleep(2)

            print('\n\n!DO YOU REALLY WANT TO DELETE THIS RECORD!\nPRESS Y\y:  ',end='')
            choice=input()
            if choice.lower()=='y':
                qry='DELETE FROM QUIZ WHERE QNO=%s'
                cur.execute(qry,qid)
                mycon.commit()
                print('\n\n\t\t\t\t\t\t\t\t\t===============================')
                print('\t\t\t\t\t\t\t\t\t!QUESTION DELETED SUCCESSFULLY!')
                print('\t\t\t\t\t\t\t\t\t===============================')
                
            else:
                print('\n\n\t\t\t\t\t\t\t\t\t=======================')
                print('\t\t\t\t\t\t\t\t\t!QUESTION NOT DELETED !')
                print('\t\t\t\t\t\t\t\t\t=======================')
                pass




    except pm.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()


#delete_ques()

#==============================================================================================================================================================================
def scoreboard():
    cur=None
    
    try:
        mycon=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)
        cur=mycon.cursor()

        qry="SELECT * FROM STUDENT_MST"
        cur.execute(qry)
        row_det=cur.fetchall()

        
        
        if row_det:
            x=pt.PrettyTable(["SID","STUDENT NAME","CRT ANS","WRNG ANS","SUBJECT","TOTAL MARKS"])
            print(' '*75+"!FETCHING STUDENTS RECORD!"+'\n'+" "*75+"========================="+"\n\n")
            time.sleep(2)
            for row in row_det:
                x.add_row(row)
            print(x)

        else:
            print(end='\n\n')
            print(' '*75+"==========================")
            print(" "*75+'!NO RECORD EXIST TILL NOW!')
            print(' '*75+"==========================")
    
    except pm.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()


#scoreboard()
#==============================================================================================================================================================================
def score_arrange():
    cur=None
    
    print('\n\n'+"="*188)
    try:
        mycon=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)
        cur=mycon.cursor()

        sub=get_subject_nm("SEARCH TOP 3 ")
        qry="SELECT * FROM STUDENT_MST WHERE SUBJECT=%s ORDER BY TOTAL_MARKS DESC"
        cur.execute(qry,sub)

        row_det=cur.fetchall()
        num=[]
        x=pt.PrettyTable(["SID","STUDENT NAME","CRT ANS","WRNG ANS","SUBJECT","TOTAL MARKS","RANK"])
        print(' '*75+"!FETCHING STUDENTS RECORD!"+'\n'+" "*75+"========================="+"\n\n")
        time.sleep(2)
        
        for row in row_det:

            if len(num)<3:
                if row[5] not in num:
                    num.append(row[5])
                rank=(len(num),)
                x.add_row(row+rank)
            elif len(num)==3:
                if row[5] in num:
                    x.add_row(row)
            elif len(num)>3:
                break
                
        if row_det:
            print('='*20+"TOP 3 STUDENTS DETAILS OF "+sub+"="*20)
            print(x)
        
        else:
            print(end='\n\n')
            print(' '*75+"==========================")
            print(" "*75+'!NO RECORD EXIST TILL NOW!')
            print(' '*75+"==========================")

            
    
    except pm.DatabaseError as e:
        if mycon:
            mycon.rollback()
            print('abhay')
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()

#score_arrange()
#====================================================================
            
def play():
    cur=None
    
    print('==========================================================================  PLAY  QUIZ  ================================================================================')

    # vALUES NEEDED  TO BE INSERTED AFTER TEST IN "STUDENT_MST" --------
    name=input("\n\nENTER YOUR NAME:  ")
    total_marks=0
    cans=0
    wans=0
    subject_name=''
    new_sid=1
    #--------------------------------------------

    try:

        
        mycon=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)
        cur=mycon.cursor()

        query="SELECT * FROM QUIZ WHERE SUBJECT=%s"
        subject_name=get_subject_nm("TAKE TEST ")
        cur.execute(query,(subject_name,))

        row_det=cur.fetchall()
        if not row_det:
            print("\n\n\t\t\t\t=============="'!NO QUESTIONS EXIST FOR THHIS SUBJECT!'+"==============")
        else:
            
            print('\n\t\t\t=================!TEST READY!=================')
            for qid,ques,op1,op2,op3,crt,sub in row_det:

                print('\n QUESTION: {}\n OPTION A: {}\n OPTION B: {}\n OPTION C: {}\n'.format(ques,op1,op2,op3))

                print('\t\tENTER YOUR ANSWER[A-C]:  ',end='')
                choice=input()

                if choice.lower()==crt.lower():
                    total_marks+=5
                    cans+=1
                else:
                    total_marks-=2
                    wans+=1

            print('\tYOUR SCORE FOR THIS TEST IS :',total_marks)

            
            
            query="SELECT MAX(S_ID) FROM STUDENT_MST"
            cur.execute(query)
            row=cur.fetchall()
            max_sid=row[0][0]
            
            if max_sid:
                new_sid=max_sid+1
                #print(new_sid)

            
            
            row_student=(int(new_sid),name,int(cans),int(wans),subject_name,int(total_marks))
            query="INSERT INTO STUDENT_MST VALUES(%s,%s,%s,%s,%s,%s)"
            cur.execute(query,row_student)


            mycon.commit()




    except pm.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()



#play()

#==============================================================================================================================================================================

def show_all():
    cur=None

    try:
        print('\n\t\t\t\t\t\t\t\t\t      =====================')
        print('=============================================================================  SHOWING ALL RECORDS  ==========================================================='+'='*30)
        print('\t\t\t\t\t\t\t\t\t      =====================\n\n')
        
        mycon=pm.connect(user=usr,passwd=passwrd,host=hst,db=dbase)
        cur=mycon.cursor()
        qry="SELECT * FROM QUIZ "

        tble=pt.PrettyTable(["QUESTION ID","QUESTION","OPTION A","OPTION B","OPTION C","CORRECT ANSWER","SUBJECT"])

        count=0
        cur.execute(qry)
        for row in cur.fetchall():
            tble.add_row(row)
            count+=1
        
        print(tble)
        print('\n\n\t\t\t\t\t\t\t\t\t\t>>>TOTAL  {}  RECORDS FETCHED<<<'.format(count))



    except pm.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()





#show_all()
#====================================================
def Create_New_Admin():
    global d
    user = input('Enter Username for new Admin : ')
    passwd=input('Enter Password for new Admin : ')
    d[user]=passwd
    print('New Admin Created Successfully')


#====================================================
def admin():
    while True:
        s='''
                            =============================
                            |       ADMIN SECTION       |
                            -----------------------------
                            | |0|   Setup               |
                            -----------------------------
                            | |1|  Add Question         |
                            -----------------------------
                            | |2|  Update Question      |
                            -----------------------------
                            | |3|  Show Question        |
                            -----------------------------
                            | |4|  Search Question      |
                            -----------------------------
                            | |5|  Delete Question      |
                            -----------------------------
                            | |6|  Create New Admin     |
                            -----------------------------
                            | |7|  Back to Application  |
                            =============================
            
        '''
        print(s)
        ch=None
        while True:
                try:
                    
                    ch=input('ENTER YOUR CHOICE: ')
                    break
                except ValueError:
                    print('\n\t\t\t\t\t\t\t\t\t\t======================\n\t\t\t\t\t\t\t\t\t\t!NUMBERS ONLY EXPECTED!\n\t\t\t\t\t\t\t\t\t\t======================')
        if ch==None:
                pass
        elif ch=='0':
                sp.create_database()
                sp.Create_Table_quiz()
                sp.Create_Table_Student()
        elif ch=='1':
                insert_many_ques()
        elif ch=='2':
                update_ques()
        elif ch=='3':
                show_all()
        elif ch=='4':
                search_ques()
        elif ch=='5':
                delete_ques()
        elif ch=='7':
                print('='*188)
                print('\n'+' '*75+'RETURNING TO HOME MENU.....\n')
                time.sleep(2)
                return
        elif ch=='6':
            print(' '*30,'Create New Admin Console')
            Create_New_Admin()
        else:
                print('\n\t\t\t\t\t\t\t\t\t\t\t!NUMBER OUT OF RANGE!')
        
        
        

#admin()
#=====================================================

#DRIVER CODE
#MAIN MENU


while True:
        print('\n\n'+'='*188)
        print(' '*50+"MAIN MENU"+"\n"+" "*50+"=========\n")
        print(' '*45+'ENTER 1 -  ADMIN SECTION')
        print(' '*45+'ENTER 2 -  PLAY SECTION')
        print(' '*45+'ENTER 3 -  VIEW SCOREBOARD')
        print(' '*45+'ENTER 4 -  VIEW TOP 3 STUDENT OF A SUBJECT')
        print(' '*45+'ENTER 5 -  EXIT THE SOFTWARE')
        #print(' '*75,'ENTER YOUR CHOICE: ',end='')

        ch=None
        while True:
            try:
                ch=int(input('ENTER YOUR CHOICE: '))
                print('='*188)
                break
            except ValueError:
                print('\n','!NUMBERS ONLY EXCEPTED!\n\n')

        if ch==None:
            continue
        elif ch==1:
            print('Enter Username : ',end=''); chu=input()
            chp=pwinput(prompt='Enter Password : ')
            if protection (chu,chp):
                print('\n'+' '*28+'REDIRECTING TO ADMIN SECTION...')
                time.sleep(2)
                admin()
        elif ch==2:
            play()
        elif ch==3:
            scoreboard()
        
        elif ch==4:
            score_arrange()
        elif ch==5:
            print()
            print('='*188)
            print('\n'+' '*75+'THANK YOU FOR USING THIS SOFTWARE')
            print('='*188)
            time.sleep(5)
            sys.exit()
        else:
            print(' '*75+'!CHOICE OUT OF RANGE!')
    

