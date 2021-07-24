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
        self.attacked = False


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


    def take_damage(self, damage):
        # if the ship breaks after this round
        if (self.ehp <= damage):
            self.ehp = 0
            return self.ehp
        # is the ship is still alive
        else :
            self.ehp -= damage
            return damage
            


# Ship(dps, high_slot_hps, mid_slot_hps, ehp, role, timer)
# the number is divided by resist


def dps():
    return Ship(1500, 0, 387, 250000, 'Dps', 0)


def healer():
    return Ship(0, 3377, 309, 100000, 'Healer', 0)


def tanker():
    return Ship(300, 0, 0, 250000, 'Tanker', 0)


class Squad:
    # type is the number of ship in order of healer, tank, dps, pm = primary mode is the order that ship gets attackted
    def __init__(self, ships = []):
        # squad has a max len of 10 people
        assert (len(ships) <= 10)
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


    def get_attacked_ship(self):
        for ship in self.ships:
            if ship.attacked:
                return ship
        return None
    

    def get_mid_slot_hps(self):
        hps = 0
        find_attacked_ship = False
        # This might be used after we differ ship by gear
        tanker_mutiply_coefficient = 1
        for ship in self.ships:
            if ship.isAlive():
                if not find_attacked_ship:
                    find_attacked_ship = True
                    ship.attacked = True
                # if the SQUAD have a tanker and it is not get attacked, then we get a double the mid_slot effect
                if (self.hasTanker() and self.get_attacked_ship().isTanker() == False):
                    tanker_mutiply_coefficient = 2
                hps += ship.mid_slot_hps
        return hps * tanker_mutiply_coefficient


    def get_high_slot_hps(self):
        hps = 0
        for ship in self.ships:
            if ship.isAlive():
                if not ship.attacked:
                    hps += ship.high_slot_hps
        return hps


    def get_alive_number(self):
        count = 0
        for ship in self.ships:
            if ship.isAlive():
                count += 1
        return count
    
    # apply the damage to ships with the order that it is in the squad
    # return the total damage "consumed"
    def take_damage(self, damage):
        total_damage_used = 0
        for ship in self.ships:
            if (total_damage_used >= damage):
                break
            used_damage = ship.take_damage(damage)
            damage -= used_damage
            total_damage_used += used_damage
        return total_damage_used

    
    def print_status(self):
        for ship in self.ships:
            print(ship.role + ' ' + str(ship.ehp))
    

class Fleet:

    def __init__(self, squads = []):
        # max number of squad allowed is 5
        assert(len(squads) <= 5)
        self.squads = squads
    

    def get_total_dps(self):
        dps = 0
        for squad in self.squads:
            dps += squad.get_total_dps
        return dps
    

    def get_total_hps(self):
        hps = 0
        find_attacked_squad = False
        for squad in self.squads:
            # if there is some ship that are still alive in squad, means the squad is "alive"
            if squad.get_alive_number() > 0:
                # the first squad get attacked first
                if find_attacked_squad == False:
                    hps += squad.get_mid_slot_hps()                    
                    find_attacked_squad = True
                hps += squad.get_high_slot_hps()
        return hps


    def get_total_dps(self):
        dps = 0
        for squad in self.squads:
            dps += squad.get_total_dps()
        return dps
    

    def get_total_alived_ship(self):
        count = 0
        for squad in self.squads:
            count += squad.get_alive_number()
        return count

    
    def take_damage(self, damage):
        for squad in self.squads:
            if (damage <= 0):
                break
            damage -= squad.take_damage(damage)


    def print_status(self):
        print("number of ship left: " + str(self.get_total_alived_ship()))
        print("total dps: " + str(self.get_total_dps()))
        print("total hps: " + str(self.get_total_hps()))
        for squad in self.squads:
            squad.print_status()
        




def simulation(fleet1, fleet2):
    total_dps_fleet1 = fleet1.get_total_dps()
    total_dps_fleet2 = fleet2.get_total_dps()
    total_hps_fleet1 = fleet1.get_total_hps()
    total_hps_fleet2 = fleet2.get_total_hps()

    abs_dmg_from_fleet1 = total_dps_fleet1 - total_hps_fleet2
    abs_dmg_from_fleet2 = total_dps_fleet2 - total_hps_fleet1

    if abs_dmg_from_fleet2 > 0:
        fleet1.take_damage(abs_dmg_from_fleet2)

    if abs_dmg_from_fleet1 > 0:
        fleet2.take_damage(abs_dmg_from_fleet1)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    s1 = Squad([healer(), tanker(), dps(), dps(), dps(), dps(), dps()])
    s2 = Squad([dps(), dps()])
    s3 = Squad(([dps()]))
    f1 = Fleet([s1])
    f2 = Fleet([s2, s3])
    for i in range(1000):
        print('duration: ' + str(i))
        simulation(f1, f2)
        print('status of Fleet1')
        f1.print_status()
        print('status of Fleet2')
        f2.print_status()
        if f1.get_total_dps() == 0 or f2.get_total_dps() == 0:
            break


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
