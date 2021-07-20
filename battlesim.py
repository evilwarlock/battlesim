# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from enum import Enum


class Ship:
    def __init__(self, dps, high_slot_hps, mid_slot_hps, ehp, role, timer):
        self.dps = dps
        self.ehp = ehp
        self.high_slot_hps = high_slot_hps
        self.mid_slot_hps = mid_slot_hps
        self.timer = timer
        self.role = role

    def isAlive(self):
        if self.ehp <= 0:
            return False
        else:
            return True

    def isHealer(self):
        if self.role == 'Healer':
            return True
        else:
            return False

    def isTanker(self):
        if self.role == 'Tanker':
            return True
        else:
            return False

    def isDps(self):
        if self.role == 'Dps':
            return True
        else:
            return False


class Fleet:
    def __init__(self, ships):
        self.ships = ships

    def hasTanker(self):
        for ship in self.ships:
            if ship.isAlive():
                if ship.isTanker():
                    return True
        return False

    def hasHealer(self):
        for ship in self.ships:
            if ship.isAlive():
                if ship.isHealer():
                    return True
        return False

    def get_total_dps(self):
        dps = 0
        for ship in self.ships:
            if ship.isAlive():
                dps += ship.dps
        return dps

    def get_total_hps(self):
        hps = 0
        healer_being_attacked = True
        for ship in self.ships:
            if ship.isAlive():
                if self.hasTanker() and self.hasHealer():
                    hps += ship.mid_slot_hps * 2
                else:
                    hps += ship.mid_slot_hps
                if ship.isHealer():
                    if healer_being_attacked:
                        healer_being_attacked = False
                    else:
                        hps += ship.high_slot_hps
        return hps

    def print_status(self):
        print('Total DPS after this round:' + str(self.get_total_dps()))
        print('Total HPS after this round:' + str(self.get_total_hps()))
        for ship in self.ships:
            print(ship.role + ' ' + str(ship.ehp))

# Ship(dps, high_slot_hps, mid_slot_hps, ehp, role, timer)
# the number is divided by resist


def dps():
    return Ship(1500, 0, 387, 250000, 'Dps', 0)


def healer():
    return Ship(0, 3377, 309, 100000, 'Healer', 0)


def tanker():
    return Ship(300, 0, 0, 250000, 'Tanker', 0)


def simulation(fleet1, fleet2):
    total_dps_fleet1 = fleet1.get_total_dps()
    total_dps_fleet2 = fleet2.get_total_dps()
    total_hps_fleet1 = fleet1.get_total_hps()
    total_hps_fleet2 = fleet2.get_total_hps()

    abs_dmg_from_fleet1 = total_dps_fleet1 - total_hps_fleet2
    abs_dmg_from_fleet2 = total_dps_fleet2 - total_hps_fleet1

    for ship in fleet1.ships:
        if ship.isAlive():
            if abs_dmg_from_fleet2 > 0:
                remain_ehp = ship.ehp
                ship.ehp -= abs_dmg_from_fleet2
                abs_dmg_from_fleet2 -= remain_ehp
    for ship in fleet2.ships:
        if ship.isAlive():
            if abs_dmg_from_fleet1 > 0:
                remain_ehp = ship.ehp
                ship.ehp -= abs_dmg_from_fleet1
                abs_dmg_from_fleet1 -= remain_ehp



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    f1 = Fleet([tanker(), dps(), dps(), dps(), dps(), dps(), dps(), dps(), dps(), dps()])
    f2 = Fleet([healer(), healer(), healer(), tanker(), dps(), dps(), dps(), dps(), dps(), dps()])
    #f2 = Fleet([tanker(), dps(), dps(), dps(), dps(), dps(), dps(), dps(), dps(), dps()])
    for i in range(0, 1000):
        print('duration: ' + str(i))
        simulation(f1, f2)
        print('status of Fleet1')
        f1.print_status()
        print('status of Fleet2')
        f2.print_status()
        if f1.get_total_dps() == 0 or f2.get_total_dps() == 0:
            break


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
