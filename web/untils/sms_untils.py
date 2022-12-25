import requests
from urllib.parse import quote
def send_sms(phone, ip, text):
    url = "https://qbaor.com/sms/sen_sms_content?phone="+str(phone)+"&product="+ip+"&remark="+quote(text)
    # print(url)
    response = requests.request("GET", url)
    print(response.text)