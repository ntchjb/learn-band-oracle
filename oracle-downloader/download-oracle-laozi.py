import requests
import os
import json
import base64
import errno

COUNTS_URL = "https://laozi-testnet2.bandchain.org/oracle/v1/counts"
DATASOURCE_BASE_URL = "https://laozi-testnet2.bandchain.org/oracle/v1/data_sources"
ORACLE_SCRIPT_BASE_URL = "https://laozi-testnet2.bandchain.org/oracle/v1/oracle_scripts"
DATA_BASE_URL = "https://laozi-testnet2.bandchain.org/oracle/v1/data"

def GET(url, height):
  return requests.get(url, headers={'User-Agent': 'curl/7.64.1', 'x-cosmos-block-height': height}).json()
def GET_FILE(url, height):
  result = requests.get(url, headers={'User-Agent': 'curl/7.64.1', 'x-cosmos-block-height': height}).json()
  return base64.b64decode(result['data'])
def WRITE_TO_FILE(filePath, msg):
  if not os.path.exists(os.path.dirname(filePath)):
    try:
      os.makedirs(os.path.dirname(filePath))
    except OSError as exc: # Guard against race condition
      if exc.errno != errno.EEXIST:
        raise
  with open(filePath, "wb") as f:
    f.write(msg)

def WRITE_JSON_TO_FILE(filePath, obj):
  if not os.path.exists(os.path.dirname(filePath)):
    try:
      os.makedirs(os.path.dirname(filePath))
    except OSError as exc: # Guard against race condition
      if exc.errno != errno.EEXIST:
        raise
  with open(filePath, 'w+', encoding='utf-8') as f:
    json.dump(obj, f)
    
def main():
  blockHeight = os.environ["BLOCK_HEIGHT"]
  filesPath = os.environ["ORACLE_FILES_PATH"]
  genesisFilePath = os.environ["GENESIS_FILE_PATH"]
  genesisFilePathOriginal = os.environ["GENESIS_FILE_PATH_ORIGINAL"]

  counts = GET(COUNTS_URL, blockHeight)
  print(counts)
  
  dataSourceCount = int(counts["data_source_count"])
  oracleScriptCount = int(counts["oracle_script_count"])

  dataSources = []
  oracleScripts = []
  for i in range(1, dataSourceCount):
    dataSource = GET(DATASOURCE_BASE_URL + "/" + str(i), blockHeight)
    print(dataSource)
    file = GET_FILE(DATA_BASE_URL + "/" + dataSource["data_source"]["filename"], blockHeight)
    WRITE_TO_FILE(filesPath + "/" + dataSource["data_source"]["filename"], file)
    dataSources.append(dataSource["data_source"])
  for i in range(1, oracleScriptCount):
    oracleScript = GET(ORACLE_SCRIPT_BASE_URL + "/" + str(i), blockHeight)
    print(oracleScript)
    file = GET_FILE(DATA_BASE_URL + "/" + oracleScript["oracle_script"]["filename"], blockHeight)
    WRITE_TO_FILE(filesPath + "/" + oracleScript["oracle_script"]["filename"], file)
    oracleScripts.append(oracleScript["oracle_script"])

  if genesisFilePathOriginal:
    with open(genesisFilePathOriginal, encoding='utf-8') as fh:
      genesisState = json.load(fh)
    genesisState["app_state"]["oracle"]["data_sources"] = dataSources
    genesisState["app_state"]["oracle"]["oracle_scripts"] = oracleScripts
    WRITE_JSON_TO_FILE(genesisFilePath, genesisState)
  
if __name__ == "__main__":
  main()
