#coding:utf-8
import pyzbar.pyzbar as pyzbar
from PIL import Image
import urllib
from urllib3 import request
import json


def bclassify(path):
    barcodes = pyzbar.decode(Image.open(path))
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        print("扫描结果==》 类别： {0} 内容： {1}".format(barcodeType, barcodeData))

        url="https://www.mxnzp.com/api/barcode/goods/details?barcode="+barcodeData
        html=urllib.request.urlopen(url)
        res=json.loads(html.read())
        print(res)
        print(res["data"]["goodsName"])
        if res["msg"] == '数据返回成功':
            if "药" in res["data"]["supplier"] or "生物科技" in res["data"]["supplier"]:
                classify = "harmtrash"
            elif "L" in res["data"]["standard"] or "l" in res["data"]["standard"] or "升" in res["data"]["standard"]:
                classify = "cycletrash"
            elif "g" in res["data"]["standard"] or "克" in res["data"]["standard"]:
                classify = "drytrash"
            else: classify=None
        else: classify=None
        print(classify)
        return classify