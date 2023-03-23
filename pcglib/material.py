import random
from perlin_noise import PerlinNoise

id_map = {
    "Air":0,
    "Stone": 1,
    "Grass Block":2,
    "Dirt":3,
    "Cobblestone":4,
    "Oak Planks":5,
    "Water":9,
    "Gold Ore":14,
    "Iron Ore":15,
    "Coal Ore":16,
    "Oak Wood" : 17,
    "Oak Leaves" : 18,
    "Bricks":45,
    "Diamond Ore":56,
    "Diamond Block": 57,
    "Stone Bricks":98
}

class material():
    def __init__(self, materials):
        self.ids = []

        for id in materials:
            self.ids.append(id_map[id])

        print("Upon init ids:", self.ids)


    def get(self,pos) -> None:
        pass

class constant_material(material):
    def __init__(self, id):
        self.id = id_map[id]

    def get(self, pos):
        return self.id

class random_material(material):
    def __init__(self, ids):
        super().__init__(ids)

        w = 1.0/len(ids)

        self.weights = [w for i in range(len(ids))]

    def get(self,pos):
        return random.choices(self.ids, weights=self.weights, k=1)


class weighted_material(material):
    def __init__(self, ids, weights):
        super().__init__(ids)
        self.weights = weights

    def get(self,pos):
        return random.choices(self.ids, weights=self.weights, k=1)


class perlin_material(material):
    def __init__(self, ids, thresholds, seed=random.randint(100,10000), octaves=8):
        super().__init__(ids)
        self.noise = PerlinNoise(octaves=octaves,seed=seed)
        self.thresholds = thresholds
        self.seed = seed

    def get(self,pos):
        # Scaling coordinates to be between 0 and 1
        pos_scaled = [(pos[0]/100.0)%1.0,(pos[1]/100.0)%1.0,(pos[2]/100.0)%1.0]

        # Calculate perlin noise and scale to be between 0.0 and 1.0
        noise_val = (self.noise.noise(pos_scaled)+1.0)/2
        
        bracket = 0

        for i in range(len(self.thresholds)):
            if self.thresholds[i] > noise_val:
                bracket = i
                break

        # print("Pos Scaled:{p}, Noise: {n} -> Id:{id} ".format(p=pos_scaled, n=noise_val,id=self.ids[bracket]))

        return self.ids[bracket]