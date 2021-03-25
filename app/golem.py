import subprocess as sp
import json

class GolemStatus:
    
    def __init__(self):
        self._activity = _get_activity()
        self._version = _get_version()
        self._config = _get_config()
        self._payment = _get_payment()

    def account(self):
        return self._config["account"]

    def node_name(self):
        return self._config["node_name"]

    def version(self):
        return self._version["current"]["version"]
        
    def network(self):
        return self._payment["network"]
    
    def subnet(self):
        return self._config["subnet"]

    def processed_total(self):
        if "Terminated" not in self._activity["total"]:
            return 0
        return self._activity["total"]["Terminated"]

    def processed_hour(self):
        if "Terminated" not in self._activity["last1h"]:
            return 0
        return self._activity["last1h"]["Terminated"]

def _run_return_json(command):
    raw = sp.check_output(command, shell=True)
    return json.loads(raw)
    
def _get_activity():
    '''
    Returns: 
    {
        "last1h": 6,
        "total": 358,
    }

    ---------
    Command: yagna activity status --json
    Returns Json:
    {
        "last1h": {
            "Terminated": 6
        },
        "lastActivityTs": null,
        "total": {
            "New": 87,
            "Ready": 2,
            "Terminated": 358,
            "Unresponsive": 1
        }
    }
    '''
    return _run_return_json('yagna activity status --json')

def _get_config():
    '''
    Command: ya-provider config get --json
    Returns Json:
    {
        "node_name": "rambolicious",
        "subnet": "public-beta",
        "account": "0x123...fff"
    }
    '''
    return _run_return_json('ya-provider config get --json')

def _get_version():
    '''
    Command: yagna version show --json
    Returns Json:
    {
        "current": {
            "insertionTs": "2021-03-23T16:40:56",
            "name": "v0.6.2 Zagajewski Armstrong",
            "releaseTs": "2021-03-22T23:04:41",
            "seen": false,
            "updateTs": "2021-03-23T16:40:56",
            "version": "0.6.2"
        },
        "pending": null
    }
    '''
    return _run_return_json('yagna version show --json')

def _get_payment():
    '''
    Command: yagna payment status --json
    Returns Json:
    {
      "amount": "0",
      "driver": "zksync",
      "incoming": {
        "accepted": {
          "agreementsCount": 0,
          "totalAmount": "0"
        },
        "confirmed": {
          "agreementsCount": 0,
          "totalAmount": "0"
        },
        "requested": {
          "agreementsCount": 0,
          "totalAmount": "0"
        }
      },
      "network": "rinkeby",
      "outgoing": {
        "accepted": {
          "agreementsCount": 0,
          "totalAmount": "0"
        },
        "confirmed": {
          "agreementsCount": 0,
          "totalAmount": "0"
        },
        "requested": {
          "agreementsCount": 0,
          "totalAmount": "0"
        }
      },
      "reserved": "0",
      "token": "tGLM"
    }
    '''
    return _run_return_json('yagna payment status --json')
