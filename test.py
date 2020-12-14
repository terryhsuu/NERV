class Equus:
    def __init__(self, is_male):
        pass
    def run(self):
        print(f'I run at speed {self.speed}')
        print(f'I\'m {self.gender}')
    
    def roar(self):
        print('Equus roars')
class Horse(Equus):
    def __init__(self, is_male):
        print('Horse init')
        self.speed = 30
        self.gender = 'male' if is_male else 'female'
        self.is_horse = True
    def roar(self):
        print('Horse: Hee haw~')
        super().roar()
class Donkey(Equus):
    def __init__(self, is_male):
        print('Donkey init')
        self.speed = 20
        self.is_donkey = True
    def roar(self):
        print('Donkey: Hee haw hee hee haw~')
        super().roar()
class Mule(Horse, Donkey):
    def __init__(self, is_male):
        print('Mule init')
        super().__init__(is_male)
    
    def roar(self):
        print('Mule: Muuuuleee~~~')
        super().roar()

mule = Mule(is_male=True)
mule.roar()
