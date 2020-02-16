import random
import math

from configuration import Configuration
from conspirator import Conspirator


class ConspiracyException(BaseException):
    pass


def next_spot(pivot, direction):
    dx = 0
    dy = 0
    if direction == 'n':
        dy = +1
    elif direction == 'e':
        dx = +1
    elif direction == 'w':
        dx = -1
    elif direction == 's':
        dy = -1
    return pivot[0] + dx, pivot[1] + dy


class Conspiracy:
    def __init__(self, ringleader):
        self.plot = dict()
        self.loose_ends = [(0, 0)]
        self.involve(ringleader, self.loose_ends[0])

    def next_conspirator(self, spot, direction):
        try:
            return self.plot[next_spot(spot, direction)]
        except KeyError:
            return None

    def involve(self, conspirator, spot):
        if spot in self.plot:
            raise ConspiracyException("Spot already used")
        if spot not in self.loose_ends:
            raise ConspiracyException("Spot unreachable")
        for direction in 'news':
            if len(self.plot) == 0 or conspirator.can_join(direction, self.next_conspirator(spot, direction)):
                self.plot[spot] = conspirator
                # if len(self.plot) == 1:
                #     print("{} starts the conspiracy @ {}".format(conspirator.name, spot))
                # else:
                #     print("{}{} involved @ {}, using its link «{}»"
                #           .format(conspirator.name,
                #                   "+" if conspirator.extra else "",
                #                   spot,
                #                   direction))
                self.loose_ends.remove(spot)
                for link_direction, link_type in conspirator.links().items():
                    if link_type is not None:
                        loose_end = next_spot(spot, link_direction)
                        if loose_end not in self.loose_ends and loose_end not in self.plot:
                            self.loose_ends.append(loose_end)
                return
        raise ConspiracyException("No matching conspirator around the spot")


ATTEMPTS_PER_CONFIGURATION = 1000
RINGLEADER = Conspirator("Principe", 'ews', 'news')
CONSPIRATORS = [
    Conspirator("Neofascista", 'n', 'nw'),
    Conspirator("Forestale", 'e', 'ne'),
    Conspirator("Mafioso", 'w', 'ewS'),
    Conspirator("Imprenditore", 's', 'Ws'),
    Conspirator("Venerabile", 'e', 'eW'),
    Conspirator("Americano", 'S', 'wS'),
    Conspirator("Carabiniere", 'W', 'EWs'),
    Conspirator("Spia", 'E', 'NE'),
    Conspirator("Generale", 'N', 'NW'),
    Conspirator("Divo", 'E', 'NEWS'),
]

CONSPIRATORS_BACKUP_4 = [
    Conspirator("Neofascista", 'n', 'nw'),
    Conspirator("Forestale", 'e', 'ne'),
    Conspirator("Mafioso", 'w', 'ewS'),
    Conspirator("Imprenditore", 's', 'Ws'),
    Conspirator("Venerabile", 'e', 'eW'),
    Conspirator("Americano", 'S', 'wS'),
    Conspirator("Carabiniere", 'W', 'EWs'),
    Conspirator("Spia", 'E', 'NE'),
    Conspirator("Generale", 'N', 'NW'),
    Conspirator("Divo", 'E', 'NEWS'),
]

CONSPIRATORS_BACKUP_3 = [
    Conspirator("Neofascista", 'n', 'nw'),
    Conspirator("Forestale", 'e', 'ne'),
    Conspirator("Mafioso", 'w', 'ewS'),
    Conspirator("Imprenditore", 's', 'Ws'),
    Conspirator("Venerabile", 'e', 'eW'),
    Conspirator("Americano", 'S', 'wS'),
    Conspirator("Carabiniere", 'W', 'EWs'),
    Conspirator("Spia", 'E', 'NE'),
    Conspirator("Divo", 'EWS', 'NEWS'),
    Conspirator("Generale", 'N', 'NW'),
]
CONSPIRATORS_BACKUP_2 = [
    Conspirator("Neofascista", 'n', 'nw'),
    Conspirator("Forestale", 'e', 'ne'),
    Conspirator("Mafioso", 'w', 'ewS'),
    Conspirator("Imprenditore", 's', 'Ws'),
    Conspirator("Venerabile", 'E', 'ES'),
    Conspirator("Americano", 'Ew', 'Ews'),
    Conspirator("Carabiniere", 'W', 'EW'),
    Conspirator("Spia", 'e', 'neS'),
    Conspirator("Generale", 'Ns', 'Nes'),
    Conspirator("Divo", 'W', 'NEWS'),
]
CONSPIRATORS_BACKUP_1 = [
    Conspirator("Neofascista", 'n', 'nw'),
    Conspirator("Forestale", 'e', 'ne'),
    Conspirator("Mafioso", 'w', 'ew'),
    Conspirator("Imprenditore", 's', 'sW'),
    Conspirator("Venerabile", 's', 'sE'),
    Conspirator("Americano", 'wE', 'wsE'),
    Conspirator("Carabiniere", 'W', 'EW'),
    Conspirator("Spia", 'eS', 'neS'),
    Conspirator("Generale", 'N', 'NS'),
    Conspirator("Divo", '', 'NEWS'),  # TODO
]
MAX_RANK = len(CONSPIRATORS) + 1


def setup_random_conspiracy(ringleader, conspirators, flips=0):
    conspiracy = Conspiracy(ringleader)
    random.shuffle(conspirators)
    baddies = [ringleader]
    baddies.extend(conspirators)
    random.shuffle(baddies)
    for baddie in baddies:
        if flips > 0:
            flips -= 1
            baddie.extra = True
        else:
            baddie.extra = False
    return conspiracy, conspirators


def setup_conspiracy(configuration):
    conspiracy = Conspiracy(RINGLEADER)
    conspirators = CONSPIRATORS.copy()
    configuration.apply(RINGLEADER, conspirators)
    random.shuffle(conspirators)
    return conspiracy, conspirators


def sim():
    inferences = {}
    solutions_count = {
        False: [0] * MAX_RANK,
        True: [0] * MAX_RANK
    }
    for i in range(0, int(math.pow(2, MAX_RANK))):
        configuration = Configuration(i)
        min_involved = 1
        for cfg, rank in inferences.items():
            if configuration.is_beyond(cfg):
                min_involved = max(min_involved, rank)
                if min_involved == MAX_RANK:
                    break
        if min_involved < MAX_RANK:
            max_involved = max_involvable(configuration, min_involved, attempts=ATTEMPTS_PER_CONFIGURATION)
            if max_involved > min_involved:
                inferences[configuration] = max_involved
                print()
            else:
                print(" (no improvement on ancestors)".format(configuration.mask))
        else:
            print("{} can be inferred to be solvable".format(configuration.mask))
        if min_involved == MAX_RANK or max_involved == MAX_RANK:
            for j in range (0, MAX_RANK):
                flipped = configuration.flipped_at(j)
                solutions_count[flipped][j] += 1
    solutions = [' '] * MAX_RANK
    for cfg, rank in sorted(inferences.items(), key=lambda x: x[1]):
        if rank == MAX_RANK:
            marker = "!"
            for i in range(0, MAX_RANK):
                role = solutions[i]
                flag = cfg.flipped_at(i)
                if role == ' ':
                    solutions[i] = '1' if flag else '0'
                elif role == '0' and flag:
                    solutions[i] = 'X'
                elif role == '1' and not flag:
                    solutions[i] = 'X'
        else:
            marker = ""
        print("{} ({}) --> {} {}".format(cfg.pad(MAX_RANK), cfg.how_many(), rank, marker))
    print("Solutions mask: {}".format("".join(solutions)))
    print("Solutions found per card (unflipped, flipped):")
    for i in range(0, MAX_RANK):
        if i == 0:
            name = RINGLEADER.name
        else:
            name = CONSPIRATORS[i - 1].name
        print("{} --> {}, {}".format(name, solutions_count[False][i], solutions_count[True][i]))


def max_involvable(configuration, min_involved, attempts):
    print(configuration.mask, end='')
    max_involved = min_involved
    while max_involved < MAX_RANK and attempts > 0:
        print(".", end='')
        attempts -= 1
        conspiracy, conspirators = setup_conspiracy(configuration)
        while True:
            involved = []
            for conspirator in conspirators:
                # print("Trying to involve {}".format(conspirator.name))
                if len(conspiracy.loose_ends) > 0:
                    random.shuffle(conspiracy.loose_ends)
                    for loose_end in conspiracy.loose_ends:
                        try:
                            conspiracy.involve(conspirator, loose_end)
                            involved.append(conspirator)
                            break
                        except ConspiracyException:
                            continue
                else:
                    # print("No more loose ends")
                    break
            if len(involved) == 0:
                break
            else:
                conspirators = [x for x in conspirators if x not in involved]
        n = len(conspiracy.plot)
        # print("{} people involved".format(n))
        max_involved = max(n, max_involved)
    print(max_involved, end='')
    # print("The best solution found involves {} people out of {}".format(max_involved, len(CONSPIRATORS) + 1))
    return max_involved


if __name__ == '__main__':
    sim()
