import os
import random
import discord
from discord import Interaction
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('Token.env')
TOKEN = os.getenv('TOKEN')
USER = os.getenv('USER')    

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# Game Constants
GRID_SIZE = 11  # 0 < GRID_SIZE < 12 Size of the grid
START_POSITION = (int(GRID_SIZE/2), int(GRID_SIZE/2))  # Starting position of the player


# Food class representing foods location
class Food:
    def __init__(self):
        # Spawn food in random location on grid
        self.position = (random.randint(0,(GRID_SIZE-1)), random.randint(0,(GRID_SIZE-1)))


# Initialize food
food = Food()


# Enemy class representing foods location
class Enemy:
    def __init__(self):
        self.position = (random.randint(0, (GRID_SIZE - 1)), random.randint(0, (GRID_SIZE - 1)))

    def move_enemy(self):
        # 50/50 chance if bot moves towards player
        if random.randint(0,1) == 1:
            if player.position[0] < self.position[0]:
                self.position = (self.position[0] - 1, self.position[1])
            elif player.position[0] > self.position[0]:
                self.position = (self.position[0] + 1, self.position[1])
            if player.position[1] < self.position[1]:
                self.position = (self.position[0], self.position[1] - 1)
            elif player.position[1] > self.position[1]:
                self.position = (self.position[0], self.position[1]+1)


# Initialize food
enemy = Enemy()


# Player class representing the player's character
class Player:
    def __init__(self):
        self.position = START_POSITION
        self.score = 0

    def player_connect(self):
        if food.position == self.position:
            self.score += 1
            food.position = (random.randint(0,(GRID_SIZE-1),) , random.randint(0,(GRID_SIZE-1),))  # Respawn food
        if enemy.position == self.position:
            self.score -= 1
            enemy.position = (random.randint(0,(GRID_SIZE-1),), random.randint(0,(GRID_SIZE-1),))  # Respawn enemy

    def move_up(self):
        if self.position[1] < 0:
            self.position = (self.position[0], GRID_SIZE - 1)
        else:
            self.position = (self.position[0], self.position[1] - 1)
        enemy.move_enemy()
        self.player_connect()

    def move_down(self):
        if self.position[1] > GRID_SIZE-2:
            self.position = (self.position[0], 0)
        else:
            self.position = (self.position[0], self.position[1] + 1)
        enemy.move_enemy()
        self.player_connect()


    def move_left(self):
        if self.position[0] < 0:
            self.position = (GRID_SIZE - 2, self.position[1])
        else:
            self.position = (self.position[0] - 1, self.position[1])
        enemy.move_enemy()
        self.player_connect()

    def move_right(self):
        if self.position[0] > GRID_SIZE - 2:
            self.position = (0, self.position[1])
        else:
            self.position = (self.position[0] + 1, self.position[1])
        enemy.move_enemy()
        self.player_connect()


# Initialize the player
player = Player()


# Game View with directional buttons
class GameView(View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    @discord.ui.button(style=discord.ButtonStyle.green, emoji='⬆️', row=0)
    async def up_button(self, interaction, button):
        player.move_up()
        await interaction.response.edit_message(content=render_game())

    @discord.ui.button(style=discord.ButtonStyle.green, emoji='⬇️', row=0)
    async def down_button(self, interaction, button):
        player.move_down()
        await interaction.response.edit_message(content=render_game())

    @discord.ui.button(style=discord.ButtonStyle.green, emoji='⬅️', row=1)
    async def left_button(self, interaction, button):
        player.move_left()
        await interaction.response.edit_message(content=render_game())

    @discord.ui.button(style=discord.ButtonStyle.green, emoji='➡️', row=1)
    async def right_button(self, interaction, button):
        player.move_right()
        await interaction.response.edit_message(content=render_game())

    # interaction check (make sure user is correct person)
    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You need to start your own game sorry!", ephemeral=True)
            return False
        else:
            return True


# Function to render the game grid
def render_game():
    player_image = ':deer:'
    enemy_image = ':person_fencing:'
    food_image = ':hamburger:'
    ground_image = ':green_square:'

    grid = [[ground_image for i in range(GRID_SIZE)] for i in range(GRID_SIZE)]  # create grid with white plots
    # assign objects x and y locations
    player_x, player_y = player.position
    enemy_x, enemy_y = enemy.position
    food_x, food_y = food.position

    # Set the objects position in the grid
    grid[food_y][food_x] = food_image
    grid[enemy_y][enemy_x] = enemy_image
    grid[player_y][player_x] = player_image

    # Convert the grid to a string
    rendered_grid = ''
    for row in grid:
        rendered_grid += ''.join(row) + '\n'

    return f'{rendered_grid} Score: {player.score}'


# Command to start the game
@client.command()
async def game(ctx):
    view = GameView(ctx)
    await ctx.send(content=render_game(), view=view)
    print("Playing game! | Rob-Bot")


# bot is officially logged in
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    print("==================================")


# text interaction
@client.event
async def on_message(message):
    if message.author != client.user:
        print(f'{message.content} | {message.author.name} | {message.channel.name}') # log user message
    if message.author.name == USER:
        # Add a thumbs-down reaction to users messagethe message
        emoji = '👎'
        await message.add_reaction(emoji)

    await client.process_commands(message)

# runs bot
if __name__ == "__main__":
    if TOKEN is None:
        raise ValueError("TOKEN is not set in the Token.env file")
    client.run(TOKEN)