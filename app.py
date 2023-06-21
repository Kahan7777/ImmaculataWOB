from flask import Flask, redirect,url_for,render_template,request
import pyrebase
import random
import traceback

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
    costOfStock = int(db.child("Stocks").child(stock).child("CurrentPrice").get().val())
    moneyInStock = int(db.child("Schools").child(school).child("Stocks").child(stock).get().val())
    moneyInStockActual = int(db.child("Schools").child(school).child("StocksActual").child(stock).get().val())
    moneyInReserve = int(db.child("Schools").child(school).child('Money').get().val())
    currentStockPrice = int(db.child("Stocks").child(stock).child("CurrentPrice").get().val())
    stockVolatility = float(db.child("Stocks").child(stock).child("Volatility").get().val())
    history = db.child("Stocks").child(stock).child("History").get().val()
    history.append(currentStockPrice)

    costOfPurchase = 0
    costOfStockUpdated = costOfStock
    for i in range(amt):
        costOfStockUpdated+=stockVolatility
        costOfPurchase+=costOfStockUpdated
    averageCost = round(costOfPurchase/amt)
    if averageCost<5:
        db.child("Stocks").child(stock).update({"CurrentPrice":0})
        db.child("Stocks").child(stock).update({"History":history})
        db.child("Stocks").child(stock).update({"Volatility":0})
        performed=False
    else:
        if moneyInReserve-costOfPurchase>=0:
            db.child("Schools").child(school).child("Stocks").update({stock:moneyInStock+costOfPurchase})
            db.child("Schools").child(school).child("StocksActual").update({stock:moneyInStockActual+amt})
            db.child("Schools").child(school).update({"Money":moneyInReserve-costOfPurchase})
            db.child("Stocks").child(stock).update({"CurrentPrice":averageCost})
            db.child("Stocks").child(stock).update({"History":history})
            performed=True
        else:
            performed=False
    return performed
def schSellStock(school,stock,amt):
    print("sell")
    costOfStock = int(db.child("Stocks").child(stock).child("CurrentPrice").get().val())
    moneyInStock = int(db.child("Schools").child(school).child("Stocks").child(stock).get().val())
    moneyInStockActual = int(db.child("Schools").child(school).child("StocksActual").child(stock).get().val())
    moneyInReserve = int(db.child("Schools").child(school).child('Money').get().val())
    currentStockPrice = int(db.child("Stocks").child(stock).child("CurrentPrice").get().val())
    stockVolatility = float(db.child("Stocks").child(stock).child("Volatility").get().val())
    history = db.child("Stocks").child(stock).child("History").get().val()
    returnOnSale = 0
    costOfStockUpdated = costOfStock
    for i in range(amt):
        costOfStockUpdated-=stockVolatility
        returnOnSale=returnOnSale + costOfStockUpdated
    averageCost = round(returnOnSale/amt)
    if averageCost<5:
        db.child("Stocks").child(stock).update({"CurrentPrice":0})
        db.child("Stocks").child(stock).update({"History":history})
        db.child("Stocks").child(stock).update({"Volatility":0})
        performed=False
    else:
        if moneyInStockActual-amt>=0:
            db.child("Schools").child(school).child("Stocks").update({stock:moneyInStock-returnOnSale})
            db.child("Schools").child(school).child("StocksActual").update({stock:moneyInStockActual-amt})
            db.child("Schools").child(school).update({"Money":moneyInReserve+returnOnSale})
            db.child("Stocks").child(stock).update({"CurrentPrice":averageCost})
            db.child("Stocks").child(stock).update({"History":history})
            performed=True
        else:
            performed=False
            print("Action cannot be performed")
    return performed
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
        try:
            print("Yeee")
            print(schoolName)
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
        except Exception:
            traceback.print_exc()
            return redirect(url_for("error", eMess1="404 Error!", eMess2="This aint an actual webpage! Why you trying to do this?"))
    elif request.method=="POST":
        return redirect(url_for("home"))
@app.route("/", methods=["POST","GET"])
def mainrun():
    return redirect(url_for("home"))

@app.errorhandler(404)
def pageNotFound(error):
    return redirect(url_for("home"))

@app.route("/stock/<name>", methods=["POST", "GET"])
def stock(name):
    print(name)
    try:
        allStockNames = [
            name
        ]
        stockList = []
        currentHighest = 0
        for i in allStockNames:
            stockInfo = db.child("Stocks").child(i).get().val()
            history=stockInfo["History"]
            history = [int(i) for i in history]
            c1 = random.randrange(0,255)
            c2 = random.randrange(0,255)
            c3 = random.randrange(0,255)
            if len(history)>currentHighest:
                currentHighest=len(history)
            stockList.append({
                "History":history,
                "CurrentPrice": stockInfo["CurrentPrice"],
                "Volatility": stockInfo["Volatility"],
                "Name":i,
                "borderColor": f"rgb(250,114,104)"
            })
        print(stockList)
        xAxis = []
        for j in range(currentHighest):
            xAxis.append(j)
        return render_template("stkDisplay2.html",stockList=stockList, xAxis=xAxis)
    except:
        return redirect(url_for("error", eMess1="Issue with sourcing information!", eMess2="Contact a volunteer if these messages are repeated."))

@app.route("/stocks")
def stocks():
    return render_template("stocks.html")

@app.route("/home", methods=["POST","GET"])
def home():
    success= {}
    success["error"]=False
    if request.method == "GET":
        return render_template("newMain.html")
    elif request.method == "POST":
        schoolName = request.form["schoolNameDropdown"]
        schoolPassword = request.form["schoolPassword"]
        buyOrSell = request.form["typeOfOrder"]
        stockName = request.form["stock"]
        noOfStocks = request.form["noOfStocks"]
        """success = manageStocks(schoolName,schoolPassword,buyOrSell,stockName,noOfStocks)
        if success is None:
            success= {}
            success["error"]=False
        if success["error"]==True:
            return redirect(url_for("error",eMess1=success["eMess1"],eMess2=success["eMess2"]))
        else:
            return render_template("main.html")"""


        isAuth = False
        school = db.child("Schools").child(schoolName).get().val()
        truePass = school["Password"]
        isAuth2=True
        errorMessage = {"error":False}
        try:
            if int(schoolPassword)==int(truePass):
                isAuth=True
        except ValueError:
            errorMessage["error"] = True
            errorMessage["eMess1"]="Password not entered!"
            errorMessage["eMess2"]="Enter the correct password to be able to sell and buy stocks."
        try:
            if int(noOfStocks)<0:
                isAuth2=False
        except ValueError:
            isAuth2=False
            errorMessage["error"] = True
            errorMessage["eMess1"]="Number. of Stocks is not true"
            errorMessage["eMess2"]="Enter a valid number of stocks to be able to sell and buy stocks."
        if isAuth2==False:
            errorMessage["error"] = True
            errorMessage["eMess1"]="Value must be above 0"
            errorMessage["eMess2"]="Enter a valid number of stocks to be able to sell and buy stocks."
        if isAuth:
            if isAuth2:
                if int(buyOrSell) == 1:   
                    perf = schBuyStock(schoolName,stockName,int(noOfStocks))
                    if perf==False:
                        errorMessage["error"] = True
                        errorMessage["eMess1"]="Cannot buy no. of stocks inputed!"
                        errorMessage["eMess2"]="Enter a valid no. of stocks to be able to buy stocks."
                        return redirect(url_for("error",eMess1=errorMessage["eMess1"],eMess2=errorMessage["eMess2"]))
                elif int(buyOrSell) == 2:
                    perf = schSellStock(schoolName,stockName,int(noOfStocks))
                    if perf==False:
                        errorMessage["error"] = True
                        errorMessage["eMess1"]="Cannot sell more stocks than owned!"
                        errorMessage["eMess2"]="Enter a valid no. of stocks to be able to sell stocks."
                        return redirect(url_for("error",eMess1=errorMessage["eMess1"],eMess2=errorMessage["eMess2"]))
                return redirect(url_for("portfolio",schoolName=schoolName))
            else:
                print("notAuth")
                errorMessage["error"] = True
                errorMessage["eMess1"]="No. of Stocks Not Provided!"
                errorMessage["eMess2"]="Enter a valid no. of stocks to be able to sell and buy stocks."
                return redirect(url_for("error",eMess1=errorMessage["eMess1"],eMess2=errorMessage["eMess2"]))
        else:
            print("notAuth")
            errorMessage["error"] = True
            errorMessage["eMess1"]="Correct Password not entered!"
            errorMessage["eMess2"]="Enter the correct password to be able to sell and buy stocks."
            return redirect(url_for("error",eMess1=errorMessage["eMess1"],eMess2=errorMessage["eMess2"]))
if __name__=="__main__":
    app.run(debug=True)