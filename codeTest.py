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
    		curFiledata = pickle.load(file.path,"rb")
    		config = curFiledata["config"]
    		winners = curFiledata["winners"]
    		for winner in winners:
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
