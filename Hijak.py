# find Hijack for any AS
# from netmiko import ConnectHandler
# import requests
# import datetime
# print("please enter your AS number")
# AS=input()
# if len(str(datetime.datetime.now().hour))==1:
#     Hour="0"+str(datetime.datetime.now().hour)
# else:
#     Hour=str(datetime.datetime.now().hour)
# url=f"https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{AS}&starttime={datetime.datetime.now().date()}T{Hour}:00"
# API_IP=requests.request("get", url).json()
# Mobinnet_IP=[]
# for i in API_IP["data"]["prefixes"]:
#     Mobinnet_IP.append(i["prefix"])
# Hijack=[]
# var_Device= ConnectHandler(device_type="cisco_ios", ip="128.223.51.103", username="rviews", password="rviews")
#
# for i in Mobinnet_IP:
#     if ":" in i:
#         continue
#     else:
#         Var_Result = var_Device.send_command( f"sh ip bgp {i} best")
#         if AS not in Var_Result.splitlines()[4]:
#             Hijack.append(i)
# print(Hijack)
###################################

from netmiko import ConnectHandler
import requests
import datetime

class Find_IP_Address_Of_AS:
    def __init__(self, url, AS):
        self.url=url
        self.AS=AS
        self.Mobinnet_IP=[]

    def Find_IP_Address(self):
        API_IP = requests.request("get", url).json()
        for i in API_IP["data"]["prefixes"]:
            self.Mobinnet_IP.append(i["prefix"])
        self.Mobinnet_IP.append('1.1.1.1')
        return self.Mobinnet_IP

class Connection:
    def __init__(self, IP, User, Pass):
        self.IP=IP
        self.User=User
        self.Pass=Pass

    def SSH_To_Device(self):
        self.var_Device = ConnectHandler(device_type="cisco_ios", ip=self.IP, username=self.User, password=self.Pass)
        return self.var_Device

class Find_Hijack ( Find_IP_Address_Of_AS, Connection ):
    def __init__(self, url, AS , IP, User, Pass):
        Find_IP_Address_Of_AS.__init__(self,url, AS)
        Connection.__init__(self,IP,User,Pass)
        self.Hijack=[]
        self.Device = self.SSH_To_Device()
        self.IP_Address= self.Find_IP_Address()

    def Hijak_IP(self):
        for i in self.IP_Address:
            if ":" in i:
                continue
            else:
                Var_Result = self.Device.send_command( f"sh ip bgp {i} best")
                if "50810" not in Var_Result.splitlines()[4]:
                    self.Hijack.append(i)
        return self.Hijack

if len(str(datetime.datetime.now().hour))==1:
    Hour="0"+str(datetime.datetime.now().hour)
else:
    Hour=str(datetime.datetime.now().hour)

AS=input("please enter your AS number: ")
url=f"https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{AS}&starttime={datetime.datetime.now().date()}T{Hour}:00"
IP="128.223.51.103"
User="rviews"
Pass="rviews"
Company=Find_Hijack(url, AS, IP, User, Pass)
print(Company.Hijak_IP())
