import time

def a():
    print("A 시작") # 1 
    time.sleep(2) # 2 
    print("A 종료") # 3

def b():
    print("B 시작") # 4
    time.sleep(2) # 5
    print("B 종료") # 6

start = time.time()
a()
b()
end = time.time()
print(f"{end - start:.3f}초")
