import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# imports .env
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

OWNER_ROLE = "Owner"


@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")


@bot.event
async def on_message(message):
    # this keeps from replying to own message to avoid infinite loops
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - do not use profanity words.")

    # this await makes sure all other things keep doing what they need to do
    await bot.process_commands(message)


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")


@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to a message")


@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)

    await poll_message.add_reaction("❤")
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("😂")


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=OWNER_ROLE)

    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {OWNER_ROLE}.")
    else:
        await ctx.send("Role doesn't exist.")


@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=OWNER_ROLE)

    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has been removed from {OWNER_ROLE}.")
    else:
        await ctx.send("Role doesn't exist.")


@bot.command()
@commands.has_role(OWNER_ROLE)
async def secret(ctx):
    await ctx.send("Welcome to the owner club!")


@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")
    else:
        await ctx.send("An error took place trying to make this call.")

# Always last, this tells bot to run
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
