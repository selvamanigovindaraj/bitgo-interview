import requests

def getTxnsForHash(hash):
    idx =0
    responseList =[]
    payload={}
    headers = {}
    while True:
        try:
            url = F"https://blockstream.info/api/block/{hash}/txs/{idx*25}"
            idx+=1
            response = requests.request("GET", url, headers=headers, data=payload)
            for  txn in response.json():
                responseList.append(txn)
        except:
            break
    return responseList

def getBlockTransactionHash(block):
    url = F"https://blockstream.info/api/block-height/{str(block)}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text

def setCurrentBlockTxns(transactionList , transactionMap):
    for idx in range(1, len(transactionList)):
        transactionMap[transactionList[idx]['txid']] = True


def getCountParenttransactions(transactionList , transtionInBlock,parents,parentTransactionCountMap):
    for idx in range (1, len(transactionList)):
        currentTxn = transactionList[idx]['txid']
        parentTxns= transactionList[idx]['vin']
        for i in range(len(parentTxns)):
            if transtionInBlock.get(parentTxns[i]['txid'], False):
                parentTransactionCountMap[currentTxn] = parentTransactionCountMap.get(currentTxn ,0)+1
                if currentTxn not in parents:
                    parents[currentTxn] = []
                parents[currentTxn].append(parentTxns[i]['txid'])
            

def getTotalCount(parentTxnCount, parentMap):
    for key in parentTxnCount:
        parents = parentMap[key]
        for txid in parents:
            parentTxnCount[key] = parentTxnCount.get(key, 0) + parentTxnCount.get(txid, 0)

def transactionAncestorySets(blockNumber):
    transactionHash= getBlockTransactionHash(blockNumber)
    transactionList = getTxnsForHash(transactionHash)
    transcationInCurrentBlock={}
    setCurrentBlockTxns(transactionList, transcationInCurrentBlock)
    parentsMap ={}
    parentTxnCountMap ={}
    getCountParenttransactions(transactionList,transcationInCurrentBlock,parentsMap,parentTxnCountMap)
    getTotalCount(parentTxnCountMap,parentsMap)
    sortedCount = sorted(parentTxnCountMap.items(), key=lambda kv:
                 (kv[1], kv[0]),reverse=True)
    for idx in range(10):
        print(sortedCount[idx][1] , sortedCount[idx][0])
    # return sortedCount[:10]



transactionAncestorySets(680000)
