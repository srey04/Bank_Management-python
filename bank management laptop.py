
#Bank managemeent system term 2 project


#IMPORT SYSTEMS 
import getpass
from lib2to3.pgen2.token import NUMBER
from pickle import FALSE
import prettytable as ptt
import mysql.connector as sql 
from sys import exit 
import random

#Function Blocks

#Function for account creation
def newaccount():
    NAME=input("Enter Account holder name: ")
    if NAME=={}:
        print("Invalid Name")
    else:
        PHONE_NO=str(input("Enter phone number: "))
        if len(PHONE_NO)!=10:
            print("Invalid phone number")
        else:
            ACCOUNT_TYPE=input("Type of account(Current or Savings): ").upper()
            if ACCOUNT_TYPE not in ['CURRENT','SAVINGS']:
                print("Invalid input")
            else:      
                #theres a possibility that account numbers provided wont be unique
                ACCOUNT_NO=''.join(random.choice('0123456789ABCDEF') for i in range(16))
                BALANCE=int(input("Enter initial amount to be deposited: "))
                PASSWORD=''.join(random.choice('0123456789') for i in range(4))
                print("Account number and password sucessfully generated")
                print("Your Account Number is: ", ACCOUNT_NO)
                print("Your Password is", PASSWORD)
                sql_insert="insert into Account_Number values('{}','{}','{}','{}','{}','{}')".format(ACCOUNT_NO, NAME, PHONE_NO, ACCOUNT_TYPE, BALANCE, PASSWORD)
                c1.execute(sql_insert)
                print()
                print("Sucessfully account created")
                scon.commit()

#Function for viewing account 
def viewacc():
    n=input("Enter your account number: ")
    pwds=getpass.getpass(prompt="Enter password: ")
    sql_z3='select * from Account_Number where ACCOUNT_NO=("{}")'.format(n)
    c1.execute(sql_z3)
    z1=c1.fetchall()
    if len(z1)<1: 
        print("Account number invalid")
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
            print("Incorrect password")   
    scon.commit()

#For deposition/withdrawl
def transaction():
    acc_input=input("Enter your account number: ")
    pd=getpass.getpass(prompt="Enter password: ")
    sql_u='select PASSWORD from Account_Number where ACCOUNT_NO=("{}")'.format(acc_input)
    c1.execute(sql_u)
    t=c1.fetchall()
    if t[0][0]==pd:
        print("1.Deposit")
        print("2.Withdraw")
        opttran=int(input("Deposit or Withdraw(1/2): "))
        if opttran==1:
            d=int(input("Enter deposit amount: "))
            if d<=0:
                print("Invalid amount")
            else:
                sql_up="update Account_Number SET BALANCE=BALANCE+{}".format(d)
                c1.execute(sql_up)
                up1=c1.fetchall()
                for i in up1: 
                    print(i)
                print("Sucessfully Deposited")
                scon.commit()
        elif opttran==2:
            w=int(input("Enter withdraw amount: "))
            if w<=0:    
                sql_op='select BALANCE from Account_Number where ACCOUNT_NO=("{}")'.format(acc_input)
                c1.execute(sql_op)
                op=c1.fetchall()
                if op[0][0] < w:
                    print("Insufficient balance") 
                else:      
                    sql_upd="update Account_Number SET BALANCE=BALANCE-{}".format(w)
                    c1.execute(sql_upd)
                    up2=c1.fetchall()
                    for i in up2:
                        print(i)
                    print("Sucessfully Withdrawn")
                scon.commit()
            #If user inputs number >=3
            else :
                print("Invalid choice")
        else:
            print("Incorrect password")

#For modfification of account
def modify():
    z=input("Enter your account number: ")
    pds=getpass.getpass(prompt="Enter password: ")
    sql_u='select PASSWORD from Account_Number where ACCOUNT_NO=("{}")'.format(z)
    c1.execute(sql_u)
    z2=c1.fetchall()
    if z2[0][0]==pds:
        print("Entries to be modified:")
        print("1.Account Holder Name")
        print("2.Phone number")
        print("3.Change password")
        optmod=int(input("Enter choice(1/2/3): "))
        if optmod==1:
            newname=input("Enter modified name: ")
            strsql2 = "UPDATE Account_Number SET NAME='{}' WHERE ACCOUNT_NO='{}'".format(newname, z)
            c1.execute(strsql2)
            print("Name sucessfully changed")
        elif optmod==2:
            newno=int(input("Enter new phone number: "))
            strsql2 = "UPDATE Account_Number SET PHONE_NO='{}' WHERE ACCOUNT_NO='{}'".format(newno, z)
            c1.execute(strsql2)
            print("Phone number sucessfully changed")
        elif optmod==3:
            newpassword=getpass.getpass(prompt="Enter new password: ")
            sql2="select PASSWORD from Account_Number WHERE ACCOUNT_NO='{}'".format(z)
            c1.execute(sql2)
            t=c1.fetchall()
            if t[0][0]==newpassword:
                print("Cant input same password, please enter a different password")
                returnexit()    
            else:
                strsql2 = "UPDATE Account_Number SET PASSWORD='{}' WHERE ACCOUNT_NO='{}'".format(newpassword, z)
                c1.execute(strsql2)
                print("Password successfully changed")
    else: 
        print("Incorrect password")
    scon.commit()

#Function for Closing account 
def close():
    z3=input("Enter your account number: ")
    pwds=getpass.getpass(prompt="Enter your password: ")
    sql_z3='select * from Account_Number where ACCOUNT_NO=("{}")'.format(z3)
    c1.execute(sql_z3)
    z1=c1.fetchall()
    if len(z1)<1: 
        print("Account number invalid")
    else:
        z4="DELETE FROM Account_Number WHERE ACCOUNT_NO='{}'".format(z3)
        c1.execute(z4)
        print("Account sucessfully closed")
    scon.commit()    

#Function for viewing database(with pin)    
def viewdb():
    id=input("Enter id: ")
    passwd=getpass.getpass(prompt="Enter password: ")
    if id=="1234" and passwd=="9999":    
        sql_r='select * from Account_Number'                
        c1.execute(sql_r)
        t=c1.fetchall()
        d_recs = ptt.PrettyTable(["ACCOUNT_NO","NAME","PHONE_NO","ACCOUNT_TYPE","BALANCE","PASSWORD"])
        for i in t: 
            d_recs.add_row(i)
        print(d_recs)

#Escape recursion
def returnexit():
    print("Do you want to return to previous menu or exit?")
    print("Press 'E' for exit")
    print("Press 'B' to return to previous menu")
    n=input("Exit(E) or Back(B): ")    
    if n=='E':
        exit()
    elif n=='B':
        menu()

scon=sql.connect(host='localhost',user='root',database='BANK_MANAGEMENT',password='sriyansh')
if scon.is_connected():
    print("sucessfully connected")
c1=scon.cursor()




    
print("                     Welcome to our Bank Management system               ")


#MainCode    
def menu():
    print()
    print("                            BANK MANAGEMENT SYSTEM                    ")
    print()
    print()
    print("1.Creating a new account")
    print("2.View account information ")
    print("3.View transactions")
    print("4.Modify account details")
    print("5.Close account")
    print("6.EXIT")
    print("7.For authorized personnel")
    print()
    secret_input=getpass.getpass(prompt="Press enter key to continue")
    opt=""
    print()
    opt=int(input("Enter your choice: "))
    #Options given by user
    if opt==1:
        newaccount()
        print()
        returnexit()

        #secret_input=getpass.getpass(prompt="Press enter key to continue")
    elif opt==2:
        viewacc()
        print()
        returnexit()

        #secret_input=getpass.getpass(prompt="Press enter key to continue")
    elif opt==3:
        transaction()
        print()
        returnexit()

        #secret_input=getpass.getpass(prompt="Press enter key to continue")
    elif opt==4:
        modify()
        print() 
        returnexit()
            
        #secret_input=getpass.getpass(prompt="Press enter key to continue")
        
    elif opt==5:
        close()
        print()
        returnexit()

        #secret_input=getpass.getpass(prompt="Press enter key to continue")
    elif opt==6:
        exit()
    elif opt==7:
        viewdb()
        print()
        returnexit()
        #secret_input=getpass.getpass(prompt="Press enter key to continue")
    #For invalid options between 1-7
    else:
        print("Invalid option")
        returnexit()

#Calling main code
menu()


'''issues
phone number unique . and 10 digits in modifying phone number, cant give the same number.
opt mei blank dene se issue aa rha hai resolve it


'''

















