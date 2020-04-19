import pickle


def readtoTestingFacilityTest():
    filename = "~/toTestingFacility.pkl"
    data = pickle.load(open(filename,"rb"))
    print(data)

def main():
    readtoTestingFacilityTest()


if __name__ == "__main__":
	main()
