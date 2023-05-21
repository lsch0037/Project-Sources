import random
import math

from perlin_noise import PerlinNoise

id_map = {
    "Air":0,
    "Stone": 1,
    "Grass Block":2,
    "Dirt":3,
    "Cobblestone":4,
    "Oak Planks":5,
    "Water":9,
    "Lava":11,
    "Gravel":13,
    "Gold Ore":14,
    "Iron Ore":15,
    "Coal Ore":16,
    "Oak Wood" : 17,
    "Oak Leaves" : 18,
    "Glass":20,
    "Gold Block":41,
    "Bricks":45,
    "Obsidian":49,
    "Diamond Ore":56,
    "Diamond Block": 57,
    "Stone Bricks":98,
    "Emerald Block":133,
    "Redstone Block":152,
    "Block of Coal":173
}

class material():
    def __init__(self, materials):
        self.ids = []

        for id in materials:
            self.ids.append(id_map[id])


    def get(self,pos) -> None:
        pass

class random_material(material):
    def __init__(self, ids, weights=None):
        super().__init__(ids)

        if weights == None:

            w = 1.0 / len(ids)
            self.weights = [w for i in range(len(ids))]
        else:
            if not len(weights) == len(ids):
                raise ValueError("Arrays 'Ids' and 'Weights' must be of the same lenght: {l1}, {l2}".format(l1=len(ids),l2=len(weights)))

            self.weights = weights


    def get(self,pos):
        return random.choices(self.ids, weights=self.weights, k=1)


class perlin_material(material):
    def __init__(self, ids, thresholds, seed, octaves):
        super().__init__(ids)
        self.noise = PerlinNoise(octaves=octaves,seed=seed)
        self.thresholds = thresholds
        self.seed = seed

    def get(self,pos):
        # Scaling coordinates to be between 0 and 1
        print("Pos:{}".format(pos))
        pos_scaled = [math.log(abs(pos[0]+1))/5,math.log(abs(pos[1]+1))/5,math.log(abs(pos[2]+1))/5]

        # Calculate perlin noise and scale to be between 0.0 and 1.0
        noise_pure = self.noise.noise(pos_scaled)
        print("Raw Noise:{}".format(noise_pure))
        noise_val = (noise_pure + 1)/2

        if noise_val > 1.0:
            raise ValueError("Perlin noise value greater than 1.0: {}".format(noise_val))
        
        bracket = 0

        for i in range(len(self.thresholds)):
            if self.thresholds[i] > noise_val:
                bracket = i
                break

        print("Pos Scaled:{p}, Noise: {n} -> Id:{id} ".format(p=pos_scaled, n=noise_val,id=self.ids[bracket]))

        return self.ids[bracket]