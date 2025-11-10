from stringtokenizer import StringTokenizer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
import base64
import os
import webview
import logging
import sys

console = Console()

class Bridge:
    def get_transfer_data(self):
        if os.path.exists("transfer.txt"):
            with open("transfer.txt", "r", encoding="utf-8") as f:
                return f.read()
        return "No transfer.txt file found."
    def save_image(self, img_data):
        # Extract Base64 content (after the comma)
        encoded = img_data.split(",")[1]
        image_bytes = base64.b64decode(encoded)

        window = webview.active_window()
        save_path = window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename="dfa_diagram.jpg"
        )

        if save_path:
            save_path = save_path[0]
            with open(save_path, "wb") as f:
                f.write(image_bytes)
            return "Image saved successfully!"
        return "Save canceled."

def display():
    # 🧩 Suppress Bottle and pywebview logs
    logging.getLogger('pywebview').setLevel(logging.ERROR)
    logging.getLogger('bottle').setLevel(logging.ERROR)

    # Redirect stdout/stderr temporarily to silence connection logs
    class DevNull:
        def write(self, _): pass
        def flush(self): pass

    sys.stdout = DevNull()
    sys.stderr = DevNull()

    try:
        html_path = os.path.abspath("index.html")
        if not os.path.exists(html_path):
            console.print("[bold red]Error Loading Webview[/bold red]")
            return
        bridge = Bridge()
        window = webview.create_window("DFA Visualizer", html_path, js_api=bridge)
        def on_loaded():
            window.maximize()
        webview.start(on_loaded, debug=False)
    finally:
        # Restore stdout/stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


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
    UNtbl=[ [ [] for _ in row ] for row in Ntbl]
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
        Dtbl.append([[] for _ in range(ns)])
        for w in range(ns):
            for i in Dsts[k]:
                merge(Dtbl[k][w],Ntbl[i][w])
        for i in Dtbl[k]:
            if i not in Dsts:
                Dsts.append(i)
        k+=1

def stateDisp(stnm,stno):
    if not stno:
        return "Φ"
    return ",".join(stnm[i] for i in stno)

def isFinal(sts,fst):
    return any(i in fst for i in sts)

def dispTbl(trns,stsnm,sts,tbl,fst,lmdtrns=[]):
    table = Table(title="Transition Table", show_lines=True)
    table.add_column("State", justify="center", style="bold cyan")
    if len(lmdtrns)>0:
        table.add_column("λ", justify="center", style="bold yellow")
    for i in trns:
        table.add_column(i, justify="center", style="green")

    for idx, state in enumerate(sts):
        row = []
        marker = ""
        if idx == 0:
            marker += "➤ "
        if isFinal(state, fst):
            marker += "* "
        row.append(marker + stateDisp(stsnm, state))
        if len(lmdtrns)>0:
            row.append(stateDisp(stsnm, lmdtrns[idx]))
        for j in range(len(tbl[idx])):
            row.append(stateDisp(stsnm, tbl[idx][j]))
        table.add_row(*row)
    console.print(table)

def genFile(trns,stsnm,sts,tbl,fst):
    k=""
    for i in range(len(sts)):
        s="("+stateDisp(stsnm,sts[i])+")"
        if isFinal(sts[i],fst):
            s='*'+s
        if i==0:
            s='>'+s
        for j in range(len(tbl[i])):
            k+=f"{s}|{trns[j]}|({stateDisp(stsnm,tbl[i][j])})\n"
    with open("transfer.txt",'w',encoding='utf-8') as f:
        f.write(k)




console.print(Panel("[bold blue]NFA → DFA Converter with λ-NFA Support[/bold blue]", expand=False))

Nsts=[]
Nstsnm=[]
while True:
    nl=Prompt.ask("[yellow]Number of States in NFA Table[/yellow]")
    if nl.isdigit() and nl!="0":
        nl=int(nl)
        break
    console.print("[red]Number of States must be a Positive Integer. Enter again.[/red]")
console.print("[cyan]Name NFA States:[/cyan]")
for i in range(nl):
    while True:
        s=Prompt.ask(f"[{i+1}] State Name")
        if s in Nstsnm:
            console.print("[red]Duplicate state name. Try again.[/red]")
        else:
            break
    Nsts.append([i])
    Nstsnm.append(s)

while True:
    ini=Prompt.ask("[green]Enter Initial State[/green]")
    if ini not in Nstsnm:
        console.print("[red]Invalid initial state.[/red]")
    else:
        break
Nstsnm.remove(ini)
Nstsnm.insert(0,ini)

fst=[]
while True:
    fx=Prompt.ask("[green]Enter Final States (comma separated)[/green]")
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
        console.print("[red]Invalid final states. Please re-enter.[/red]")

while True:
    nt=Prompt.ask("[yellow]Number of Transitions in NFA Table[/yellow]")
    if nt.isdigit() and nt!="0":
        nt=int(nt)
        break
    console.print("[red]Number of Transitions must be a Positive Integer. Enter again.[/red]")
Ntrns=[]
console.print("[cyan]Name NFA Transitions:[/cyan]")
for i in range(nt):
    while True:
        s=Prompt.ask(f"[{i+1}] Transition symbol")
        if s in Ntrns:
            console.print("[red]Duplicate transition. Try again.[/red]")
        elif s=="":
            console.print("[red]Transition needs a Symbol. Try again.[/red]")
        else:
            break
    Ntrns.append(s)

Ntbl=[]
for i in range(nl):
    Ntbl.append([])
    j=0
    while j<nt:
        s=Prompt.ask(f"ζ({Nstsnm[i]},{Ntrns[j]}) => [dim]comma separated[/dim]")
        st=StringTokenizer(s,",")
        lst=[]
        fl=False
        while(st.hasMoreTokens()):
            ss=st.nextToken()
            if ss not in Nstsnm and len(ss)>0:
                console.print("[red]Invalid state in transition![/red]")
                lst=[]
                fl=True
                break
            else:
                if len(ss)>0 and Nstsnm.index(ss) not in lst:
                    lst.append(Nstsnm.index(ss))
        if fl:
            continue
        lst.sort()
        Ntbl[i].append(lst)
        j+=1

if Confirm.ask("[magenta]Is this a λ-NFA?[/magenta]"):
    lmdtrns=[]
    i=0
    while i<len(Nstsnm):
        s=Prompt.ask(f"ζ({Nstsnm[i]},λ) => [dim]comma separated[/dim]")
        st=StringTokenizer(s,",")
        lmd=[]
        fl=False
        while(st.hasMoreTokens()):
            ss=st.nextToken()
            if ss not in Nstsnm and len(ss)>0:
                console.print("[red]Invalid λ transition![/red]")
                lmd=[]
                fl=True
                break
            else:
                if len(ss)>0 and Nstsnm.index(ss) not in lmd:
                    lmd.append(Nstsnm.index(ss))
        if fl:
            continue
        lmdtrns.append(lmd)
        i+=1
    console.print("\n[bold yellow]λ-NFA Transition Table:[/bold yellow]")
    dispTbl(Ntrns,Nstsnm,Nsts,Ntbl,fst,lmdtrns)
    Ntbl=LNFAtoNFA(Ntbl,lmdtrns)
else:
    lmdtrns=[]

console.print("\n[bold cyan]NFA Transition Table:[/bold cyan]")
dispTbl(Ntrns,Nstsnm,Nsts,Ntbl,fst)

Dsts=[]
Dtbl=[]
NFAtoDFA(Nsts,Ntbl,Dsts,Dtbl,lmdtrns)
console.print("\n[bold green]Equivalent DFA Transition Table:[/bold green]")
dispTbl(Ntrns,Nstsnm,Dsts,Dtbl,fst)

if Confirm.ask("[yellow]Do you want to visualize DFA diagram?[/yellow]"):
    genFile(Ntrns,Nstsnm,Dsts,Dtbl,fst)
    display()

if os.path.exists('transfer.txt'):
    os.remove('transfer.txt')

console.input("[bold cyan]Press Enter to Exit...[/bold cyan]")