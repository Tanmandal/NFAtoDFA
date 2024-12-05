from stringtokenizer import StringTokenizer
import os
import http.server
import socketserver
import webbrowser
import threading

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Override this method to suppress the logging output

def start_server():
    with socketserver.TCPServer(("", 0), QuietHandler) as httpd:  # Bind to port 0 for automatic port assignment
        port = httpd.server_address[1]  # Get the assigned port number
        print(f"Serving at port {port}")
        
        # Open the local server in the default web browser
        webbrowser.open(f'http://localhost:{port}')

        httpd.serve_forever()

def display():
    # Run the server in a separate thread to avoid blocking the program
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # Allows the program to exit even if the thread is running
    server_thread.start()

    input("Press Enter to stop the server...\n")  # Keep the program running until Enter is pressed
def merge(l1,l2):
    for i in l2:
        if i not in l1:
            l1.append(i)
    l1.sort()
def Eclosure(st,lmdtrns,Eclsr):
    if st in Eclsr:
        return
    Eclsr.append(st)
    for i in lmdtrns[st]:
        Eclosure(i,lmdtrns,Eclsr)
def Eclsrtbl(lmdtrns):
    Ectbl=[]
    for i in range(len(lmdtrns)):
        Eclsr=[]
        Eclosure(i,lmdtrns,Eclsr)
        Eclsr.sort()
        Ectbl.append(Eclsr)
    return Ectbl
def LNFAtoNFA(Ntbl,lmdtrns):
    Ectbl=Eclsrtbl(lmdtrns)
    UNtbl=[]
    for i in range(len(Ntbl)):
        UNtbl.append([])
        for j in range(len(Ntbl[i])):
            UNtbl[i].append([])
    for i in range(len(Ectbl)):
        for j in Ectbl[i]:
            for k in range(len(Ntbl[j])):
                merge(UNtbl[i][k],Ntbl[j][k])
    for i in range(len(UNtbl)):
        for j in range(len(UNtbl[i])):
            l=[]
            for k in UNtbl[i][j]:
                merge(l,Ectbl[k])
            UNtbl[i][j]=l
    return UNtbl
def NFAtoDFA(Nsts,Ntbl,Dsts,Dtbl,lmdtrns=[]):
    ns=len(Ntbl[0])
    x=Nsts[0]
    Eclsr=[]
    if len(lmdtrns)>0:
        Eclosure(0,lmdtrns,Eclsr)
        x=Eclsr
    Dtbl.append(Ntbl[0])
    Dsts.append(x)
    for i in Dtbl[0]:
        if i not in Dsts:
            Dsts.append(i)
    k=1
    while k<len(Dsts):
        Dtbl.append([])
        for w in range(ns):
            Dtbl[k].append([])
        for w in range(ns):
            for i in Dsts[k]:
                merge(Dtbl[k][w],Ntbl[i][w])
        for i in Dtbl[k]:
            if i not in Dsts:
                Dsts.append(i)
        k+=1
def stateDisp(stnm,stno):
    s=""
    for i in stno:
        if(len(s)>0):
            s+=","
        s+=stnm[i]
    if len(s)==0:
        s="Φ"
    return s
def isFinal(sts,fst):
    for i in sts:
        for j in fst:
            if i==j:
                return True
    return False
def dispTbl(trns,stsnm,sts,tbl,fst,lmdtrns=[]):
    buf=15
    print(' '*buf,end='')
    if len(lmdtrns)>0:
        print("λ".ljust(buf),end='')
    for i in trns:
        print(i.ljust(buf),end='')
    print('\n')
    for i in range(len(sts)):
        if(i==0):
            print('> ',end='')
        if isFinal(sts[i],fst):
            print('* ',end='')
        print(stateDisp(stsnm,sts[i]).ljust(buf),end='')
        if len(lmdtrns)>0:
            print(stateDisp(stsnm,lmdtrns[i]).ljust(buf),end='')
        for j in range(len(tbl[i])):
            print(stateDisp(stsnm,tbl[i][j]).ljust(buf),end='')
        print("\n")
def genFile(trns,stsnm,sts,tbl,fst):
    k=""
    for i in range(len(sts)):
        s="("+stateDisp(stsnm,sts[i])+")"
        if isFinal(sts[i],fst):
            s='*'+s
        if i==0:
            s='>'+s
        for j in range(len(tbl[i])):
            k=k+s+"|"+trns[j]+"|("+stateDisp(stsnm,tbl[i][j])+")\n"
    f=open("transfer.txt",'w',encoding='utf-8')
    f.write(k)

Nsts=[]
Nstsnm=[]
nl=int(input("Number of States in NFA Table : "))
print("Name NFA States : " )
for i in range(nl):
    s=""
    while True:
        s=input(str(i+1)+". ")
        if(s in Nstsnm):
            print("Same Name of State Used Again. Please Re-Enter\n")
        else:
            break
    Nsts.append([i])
    Nstsnm.append(s)
ini=""
while True:
    ini=input("Enter Initial State : ")
    if ini not in Nstsnm:
        print("Invalid Initial State. Please Enter Again")
    else:
        break
Nstsnm.remove(ini)
Nstsnm.insert(0,ini)
fst=[]
while True:
    fx=input("Enter Final States : ")
    st=StringTokenizer(fx,',')
    br=True
    while st.hasMoreTokens():
        fs=st.nextToken()
        if fs in Nstsnm:
            fst.append(Nstsnm.index(fs))
        else:
            br=False
            break
    if br:
        break
    else:
        fst=[]
        print("Invalid Final States. Please Enter Again")
nt=int(input("Number of Transitions in NFA Table : "))
Ntrns=[]
print("Name NFA Transitions : " )
for i in range(nt):
    s=""
    while True:
        s=input(str(i+1)+". ")
        if(s in Ntrns):
            print("Same Transition Entered Again. Please Re-Enter\n")
        else:
            break
    Ntrns.append(s)
Ntbl=[]
for i in range(nl):
    Ntbl.append([])
    j=0
    while j<nt:
        if j==len(Ntbl[i]):
            Ntbl[i].append([])
        s=input("ζ("+Nstsnm[i]+","+Ntrns[j]+")=> ")
        st=StringTokenizer(s,",")
        while(st.hasMoreTokens()):
            ss=st.nextToken()
            if ss not in Nstsnm and len(ss)>0:
                print("Invalid Transition States . Please Re-Enter")
                j-=1
                break
            else:
                if Nstsnm.index(ss) not in Ntbl[i][j]:
                    Ntbl[i][j].append(Nstsnm.index(ss))
            Ntbl[i][j].sort()
        j+=1
ch="N"+(input("Enter Y for λ-NFA : "))
ch=ch[-1]
lmdtrns=[]
if(ch=='Y' or ch=='y'):
    i=0
    while i<(len(Nstsnm)):
        s=input("ζ("+Nstsnm[i]+",λ)=> ")
        st=StringTokenizer(s,",")
        if i==len(lmdtrns):
            lmdtrns.append([])
        while(st.hasMoreTokens()):
            ss=st.nextToken()
            if ss not in Nstsnm and len(ss)>0:
                print("Invalid Transition States . Please Re-Enter")
                i-=1
            else:
                if Nstsnm.index(ss) not in lmdtrns[i]:
                    lmdtrns[i].append(Nstsnm.index(ss))
        i+=1
    print("λ-NFA : ")
    dispTbl(Ntrns,Nstsnm,Nsts,Ntbl,fst,lmdtrns)
    Ntbl=LNFAtoNFA(Ntbl,lmdtrns)
print("NFA : ")
dispTbl(Ntrns,Nstsnm,Nsts,Ntbl,fst)
Dsts=[]
Dtbl=[]
NFAtoDFA(Nsts,Ntbl,Dsts,Dtbl,lmdtrns);
print("DFA : ")
dispTbl(Ntrns,Nstsnm,Dsts,Dtbl,fst)

ch="N"+(input("Enter Y to See DFA diagram : "))
ch=ch[-1]

if ch=='y' or ch=='Y':
    genFile(Ntrns,Nstsnm,Dsts,Dtbl,fst)
    display()
if(os.path.exists('transfer.txt')):
    os.remove('transfer.txt')
input("Press Enter to Exit")