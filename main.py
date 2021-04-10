import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import os
import tokens as t


def get_prefix(Client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

Client = commands.Bot(command_prefix = get_prefix)

@Client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(Client))

@Client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = 'i!'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    with open('channels.json', 'r') as f:
        channels = json.load(f)
    channels[str(guild.id)] = str(guild.id)
    with open('channels.json', 'w') as f:
        json.dump(channels, f, indent=4)

@Client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    with open('channels.json', 'r') as f:
        channels = json.load(f)
    channels.pop(str(guild.id))
    with open('channels.json', 'w') as f:
        json.dump(channels, f, indent=4)

@Client.command()
@has_permissions(manage_guild=True)
async def prefix(ctx, arg):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = arg
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.channel.send('Prefix = \'' + arg + '\'')

@Client.command()
@has_permissions(manage_guild=True)
async def inform(ctx):
    info = str.replace(ctx.message.content, get_prefix(Client, ctx) + 'inform ', '')
    embedVar = discord.Embed(title="Info", description=info, color=0xEADE48)
    with open('channels.json', 'r') as f:
        channels = json.load(f)
    ch = ctx.channel
    for c in ctx.guild.channels:
        if c.name == channels[str(ctx.guild.id)]:
            print('hi')
            ch = Client.get_channel(c.id)
    await ch.send("<@everyone>")
    await ch.send(embed=embedVar)


@Client.command()
@has_permissions(manage_guild=True)
async def channel(ctx, arg):
    with open('channels.json', 'r') as f:
        channels = json.load(f)
    channels[str(ctx.guild.id)] = arg
    with open('channels.json', 'w') as f:
        json.dump(channels, f, indent=4)
    await ctx.channel.send('Update Channel = \'' + arg + '\'')

@Client.command()
@has_permissions(manage_guild=True)
async def cmds(ctx):
    embedVar = discord.Embed(title="Help", description="", color=0xEADE48)
    embedVar.add_field(name=get_prefix(Client, ctx) + "cmds", value="Shows this list", inline=False)
    embedVar.add_field(name=get_prefix(Client, ctx) + "prefix {new prefix}", value="Changes the prefix", inline=False)
    embedVar.add_field(name=get_prefix(Client, ctx) + "channel {new channel}" , value="Sets the info channel", inline=False)
    await ctx.channel.send(embed=embedVar)

Client.run(t.token)