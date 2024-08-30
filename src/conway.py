import numpy as np


class Conway:

    def __init__(self, rows, cols):
        self.generation = 0
        self.rows = rows
        self.cols = cols
        self.data = np.zeros((rows, cols))
        self.running = False

    def get_generation(self):
        return self.data

    def next_generation(self):
        self.generation += 1

        new_grid = self.data.copy()

        for y in range(len(self.data)):
            for x in range(len(self.data[y])):  
                total = 0
                for yy in (max(0,y-1),y,min(self.rows-1,y+1)):
                    for xx in (max(0, x-1),x,min(self.cols-1,x+1)):
                        total += self.data[yy][xx]
                total -= self.data[y][x]

                # total = sum(self.data[yy][xx] for yy in (max(0,y-1),y,min(self.rows-1,y+1)) for xx in (max(0, x-1),x,min(self.cols-1,x+1))) - self.data[y][x]


                if self.data[y][x] == 1 and (total < 2 or total > 3):
                    new_grid[y][x] = 0

                elif self.data[y][x] == 0 and total == 3:
                    new_grid[y][x] = 1

        self.data = new_grid

    def load_from_csv(self, file_path):
        self.data = np.zeros((self.rows, self.cols))
        with open(file_path, "r") as file:
            for y, row in enumerate(file.readlines()[:self.rows]):
                for x, cell in enumerate(row.split(",")[:self.cols]):
                    self.data[y][x] = int(cell)

if __name__ == "__main__":
    c = Conway(50, 75)
    c.load_from_csv("src/example.csv")
    print(c.data)


