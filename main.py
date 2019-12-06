import sentiment
import history
from threading import Thread


def main():
    sen = Thread(target=sentiment.main)
    sen.start()
    # history.main()


if __name__ == "__main__":
    print("Starting!")
    main()
