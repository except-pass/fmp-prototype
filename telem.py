import json

from typing import OrderedDict

packet = {
    "CellV": 321,
    "CellTmp": 283,
    "CellSt": 0
}

repeating = OrderedDict()
for i in range(16):
    repeating[str(i)] = packet

whole = {
    "id": 805,  
    "fixed": {
        "StrIdx": 0,
        "ModIdx": 0,
        "NCell": 16,
        "SoC": 894,
        "SoH": 999,
        "V": 513,
        "CellVMax": 34,
        "CellVMaxCell": 3,
        "CellVMin": 31,
        "CellVMinCell": 14,
        "CellVAvg": 32,
        "CellTmpMax": 281,
        "CellTmpMaxCell": 7,
        "CellTmpMin": 265,
        "CellTmpMinCell": 3,
        "CellTmpAvg": 274,
        "NCellBal": 0,
        "SN": 2022050009
    },
        "repeating": repeating
    }

print(json.dumps(whole, indent=4))