import requests
import datetime
import json
import hashlib
import flask
import random

class Blockchain:
    difficulty = "0000"

    def __init__(self, difficulty="0000"):
        self.chain = []
        self.createBlock(previousHash = 0)          #genesis block
        self.difficulty = difficulty

    def getDifficulty(self):
        return self.difficulty

    def createBlock(self, previousHash):
        block = {
            'index' : len(self.chain)+1,
            'timestamp' : str(datetime.datetime.now()),
            'previousHash' : previousHash,
        }
        block['proofOfWork'] = self.getProofOfWork(block)
        self.chain.append({
            'block' : block,
            'hash' : self.getHash(block),
        })
        return block
    
    def getProofOfWork(self, block):
        proof = 1                                   #Nothin but brute force
        proofFound = False
        while not proofFound:
            block['proofOfWork'] = proof
            currentHash = self.getHash(block)
            if currentHash[:4] == self.getDifficulty():
                proofFound = True
            else:
                proof += 1
        return proof

    def getHash(self, block):
        encodedBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()

    def getLastBlock(self):
        return self.chain[-1]

    def isChainValid(self):
        previousBlockIndex = 0
        currentBlockIndex = 1
        isValid = True
        while currentBlockIndex < len(self.chain):
            previousBlock = self.chain[previousBlockIndex]
            prevHash = previousBlock['hash']
            if self.chain[currentBlockIndex]['block']['previousHash'] != prevHash:
                return False
            # if self.chain[currentBlockIndex]['hash'][:4] != self.difficulty:
            #     return False
            else:
                previousBlockIndex = currentBlockIndex
                currentBlockIndex += 1
        return isValid

    def hackBlock(self, blockIndex, changes):
        for property, newValue in changes:
                self.chain[blockIndex][property] = newValue
    
    def setDifficulty(self, difficulty):
        self.difficulty = difficulty



#Creating Flask environment
app = flask.Flask(__name__)

#Creating Blockchain object
blockchain = Blockchain()
chainLength = 1

#Mining a block
@app.route('/mineBlock', methods=['GET'])
def mineBlock():
    lastBlockHash = blockchain.getLastBlock()['hash']
    newBlock = blockchain.createBlock(lastBlockHash)
    response = {
        'index' : newBlock['index'],
        'timestamp' : newBlock['timestamp'],
        'proofOfWork' : newBlock['proofOfWork'],                #Nonce basically
        'previousHash' : newBlock['previousHash']
    }
    global chainLength
    chainLength += 1
    return flask.jsonify(response)

#Fetching the chain
@app.route('/fetchChain', methods = ['GET'])
def fetchChain():
    chain = {
        'Blockchain' : blockchain.chain,
        'length' : chainLength,
    }
    return flask.jsonify(chain)

#Checking if blockchain is valid
@app.route('/isValid', methods = ['GET'])
def isValid():
    isValid = blockchain.isChainValid()
    if isValid:
        return flask.jsonify({
            'Alert' : 'Valid'
        })
    else:
        return flask.jsonify({
            'Alert' : "It's broken man, sorry"
        })

#Under construction 
# @app.route('/setDifficulty')
# def setDiff():
#     diff = "000000"
#     blockchain.setDifficulty(diff)

# @app.route('/tamper')
# def tamper():
#     randomIndex = random.randint(0, chainLength)
#     changes = {
#         'hash' : "randomHash"
#     }
#     blockchain.hackBlock(randomIndex, changes)
#     isValid()

app.run(host = '0.0.0.0', port = 5000) #runs on 127.0.0.1:5000/functionPathName