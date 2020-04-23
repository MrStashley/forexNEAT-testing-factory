import pickle
import neat
import os


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
