class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name
    
    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, repro_rate, initial_infected):

        f = open(self.file_name, 'w')
        f.write(f'********HERD IMMUNITY SIMULATION********')
        f.write('\n')
        f.write(f'Population Size: {pop_size}\n Initially Vaccinated: {vacc_percentage * 100}%\n Initially Infected: {initial_infected}\n Virus: {virus_name}\n Mortality Rate: {mortality_rate}\n Reproductive Rate: {repro_rate}\n')
        f.write(f'Simulation loading...')
        f.close() 

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        f = open(self.file_name, 'a')
        if random_person_sick:
            f.write(f'{person._id} did not infect {random_person._id} because they are already sick.\n')
        elif random_person_vacc:
            f.write(f'{person._id} did not infect {random_person._id} because they are vaccinated against the virus.\n')
        else:
            f.write(f'{person._id} infected {random_person._id}\n')
        f.close()

    def log_infection_survival(self, person, survived_infection):
        f = open(self.file_name, 'a')

        if survived_infection:
            f.write(f'{person._id} survived! \n')
        else: 
            f.write(f'{person._id} died. \n')
        f.close()

    def log_summary(self, total_living, total_dead, total_vaccinated, number_interactions, vaccine_interactions, death_interactions):
        f = open(self.file_name, 'a')
        f.write('\n')
        f.write(f'~ Summary of Simulation ~ \n')
        f.write(f'Total living: {total_living}\n')
        f.write(f'Total dead: {total_dead}\n')
        f.write(f'Total of vaccinations: {total_vaccinated}\n')
        f.write(f'Total number of interactions: {number_interactions}\n')
        f.write(f'Number vaccinations after interacting: {vaccine_interactions}\n')
        f.write(f'Number deaths after interacting: {death_interactions}\n')
        f.close()
        
