import subprocess as sp
import json
import re

class GolemStatus:
    
    def __init__(self):
        self._activity = _get_activity()
        self._version = _get_version()
        self._config = _get_config()
        self._payment = _get_payment()
        self._status = _get_golemsp_status()
        self._appkey_list = _get_appkey_list()
        self._profile_name = _get_profile_name()
        self._profile = _get_profile()

    def account(self):
        return self._config["account"]

    def node_name(self):
        return self._config["node_name"]

    def version(self):
        return self._version["current"]["version"]

    def update(self):
        if (self._version["pending"] == None):
            return False
        else:
            return self._version["pending"]["version"]
        
    def network(self):
        return self._get_first_group('network\s+\x1b\S+?m(\S+)\x1b')
        # return self._payment["network"]
    
    def subnet(self):
        return self._config["subnet"]

    def cpu_threads(self):
        return self._profile[self._profile_name]["cpu_threads"]

    def mem_gib(self):
        return self._profile[self._profile_name]["mem_gib"]

    def storage_gib(self):
        return self._profile[self._profile_name]["storage_gib"]

    def processed_total(self):
        if "Terminated" not in self._activity["total"]:
            return 0
        return self._activity["total"]["Terminated"]

    def processed_hour(self):
        if "Terminated" not in self._activity["last1h"]:
            return 0
        return self._activity["last1h"]["Terminated"]
    
    def id(self):
        headers = self._appkey_list["headers"]
        index_name = headers.index("name")
        index_id = headers.index("id")

        data = self._appkey_list["values"]
        for values in data:
            if values[index_name] == "golem-cli":
                return values[index_id]
        return None

    def _get_first_group(self, regex):
        matches = re.finditer(regex, self._status, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                return match.group(groupNum)
        return None

def _get_golemsp_status():
    o = sp.check_output(["golemsp status"], shell=True).decode()
    if "┌─────" not in o:
        return None
    return o

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

def _get_profile_name():
    '''
    Command: ya-provider profile active
    Returns:
    "default"
    '''
    return _run_return_json('ya-provider profile active')

def _get_profile():
    '''
    Command: ya-provider profile list --json
    Returns Json:
    {
      "default": {
        "cpu_threads": 15,
        "mem_gib": 30.0,
        "storage_gib": 170.0
      }
    }
    '''
    return _run_return_json('ya-provider profile list --json')

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

def _get_appkey_list():
    '''
    Command: yagna app-key list --json
    JSON Returns:
    {
        "headers": [
            "name",
            "key",
            "id",
            "role",
            "created"
        ],
        "values": [
            [
                "golem-cli",
                "42f8ee51921641b0a698acb7ba3e3127",
                "0x08d8cf128538b5cf5bb753480db35ed03e5261ff",
                "manager",
                "2021-03-17T03:24:33.801245867"
            ]
        ]
    }
    '''
    return _run_return_json('yagna app-key list --json')
