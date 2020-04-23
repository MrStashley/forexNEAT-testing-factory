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
    	try:
            print("running1")
            print(file.path)
            curFiledata = pickle.load(file.path,"rb")
            print("rinning2")
            config = curFiledata["config"]
            winners = curFiledata["winners"]
            print("running 3")
            for winner in winners:
                print("running4")
                data.append({
                	"id": winner["id"],
                	"genome": winner[genome],
                	"config": config
                })
    	except:
    		print("an error has occured with " + str(file.path))

    	os.remove(file.path)

    print(data)
    pickle.dump(data, open("testingFacilitySnakeData.pkl", "wb"))

def main():
    readtoTestingFacilityTest()


if __name__ == "__main__":
    main()
