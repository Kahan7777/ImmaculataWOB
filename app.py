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
    costOfStock = db.child("Stocks").child(stock).child("CurrentPrice").get().val()
    moneyInStock = db.child("Schools").child(school).child("Stocks").child(stock).get().val()
    moneyInStockActual = db.child("Schools").child(school).child("StocksActual").child(stock).get().val()
    moneyInReserve = db.child("Schools").child(school).child('Money').get().val()
    currentStockPrice = db.child("Stocks").child(stock).child("CurrentPrice").get().val()
    stockVolatility = db.child("Stocks").child(stock).child("Volatility").get().val()
    history = db.child("Stocks").child(stock).child("History").get().val()
    history.append(currentStockPrice)

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
    return redirect(url_for("portfolio",schoolName=school))
def schSellStock(school,stock,amt):
    print("sell")
    costOfStock = db.child("Stocks").child(stock).child("CurrentPrice").get().val()
    moneyInStock = db.child("Schools").child(school).child("Stocks").child(stock).get().val()
    moneyInStockActual = db.child("Schools").child(school).child("StocksActual").child(stock).get().val()
    moneyInReserve = db.child("Schools").child(school).child('Money').get().val()
    currentStockPrice = db.child("Stocks").child(stock).child("CurrentPrice").get().val()
    stockVolatility = db.child("Stocks").child(stock).child("Volatility").get().val()
    history = db.child("Stocks").child(stock).child("History").get().val()
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
    isAuth2=True
    try:
        if int(password)==int(truePass):
            isAuth=True
    except ValueError:
        return {"error":True,
                "eMess1":"Password not entered!",
                "eMess2":"Enter the correct password to be able to sell and buy stocks."}
    try:
        if int(no)<0:
            isAuth2=False
    except ValueError:
        return {"error":True,
                "eMess1":"Number. of Stocks is not true",
                "eMess2":"Enter a valid number of stocks to be able to sell and buy stocks."}
    if isAuth2==False:
        return {"error":True,
                "eMess1":"Value must be above 0",
                "eMess2":"Enter a valid number of stocks to be able to sell and buy stocks."}
    if isAuth:
        if int(option) == 1:   
            schBuyStock(name,stock,int(no))
        elif int(option) == 2:
            schSellStock(name,stock,int(no))
    else:
        print("notAuth")
        return {"error":True,
                "eMess1":"Correct password not entered!",
                "eMess2":"Enter the correct password to be able to sell and buy stocks."}
app = Flask(__name__)

@app.route("/error/<eMess1>/<eMess2>", methods=["POST","GET"])
def error(eMess1,eMess2):
    if request.method=="GET":
        print("Nas")
        return render_template("error.html",eMess1=eMess1,eMess2=eMess2)
    elif request.method=="POST":
        print("Wee")
        return redirect(url_for("home"))
    
@app.route("/portfolio/<schoolName>",methods=["POST","GET"])
def portfolio(schoolName):
    if request.method=="GET":
        print("Yeee")
        schoolMoney = db.child("Schools").child(schoolName).child("Money").get().val()
        schoolStocks = db.child("Schools").child(schoolName).child("StocksActual").get()
        allStockNames = [
            "Burrmanfabrics",
            "GENOFoods",
            "GoliathBanks",
            "NPCTech",
            "NatFuels",
            "WrightAirlines",
            "aquaFortis",
            "buildScape",
            "healthQuest",
            "ignitedMinds",
            "prasiddhiAutos"
        ]
        i=0
        allStocks = {}
        for stock in schoolStocks.each():
            allStocks[allStockNames[i]]=stock.val()
            i=i+1
        print(allStocks)
        return render_template("portfolio.html",values=allStocks,money=schoolMoney)
    elif request.method=="POST":
        return redirect(url_for("home"))
@app.route("/", methods=["POST","GET"])
def mainrun():
    return redirect(url_for("home"))


@app.errorhandler(404)
def pageNotFound(error):
    return redirect(url_for("home"))
@app.route("/home", methods=["POST","GET"])
def home():
    success= {}
    success["error"]=False
    if request.method == "GET":
        return render_template("main.html")
    elif request.method == "POST":
        schoolName = request.form["schoolNameDropdown"]
        schoolPassword = request.form["schoolPassword"]
        buyOrSell = request.form["typeOfOrder"]
        stockName = request.form["stock"]
        noOfStocks = request.form["noOfStocks"]
        success = manageStocks(schoolName,schoolPassword,buyOrSell,stockName,noOfStocks)
        if success is None:
            success= {}
            success["error"]=False
        if success["error"]==True:
            return redirect(url_for("error",eMess1=success["eMess1"],eMess2=success["eMess2"]))
        else:
            return render_template("main.html")

if __name__=="__main__":
    app.run(debug=True)