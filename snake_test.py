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
        curFiledata = pickle.load(open(file.path,"rb"))
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
            test_snake(data.pop())

def test_snake(snake):
    tester = snakeTester(snake);
    tester.run(True)
    results = tester.getResults()

    positive_fitness_count = 0
    failed_count = 0
    top_fitness = 0
    bottom_fitness = 3000
    fitness_total = 0
    for result, genomes in results:
        fitness = result["fitness"];
        balance = result["balance"];
        equity = result["equity"];
        failed = result["failed"];
        id = result["id"];

        fitness_total += fitness

        if fitness > 0:
            positive_fitness_count+=1
        if failed:
            failed_count+=1
        if fitness > top_fitness:
            top_fitness = fitness
        if fitness < bottom_fitness:
            bottom_fitness = fitness

    average_fitness = fitness_total / len(results)
    positive_fitness_decimal = positive_fitness_count/len(results)

    sendUpdateToServer({
        "top_fitness": top_fitness,
        "bottom_fitness": bottom_fitness,
        "average_fitness": average_fitness,
        "positive_fitness_decimal": positive_fitness_decimal,
        "positive_fitness_count": positive_fitness_count,
        "failed_count": failed_count
    })

if __name__ == "__main__":
    testing_driver()
