# Std Lib imports
import logging
import sys
from dataclasses import dataclass, asdict
from csv import DictWriter

# External imports
import requests


# Module-level variables
log = logging.getLogger(__name__)
token = None


@dataclass
class Device:
    hostname: str
    ip: str = None
    Building: str = None
    Closet: str = None
    Serial: str = None
    model: str = None
    vendor: str = None
    version: str = None
    description: str = None
    editDate: str = None
    id: str = None
    location: int = 0
    rack: str = None
    rack_size: str = None
    rack_start: str = None
    sections: str = '9;14'
    snmp_community: str = None
    snmp_port: str = None
    snmp_queries: str = None
    snmp_timeout: str = None
    snmp_v3_auth_pass: str = None
    snmp_v3_auth_protocol: str = None
    snmp_v3_ctx_engine_id: str = None
    snmp_v3_ctx_name: str = None
    snmp_v3_priv_pass: str = None
    snmp_v3_priv_protocol: str = None
    snmp_v3_sec_level: str = None
    snmp_version: str = None
    type: int = 1

    def asdict(self):
        return {
            key: value for key, value in asdict(self).items()
            if value is not None
        }


def authenticate(url, username, passw):
    global token
    if token:
        return {"token": token}

    auth_url = url + "user/"
    log.info("Authenticating to: " + auth_url)
    log.info("With username: " + username)
    try:
        response = requests.request("POST", auth_url,
                                    auth=(username, passw))
    except requests.exceptions.ConnectionError:
        raise Exception(
            "Authentication has failed. Please try again. If problem persists, "
            "please contact Alex"
        )
    if "data" in response.json():
        log.info("Authenticated successfully")
        token = response.json()["data"]["token"]
        log.info("Auth token: " + token)
        return {"token": token}
    else:
        raise Exception(
            "Authentication has failed. Please try again. If problem persists, "
            "please contact Alex"
        )


def printTable(myDict, colList=None):
   """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
   If column names (colList) aren't specified, they will show in random order.
   Author: Thierry Husson - Use it as you want but don't blame me.
   """
   if not colList: colList = list(myDict[0].keys() if myDict else [])
   myList = [colList] # 1st row = header
   for item in myDict: myList.append([str(item[col] or '') for col in colList])
   colSize = [max(map(len,col)) for col in zip(*myList)]
   formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
   myList.insert(1, ['-' * i for i in colSize]) # Seperating line
   for item in myList: print(formatStr.format(*item))


def get(url, username, password, search_word=None, csv_mode=False):
    headers = authenticate(url, username, password)
    if search_word:
        resp = requests.get(
            url + "devices/search/" + search_word + "/", headers=headers
        )
    else:
        resp = requests.get(url + "devices/", headers=headers)
    json = resp.json()
    if 'data' not in json:
        log.error("Response from server: " + json['message'])
    else:
        data = resp.json()['data']
        if csv_mode:
            writer = DictWriter(sys.stdout, data.keys())
            writer.writeheader()
            writer.writerows(data)
        else:
            printTable(data, ['hostname', 'ip', 'Building', 'Closet', 'vendor', 'model'])
            print("Total # of entries: " + str(len(data)))


def create(url, username, password, device: Device):
    sys.stderr.write(
        "Errors: the phpIPAM device API does not currently support creating "
        "new devices. see https://github.com/phpipam/phpipam/issues/1983 for "
        "details"
    )
    sys.exit(1)
    # headers = authenticate(url, username, password)
    # data = device.asdict()
    # resp = requests.post(url + "devices/", data=data, headers=headers)
    # json = resp.json()
    # if json.get('success') is not True:
    #     log.error(
    #         "Attempting to create device. \nResponse from server: " +
    #         json['message']
    #     )
    # else:
    #
    #     dev_id = json['id']
    #     resp = requests.patch(
    #         url + "devices/", headers=headers,
    #         data={"id": dev_id, "type": type_id}
    #     )
    #     json = resp.json()
    #     if json.get('success') is not True:
    #         log.error(
    #             "Attempting to update device type for newly created device. "
    #             "\nResponse from server: " + json['message']
    #         )
    #     else:
    #         print("Device created successfully!")
