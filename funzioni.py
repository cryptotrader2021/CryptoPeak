import requests,hmac,hashlib,base64,time,pygame, numpy, math, json,time,random,string,smtplib,locale
from email.mime.text import MIMEText

timeOut = 3
FIAT = "USDT"

#Kucoin client
class Client:
    def __init__(self, api_key, api_secret, api_passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
        self.orderID = 0
        
    def get_symbol_ticker(self,symbol):
        url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-{FIAT}"
        now = int(time.time() * 1000)
        str_to_sign = str(now) + 'GET' + f"/api/v1/market/orderbook/level1?symbol={symbol}-{FIAT}"
        signature = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())

        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": self.passphrase,
            "KC-API-KEY-VERSION": "2"
        }
        response = requests.request('get', url, headers=headers,timeout=TimeOut)
        if response.json()['code']!='200000':
            print(f"\nErrore get_symbol_ticker: {response.json()}")
            return None
        else:
            #print(f"\nget_symbol_ticker {symbol}: {response.json()}")
            return response.json()['data']
        
    def allTickers(self):
        url = f"https://api.kucoin.com/api/v1/market/allTickers"
        now = int(time.time() * 1000)
        str_to_sign = str(now) + 'GET' + f"/api/v1/market/allTickers"
        signature = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())

        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": self.passphrase,
            "KC-API-KEY-VERSION": "2"
        }
        try:
            response = requests.request('get', url, headers=headers,timeout=timeOut)
            if response.json()['code']!='200000':
                print(f"\nErrore get_symbol_ticker: {response.json()}")
                return None
            else:
                #print("Return data")
                return response.json()['data']
        except requests.Timeout:
            print('allTicker Timeout error')
            return None
        
        except requests.RequestException as e:
            print(f'allTicker error: {e}') 
            return None
  
    def orderMarketSell(self,symbol,quantity):
        orderID = casualOrderID()
        
        url = 'https://api.kucoin.com/api/v1/orders'

        now = int(time.time() * 1000)
        data = {
            "clientOid":orderID,
            "tipe":"market",
            "tradeType": "TRADE",
            "size": quantity,
            "side": "sell",
            "symbol": symbol,
            "type": "market",
            "timeInForce": "GTC"
        }
        data_json = json.dumps(data)
        str_to_sign = str(now) + 'POST' + '/api/v1/orders' + data_json
        signature = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        passphrase = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), self.api_passphrase.encode('utf-8'), hashlib.sha256).digest())
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json" # specifying content type or using json=data in request
        }
        try:
            response = requests.request('post', url, headers=headers, data=data_json,timeout=timeOut)
            if response.json()['code']!='200000':
                print(f"\nError orderMarketSell {symbol} quantita {quantity}: {response.json()}")
                return None
            else:
                #print(f"\nOrdine di vendita {symbol}: {response.json()}")
                self.orderID+=1
                return response.json()['data'] 
        except requests.Timeout:
            print('Timeout error orderMarketSell')
            return None
        
        except requests.RequestException as e:
            print(f'Error orderMarketSell: {e}') 
            return None

    def orderMarketSellLimit(self,symbol,quantity,price):
        orderID = casualOrderID()
        
        url = 'https://api.kucoin.com/api/v1/orders'

        now = int(time.time() * 1000)
        data = {
            "clientOid":orderID,
            "tipe":"market",
            "tradeType": "TRADE",
            "size": quantity,
            "price":price,
            "side": "sell",
            "symbol": symbol,
            "type": "limit",
            "timeInForce": "GTC"
        }
        data_json = json.dumps(data)
        str_to_sign = str(now) + 'POST' + '/api/v1/orders' + data_json
        signature = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        passphrase = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), self.api_passphrase.encode('utf-8'), hashlib.sha256).digest())
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json" # specifying content type or using json=data in request
        }
        try:
            response = requests.request('post', url, headers=headers, data=data_json,timeout=timeOut)
            if response.json()['code']!='200000':
                print(f"\nErrore orderMarketSell {symbol} quantita {quantity}: {response.json()}")
                return None
            else:
                #print(f"\nOrdine di vendita {symbol}: {response.json()}")
                self.orderID+=1
                return response.json()['data']
        except requests.Timeout:
            print('Timeout error orderMarketSellLimit')
            return None
        
        except requests.RequestException as e:
            print(f'Error orderMarketSellLimit: {e}') 
            return None
    
    def orderMarketBuy(self,symbol,quantity):
        orderID = casualOrderID()
        
        url = 'https://api.kucoin.com/api/v1/orders'

        now = int(time.time() * 1000)
        data = {
            "clientOid":orderID,
            "tipe":"market",
            "tradeType": "TRADE",
            "funds": quantity,
            "side": "buy",
            "symbol": symbol,
            "type": "market",
            "timeInForce": "GTC"
        }
        data_json = json.dumps(data)
        str_to_sign = str(now) + 'POST' + '/api/v1/orders' + data_json
        signature = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        passphrase = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), self.api_passphrase.encode('utf-8'), hashlib.sha256).digest())
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json" # specifying content type or using json=data in request
        }
        try:
            response = requests.request('post', url, headers=headers, data=data_json,timeout=timeOut)
        
            if response.json()['code']!='200000':
                print(f"\nErrore orderMarketBuy {symbol} quantita {quantity}: {response.json()}")
                return None
            else:
                self.orderID+=1
                return response.json()['data']  
        except requests.Timeout:
            print('Timeout error orderMarketBuy')
            return None
        
        except requests.RequestException as e:
            print(f'Error orderMarketBuy: {e}') 
            return None
    
    def getOrder(self,orderId,TimeOut):
        url = f"https://api.kucoin.com/api/v1/fills?orderId={orderId}"

        now = int(time.time() * 1000)
        str_to_sign = str(now) + 'GET' + f"/api/v1/fills?orderId={orderId}"
        signature = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        passphrase = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), self.api_passphrase.encode('utf-8'), hashlib.sha256).digest())
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2"
        }
        try:
            response = requests.request('get', url, headers=headers,timeout=TimeOut)
            if response.json()['code']!='200000':
                print(f"\nErrore estrazione dati ordine {orderId}, code: "+response.json()['code'])
                return None
            else:
                #print(f"\nEstrazione dati ordine {orderId}: {response.json()}")
                return response.json()['data']['items']
        except requests.Timeout:
            print('Timeout error getOrder')
            return None
        
        except requests.RequestException as e:
            print(f'Error getOrder: {e}') 
            return None

    def serverTime(self):
        url = f"https://api.kucoin.com/api/v1/timestamp"
        response = requests.request('get', url)
        if response.json()['code']!='200000':
            print(f"\nErrore get_symbol_ticker: {response.json()}")
            return None
        else:
            #print(f"\nget_symbol_ticker {symbol}: {response.json()}")
            return response.json()['data'] 
 
#casual orderID generation
def casualOrderID():
    cifre = string.digits
    lunghezza = 16

    stringa_casuale = ''.join(random.choice(cifre) for _ in range(lunghezza))
    return stringa_casuale

#sound advise
def playSound(step,duration):
    sample_rate = 44100
    bits = 16
    frequency = 3000

    try:
        pygame.mixer.init(frequency = sample_rate, size = -bits, channels = 2)
        n_samples = int(round(duration*sample_rate))
        buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
        max_sample = 2**(bits - 1) - 1
        for s in range(n_samples):
            t = float(s)/sample_rate # time in seconds
            buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency*t)))
        # left
            buf[s][1] = int(round(max_sample*0.5*math.sin(2*math.pi*frequency*t))) # right
        sound = pygame.sndarray.make_sound(buf)
        for a in range(step):
            sound.play()
            pygame.time.wait(int(round(1000*duration)))
            time.sleep(duration)
    finally:
        pygame.mixer.quit()

#send email
personalEmail = ""
googleEmail = ""
googleAppPassword = ""
def send_email(subject, message):

    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["To"] = personalEmail
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
           smtp_server.login(googleEmail, googleAppPassword)
           smtp_server.sendmail(googleEmail, personalEmail, msg.as_string())

    except Exception as e:
            print(f"\ne-mail send error: {str(e)}")
