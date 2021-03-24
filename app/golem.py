import re
import sys
import subprocess as sp

def get_status():
    o = sp.check_output(["golemsp", "status"]).decode()
    if "┌─────" not in o:
        return None
    return o

class GolemStatus:
    def __init__(self, status):
        self.status = status

    def _get_first_group(self, regex):
        matches = re.finditer(regex, self.status, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                return match.group(groupNum)
        return None

    def wallet(self):
        return self._get_first_group(r'(0x\S+)\x1b')

    def node_name(self):
        return self._get_first_group(r'Node\sName\s+(\S+)')

    def version(self):
        return self._get_first_group(r'│\s+Version\s+(\S+)')

    def network(self):
        return self._get_first_group(r'network\s+\x1b\S+?m(\S+)\x1b')
    
    def subnet(self):
        return self._get_first_group(r'Subnet\s+(\S+)')

    def processed_total(self):
        return self._get_first_group(r'total processed\s+(\d+)')

    def processed_hour(self):
        return self._get_first_group(r'last 1h processed\s+(\d+)')

    def processing_hour(self):
        return self._get_first_group(r'last 1h in progress\s+(\d+)')