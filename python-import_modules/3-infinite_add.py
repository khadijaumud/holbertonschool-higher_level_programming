#!/usr/bin/python3

if __name__ == "__main__":
    import sys
    total = 0
    if len(sys.argv) == 1:
        print(0)
    else:
        for i in range(1, len(sys.argv)):
            num = int(sys.argv[i])
            total = total + num
        print(total)
