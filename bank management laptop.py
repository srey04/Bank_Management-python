

   
#Bank Management System Term 2 Project


#IMPORT SYSTEMS 
import datetime
import getpass
import prettytable as ptt
import mysql.connector as sql 
from sys import exit 
import random
import datetime

#SQL Statements
scon=sql.connect(host='localhost',user='root',database='BANK_MANAGEMENT',password='sriyansh')
if scon.is_connected():
    print("sucessfully connected")
c1=scon.cursor()

#Function Blocks

#Function for account creation
def newaccount():
    NAME=input("Enter Account Holder Name: ")
    if NAME=={}:
        print("Invalid Name")
    else:
        PHONE_NO=str(input("Enter Phone Number: "))
        if len(PHONE_NO)!=10:
            print("Invalid Phone Number")
        else:
            ACCOUNT_TYPE=input("Type of Account(Current or Savings): ").upper()
            if ACCOUNT_TYPE not in ['CURRENT','SAVINGS']:
                print("Invalid input")
            else:      
                #theres a possibility that account numbers provided wont be unique
                ACCOUNT_NO=''.join(random.choice('0123456789ABCDEF') for i in range(16))
                BALANCE=int(input("Enter initial amount to be deposited: "))
                PASSWORD=''.join(random.choice('0123456789') for i in range(4))
                print("Account Number and Password successfully generated")
                print("Your Account Number is: ", ACCOUNT_NO)
                print("Your Password is", PASSWORD)
                sql_insert="insert into Account_Number values('{}','{}','{}','{}','{}','{}')".format(ACCOUNT_NO, NAME, PHONE_NO, ACCOUNT_TYPE, BALANCE, PASSWORD)
                c1.execute(sql_insert)
                print()
                print("Successfully account created")
                scon.commit()

#Function for viewing account 
def viewacc():
    n=input("Enter your Account Number: ")
    pwds=getpass.getpass(prompt="Enter Password: ")
    sql_z3='select * from Account_Number where ACCOUNT_NO=("{}")'.format(n)
    c1.execute(sql_z3)
    z1=c1.fetchall()
    if len(z1)<1: 
        print("Account Number invalid")
    else:
        sql_u='select password from Account_Number where ACCOUNT_NO=("{}")'.format(n)
        c1.execute(sql_u)
        t=c1.fetchall()
        if t[0][0]==pwds:
            sql_e="select ACCOUNT_NO,NAME,PHONE_NO,ACCOUNT_TYPE,BALANCE from Account_Number where ACCOUNT_NO='{}'".format(n)
            c1.execute(sql_e)
            o=c1.fetchall()
            d_recs = ptt.PrettyTable(["ACCOUNT_NO","NAME","PHONE_NO","ACCOUNT_TYPE","BALANCE"])
            for i in o: 
                d_recs.add_row(i)
            print(d_recs)          
        else:
            print("Incorrect Password")   
    scon.commit()

#Function For deposition/withdrawl
def transaction():
    acc_input=input("Enter your Account Number: ")
    pd=getpass.getpass(prompt="Enter Password: ")
    sql_u='select PASSWORD from Account_Number where ACCOUNT_NO=("{}")'.format(acc_input)
    c1.execute(sql_u)
    t=c1.fetchall()
    if t[0][0]==pd:
        print("1.Deposit")
        print("2.Withdraw")
        opttran=int(input("Deposit or Withdraw(1/2): "))
        if opttran==1:
            d=int(input("Enter Deposit Amount: "))
            if d<=0:
                print("Invalid Amount")
            else:
                sql_up="update Account_Number SET BALANCE=BALANCE+{}".format(d)
                c1.execute(sql_up)
                up1=c1.fetchall()
                for i in up1: 
                    print(i)
                print("Successfully Deposited")
                transactionsummary(acc_input,d)
                scon.commit()
        elif opttran==2:
            w=int(input("Enter Withdraw Amount: "))
            if w>=0:    
                sql_op='select BALANCE from Account_Number where ACCOUNT_NO=("{}")'.format(acc_input)
                c1.execute(sql_op)
                op=c1.fetchall()
                if op[0][0] < w:
                    print("Insufficient Balance") 
                else:      
                    sql_upd="update Account_Number SET BALANCE=BALANCE-{}".format(w)
                    c1.execute(sql_upd)
                    up2=c1.fetchall()
                    for i in up2:
                        print(i)
                    print("Successfully Withdrawn")
                    transactionsummary(acc_input,w*(-1))
                scon.commit()
            #If user inputs number >=3
            else :
                print("Invalid choice")
        else:
            print("Incorrect Password")

#For modfification of account details
def modify():
    z=input("Enter your Account Number: ")
    pds=getpass.getpass(prompt="Enter Password: ")
    sql_u='select PASSWORD from Account_Number where ACCOUNT_NO=("{}")'.format(z)
    c1.execute(sql_u)
    z2=c1.fetchall()
    if z2[0][0]==pds:
        print("Entries to be modified:")
        print("1.Account Holder Name")
        print("2.Phone Number")
        print("3.Change Password")
        optmod=int(input("Enter choice(1/2/3): "))
        if optmod==1:
            newname=input("Enter modified Name: ")
            strsql2 = "UPDATE Account_Number SET NAME='{}' WHERE ACCOUNT_NO='{}'".format(newname, z)
            c1.execute(strsql2)
            print("Name Successfully changed")
        elif optmod==2:
            newno=int(input("Enter New Phone Number: "))
            strsql2 = "UPDATE Account_Number SET PHONE_NO='{}' WHERE ACCOUNT_NO='{}'".format(newno, z)
            c1.execute(strsql2)
            print("Phone Number successfully changed")
        elif optmod==3:
            newpassword=getpass.getpass(prompt="Enter new password(4 digit characters only): ")
            sql2="select PASSWORD from Account_Number WHERE ACCOUNT_NO='{}'".format(z)
            c1.execute(sql2)
            t=c1.fetchall()
            if t[0][0]==newpassword:
                print("Cant input same Password, please enter a different Password")
                returnexit()    
            else:
                strsql2 = "UPDATE Account_Number SET PASSWORD='{}' WHERE ACCOUNT_NO='{}'".format(newpassword, z)
                c1.execute(strsql2)
                print("Password successfully changed")
    else: 
        print("Incorrect Password")
    scon.commit()

#Function for Closing account 
def close():
    z3=input("Enter your Account Number: ")
    pwds=getpass.getpass(prompt="Enter your Password: ")
    sql_z3='select * from Account_Number where ACCOUNT_NO=("{}")'.format(z3)
    c1.execute(sql_z3)
    z1=c1.fetchall()
    if len(z1)<1: 
        print("Account Number invalid")
    else:
        z4="DELETE FROM Account_Number WHERE ACCOUNT_NO='{}'".format(z3)
        c1.execute(z4)
        print("Account successfully closed")
    scon.commit()    

#Function for viewing database(with pin) for authorized personnel 
def viewdb():
    id=input("Enter ID: ")
    passwd=getpass.getpass(prompt="Enter Password: ")
    if id=="1234" and passwd=="9999":    
        sql_r='select * from Account_Number'                
        c1.execute(sql_r)
        t=c1.fetchall()
        d_recs = ptt.PrettyTable(["ACCOUNT_NO","NAME","PHONE_NO","ACCOUNT_TYPE","BALANCE","PASSWORD"])
        for i in t: 
            d_recs.add_row(i)
        print(d_recs)

#Function for returning to previous menu function/exiting code block
def returnexit():
    print("Do you want to return to previous menu or exit?")
    print("Press 'E' for exit")
    print("Press 'B' to return to previous menu")
    n=input("Exit(E) or Back(B): ")    
    if n in'Ee':
        exit()
    elif n in 'Bb':
        menu()
        
#Function for inputting values into TRANSACTIONS Table
def transactionsummary(ACCOUNT_NO,AMOUNT):   
    sql_r='INSERT INTO TRANSACTIONS VALUES(%s,%s,%s)'
    t1=datetime.datetime.now()
    c1.execute(sql_r,(ACCOUNT_NO,AMOUNT,t1))
    scon.commit()
    
#Function for viewing transaction summary
def viewsummary():
    n=input("Enter your Account Number: ")
    passwd=input("Enter your Password: ")
    sql_u='select PASSWORD from Account_Number where ACCOUNT_NO=("{}")'.format(n)
    c1.execute(sql_u)
    t=c1.fetchall()
    if t[0][0]==passwd:
        c1.execute('select * from TRANSACTIONS where ACCOUNT_NO=("{}")'.format(n))
        t2=c1.fetchall()
        d_recs = ptt.PrettyTable(["ACCOUNT_NO","AMOUNT","DATE"])
        for i in t2: 
            d_recs.add_row(i)
        print(d_recs)
        






    
print("                     Welcome to our Bank Management system               ")


#MainCode    
def menu():
    print()
    print("                            BANK MANAGEMENT SYSTEM                    ")
    print()
    print()
    print("1.Creating a New Account")
    print("2.View Account Information ")
    print("3.Transactions")
    print("4.Modify Account Details")
    print("5.Close Account")
    print("6.View Transaction Summary")
    print("7.EXIT")
    print("8.For Authorized Personnel")
    print()
    secret_input=getpass.getpass(prompt="Press any key to continue")
    opt=""
    print()
    opt=int(input("Enter your choice: "))
    #Options given by user
    if opt==1:
        newaccount()
        print()
        returnexit()    
    elif opt==2:
        viewacc()
        print()
        returnexit()       
    elif opt==3:
        transaction()
        print()
        returnexit()        
    elif opt==4:
        modify()
        print() 
        returnexit()       
    elif opt==5:
        close()
        print()
        returnexit()        
    elif opt==6:
        viewsummary()
        print()
        returnexit()
    elif opt==7:
        exit()
    elif opt==8:
        viewdb()
        print()
        returnexit()
       
    #For invalid options between 1-7
    else:
        print("Invalid option")
        returnexit()

#Calling main code
menu()





