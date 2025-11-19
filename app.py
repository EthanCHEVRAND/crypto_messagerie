from tools.crypto import *
from tools.files import *

def main():
    f = create_file("test.txt", "salut c'est moi tchoupi")
    print(f.read())
    return 0

if __name__ == "__main__":
    main()
