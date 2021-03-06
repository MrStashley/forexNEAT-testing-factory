import neat
import time
import numpy as np
from multiprocessing import Process, Pool
from marketAPI import trainingMarketAPI, initMarketData

class snakeNN(object):

    def __init__(self,genome, config, id):
        self.genome = genome
        self.neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
        self.id = id
        self.results = None;
        self.lastAction = 2

    def runNN(self,input):
        output = self.neural_network.activate(input)
        output = [ (1/(1 + np.exp(-i))) for i in output ]
        return output.index(max(output));

    def test(self, genData):
        #runs the NN in a test environment for the purpose of evaluating
        #fitness for training
        marketAPI = trainingMarketAPI(genData);
        marketAPI.start()

        startTime = time.time()
        while marketAPI.end() == False:
            input = marketAPI.getInputData();
            output = self.runNN(input);

            if output == 0:
                if self.lastAction != 0:
                    self.lastAction = 0;
                    marketAPI.openPosition()
            elif output == 1:
                if self.lastAction != 1:
                    self.lastAction = 1;
                    marketAPI.closePosition();
            elif output == 2:
                self.lastAction = 2


        self.results = marketAPI.getResults();
        self.results["id"] = self.id;
        return self.results;

class snakeTester(object):
    def __init__(self, snake):
        print(snake)
        config = snake["config"]
        self.config = config
        genome = snake["genome"]
        id = snake["id"]
        self.snake = snakeNN(genome,config,id)
        self.threads = []
        self.results = []
        self.numTests = 250


    def run(self,save):
        pool = Pool(processes = self.numTests);
        snake = self.snake
        for i in range(self.numTests):
            self.threads.append(pool.apply_async(snake.test,(initMarketData(),)))
        pool.close();
        pool.join();
        for index, thread in enumerate(self.threads):
            self.results.append((self.threads[index].get(),snake.genome, self.config));

    def getResults(self):
        return self.results
