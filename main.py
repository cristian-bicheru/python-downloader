import requests
import math

dlurl = input("Enter the download url: ")
filename = input("Enter the file name and directory: ")

def download(dlurl, filename):
    try:
        dl = requests.get(dlurl, stream=True, timeout=10)
        dlsize = int(requests.head(dlurl).headers["Content-Length"])
        failed = 0
    except:
        print("initial retrival failed")
        failed = 1
    if failed == 1:
        while True:
                try:
                    dl = requests.get(dlurl, stream=True, timeout=10)
                    dlsize = int(requests.head(dlurl).headers["Content-Length"])
                    break
                except:
                    print("retriaval failure")
    try:
        if dl.status_code == 200:
            print("download initiated")
            bytesdl = 0
            file = open(filename, 'ab')
            for chunk in dl.iter_content(chunk_size=512):
                file.write(chunk)
                bytesdl += len(chunk)
                pct = bytesdl/dlsize*100
                if pct % 1 <= 0.0000001 and pct != 0:
                    print(pct)
        else:
            return "Failed"
    except:
        print("dl fail, retrying at " + str(pct))
        if dl.status_code == 200:
            while True:
                try:
                    if dlsize >= bytesdl:
                        dl = requests.get(dlurl, {'Range': 'bytes=%d-' % bytesdl}, stream=True, timeout=10)
                        for chunk in dl.iter_content(chunk_size=512):
                            file.write(chunk)
                            bytesdl += len(chunk)
                            pct = bytesdl/dlsize*100
                            if pct % 1 <= 0.0000001 and pct != 0:
                                print(pct)
                    else:
                        break
                except:
                    print("dl fail, retrying at " + str(pct))
        else:
            return "Failed"
    file.close()

download(dlurl, filename)
