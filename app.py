from flask import Flask, redirect,url_for,render_template,request
import pyrebase

config = {
    "apiKey": "AIzaSyBz0ZmNlIwmZXNr0H-frf4ivbSIyIycnOg",
    "authDomain": "immacootb.firebaseapp.com",
    "databaseURL": "https://immacootb-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "immacootb",
    "storageBucket": "immacootb.appspot.com",
    "messagingSenderId": "413658342655",
    "appId": "1:413658342655:web:814eef54c95805ec8b58ca",
    "measurementId": "G-66701556S4"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def schBuyStock(school,stock,amt):
    print("buy")
    #currentStockBalance = db.child("Schools").child(school).child(stock).get().val()
    #currentStockBalance = db.child("Schools").child(school).child(stock+"").get().val()
    costOfStock = db.child("Stocks").child(stock).child("CurrentPrice").get().val()
    moneyInStock = db.child("Schools").child(school).child("Stocks").child(stock).get().val()
    moneyInStockActual = db.child("Schools").child(school).child("StocksActual").child(stock).get().val()
    moneyInReserve = db.child("Schools").child(school).child('Money').get().val()
    currentStockPrice = db.child("Stocks").child(stock).child("CurrentPrice").get().val()
    stockVolatility = db.child("Stocks").child(stock).child("Volatility").get().val()
    history = db.child("Stocks").child(stock).child("History").get().val()
    history.append(currentStockPrice)
    """volatilityInc = 0
    for i in range(amt+1):
        volatilityInc += i
    print(volatilityInc)
    volatilityInc = volatilityInc*stockVolatility
    print(volatilityInc)
    print(moneyInReserve-costOfStock*amt-volatilityInc)
    if costOfStock<5:
        db.child("Stocks").child(stock).update({"CurrentPrice":0})
        db.child("Stocks").child(stock).update({"History":history})
        db.child("Stocks").child(stock).update({"Volatility":0})
    else:
        if moneyInReserve-costOfStock*amt-volatilityInc>0:
            db.child("Schools").child(school).child("Stocks").update({stock:moneyInStock+costOfStock*amt+volatilityInc})
            db.child("Schools").child(school).child("StocksActual").update({stock:moneyInStockActual+amt})
            db.child("Schools").child(school).update({"Money":moneyInReserve-costOfStock*amt-volatilityInc})
            print(moneyInReserve-costOfStock*amt-volatilityInc)
            db.child("Stocks").child(stock).update({"CurrentPrice":currentStockPrice+volatilityInc})
            db.child("Stocks").child(stock).update({"History":history})
        else:
            print("Action cannot be performed")"""
    costOfPurchase = 0
    costOfStockUpdated = costOfStock
    for i in range(amt):
        costOfStockUpdated+=stockVolatility
        costOfPurchase+=costOfStockUpdated
    averageCost = round(costOfPurchase/amt)
    if costOfStock<5:
        db.child("Stocks").child(stock).update({"CurrentPrice":0})
        db.child("Stocks").child(stock).update({"History":history})
        db.child("Stocks").child(stock).update({"Volatility":0})
    else:
        if moneyInReserve-costOfPurchase>=0:
            db.child("Schools").child(school).child("Stocks").update({stock:moneyInStock+costOfPurchase})
            db.child("Schools").child(school).child("StocksActual").update({stock:moneyInStockActual+amt})
            db.child("Schools").child(school).update({"Money":moneyInReserve-costOfPurchase})
            db.child("Stocks").child(stock).update({"CurrentPrice":averageCost})
            db.child("Stocks").child(stock).update({"History":history})
        else:
            print("Action cannot be performed")
def schSellStock(school,stock,amt):
    print("sell")
    #currentStockBalance = db.child("Schools").child(school).child(stock).get().val()
    #currentStockBalance = db.child("Schools").child(school).child(stock+"").get().val()
    costOfStock = db.child("Stocks").child(stock).child("CurrentPrice").get().val()
    moneyInStock = db.child("Schools").child(school).child("Stocks").child(stock).get().val()
    moneyInStockActual = db.child("Schools").child(school).child("StocksActual").child(stock).get().val()
    moneyInReserve = db.child("Schools").child(school).child('Money').get().val()
    currentStockPrice = db.child("Stocks").child(stock).child("CurrentPrice").get().val()
    stockVolatility = db.child("Stocks").child(stock).child("Volatility").get().val()
    history = db.child("Stocks").child(stock).child("History").get().val()
    """flatStop=costOfStock*amt/3
    history.append(currentStockPrice)
    volatilityInc = 0
    for i in range(amt+1):
        volatilityInc += i
    print(volatilityInc)
    volatilityInc = volatilityInc*stockVolatility
    print(volatilityInc)
    if costOfStock<5:
        db.child("Stocks").child(stock).update({"CurrentPrice":0})
        db.child("Stocks").child(stock).update({"History":history})
        db.child("Stocks").child(stock).update({"Volatility":0})
    else:
        if moneyInStockActual-amt>=0:
            db.child("Schools").child(school).child("Stocks").update({stock:moneyInStock-costOfStock*amt+volatilityInc})
            db.child("Schools").child(school).child("StocksActual").update({stock:moneyInStockActual-amt})
            db.child("Schools").child(school).update({"Money":moneyInReserve+costOfStock*amt-volatilityInc-int(flatStop)})
            db.child("Stocks").child(stock).update({"CurrentPrice":currentStockPrice-volatilityInc})
            db.child("Stocks").child(stock).update({"History":history})
        else:
            print("Action cannot be performed")"""
    returnOnSale = 0
    costOfStockUpdated = costOfStock
    for i in range(amt):
        costOfStockUpdated-=stockVolatility
        returnOnSale=returnOnSale + costOfStockUpdated
    averageCost = round(returnOnSale/amt)
    if costOfStock<5:
        db.child("Stocks").child(stock).update({"CurrentPrice":0})
        db.child("Stocks").child(stock).update({"History":history})
        db.child("Stocks").child(stock).update({"Volatility":0})
    else:
        if moneyInStockActual-amt>=0:
            db.child("Schools").child(school).child("Stocks").update({stock:moneyInStock-returnOnSale})
            db.child("Schools").child(school).child("StocksActual").update({stock:moneyInStockActual-amt})
            db.child("Schools").child(school).update({"Money":moneyInReserve+returnOnSale})
            db.child("Stocks").child(stock).update({"CurrentPrice":averageCost})
            db.child("Stocks").child(stock).update({"History":history})
        else:
            print("Action cannot be performed")
def manageStocks(name,password,option,stock,no):
    isAuth = False
    school = db.child("Schools").child(name).get().val()
    truePass = school["Password"]
    if int(password)==int(truePass):
        isAuth=True
    if int(no)<0:
        isAuth=False
    if isAuth:
        if int(option) == 1:   
            schBuyStock(name,stock,int(no))
        elif int(option) == 2:
            schSellStock(name,stock,int(no))
app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def home():
    if request.method == "GET":
        return render_template("main.html")
    elif request.method == "POST":
        schoolName = request.form["schoolNameDropdown"]
        schoolPassword = request.form["schoolPassword"]
        buyOrSell = request.form["typeOfOrder"]
        stockName = request.form["stock"]
        noOfStocks = request.form["noOfStocks"]
        manageStocks(schoolName,schoolPassword,buyOrSell,stockName,noOfStocks)
        print("Ok")
        return render_template("main.html") 
if __name__=="__main__":
    app.run()