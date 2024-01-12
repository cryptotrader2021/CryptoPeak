import importlib
from socket import timeout
import subprocess

#check pip installation
def check_pip():
    try:
        result = subprocess.run(['pip', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Pip hasn't been found on your PC. Please install it before using this software")
            quit()
            
    except FileNotFoundError:
        print("Pip hasn't been found on your PC. Please install it before using this software")
        quit()
        
check_pip()

#check and install python library
requiredLibraries = [
    'requests', 'hmac', 'hashlib', 'base64', 'time', 'pygame', 'numpy', 'math',
    'json', 'time', 'random', 'string', 'smtplib', 'locale', 'sqlite3','time','os',
    'datetime','webbrowser','math','datetime','gc','email','tkinter','threading'
]

missingLibs = []
for lib in requiredLibraries:
    try:
        importlib.import_module(lib)
    except ImportError:
        missingLibs.append(lib)

if missingLibs:
    print("Installing missing libraries:", missingLibs)
    subprocess.run(['pip', 'install', *missingLibs], check=True)
    print("Libraries installed successfully.\n")

import funzioni,sqlite3,time,datetime,webbrowser,math,datetime,gc,threading
import tkinter as tk
from tkinter import messagebox

#disclaimer accept
reply = messagebox.askyesno("Disclaimer", "The use of this cryptocurrency order automation software is entirely at the user's risk. The user is solely responsible for any financial loss, damages, or consequences arising from the use of this software. Please be aware that executing automatic orders carries significant risks, including but not limited to sudden market changes, cryptocurrency price fluctuations, and possible technical malfunctions. This software is provided without any warranties, express or implied. By using this software, you agree to waive any liability from the creators or developers. It is strongly advised to exercise caution, fully understand the risks involved, and consult with a qualified financial professional before using this software for cryptocurrency trading. Do you accept these terms?")
if not reply:
    quit()

#check for numeric input 
def checkNumber(text):
    try:
        text = float(text)
        if text<=0:
            return False
        
        return True
    
    except ValueError:
        return False
  
con = sqlite3.connect("cryptoDB.db")
cursor = con.cursor()
    
#check and assign all parameter
def startButtonlick():
    
    global clientKucoin,startThread,onlyCrypto,apiKey,apiSecret,apiPassphrase,percPriceChange,waitingSecondForChange,maxOrder,orderAmount,percGain
    
    apiKey = apiKey_entry.get("1.0", tk.END).strip()
    apiSecret = apiSecret_entry.get("1.0", tk.END).strip()
    apiPassphrase = apiPassphrase_entry.get("1.0", tk.END).strip()
    
    if apiKey=="" or apiSecret=="" or apiPassphrase=="":
        messagebox.showerror("Error", "To connect to Kucoin, it is necessary to fill out all the fields")
        return
    
    clientKucoin = funzioni.Client(apiKey,apiSecret,apiPassphrase)

    funzioni.personalEmail = personalEmail_entry.get("1.0", tk.END).lower().strip()
    funzioni.googleEmail = googleEmail_entry.get("1.0", tk.END).lower().strip()
    funzioni.googleAppPassword = googleAppPassword_entry.get("1.0", tk.END).strip()
    
    if funzioni.personalEmail != "" or funzioni.googleEmail != "" or funzioni.googleAppPassword != "":
        if funzioni.personalEmail == "" or funzioni.googleEmail == "" or funzioni.googleAppPassword == "":
            messagebox.showerror("Error", "If you want to receive emails, it is essential to complete all the parameters associated with email")
            return  

    onlyCrypto.clear()
    
    text = onlyCrypto_entry.get("1.0", tk.END).upper().strip()
    for word in text.split(","):
        if word!="":
            onlyCrypto.append(word+"-USDT")
    
    percPriceChange = percPriceChange_entry.get("1.0", tk.END).strip()
    waitingSecondForChange = waitingSecondForChange_entry.get("1.0", tk.END).strip()
    maxOrder = maxOrder_entry.get("1.0", tk.END).strip()
    orderAmount = orderAmount_entry.get("1.0", tk.END).strip()
    percGain = percGain_entry.get("1.0", tk.END).strip()
    bodyFactor = bodyFactor_entry.get("1.0", tk.END).strip()
    timeOut = timeOut_entry.get("1.0", tk.END).strip()
    
    if not checkNumber(percPriceChange) or not checkNumber(waitingSecondForChange) or not checkNumber(bodyFactor) or not checkNumber(timeOut):
        messagebox.showerror("Error", "Please compile and enter only number in max orders, order amount, perc gain, body factor, timeout") 
        return

    if percPriceChange == "" or waitingSecondForChange == "":
        messagebox.showerror("Error", "To price monitor, it is necessary to fill Price Change and Seconds")
        return 
    
    percPriceChange = float(percPriceChange)
    funzioni.timeOut = int(timeOut)
    waitingSecondForChange = int(waitingSecondForChange)
    bodyFactor = int(bodyFactor)  
    
    if waitingSecondForChange>55 or waitingSecondForChange<5:
        messagebox.showerror("Error", "The seconds change value must be from 5 to 55")
        return

    if bodyFactor<1:
        messagebox.showerror("Error", "Factor value must be >0")
        return          

    if maxOrder != "" or orderAmount != "" or percGain != "":
        if maxOrder == "" or orderAmount == "" or percGain == "": 
            messagebox.showerror("Error", "If you want to place automatic orders, it is essential to complete all the parameters associated with orders")
            maxOrder=-1
            return
        
        if not checkNumber(maxOrder) or not checkNumber(orderAmount) or not checkNumber(percGain):
            messagebox.showerror("Error", "Please only number2") 
            return 
        
        maxOrder = int(maxOrder)
        orderAmount = float(orderAmount)
        percGain = float(percGain)
    
    else:
        maxOrder=-1

    con = sqlite3.connect("cryptoDB.db")
    cursor = con.cursor()

    cursor.execute(f"UPDATE credenziali SET apiKey='{apiKey}', apiSecret='{apiSecret}', apiPassphrase='{apiPassphrase}', personalEmail='{funzioni.personalEmail}', googleEmail='{funzioni.googleEmail}', googleAppPassword='{funzioni.googleAppPassword}', onlyCrypto='{text}', timeOut='{timeOut}'")
    con.commit()
    
    cursor.close()
    con.close()
    
    
    if startThread==False:
        startThread=True
        startButton.config(text="Stop monitoring") 
        
    else:
        startThread=False
        startButton.config(text="Start monitoring")
        statusLabel.config(text="STATUS: End scanning") 

print("***************** AUTOMATED CRYPTO TRADING PRICE PEAK INTERCEPTOR *******************")

startThread=False
apiKey = ""
apiSecret = ""
apiPassphrase = ""
percPriceChange = 0
percGain = 0
bodyFactor = 1
openBrowser = False
sendEmail = False
checkPreviuosBar = False
onlyCrypto = []


#main windows build
window = tk.Tk()
window.title("Crypto peak detecting")
window.geometry("1115x750")
window.iconbitmap('trb.ico')
window.update()

top=10
height=20
space=10
lblWidth=135
txtWidth=400

#Kucoin credential
label1 = tk.Label(window, text="Kucoin API Key", anchor="w")
label1.place(x=10, y=top, w=lblWidth, h=height)
apiKey_entry = tk.Text(window, width=580)
apiKey_entry.place(x=lblWidth+10, y=top, w=txtWidth, h=height)
top+=height+space

label1 = tk.Label(window, text="Kucoin API Secret", anchor="w")
label1.place(x=10, y=top, w=lblWidth, h=height)
apiSecret_entry = tk.Text(window, width=580)
apiSecret_entry.place(x=lblWidth+10, y=top, w=txtWidth, h=height)
top+=height+space

label1 = tk.Label(window, text="Kucoin API Passphrase", anchor="w")
label1.place(x=10, y=top, w=lblWidth, h=height)
apiPassphrase_entry = tk.Text(window, width=580)
apiPassphrase_entry.place(x=lblWidth+10, y=top, w=txtWidth, h=height)

top=10

#Google credential
label1 = tk.Label(window, text="Personal e-mail", anchor="w")
label1.place(x=lblWidth+txtWidth+30, y=top, w=lblWidth, h=height)
personalEmail_entry = tk.Text(window, width=580)
personalEmail_entry.place(x=(lblWidth*2)+txtWidth+30, y=top, w=txtWidth, h=height)
top+=height+space

label1 = tk.Label(window, text="Google e-mail", anchor="w")
label1.place(x=lblWidth+txtWidth+30, y=top, w=lblWidth, h=height)
googleEmail_entry = tk.Text(window, width=580)
googleEmail_entry.place(x=(lblWidth*2)+txtWidth+30, y=top, w=txtWidth, h=height)
top+=height+space

label1 = tk.Label(window, text="Google App Password", anchor="w")
label1.place(x=lblWidth+txtWidth+30, y=top, w=lblWidth, h=height)
googleAppPassword_entry = tk.Text(window, width=580)
googleAppPassword_entry.place(x=(lblWidth*2)+txtWidth+30, y=top, w=txtWidth, h=height)
top+=height+space*2

#Peak settings
label1 = tk.Label(window, text="Symbol to monitor (separated by a comma, ex. BTC,ETH,DOGE)", anchor="w")
label1.place(x=10, y=top, w=340, h=height)
onlyCrypto_entry = tk.Text(window, width=580)
onlyCrypto_entry.place(x=360, y=top, w=740, h=height)
top+=height+space

#Peak settings
label1 = tk.Label(window, text="Percentage change in price to be intercepted", anchor="w")
label1.place(x=10, y=top, w=250, h=height)
percPriceChange_entry = tk.Text(window, width=580)
percPriceChange_entry.place(x=290, y=top, w=60, h=height)
top+=height+space

label1 = tk.Label(window, text="How many seconds should the price change occur", anchor="w")
label1.place(x=10, y=top, w=280, h=height)
waitingSecondForChange_entry = tk.Text(window, width=580)
waitingSecondForChange_entry.place(x=290, y=top, w=60, h=height)
top+=height+space

label1 = tk.Label(window, text="Factor candle's body compared to the first", anchor="w")
label1.place(x=10, y=top, w=280, h=height)
bodyFactor_entry = tk.Text(window, width=580)
bodyFactor_entry.place(x=290, y=top, w=60, h=height)
top+=height+space*2


#Order settings
label1 = tk.Label(window, text="Max nr. orders", anchor="w")
label1.place(x=10, y=top, w=100, h=height)
maxOrder_entry = tk.Text(window, width=580)
maxOrder_entry.place(x=110, y=top, w=60, h=height)
top+=height+space

label1 = tk.Label(window, text="Order amount", anchor="w")
label1.place(x=10, y=top, w=100, h=height)
orderAmount_entry = tk.Text(window, width=580)
orderAmount_entry.place(x=110, y=top, w=60, h=height)
top+=height+space

label1 = tk.Label(window, text="Profit percentage", anchor="w")
label1.place(x=10, y=top, w=100, h=height)
percGain_entry = tk.Text(window, width=580)
percGain_entry.place(x=110, y=top, w=60, h=height)
top+=height+space*2

#Open browser
label1 = tk.Label(window, text="Browser open upon peak detection", anchor="w")
label1.place(x=10, y=top, w=190, h=height)
openBrowserVar = tk.BooleanVar()

def readOpenBrowserVar():
    global openBrowser
    openBrowser = openBrowserVar.get()
    
chkOpenBrowser = tk.Checkbutton(window, variable=openBrowserVar, command=readOpenBrowserVar)
chkOpenBrowser.place(x=210, y=top-2)
top+=height+space

#Send email
label1 = tk.Label(window, text="Send email upon peak detection", anchor="w")
label1.place(x=10, y=top, w=190, h=height)
sendEmailVar = tk.BooleanVar()

def readSendEmailVar():
    global sendEmail
    
    sendEmail = sendEmailVar.get()
    
    if sendEmail:

        funzioni.personalEmail = personalEmail_entry.get("1.0", tk.END).lower().strip()
        funzioni.googleEmail = googleEmail_entry.get("1.0", tk.END).lower().strip()
        funzioni.googleAppPassword = googleAppPassword_entry.get("1.0", tk.END).strip()

        if funzioni.personalEmail != "" or funzioni.googleEmail != "" or funzioni.googleAppPassword != "":
            if funzioni.personalEmail == "" or funzioni.googleEmail == "" or funzioni.googleAppPassword == "":
                messagebox.showerror("Error", "If you want to receive emails, it is essential to complete all the parameters associated with email")
                sendEmailVar.set(False)
                return
        else:
            messagebox.showerror("Error", "If you want to receive emails, it is essential to complete all the parameters associated with email")
            sendEmailVar.set(False)
        
chkSendEmail = tk.Checkbutton(window, variable=sendEmailVar, command=readSendEmailVar)
chkSendEmail.place(x=210, y=top-2)

top+=height+space*2

#TimeOut operations
label1 = tk.Label(window, text="Request timeout", anchor="w")
label1.place(x=10, y=top, w=90, h=height)
timeOut_entry = tk.Text(window, width=580)
timeOut_entry.place(x=110, y=top, w=20, h=height)
top+=height+space*2

#Start startButton
startButton = tk.Button(window, text="Start monitoring", command=startButtonlick)
startButton.place(x=10, y=top, w=150, h=height*1.5)
top+=height+space*3

#Operations label
statusLabel = tk.Label(window, text="STATUS: Awaiting for start monitoring", anchor="w")
statusLabel.place(x=10, y=top, w=1000, h=height)
top+=height+space

#Peak report
listbox = tk.Listbox(window, selectmode=tk.SINGLE)
listbox.place(x=10, y=top, w=1095, h=200)
scrollbar = tk.Scrollbar(listbox, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

window.update()

listbox.insert(tk.END, "Peak report")
listbox.yview(tk.END)

#data DB extraction
cursor.execute("SELECT * FROM credenziali")
row = cursor.fetchone()
apiKey_entry.insert(tk.END, row[0]) 
apiSecret_entry.insert(tk.END, row[1]) 
apiPassphrase_entry.insert(tk.END, row[2]) 
personalEmail_entry.insert(tk.END, row[3]) 
googleEmail_entry.insert(tk.END, row[4]) 
googleAppPassword_entry.insert(tk.END, row[5])
onlyCrypto_entry.insert(tk.END, row[6])
timeOut_entry.insert(tk.END, row[7])

#client init
clientKucoin = '' 

#price decimal count
def decimalCount(numero):
    parti = str(numero).split('.')
    
    if len(parti) == 2:
        return int((10 ** len(parti[1]))/10)
    else:
        return 1
    
#limit and market order execution
def makeOrder(symbol,price):
    
    global maxOrder,startThread
    
    _percGain = 1+((1/100)*percGain) 
    
    orderBuy = clientKucoin.orderMarketBuy(symbol,orderAmount)
                
    if orderBuy != None:
        orderId = orderBuy['orderId']
        maxOrder-=1
    
    time.sleep(0.5)
                
    #extract order data to obtain the purchase price and quantity.
    quantita=0
    buyingPrice=0 
    conta=0
    while True:
        orderData = clientKucoin.getOrder(orderId)
                    
        if len(orderData)>0:
               
            for dati in orderData:
                buyingPrice+=float(dati['price'])
                quantita+=float(dati['size'])
            
            #calculate the selling price and place the limit order
            buyingPrice/=len(orderData)
            if buyingPrice<=0:
                buyingPrice=price
                
            date =datetime.datetime.now().strftime("%d-%m-%Y - %H:%M.%S")
            listbox.insert(tk.END, f"{date} - Buy order executed: {symbol}, ID = {orderId}, price:{buyingPrice}")
            listbox.yview(tk.END)
            
            priceVendita = math.floor((buyingPrice*_percGain)*decimalCount(dati['price']))/decimalCount(dati['price'])
            quantita = math.floor(quantita*decimalCount(dati['size']))/decimalCount(dati['size'])
            
            orderSellLimit = clientKucoin.orderMarketSellLimit(symbol,quantita,priceVendita)
            del orderData
            break
            
        time.sleep(0.5)
        conta+=1
        if conta==50:
            date =datetime.datetime.now().strftime("%d-%m-%Y - %H:%M.%S")
            listbox.insert(tk.END, f"{date} - Failed attempt to place a sell order of {symbol}, please manually place a sell order on KuCoin at soon possible!")
            listbox.yview(tk.END)
            funzioni.playSound(10,0.2)
            break
        
    if orderSellLimit != None:
        date =datetime.datetime.now().strftime("%d-%m-%Y - %H:%M.%S")
        orderId = orderSellLimit['orderId']
        listbox.insert(tk.END, f"{date} - Sell limit order placed: {symbol}, qty:{quantita}, price:{priceVendita}\n")
        listbox.yview(tk.END)
        funzioni.playSound(1,0.5)
        del orderSellLimit
        
    else:
        date =datetime.datetime.now().strftime("%d-%m-%Y - %H:%M.%S")
        listbox.insert(tk.END, f"{date} - Failed attempt to place a sell order of {symbol}, please manually place a sell order on KuCoin at soon possible!")
        listbox.yview(tk.END)
        funzioni.playSound(10,0.2)
        
    if maxOrder==0:
        startThread=False
        statusLabel.config(text="STATUS: End scanning")
        startButton.config(text="Start monitoring")         

#check exclusion for leverage crypto and not USDT exchange
excludedText = ['1S','2S','3S','4S','5S','1L','3L','2L','4L','5L','UP','DOWN','WBTC','WETH','WBNB'] 
def check(text):
    
    if not text.endswith('USDT'):
        return False
    
    for word in excludedText:
        if word in text:
            return False
        
    return True   

#********************* start **********************
def start():

    global startThread,statusLabel,prevSymbolName
    
    prevSymbolName=""    

    con = sqlite3.connect("cryptoDB.db")
    cursor = con.cursor()

    while True:       
        while not startThread:
            time.sleep(1)
            
        _percPriceChange = 1+((1/100)*percPriceChange)
        
        cursor.execute("DELETE FROM simboli")
        con.commit()

        secondNow = datetime.datetime.now().second
        
        while secondNow!=0 and startThread:
            statusLabel.config(text=f"STATUS: Waiting {59-secondNow} seconds for get open price list")            
            time.sleep(0.5)
            secondNow = datetime.datetime.now().second
            
        #Add symbol and priceBefore to the dict1
        cryptoList = clientKucoin.allTickers()
        if cryptoList==None:
            date =datetime.datetime.now().strftime("%d-%m-%Y - %H:%M.%S")
            listbox.insert(tk.END, f"{date} - Error get Kucoin price list")
            listbox.yview(tk.END)  
            time.sleep(1)
            continue
        
        for data in cryptoList['ticker']:
            if not data['last']==None:
                symbol = data['symbol']
                price = float(data['last'])
                
                if symbol in onlyCrypto or not onlyCrypto:
                    if check(symbol) and price>0:
                        cursor.execute("INSERT INTO simboli (symbol, priceBefore) VALUES (?, ?)", (symbol, price)) 
        con.commit()
        
        while secondNow==0 and startThread:
            secondNow = datetime.datetime.now().second
            time.sleep(0.5)
        
        while secondNow!=0 and startThread:
            statusLabel.config(text=f"STATUS: Waiting {59-secondNow} seconds for get close price list")            
            time.sleep(0.5)
            secondNow = datetime.datetime.now().second
         
        #Add priceAfter and body to the DB
        cryptoList = clientKucoin.allTickers()        
        if cryptoList==None:
            date =datetime.datetime.now().strftime("%d-%m-%Y - %H:%M.%S")
            listbox.insert(tk.END, f"{date} - Error get Kucoin price list")
            listbox.yview(tk.END)  
            time.sleep(1)
            continue
        
        for data in cryptoList['ticker']:
            if not data['last']==None:
                symbol = data['symbol']
                price = float(data['last'])
                
                if symbol in onlyCrypto or len(onlyCrypto)==0:
                    if check(symbol) and price>0:
                        cursor.execute(f"SELECT priceBefore FROM simboli WHERE symbol='{symbol}'")
                        row = cursor.fetchone()
                        if row:
                            body = math.fabs(price-row[0])
                            cursor.execute("UPDATE simboli SET priceAfter=?, body=? WHERE symbol=?", (price, body, symbol))
                            con.commit()
                         
        secondNow = datetime.datetime.now().second
        while secondNow==0 and startThread:
            secondNow = datetime.datetime.now().second
            time.sleep(0.25)
            
        #wait for waitingSecondForChange and check for condition price
        while secondNow<waitingSecondForChange and startThread:
            statusLabel.config(text=f"STATUS: Waiting {waitingSecondForChange-secondNow} seconds for peak check")            
            time.sleep(0.5)
            secondNow = datetime.datetime.now().second
            
        statusLabel.config(text=f"STATUS: Download prices list")
            
        cryptoList = clientKucoin.allTickers()
        if cryptoList==None:
            date =datetime.datetime.now().strftime("%d-%m-%Y - %H:%M.%S")
            listbox.insert(tk.END, f"{date} - Error get Kucoin price list")
            listbox.yview(tk.END) 
            time.sleep(1)
            continue   

        #check for peak
        for data in cryptoList['ticker']:
        
            if not data['last']==None:
                symbol = data['symbol']
                price = float(data['last'])
                
                if (symbol in onlyCrypto or len(onlyCrypto)==0) and symbol!=prevSymbolName:
                            
                    if check(symbol) and price>0:

                        cursor.execute(f"SELECT * FROM simboli WHERE symbol='{symbol}'")
                        row = cursor.fetchone()
                        if row:                      
                            if(price>row[2]*_percPriceChange):
                                if(price-row[2]>row[3]*bodyFactor):
                                    prevSymbolName=symbol
                                        
                                    if maxOrder>0:
                                        statusLabel.config(text="STATUS: Peak detected, start order")
                                        makeOrder(symbol,price)
                                    else:
                                        statusLabel.config(text="STATUS: Peak detected")
                                            
                                    date =datetime.datetime.now().strftime("%d-%m-%Y - %H:%M.%S")
                                    listbox.insert(tk.END, f"{date} - Peak detected: {symbol}")
                                    listbox.yview(tk.END)
                                        
                                    if openBrowser:
                                        webbrowser.open(f"https://www.kucoin.com/trade/{symbol}")

                                    funzioni.playSound(1,0.5)
                                
                                    if sendEmail:
                                        statusLabel.config(text="STATUS: ending email")
                                        funzioni.send_email("Price peak detected", f"The crypto {symbol} has experienced a price increase of {_percPriceChange}%")
        if not startThread:
            listbox.insert(tk.END,"##### End scanning #####")
            listbox.yview(tk.END)
        gc.collect()

thread = threading.Thread(target=start)
thread.start()

window.mainloop()
