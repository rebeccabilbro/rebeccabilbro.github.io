class RollingHash:

    def __init__(self, text, wordsize):
        self.text = text
        self.hash = 0
        self.wordsize = wordsize

        for i in range(0, wordsize):
            #ord maps the character to a number
            #subtract out the ASCII value of "a" to start the indexing at zero
            self.hash += (ord(self.text[i]) - ord("a")+1)*(26**(wordsize - i -1))

        #start index of current window
        self.start = 0
        #end of index window
        self.end = wordsize

    def move_window(self):
        if self.end <= len(self.text) - 1:
            #remove left letter from hash value
            self.hash -= (ord(self.text[self.start]) - ord("a")+1)*26**(self.wordsize-1)
            self.hash *= 26
            self.hash += ord(self.text[self.end]) - ord("a")+1
            self.start += 1
            self.end += 1

    def window_text(self):
        return self.text[self.start:self.end]

if __name__ == '__main__':

    def rabin_karp(word, text):
        if word == "" or text == "":
            return None
        if len(word) > len(text):
            return None

        rolling_hash = RollingHash(text, len(word))
        word_hash = RollingHash(word, len(word))
        #word_hash.move_window()

        for i in range(len(text) - len(word) + 1):
            if rolling_hash.hash == word_hash.hash:
                if rolling_hash.window_text() == word:
                    return i
            rolling_hash.move_window()
        return None

    print(rabin_karp("a", "abcdefgh"))
    print(rabin_karp("d", "abcdefgh"))
    print(rabin_karp("cupcakes", "balloonsandcupcakes"))
