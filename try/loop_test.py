import time
def main():
    cnt=0
    while True:
        time.sleep(2)
        cnt+=1
        print('current count is %s'%cnt)

if __name__=='__main__':
    main()