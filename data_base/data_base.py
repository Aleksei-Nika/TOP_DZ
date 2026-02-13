MAX_H2O = 100.0
MAX_O2 = 100.0
MAX_CO2 = 100.0

H2O = 100.0
O2 = 20.0
CO2 = 0.0

GIDROLIZE_H2O = 2.0 * 2
GIDROLIZE_O2 = 1.8 * 2

CONSUNPTION_O2_O2 = 2.0
CONSUNPTION_O2_CO2 = 1.8

GENER_H2O_CO2 = 2.0
GENER_H2O_H2O = 1.8

class Gidrolize:
    def __init__(self):
        self.consumption = GIDROLIZE_H2O
        self.revenue = GIDROLIZE_O2
    @property
    def consumption(self):
        self.consumption
    @property
    def revenue(self):
        self.revenue

class Breath:
    def __init__(self):
        self.consumption = CONSUNPTION_O2_O2
        self.revenue = CONSUNPTION_O2_CO2
    @property
    def consumption(self):
        self.consumption
    @property
    def revenue(self):
        self.revenue

class Geneg_water:
    def __init__(self):
        self.consumption = GENER_H2O_CO2
        self.revenue = GENER_H2O_H2O
    @property
    def consumption(self):
        self.consumption
    @property
    def revenue(self):
        self.revenue


class StarShip:
    def __init__(self):
        self.banck_h2o = MAX_H2O
        self.banck_o2 = MAX_O2
        self.banck_co2 = MAX_CO2
        self.h2o = H2O
        self.o2 = O2
        self.co2 = CO2

        self.day_of_flight = 0
        self.max_day_of_flight = 200

        self.module = (Gidrolize(), Breath(), Geneg_water())

    def gidrolize(self):
        if self.o2 < self.banck_o2 and self.h2o >= GIDROLIZE_H2O:
            self.h2o -= GIDROLIZE_H2O
            if self.o2 <= self.banck_o2 - GIDROLIZE_O2:
                self.o2 += GIDROLIZE_O2
            else:
                self.o2 = 100

    def consumption_o2(self):
        if self.o2 >= CONSUNPTION_O2_O2:
            self.o2 -= CONSUNPTION_O2_O2
            if self.co2 <= self.banck_co2 - CONSUNPTION_O2_CO2:
                self.co2 += CONSUNPTION_O2_CO2
            else:
                self.co2 = 100
        else:
            self.o2 = 0
    
    def gener_h2o(self):
        if self.h2o < self.banck_h2o and self.co2 >= GENER_H2O_CO2:
            self.co2 -= GENER_H2O_CO2
            if self.h2o <= self.banck_h2o - GENER_H2O_H2O:
                self.h2o += GENER_H2O_H2O
            else:
                self.h2o = 100

def flaght(ship):
    while True: #ship.day_of_flight <= ship.max_day_of_flight:
        ship.gener_h2o()
        ship.gidrolize()
        ship.consumption_o2()
        print(f'день полёта {ship.day_of_flight}')
        print(f'H2O: {ship.h2o:.1f}/{ship.banck_h2o}')
        print(f' O2: {ship.o2:.1f}/{ship.banck_o2}')
        print(f'CO2: {ship.co2:.1f}/{ship.banck_co2}')
        print(f'Общий показатель: {ship.h2o + ship.o2 + ship.co2:.1f}')
        print()
        ship.day_of_flight += 1
        input()
        if ship.h2o <= 0 or ship.o2 <= 0:
            print('Жизненоважные показатели упали ниже допустимого уровня')
            break

#flaght(StarShip())

if __name__ == '__main__':
    class Dfg:
        pass