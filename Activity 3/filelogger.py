import sys


def log(message):
    file = open("log.txt", "a")
    file.write(message+'\n')
    file.close()


if __name__ == "__main__":
    log(' '.join(sys.argv[1:]) or 'info: hello world')
