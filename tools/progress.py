from rich.progress import track
import time

dic = {}
dic[1] = 1
dic[2] = 2
for k, v in track(dic.items()):
    time.sleep(0.5)