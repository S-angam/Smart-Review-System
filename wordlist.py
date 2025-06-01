def get_wordlist():
    with open("./wordlist.txt", "r") as file:
        wordlist = file.read().splitlines()
    return wordlist