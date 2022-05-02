import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, pop_size, virus, vacc_percentage, initial_infected=1):
        self.logger = Logger('answers.txt')
        self.pop_size = pop_size # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_vaccinated = 0
        self.total_infected = 0 # Int
        self.total_dead = 0 # Int
        self.population = [] # List of Person objects
        self.file_name = f"{self.virus.name}_simulation_pop_{pop_size}_vp_{vacc_percentage}_infected_{initial_infected}.txt"
        self.newly_infected = []
        self.dead_population = [] # tip
        self.num_interactions = 0
        self.vaccine_interactions = 0
        self.death_interactions = 0

    def _create_population(self, initial_infected):
        people = []
        vaccinated = int(self.pop_size * self.vacc_percentage)
        unaffected = self.pop_size - vaccinated - initial_infected

        for i in range(vaccinated):
            people.append(Person(i + 1, True, None))
        
        for i in range(initial_infected):
            self.total_infected += 1
            people.append(Person(1 + len(people), False, self.virus))

        for i in range(unaffected):
            people.append(Person(1 + len(people), False, None))

        random.shuffle(people)

        return people 


    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        # TODO: Complete this helper method.  Returns a Boolean.
        should_continue = True

        if self.pop_size == self.total_vaccinated + self.total_dead:
            should_continue = False 

        if self.total_infected == 0:
            should_continue = False 
        
        return should_continue

    def run(self):
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.repro_rate, self.initial_infected)
        time_step_counter = 0

        while self._simulation_should_continue():
            self.time_step(time_step_counter)
            time_step_counter += 1
        
        print(f'The simulation ran for {time_step_counter} steps. To see a summary of the steps, run:\n grep "Step [0-9]" answers.txt -A 5 ')
        total_living = self.pop_size - self.total_dead
        self.logger.log_summary(total_living, self.total_dead, self.total_vaccinated, self.num_interactions, self.vaccine_interactions, self.death_interactions)

    def time_step(self, time_step_counter):
        # TODO: Finish this method.
        deaths = 0
        # TODO: Finish this method.
        for person in self.population:
            if person.infection:
                for interaction in range(100):
                    random_person = random.choice(self.population)
                    while not random_person.is_alive or random_person._id == person._id:
                        random_person = random.choice(self.population)
                    self.interaction(person, random_person)
                    self.num_interactions += 1
                if person.did_survive_infection():
                    self.total_vaccinated += 1
                    self.vaccine_interactions += 1
                    self.total_infected -= 1
                    self.logger.log_infection_survival(person, True)
                else:
                    self.dead_population.append(person)
                    self.total_dead += 1
                    self.total_infected -= 1
                    deaths += 1
                    self.logger.log_infection_survival(person, False)
        
        self.death_interactions += deaths
        # print('total vaccinated:', self.total_vaccinated)
        # print('total dead:', self.total_dead)
        # print('total infected:', self.total_infected)
        # print(len(self.population) == self.total_vaccinated + self.total_dead)
        total_living = self.pop_size - self.total_dead
        self.logger.log_time_step(time_step_counter, len(self.newly_infected), deaths, total_living, self.total_vaccinated, self.total_dead)
        self._infect_newly_infected()

    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True
        if random_person.is_vaccinated == False and random_person.infection == None:
            if random.uniform(0,1) < person.infection.repro_rate:  
                if random_person._id not in self.newly_infected:
                    self.newly_infected.append(random_person._id)
                    self.total_infected += 1
        elif random_person.infection != None or random_person.is_vaccinated == True:
            pass 

    def _infect_newly_infected(self):
        for person in self.population:
            if person._id == id:
                person.infection = self.virus
        self.newly_infected = []

if __name__ == "__main__":
    params = sys.argv[1:]
    name = str(params[2])
    repro_rate = float(params[1])
    mortality_rate = float(params[3])

    pop_size = int(params[0])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    virus = Virus(name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    sim.run()


# python3 simulation.py "Ebola" 0.5 0.5 80 0 1