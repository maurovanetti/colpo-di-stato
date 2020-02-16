class Configuration:
    def __init__(self, n):
        self.mask = bin(n).split(sep='b')[1][::-1]

    def flipped_at(self, i):
        return False if i >= len(self.mask) else (self.mask[i] == '1')

    def apply(self, ringleader, conspirators):
        ringleader.extra = self.flipped_at(0)
        for i in range(1, len(conspirators)):
            conspirators[i].extra = self.flipped_at(i)

    def is_beyond(self, other):
        for i in range(0, len(other.mask)):
            if other.flipped_at(i) and not self.flipped_at(i):
                return False
        return True

    def pad(self, min_length):
        return self.mask + ('0' * (min_length - len(self.mask)))

    def how_many(self):
        return self.mask.count('1')
