import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and     should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        self.logger = Logger('answers.txt')
        self.pop_size = pop_size # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.vacc_percentage = float(vacc_percentage) # float between 0 and 1
        self.total_vaccinated = 0
        self.total_infected = 0 # Int
        self.total_dead = 0 # Int
        self.population = [] # List of Person objects
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, pop_size, vacc_percentage, initial_infected)
        self.newly_infected = []
        self.dead_population = [] # tip
        self.num_interactions = 0
        self.vaccine_interactions = 0
        self.death_interactions = 0

    def _create_population(self):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        people = []
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.
        vaccinated = int(self.pop_size * self.vacc_percentage)

        #infected
        for id in range(self.initial_infected):
            self.population.append(Person(id, False, self.virus))

        #vaccinated
        for id in range(vaccinated):
            self.population.append(Person(id, True))

        #not-vaccinated
        for id in range(self.pop_size - (vaccinated+self.initial_infected)):
            self.population.append(Person(id, False))

        return self.population

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
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate, self.initial_infected)
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper
        time_step_counter = 0

        while self._simulation_should_continue():
            self.time_step(time_step_counter)
            time_step_counter += 1
        
        print(f'The simulation ran for {time_step_counter} steps. To see a summary of the steps, run:\n grep "Step [0-9]" answers.txt -A 5 ')
        total_living = self.pop_size - self.total_dead
        self.logger.log_summary(total_living, self.total_dead, self.total_vaccinated, self.num_interactions, self.vaccine_interactions, self.death_interactions)

    def time_step(self, time_step_counter):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
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
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call slogger method during this method.
        if random_person.is_vaccinated == False and random_person.infection == None:
            if random.uniform(0,1) < person.infection.repro_rate:  
                if random_person._id not in self.newly_infected:
                    self.newly_infected.append(random_person._id)
                    self.total_infected += 1
        elif random_person.infection != None or random_person.is_vaccinated == True:
            pass 

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        for id in self.newly_infected:
            for person in self.population:
                if person._id == id:
                    person.infection = self.virus
        self.newly_infected = []
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.

if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name, repro_rate, mortality_rate = str(params[0]), float(params[1]), float(params[2])

    pop_size, vacc_percentage, initial_infected = int(params[3]), float(params[4]), float(params[5])

    virus = Virus(virus_name, repro_rate, mortality_rate)

    sim = Simulation(pop_size, vacc_percentage, initial_infected)

    sim.run()

# python3 simulation.py "Ebola" 0.5 0.5 80 0 1