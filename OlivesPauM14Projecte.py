from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from subprocess import PIPE, Popen
import time

def downloadFirewallFile():

    if rfirewall.get() == '':
        rutafitxer = "/firewall/firewall.sh"
        fitxerfirewall = "firewall.sh"
    else:
        rutafitxer = rfirewall.get()
        fitxerfirewall = rfirewall.get().rsplit('/', 1)[-1]
        
    ruta = usr.get()+'@'+ip.get()+':'+rutafitxer
    proces=Popen(['sshpass','-p', pwd.get(), 'scp',ruta,'.'],
            stdout=PIPE,stderr=PIPE, stdin=PIPE)
    
    textError=proces.stderr.read()
    proces.stderr.close()
    textOK=proces.stdout.read()
    proces.stdout.close()
    if not textError:

        p_cat=Popen(['cat', fitxerfirewall],stdout=PIPE,stderr=PIPE, stdin=PIPE)

        t_cat=p_cat.stdout.read()
        p_cat.stdout.close()
        text=str(t_cat.decode())
    else:
        text=textError

    Ti2.insert(END,text)

def sendFirewallFile(textbox):
    if rfirewall.get() == '':
        rutafitxer = "/firewall/firewall.sh"
        fitxerfirewall = "firewall.sh"
    else:
        rutafitxer = rfirewall.get()
        fitxerfirewall = rfirewall.get().rsplit('/', 1)[-1]

    if textbox == 1:
        punter = open(fitxerfirewall,"w")
        punter.write(Ti.get(1.0,"end"))
        punter.close()
    elif textbox == 2:
        punter = open(fitxerfirewall,"w")
        punter.write(Ti2.get(1.0,"end"))
        punter.close()

    ruta = usr.get()+'@'+ip.get()+':'+rutafitxer
    proces=Popen(['sshpass','-p', pwd.get(), 'scp', fitxerfirewall, ruta], stdout=PIPE,stderr=PIPE, stdin=PIPE)

    tproces=proces.stdout.read()
    proces.stdout.close()

    textError=proces.stderr.read()
    proces.stderr.close()

    if not textError:
        text="Enviat Correctament"
    else:
        text=textError

    if textbox == 1:
        Ti.insert(END,text)
    elif textbox == 2:
        Ti2.insert(END,text)

def addContent(option):
    if option == 1:
        text = "\niptables -F\n"
        Ti.insert(END,text)
    elif option == 2:
        if optionppd.get() == "Llista Negre":
            text = "\niptables -P INPUT ACCEPT\niptables -P OUTPUT ACCEPT\niptables -P FORWARD ACCEPT\n"
            Ti.insert(END,text)
        elif optionppd.get() == "Llista Blanca":
            text = "\niptables -P INPUT DROP\niptables -P OUTPUT DROP\niptables -P FORWARD DROP\n"
            Ti.insert(END,text)
        else:
            print(optionppd)
            print("Error")
    elif option == 3:
        text = "\niptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT\niptables -A OUTPUT -m state --state RELATED,ESTABLISHED -j ACCEPT\niptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT\n"
        Ti.insert(END,text)
    elif option == 4:
        text = "\niptables -A INPUT -s "+ipblock.get()+" -j DROP\n"
        Ti.insert(END,text)
    elif option == 5:
        text = "\niptables -A INPUT -s "+ipaccept.get()+" -j ACCEPT\n"
        Ti.insert(END,text)
    elif option == 6:
        text = "\niptables -A "+optionbp.get()+" -p "+protocolbp.get()+" --dport "+portbp.get()+" -j DROP\n"
        Ti.insert(END,text)
    elif option == 7:
        text = "\niptables -A "+optionpp.get()+" -p "+protocolpp.get()+" --dport "+portpp.get()+" -j ACCEPT\n"
        Ti.insert(END,text)

def deleteFrameContent():
    llista = marc2.grid_slaves()
    for l in llista:
        l.destroy()

def getFirewallOption():

    deleteFrameContent()

    if clicked.get() == "Borrar regles anteriors":
        global optionppd
        labelbra = Label(marc2, text="Vols borrar les regles anteriors?")
        labelbra.grid(column=0, row=0)
        brabutton = ttk.Button(marc2, text="Afegeix", command=lambda:[addContent(1), deleteFrameContent()])
        brabutton.grid(column=0, row=1)
    elif clicked.get() == "Politica per defecte":
        optionsppd = ["Tria una opcio...","Llista Negre","Llista Blanca"]
        optionppd = StringVar()
        dropdown = OptionMenu(marc2, optionppd, *optionsppd )
        dropdown.grid(column=0, row=0)
        ppdbutton = ttk.Button(marc2, text="Afegeix", command=lambda:[addContent(2), deleteFrameContent()])
        ppdbutton.grid(column=0, row=1)
    elif clicked.get() == "Permetre respostes":
        labelRespostes = Label(marc2, text="Vols permetre les respostes?")
        labelRespostes.grid(column=0, row=0)
        respostesbutton = ttk.Button(marc2, text="Afegeix", command=lambda:[addContent(3), deleteFrameContent()])
        respostesbutton.grid(column=0, row=1)
    elif clicked.get() == "Bloquejar connexio":
        global ipblock
        ipblock = StringVar()
        bclabel = Label(marc2, text="IP:")
        bclabel.grid(column=0, row=0)
        bcinput = Entry(marc2, width=30, textvariable=ipblock)
        bcinput.grid(column=1, row=0)
        bcbutton = ttk.Button(marc2, text="Afegeix", command=lambda:[addContent(4), deleteFrameContent()])
        bcbutton.grid(column=0, row=3)
    elif clicked.get() == "Permetre connexio":
        global ipaccept
        ipaccept = StringVar()
        bclabel = Label(marc2, text="IP:")
        bclabel.grid(column=0, row=0)
        bcinput = Entry(marc2, width=30, textvariable=ipaccept)
        bcinput.grid(column=1, row=0)
        bcbutton = ttk.Button(marc2, text="Afegeix", command=lambda:[addContent(5), deleteFrameContent()])
        bcbutton.grid(column=0, row=3)
    elif clicked.get() == "Bloquejar protocol":
        global protocolbp
        global portbp
        global optionbp
        protocolbp = StringVar()
        portbp = StringVar()
        optionbp = StringVar()
        bpprotocollabel = Label(marc2, text="Protocol:")
        bpprotocollabel.grid(column=0, row=0)
        bpprotocolinput = Entry(marc2, width=30, textvariable=protocolbp)
        bpprotocolinput.grid(column=1, row=0)
        bpportlabel = Label(marc2, text="Port:")
        bpportlabel.grid(column=0, row=1)
        bpportinput = Entry(marc2, width=30, textvariable=portbp)
        bpportinput.grid(column=1, row=1)
        bpoptionlabel = Label(marc2, text="INPUNT / OUTPUT:")
        bpoptionlabel.grid(column=0, row=2)
        bpoptioninput = Entry(marc2, width=30, textvariable=optionbp)
        bpoptioninput.grid(column=1, row=2)
        bpbutton = ttk.Button(marc2, text="Afegeix", command=lambda:[addContent(6), deleteFrameContent()])
        bpbutton.grid(column=0, row=3)
    elif clicked.get() == "Permetre protocol":
        global protocolpp
        global portpp
        global optionpp
        protocolpp = StringVar()
        portpp = StringVar()
        optionpp = StringVar()
        ppprotocollabel = Label(marc2, text="Protocol:")
        ppprotocollabel.grid(column=0, row=0)
        ppprotocolinput = Entry(marc2, width=30, textvariable=protocolpp)
        ppprotocolinput.grid(column=1, row=0)
        ppportlabel = Label(marc2, text="Port:")
        ppportlabel.grid(column=0, row=1)
        ppportinput = Entry(marc2, width=30, textvariable=portpp)
        ppportinput.grid(column=1, row=1)
        ppoptionlabel = Label(marc2, text="INPUNT / OUTPUT:")
        ppoptionlabel.grid(column=0, row=2)
        ppoptioninput = Entry(marc2, width=30, textvariable=optionpp)
        ppoptioninput.grid(column=1, row=2)
        ppbutton = ttk.Button(marc2, text="Afegeix", command=lambda:[addContent(7), deleteFrameContent()])
        ppbutton.grid(column=0, row=3)


def OpenWorkScreen():

    WorkScreen=Tk()
    WorkScreen.title("Firewall Remote V2 - Configuracio")
    w, h = WorkScreen.winfo_screenwidth()/2, WorkScreen.winfo_screenheight()/1.8
    WorkScreen.geometry("%dx%d+0+0" % (w, h))
    WorkScreen.configure(background='#4c95ff')
    menubar = Menu(WorkScreen)
    WorkScreen.config(menu=menubar)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Canviar Servidor", command=lambda:[WorkScreen.destroy(), OpenLoginScreen()])
    filemenu.add_separator()
    filemenu.add_command(label="Sortir", command=quit)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Iptables")

    menubar.add_cascade(label="Opcions", menu=filemenu)
    menubar.add_cascade(label="Ajuda", menu=helpmenu)

    tabControl = ttk.Notebook(WorkScreen)
  
    tab1 = Frame(tabControl)
    tab2 = Frame(tabControl)
      
    tabControl.add(tab1, text ='Basic')
    tabControl.add(tab2, text ='Avançat')
    tabControl.pack(expand = 1, fill ="both")

    global rfirewall
    global Ti
    global Ti2
    global clicked
    global marc2
    rfirewall = StringVar()

    marc=Frame(tab1)
    marc.grid()
    marc2=Frame(marc)
    marc2.grid(column=0, row=2, rowspan=2, sticky="nsew", padx=20)

    optionLabel = Label(marc, text="Selecciona una opcio: ")
    optionSendButton = ttk.Button(marc, text="Següent", command=getFirewallOption)
    botoDFirewall=ttk.Button(tab2,text="Descarrega Fitxer Firewall", command=downloadFirewallFile)
    botoEFirewall=ttk.Button(marc,text="Enviar", command=lambda:sendFirewallFile(1))
    botoEFirewall2=ttk.Button(tab2,text="Enviar", command=lambda:sendFirewallFile(2))

    RutaFirewall=Entry(tab2,width=30, textvariable=rfirewall)

    Ti=Text(marc, wrap='none', width=45)
    Svi=Scrollbar(marc, orient="vertical", command=Ti.yview)
    Shi=Scrollbar(marc, orient="horizontal", command=Ti.xview)
    Ti.config(yscrollcommand=Svi.set)
    Ti.config(xscrollcommand=Shi.set)

    Ti2=Text(tab2,height=20,width=110, wrap='none')
    Svi2=Scrollbar(tab2, orient="vertical", command=Ti2.yview)
    Shi2=Scrollbar(tab2, orient="horizontal", command=Ti2.xview)
    Ti2.config(yscrollcommand=Svi2.set)
    Ti2.config(xscrollcommand=Shi2.set)

    options = ["Tria una opcio...","Borrar regles anteriors","Politica per defecte","Permetre respostes","Bloquejar connexio","Permetre connexio","Bloquejar protocol","Permetre protocol"]
    clicked = StringVar()
    drop = OptionMenu(marc, clicked, *options )
    drop.grid(column=0, row=0, padx=180)

    optionLabel.grid(row=0, column=0, sticky="w", padx=20, pady=20)
    optionSendButton.grid(row=1, column=0, sticky="wn", padx=160)
    botoDFirewall.grid(column=0, row=0, columnspan=2, padx=5, pady=5)
    RutaFirewall.grid(column=0, row=0, sticky=(W,N), padx=5, pady=5)
    Ti.grid(column=1, row=0, rowspan=3, sticky="nsew")
    Svi.grid(column=2, row=0, rowspan=3, sticky=N+S)
    Shi.grid(column=1, row=3, sticky=W+E)
    Ti2.grid(column=0, row=1, sticky=(W,N))
    Svi2.grid(column=1, row=1, sticky=N+S)
    Shi2.grid(column=0, row=2, sticky=W+E)
    botoEFirewall.grid(column=1, row=4, padx=5, pady=5)
    botoEFirewall2.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

    WorkScreen.mainloop()

def OpenLoginScreen():
    
    LoginScreen=Tk()
    LoginScreen.title("Firewall Remote V2 - Login")
    w, h = LoginScreen.winfo_screenwidth()/2, LoginScreen.winfo_screenheight()/2
    LoginScreen.geometry("%dx%d+0+0" % (w, h))
    LoginScreen.configure(background='#4c95ff')
    
    global pwd
    global ip
    global usr

    pwd = StringVar()
    ip = StringVar()
    usr = StringVar()

    TitleText = Label(LoginScreen, text="FIREWALL REMOTE V2", background="#4c95ff", foreground="white", font='Montserrat 25 bold', anchor="center")
    TitleText.grid(row=0, column=0, sticky="nsew", pady=(80,0))
    labelUsr = Label(LoginScreen, text="Usuari: ", foreground="white", font='Montserrat 16 bold', background="#4c95ff")
    entryUsr = Entry(LoginScreen, width=15, textvariable=usr)
    labelPwd = Label(LoginScreen, text="Contrasenya: ", foreground="white", font='Montserrat 16 bold', background="#4c95ff")
    entryPwd = Entry(LoginScreen, show="*", width=15, textvariable=pwd)
    labelIp = Label(LoginScreen, text="IP: ", foreground="white", font='Montserrat 16 bold', background="#4c95ff")
    entryIp = Entry(LoginScreen, width=15, textvariable=ip)
    botoSubmit = Button(LoginScreen,text='Connecta', width=40, style="botoSubmit.TButton", command=lambda:[LoginScreen.destroy(), OpenWorkScreen()])

    s = Style()
    s.configure("botoSubmit.TButton", borderwidth=4, foreground="white", background="#454545", font='Montserrat 10 bold')

    labelUsr.grid(row=1, column=0, sticky="nsew", pady=(30,0), padx=300)
    entryUsr.grid(row=1, column=0, sticky="nsew", pady=(30,0), padx=(470,300))
    labelPwd.grid(row=2, column=0, sticky="nsew", pady=(10,0), padx=300)
    entryPwd.grid(row=2, column=0, sticky="nsew", pady=(10,0), padx=(470,300))
    labelIp.grid(row=3, column=0, sticky="nsew", pady=(10,0), padx=300)
    entryIp.grid(row=3, column=0, sticky="nsew", pady=(10,0), padx=(470,300))
    botoSubmit.grid(column=0, row=4, columnspan=2, pady=(20,0))

    Grid.rowconfigure(LoginScreen, 0, weight=0)
    Grid.columnconfigure(LoginScreen, 0, weight=1)
    Grid.rowconfigure(LoginScreen, 1, weight=0)
    Grid.rowconfigure(LoginScreen, 2, weight=0)

    entryUsr.focus()
    LoginScreen.bind('<Return>',OpenWorkScreen)
    LoginScreen.mainloop()

def OpenLoadingScreen():
    LoadingScreen=Tk()
    LoadingScreen.title("Firewall Remote V2")
    w, h = LoadingScreen.winfo_screenwidth()/2, LoadingScreen.winfo_screenheight()/2
    LoadingScreen.geometry("%dx%d+0+0" % (w, h))
    LoadingScreen.configure(background='#4c95ff')

    TitleText = Label(LoadingScreen, text="FIREWALL REMOTE V2", background="#4c95ff", foreground="white", font='Montserrat 25 bold', anchor="center")
    TitleText.grid(row=0, column=0, sticky="nsew", pady=(80,0))
    LoadingText = Label(LoadingScreen, text="Carregant...", background="#4c95ff", foreground="white", font='Montserrat 18 bold')
    LoadingText.grid(row=1, column=0, sticky="nsew", padx=100, pady=(100,0))
    
    s = Style()
    s.theme_use('default')
    s.configure("red.Horizontal.TProgressbar", troughcolor ='#454545', background='white', thickness=30, borderwidth="0")
    progress = Progressbar(LoadingScreen, style="red.Horizontal.TProgressbar", orient = HORIZONTAL,length = LoadingScreen.winfo_screenheight()/2, mode = 'determinate')
    progress.grid(row=2, column=0, sticky="nsew", padx=100, pady=10)

    Grid.rowconfigure(LoadingScreen, 0, weight=0)
    Grid.columnconfigure(LoadingScreen, 0, weight=1)
    Grid.rowconfigure(LoadingScreen, 1, weight=0)
    Grid.rowconfigure(LoadingScreen, 2, weight=0)

    def StartProgressBar():

        progress['value'] = 0
        LoadingScreen.update_idletasks()
        time.sleep(0.7)

        progress['value'] = 20
        LoadingScreen.update_idletasks()
        time.sleep(0.5)
      
        progress['value'] = 40
        LoadingScreen.update_idletasks()
        time.sleep(0.5)
      
        progress['value'] = 50
        LoadingScreen.update_idletasks()
        time.sleep(0.5)
      
        progress['value'] = 60
        LoadingScreen.update_idletasks()
        time.sleep(0.5)
      
        progress['value'] = 80
        LoadingScreen.update_idletasks()
        time.sleep(0.5)
      
        progress['value'] = 100
        LoadingScreen.update_idletasks()
        time.sleep(0.5)

        LoadingScreen.destroy()
        OpenLoginScreen()
  
    StartProgressBar()
    LoadingScreen.mainloop()

OpenLoadingScreen()