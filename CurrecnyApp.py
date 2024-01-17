import tkinter as tk
import ttkbootstrap as tb
from PIL import Image, ImageTk
import requests

ApiKey = "fca_live_q2HVf2DBGVtIwD63RCPsumI5YIKH9sp8lF9EVpzW"

LatestRateApiUrl = "https://api.freecurrencyapi.com/v1/latest"

def AllCurrencies():
    try:
        response = requests.get(f"https://api.freecurrencyapi.com/v1/currencies?apikey={ApiKey}")
        response.raise_for_status()  
        data = response.json()
        return list(data.get("data", {}).keys())
    
    except requests.exceptions.RequestException as e:
        print(f"Error getting currencies: {e}")
        return []

def ConvertCurrency():
    amount = float(AmountSpinbox.get())
    CurrencyFrom = CurrencyComboboxOne.get()
    CurrencyTo = CurrencyComboboxTwo.get()

    try:
        response = requests.get(f"{LatestRateApiUrl}?apikey={ApiKey}&base_currency={CurrencyFrom}&currencies={CurrencyTo}")
        response.raise_for_status()

        data = response.json()
        ExchangeRate = data.get("data", {}).get(CurrencyTo)

        if ExchangeRate is not None:
            ConvertedAmount = amount * ExchangeRate
            ResultLabel.config(text=f"{amount} {CurrencyFrom} = {ConvertedAmount:.2f} {CurrencyTo}")
        else:
            ResultLabel.config(text="Error: Exchange rate not found.")
    except requests.exceptions.RequestException as e:
        ResultLabel.config(text=f"Error converting currency: {e}")

CurrencyGui = tk.Tk()
CurrencyGui.title("Currency Converter")
CurrencyGui.geometry('300x380')
CurrencyGui.config(bg="#FFFFFF")

AppLabel = tk.Label(CurrencyGui, text="Currency Converter" , font=('Courier New', 16, 'bold'), background="#FFFFFF")
AppLabel.place(x=35, y=145)

ImagePath = "currency.jpg" 
OriginalImage = Image.open(ImagePath)
ResizedImage = OriginalImage.resize((100, 100)) 
Image = ImageTk.PhotoImage(ResizedImage)

ImageLabel = tk.Label(CurrencyGui, image=Image)
ImageLabel.place(x=100 , y= 30)

AmountLabel = tk.Label(CurrencyGui, text="Amount:" , font=('Bahnschrift', 12), background="#FFFFFF")
AmountLabel.place(x=10, y=190)

AmountSpinbox = tb.Spinbox(CurrencyGui, from_=0, to=float('inf'), increment=1, width=41)
AmountSpinbox.insert(tk.END, "10")
AmountSpinbox.place(x=10, y=220)

currencies = AllCurrencies()

CurrencyComboboxOne = tb.Combobox(CurrencyGui, values=currencies , width=18)
CurrencyComboboxOne.set("USD")
CurrencyComboboxOne.place(x=10, y=260)

CurrencyComboboxTwo = tb.Combobox(CurrencyGui, values=currencies, width=18)
CurrencyComboboxTwo.set("EUR")
CurrencyComboboxTwo.place(x=157, y=260)

ConvertButton = tb.Button(CurrencyGui, text="Convert", command=ConvertCurrency, width=43)
ConvertButton.place(x=10, y=300)

ResultFrame = tk.Frame(CurrencyGui, background='lightgrey')
ResultFrame.place(x=11, y=340)

ResultLabel = tb.Label(ResultFrame, text="", width=46, background='lightgrey' , anchor='center')
ResultLabel.pack(ipady=3.5)
CurrencyGui.mainloop()  