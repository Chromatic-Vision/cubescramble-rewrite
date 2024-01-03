import random
import discord
import common
import logger

from assets.puzzles.abstract_puzzle_solver import AbstractPuzzleSolver, AbstractPuzzleEmulator
from assets.puzzles.clock.puzzle import Clock

intents = discord.Intents.all()
client = discord.Client(intents=intents)

logger = logger.Logger(True,
                       True,
                       "$color[$info]$reset $timecolor[%H:%M:%S.%f]$reset $message $tracecolor($filename/$funcname:$line)$reset")
logger.reset_log()

# ----------------------------------------------------------------------------------------------------------------------

try:
    with open("token.txt", "r", encoding="utf-8") as f:
        token = f.read()
        f.close()
except Exception as e:

    logger.error(repr(e))
    logger.error("Token could not be read. Please provide a valid token inside token.txt.")
    raise SystemExit

# ----------------------------------------------------------------------------------------------------------------------

class Bot:

    def __init__(self):
        self.prefix = "<"
        self.description_filename = "description.txt"
        self.clock = Clock()
        self.emulator: AbstractPuzzleEmulator = self.clock.emulator
        self.solver: AbstractPuzzleSolver = self.clock.solver


    async def process_message(self, raw: discord.Message):

        message: str = raw.content

        if not message.startswith(self.prefix) or raw.author.bot:
            return

        logger.log(f"{raw.author.name} issued the following command: {message}")

        command = message[self.prefix.__len__():]
        base = command.split(" ")[0]
        branch = command.split(" ", 1)[1] if command.split().__len__() >= 2 else None
        branches = branch.split(" ") if branch is not None else [""]

        if base.lower() == "help":

            embed_data = {
                "title": "Cubescramble bot help menu",
                "description": "Commands:",
                "footer": {
                    "text": f"Executed by {raw.author}",
                    "icon_url": raw.author.avatar.url if raw.author.avatar is not None else None
                },
                "fields": [
                    {
                        "name": f"{self.prefix}help",
                        "value": "Displays a help menu.",
                        "inline": True
                    },
                    {
                        "name": f"{self.prefix}solve [scramble: str]",
                        "value": "Returns optimal solution(s) using Tommy 7-simul.",
                        "inline": False
                    }
                ]
            }

            embed = await common.create_embed(embed_data)
            await raw.reply(embed=embed)

        elif base.lower() == "scrambles":

            res = ""

            for i in range(20):
                res += str(i) + " " + self.clock.scrambler.get_random_scramble() + "\n"

            await raw.reply(res)

        elif base.lower() == "optclock" or base.lower() == "solve":

            scramble = str(branch)

            self.emulator.reset()
            self.emulator.convert_scramble(scramble)

            optimal_solutions = self.solver.solve(self.emulator) # solve() returns (int, list[str]), which str is solution

            fields = []

            for i, solution in enumerate(optimal_solutions[1]):

                print(solution)

                lr = solution.split("\n")[0]
                ud = solution.split("\n")[1]

                fields.append(
                    {
                        "name": f"{lr}",
                        "value": f"{ud}",
                        "inline": bool(i % 2)
                    })

            embed_data = {
                "title": "Optimal solutions",
                "description": f"Scramble: {scramble}\n\n"
                               f"Following solution{'s' if optimal_solutions[1].__len__() > 1 else ''} "
                               f"with {optimal_solutions[0]} ticks {'are' if optimal_solutions[1].__len__() > 1 else 'is'} optimal:",
                "footer": {
                    "text": f"Executed by {raw.author}",
                    "icon_url": raw.author.avatar.url if raw.author.avatar is not None else None
                },
                "fields": fields
            }

            embed = await common.create_embed(embed_data)

            await raw.reply(embed=embed)

bot = Bot()

@client.event
async def on_ready():

    logger.log("Successfully initialized " + client.user.name)

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='Clock'))

@client.event
async def on_message(raw):
    await bot.process_message(raw)


client.run(token)