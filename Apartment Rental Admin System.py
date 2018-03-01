# 1 room for 1 student
# A unit: 2 bedrooms (RM300)
# B unit: 1 master bedroom (RM280) and 2 bedrooms (RM200)
# Upon register: RM100 + 1-month deposit + 1-month rental

import pickle
# error checking for database
try:
    A = pickle.load(open('configA.txt','rb'))
except EOFError:
    with open('configA.txt','wb') as f:
        pickle.dump([],f)
        
A = pickle.load(open('configA.txt','rb')) # initial database import

# error checking for database
try:
    B = pickle.load(open('configB.txt','rb'))
except EOFError:
    with open('configB.txt','wb') as f:
        pickle.dump([],f)
        
B = pickle.load(open('configB.txt','rb')) # initial database import

import datetime
t = datetime.date.today()
d = datetime.timedelta(days=140)
d1 = t + d

#check status
def stat():
    
    print('''
[Status Check]
*For apartment A, Insert - 1.
*For apartment B, Insert - 2.''')
    userInputStat = input('Insert Apartment: ')
    if userInputStat == '1':
        print('\nLoading...')
        for i,u in enumerate(A,1): # i=index, u=unit, A=apartment, 1=(start counting from 1)
            print('\n')
            for r in u:
                if r == 'empty':
                    print('A'+str(i),r)
                else:
                    print('A'+str(i),r[0],r[1]) # print unit number and details
        print('\nNo more result.')
        return
    if userInputStat == '2':
        print('\nLoading...')
        for i,u in enumerate(B,1):
            print('\n')
            for r in u:
                if r == 'empty':
                    print('B'+str(i),r)
                else:
                    print('B'+str(i),r[0],r[1],r[2])
        print('\nNo more result.')
        return
    else:
        print('\nError.')
        return


def registerA():
    
    name = str(input('\n[Registration]\nInsert Name: '))      
    for u in A: # u = unit       
        if u[0] == 'empty':
            u[0] = [name,d1] #d1 is a date 
            print('\nRegistration Successful!')
            print("\n{}'s unit is {}, contract valid until {}.".format(name,'A'+str(A.index(u)+1),d1))
            return
        elif u[1] == 'empty':
            u[1] = [name,d1]
            print('\nRegistration Successful!')
            print("\n{}'s unit is {}, contract valid until {}.".format(name,'A'+str(A.index(u)+1),d1))
            return
    # no more empty unit,
    A.append([[name,d1],'empty']) # create new unit
    num = A.index([[name,d1],'empty']) + 1
    print("\n{}'s unit is {}, contract valid until {}.".format(name,'A'+str(num),d1))
    return 


def registerB():
    
    print('''
[Room Choice]
*For master bedroom, Insert - 1.
*For normal bedroom, Insert - 2.''')
    room = input('Insert Room: ')
    
    if room == '1': #Master bedroom
        print('\nLoading...')
        name = str(input('\n[Registration]\nInsert ID: '))
        for u in B:
            if u[0] == 'empty': #first room
                # unit not full,
                    print('\nRegistration Successful!')
                    u[0] = ['Master',name,d1]
                    print("\n{}'s unit is {}, contract valid until {}.".format(name,'B'+str(B.index(u)+1),d1))
                    return            
        # no more empty unit,
        print('\nRegistration Successful!')
        B.append([['Master',name,d1],'empty','empty']) # create new unit
        num = B.index([['Master',name,d1],'empty','empty']) + 1
        print("\n{}'s unit is {}, contract valid until {}.".format(name,'B'+str(num),d1))
        return 
        
                 
    if room == '2':  #Normal bedroom
        print('\nLoading...')
        name = str(input('\n[Registration]\nInsert ID: '))
        for u in B:
            if u[1] == 'empty': #second room           
                print('\nRegistration Successful!')
                u[1] = ['Normal',name,d1]
                print("\n{}'s unit is {}, contract valid until {}.".format(name,'B'+str(B.index(u)+1),d1))
                return
            if u[2] == 'empty': #third room
                print('\nRegistration Successful!')
                u[2] = ['Normal',name,d1]
                print("\n{}'s unit is {}, contract valid until {}.".format(name,'B'+str(B.index(u)+1),d1))
                return       
        # no more empty unit,
        print('\nRegistration Successful!')
        B.append(['empty','empty',['Normal',name,d1]]) # create new unit
        num = B.index(['empty','empty',['Normal',name,d1]]) + 1
        print("\n{}'s unit is {}, contract valid until {}.".format(name,'B'+str(num),d1))
        return
    
    else:
        print('\nError.')
        return


def movIn():
    
    print('''
[Apartment Rental]
*For apartment A, Insert - 1.
*For apartment B, Insert - 2.''')
    userInputReg = input('Insert Apartment: ')
    if userInputReg == '1':
        print('\nLoading...')
        registerA()
        return
    if userInputReg == '2':
        print('\nLoading...')
        registerB()
        return
    else:
        print('\nError.')
        return


def remove(name,apa):
    apatype = 0 # for print output
    if apa == A:
        apatype = 'A'
    if apa == B:
        apatype = 'B'
    for u in apa:
        uno = apa.index(u) # unit number
        for i,r in enumerate(u):
            if name in r:
                # print unit number and room info,
                print('\nLoading...\n\nEntry found:',apatype+str(uno+1),r)
                print('\n*If correct, Insert - 1\n*If wrong, Insert - 2')
                answer = input('Insert answer: ')
                if answer == '1':
                    u[i] = 'empty' # remove entry
                    print('\n'+name,'is removed from',apatype+str(uno+1)+'!')
                    return 'Y'
                if answer == '2':
                    continue # continue lookup
                else:
                    print('\nError.')
                    return 'E'
    # no more result,
    return 'N'


def movOut():
    
    print('\n[Check-Out]')
    name = str(input('Insert ID: '))
    resultA = remove(name,A)
    if resultA == 'Y':
        return
    if resultA == 'N':
        resultB = remove(name,B)
        if resultB == 'Y':
            return
        if resultB == 'N':
            # no matched name,        
            print('\nNo entry found.')
            return
    else:
        return


def update():
    
    # update database,
    global A, B
    with open('configA.txt','wb') as f:   #f is a file pointer
        pickle.dump(A,f)
    with open('configB.txt','wb') as f:
        pickle.dump(B,f)
    # update variables,
    A = pickle.load(open('configA.txt','rb'))
    B = pickle.load(open('configB.txt','rb'))

        
def main():

    update()
    print('\n'*10)
    print('''
-----------------------------------------------
[Main Menu]
*For status check, Insert - 1.
*For check-in, Insert - 2.
*For check-out, Insert - 3.''')
    userInputMain = input('Insert Command: ')
    if userInputMain == '1':
        print('\nLoading...')
        stat()
        main()
    elif userInputMain == '2':
        print('\nLoading...')
        movIn()
        main()
    elif userInputMain == '3':
        print('\nLoading...')
        movOut()
        main()
    else:
        print('\nError.')
        main()


main()

