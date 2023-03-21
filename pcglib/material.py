import random
from perlin_noise import PerlinNoise

class material():
    def __init__(self, ids, selector='rand', weights=None, seed=random.randint(1000,1000), octaves=random.randint(0,24)):
        selector_types = ['rand','weighted','perlin']

        if selector not in selector_types:
            raise ValueError("Invalid selector {s}, expected one of :{t}".format(s=selector, t=selector_types))
        
        self.f = selector
        self.ids = ids

        if selector == 'rand':
            pass

        elif selector == 'weighted':
            self.weigths = weights

        elif selector == 'perlin':
            self.weigths = weights
            self.seed = seed
            self.noise = PerlinNoise(octaves=octaves,seed=seed)

    def get(self,*args):
        if self.f == 'rand':
            return random.choice(self.ids)

        elif self.f == 'weighted':
            return random.choices(self.ids, weights=self.weigths, k=1)
        
        elif self.f == 'perlin':
            pos = args[0]

            # Scaling coordinates to be between 0 and 1
            pos_scaled = [(pos[0]/100.0)%1.0,(pos[1]/100.0)%1.0,(pos[2]/100.0)%1.0]

    	    # Calculate perlin noise and scale to be between 0.0 and 1.0
            noise_val = (self.noise.noise(pos_scaled) + 1)/2
            print("Pos {p}, Noise: {n} ".format(p=pos, n=noise_val))

            # Cumulative threshold
            thresholds = []
            cumultative_sum=0
            for i in range(len(self.weigths)):
                cumultative_sum+=self.weigths[i]
                thresholds.append(cumultative_sum)
            
            print("Thresholds: {t}".format(t=thresholds))

            bracket = 0
            for i in range(len(self.ids)):
                if thresholds[i] > noise_val:
                    bracket = i
                    break

            return self.ids[bracket]