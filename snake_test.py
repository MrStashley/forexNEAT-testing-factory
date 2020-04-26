import requests
import json
import pickle
import os
import neat
from snakeTester import snakeTester, snakeNN

def sendUpdateToServer(info):
    dataString = json.dumps(info)
    updateURL = "https://forexnntracker.herokuapp.com/testingfactoryupdate"
    data = {"info": dataString}
    r = requests.post(updateURL, data = data)

def checkIncoming():
    filename = "testingFacilitySnakeData.pkl"
    data = []
    files = os.scandir("/home/ec2-user/forexNEAT-testing-factory/toTestingFactory")

    for file in files:
        if file.is_file() == False:
            continue
        try:
            curFiledata = pickle.load(open(file.path,"rb"))
        except:
            pass
        config = curFiledata["config"]
        winners = curFiledata["winners"]
        for winner in winners:
            data.append({
                "id": winner["id"],
                "genome": winner["genome"],
                "config": config
            })

        os.remove(file.path)

    try:
        curData = pickle.load(open("testingFacilitySnakeData.pkl", "rb"))
    except:
        curData = []
    curData.extend(data)
    pickle.dump(curData, open("testingFacilitySnakeData.pkl", "wb"))
    return data

def testing_driver():
    run = True
    try:
        data = pickle.load(open("testingFacilitySnakeData.pkl", "rb"))
    except:
        data = []

    while (run):
        newData = checkIncoming()
        data.extend(newData)
        if len(data) > 0:
            run = True
            while run:
                try:
                    test_snake(data.pop())
                    run = False
                except Exception as e:
                    print(e)

def test_snake(snake):
    tester = snakeTester(snake);
    tester.run(True)
    results = tester.getResults()

    positive_fitness_count = 0
    failed_count = 0
    top_fitness = 0
    bottom_fitness = 3000
    fitness_total = 0
    totalLoss_total = 0
    totalProfit_total = 0
    profitability_ratio_total = 0
    top_totalProfit = 0
    bottom_totalProfit = 500000
    top_totalLoss = 0
    bottom_totalLoss = 3000
    top_profitability_ratio = 0
    bottom_profitability_ratio = 3000
    total_max_drawdown = 0
    top_max_drawdown = 0
    bottom_max_drawdown = 3000
    balance_equity_disparity_total = 0
    for result, genome, config in results:
        fitness = result["fitness"];
        balance = result["balance"];
        equity = result["equity"];
        failed = result["failed"];
        id = result["id"];
        totalLoss = result["totalLoss"]
        totalProfit = result["totalProfit"]
        max_drawdown = result["max_drawdown"]

        balance_equity_disparity = equity-balance
        balance_equity_disparity_total += balance_equity_disparity

        total_max_drawdown += max_drawdown

        if max_drawdown > top_max_drawdown:
            top_max_drawdown = max_drawdown
        if max_drawdown < bottom_max_drawdown:
            bottom_max_drawdown = max_drawdown

        if totalLoss == 0:
            profitability_ratio = totalProfit
        else:
            profitability_ratio = (totalProfit / totalLoss)

        totalProfit_total += totalProfit
        totalLoss_total += totalLoss
        profitability_ratio_total += profitability_ratio

        if totalLoss > top_totalLoss:
            top_totalLoss = totalLoss
        if totalLoss < bottom_totalLoss:
            bottom_totalLoss = totalLoss
        if totalProfit > top_totalProfit:
            top_totalProfit = totalProfit
        if totalProfit < bottom_totalProfit:
            bottom_totalProfit = totalProfit
        if profitability_ratio > top_profitability_ratio:
            top_profitability_ratio = profitability_ratio
        if profitability_ratio < bottom_profitability_ratio:
            bottom_profitability_ratio = profitability_ratio

        fitness_total += fitness

        if fitness > 0:
            positive_fitness_count+=1
        if failed:
            failed_count+=1
        if fitness > top_fitness:
            top_fitness = fitness
        if fitness < bottom_fitness:
            bottom_fitness = fitness

    total = len(results)

    average_fitness = fitness_total / total
    positive_fitness_decimal = positive_fitness_count / total

    average_total_loss = totalLoss_total / total
    average_total_profit = totalProfit_total / total
    average_profitability_ratio = profitability_ratio_total / total

    average_max_drawdown = total_max_drawdown / total

    average_balance_equity_disparity = balance_equity_disparity_total / total

    snakeData = (id,genome,config)
    try:
        testedSnakes = pickle.load(open("testedSnakeData.pkl", "rb"))
    except:
        testedSnakes = []
    testedSnakes.append(snakeData)
    pickle.dump(testedSnakes, open("testedSnakeData.pkl","wb"))

    sendUpdateToServer({
        "id": id,
        "top_money_made": top_fitness,
        "bottom_money_made": bottom_fitness,
        "average_money_made": average_fitness,
        "positive_money_made_decimal": positive_fitness_decimal,
        "positive_money_made_count": positive_fitness_count,
        "failed_count": failed_count,
        "average_total_loss": average_total_loss,
        "average_total_profit": average_total_profit,
        "average_profitability_ratio": average_profitability_ratio,
        "top_total_loss": top_totalLoss,
        "top_total_profit": top_totalProfit,
        "top_profitability_ratio": top_profitability_ratio,
        "bottom_total_loss": bottom_totalLoss,
        "bottom_total_profit": bottom_totalProfit,
        "bottom_profitability_ratio": bottom_profitability_ratio,
        "average_max_drawdown": average_max_drawdown,
        "top_max_drawdown": top_max_drawdown,
        "bottom_max_drawdown": bottom_max_drawdown,
        "average_balance_equity_disparity": average_balance_equity_disparity,
        "total": total
    })

if __name__ == "__main__":
    testing_driver()
