import random

class Game:
    def __init__(self, size):
        self.size = size
        self.player = [random.randint(0, size-1), random.randint(0, size-1)]
        self.enemy = [random.randint(0, size-1), random.randint(0, size-1)]

    def move_player(self, direction):
        if direction == 'up' and self.player[1] > 0:
            self.player[1] -= 1
        elif direction == 'down' and self.player[1] < self.size - 1:
            self.player[1] += 1
        elif direction == 'left' and self.player[0] > 0:
            self.player[0] -= 1
        elif direction == 'right' and self.player[0] < self.size - 1:
            self.player[0] += 1

        self.move_enemy()

    def move_enemy(self):
        if self.player[0] < self.enemy[0]:
            self.enemy[0] -= 1
        elif self.player[0] > self.enemy[0]:
            self.enemy[0] += 1

        if self.player[1] < self.enemy[1]:
            self.enemy[1] -= 1
        elif self.player[1] > self.enemy[1]:
            self.enemy[1] += 1

    def render(self):
        for y in range(self.size):
            for x in range(self.size):
                if [x, y] == self.player:
                    print('P', end=' ')
                elif [x, y] == self.enemy:
                    print('E', end=' ')
                else:
                    print('.', end=' ')
            print()

# Example usage
game = Game(5)
game.render()

while True:
    direction = input("Enter direction (up/down/left/right): ")
    game.move_player(direction)
    game.render()
