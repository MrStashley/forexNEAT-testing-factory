import pickle
import neat
import os
from snake_test import sendUpdateToServer

def sendUpdateToServerTest():
    sendUpdateToServer({
        "id": 10578,
        "top_money_made": 10000.4,
        "bottom_money_made": 8764.3,
        "average_money_made": 9462.8,
        "positive_money_made_decimal": 1,
        "positive_money_made_count": 250,
        "failed_count": 0,
        "average_total_loss": 30,
        "average_total_profit": 9980.5,
        "average_profitability_ratio": 8,
        "top_total_loss": 70,
        "top_total_profit": 10064,
        "top_profitability_ratio": 20,
        "bottom_total_loss": 15,
        "bottom_total_profit": 6675.4,
        "bottom_profitability_ratio": 4,
        "average_max_drawdown": 5,
        "top_max_drawdown": 10,
        "bottom_max_drawdown": 1,
        "average_balance_equity_disparity": 40,
        "total": 250
    })


def readtoTestingFacilityTest():
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

    print(data)
    pickle.dump(data, open("testingFacilitySnakeData.pkl", "wb"))

def main():
    readtoTestingFacilityTest()


if __name__ == "__main__":
    main()
