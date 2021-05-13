import sys
import os
import telnetlib
import io
import datetime
import string
import getpass
import os

def printList (list4, host_1):
    print ("0 "+host_1+" list count", len(list4))
    n=1
    for item in list4:
        print (item)
        out_f.write(item+'\n')

        n=n+1

#d = input("Czy wyczyscic plik wyjsciowy t/n\n")
d = "t"

if (d=="t"):
    out_f=open('out_AX.txt', 'w') 
    out_f_det=open('out_AX_det.txt', 'w')    
   
else:
    out_f=open('out_AX.txt', 'a')
    out_f_det=open('out_AX_det.txt', 'w')    



in_f=open("AX_IN.txt","r")
cmm_f=open('AX_CMM.txt', 'r')



print ("the node name of this file is ", in_f.name)
print ("the close status of this node file is", in_f.closed)
print ("mode of this node file is", in_f.mode)
print ("---------------------------------------------------------------------------")
print ("the node cmm of this file is ", cmm_f.name)
print ("the close status of this cmm file is", cmm_f.closed)
print ("mode of this cmm file is", cmm_f.mode)

user = 'xxxx'
password = 'xxxx'

prompt = ''

#f.write ("this is my line 1 - written from python")
cnt = 0
count = len(in_f.readlines(  ))

in_f.seek(0)

for line in in_f:
    
    cnt = cnt+1
    
    datetime_object = datetime.datetime.now().strftime("%d/%m/%Y; %H:%M:%S")
    print      ("-----------------------------------------------START-----------------------------------------------")
    out_f.write("-----------------------------------------------START-----------------------------------------------\n")
    HOST = line.strip()
    print ("Proboje sie dostac do ", HOST, " jest to wezel numer ", cnt, " z pliku w którym jest ", count, " linii")
    out_f.write("Proboje sie dostac do "+ str(HOST) + " jest to wezel numer "+ str(cnt) + " z pliku w ktorym jest "+ str(count)+ " linii\n")
    out_f.write("Proboje sie dostac do "+ HOST+"\n")

    try:
        tn = telnetlib.Telnet (HOST, 23, 5)
    except Exception as e:
        print ("Cannot CONNECT!!!")
        out_f.write("Cannot CONNECT!!!\n")
        continue

    #tn.set_debuglevel(10)

    try:
       response=tn.read_until(b"Login:", timeout=3)
    except EOFError as e:
        print ("Connection closed")
        out_f.write("Connection closed\n")

    if (response.count(b">")>0):
        print ("NON LOGIN NEEDED")
        out_f.write("NON LOGIN NEEDED\n")
    else:
        tn.write(user.encode('utf-8')  + b"\r\n")
        tn.read_until(b"Password:")
        tn.write(password.encode('utf-8') + b"\r\n")

    try:
        #tn.write(b"enable\r\n")
        #time.sleep(2)
        file_like_io = io.StringIO(tn.read_until(b"#").decode('ascii'))
        
        for line in file_like_io:
            stri = line.rstrip()
        
        prompt = stri

        prompt=prompt.lstrip("A:")
        prompt=prompt.lstrip("B:")

        print ("Szukany będzie prompt: ", prompt)

            #printList (stri, "tutaj")
        out_f.write(prompt)


    
    except:
        print ("-------------------------------------------------------------------------------------------------------------------------------")
        print ("---wyjąteczek ")
        print ("-------------------------------------------------------------------------------------------------------------------------------")
        out_f.write ("-------------------------------------------------------------------------------------------------------------------------------")
        out_f.write ("---wyjąteczek ")
        out_f.write ("-------------------------------------------------------------------------------------------------------------------------------")
        pass

    cmm_f=open('AX_CMM.txt', 'r')

    try:
        for line1 in cmm_f:
            print       ("\n\n\n\n---wykonuje komende ", line1)
            out_f.write ("---wykonuje komende " + line1 +"\n")

            #tn.write(b"show ip interface brief| include0/0\r\n")
            #tn.write(b"show sw-version | include appl-sw\r\n")
            #tn.write(b"show ip interface brief | include 0/0\r\n")
            line2 = "\r\n"
            tn.write(bytes(line1, 'utf-8')+ bytes(line2, 'utf-8'))
            #tn.read_until(b"#")

            #time.sleep(3)
            
            

            print ("Szukany będzie prompt: ", prompt)

            #file_like_io = io.StringIO(tn.read_until(b"#").decode('ascii'))
            #file_like_io = io.StringIO(tn.read_until(bytes(prompt, 'ascii')))            
            file_like_io = io.StringIO(tn.read_until(bytes(prompt, 'utf-8')).decode('ascii'))



                

            m_1 = []
            m_2 = []
            stri =""

            out_f.write(str(datetime_object))

            for line in file_like_io:
                #stri = str(datetime_object)+", "+HOST.rstrip().lstrip()+", "+line.rstrip()
                stri = line.rstrip().lstrip()
                m_1.append(stri)

            #m_1.pop(0)
            #m_1.pop(0)

            #m_1.pop()

            m=1
            #count lines
            for line in m_1:
                m_2.append(str(m)+' '+line)
                m=m+1

            #printList (m_2, HOST.rstrip())


            if (line1=="show card"):

                FoundMarkingLine = False
                for item in m_1:
                    if ('===============================================================================' in item):
                        FoundMarkingLine=False  

                    
                    if (FoundMarkingLine):
                        print (item)
                        CardNo=item[:3]
                        if not ((CardNo.lstrip().rstrip() =="A")or(CardNo.lstrip().rstrip() =="B")):
                            line4 = 'show card ' + CardNo + ' detail |  match "internal memory error"'
                            print       ("     ---wykonuje komende ", line4)
                            out_f.write ("     ---wykonuje komende " + line4 +"\n")

                            tn.write(bytes(line4, 'utf-8')+ bytes(line2, 'utf-8'))
                            
                            file_like_io = io.StringIO(tn.read_until(bytes(prompt, 'utf-8')).decode('ascii'))


                            print (line4)
                            m_1 = []
                            linesCount = 0
                            for line in file_like_io:
                                #stri = str(datetime_object)+", "+HOST.rstrip().lstrip()+", "+line.rstrip()
                                stri = line.rstrip().lstrip()
                                m_1.append(stri)
                                linesCount=linesCount+1
                            
                            print           (str(datetime_object)+" "+HOST.rstrip() +" " + prompt+" lines count for command, ", line4 , " is " , linesCount-2)
                            out_f_det.write (str(datetime_object)+"; "+HOST.rstrip() +"; " + prompt+" lines count for command, "+ line4 + "; " + str(linesCount-2) + "\n")
                            out_f.write     (str(datetime_object)+" "+HOST.rstrip() +" " + prompt+" lines count for command, "+ line4 + " is " + str(linesCount-2) + "\n")
                            #printList (m_1, HOST.rstrip())



                    if ('-------------------------------------------------------------------------------' in item):
                        FoundMarkingLine=True  
        
    except:
        print ("-------------------------------------------------------------------------------------------------------------------------------")
        print ("---wyjąteczek ")
        print ("-------------------------------------------------------------------------------------------------------------------------------")
        out_f.write ("-------------------------------------------------------------------------------------------------------------------------------")
        out_f.write ("---wyjąteczek ")
        out_f.write ("-------------------------------------------------------------------------------------------------------------------------------")
    
    tn.write(b"exit\r\n")
    tn.close()

    print      ("-----------------------------------------------OVER------------------------------------------------\n")
    out_f.write("-----------------------------------------------OVER------------------------------------------------\n")
    cmm_f.close


print ("-------------FINITO-------------\n\n\n\n\n\n\n")
out_f.write("------------FINITO-------------\n")



in_f.close
out_f.close
out_f_det.close
cmm_f.close
