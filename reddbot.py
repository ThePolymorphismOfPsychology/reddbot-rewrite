rbversion = "rewrite-0.0.1 Auspicious Anteater"
import random
import sys
try:
  import discord
except Import Error:
  print("Sorry, but Discord.PY needs to be installed to run ReddBot.")
  sys.exit(1)
import asyncio
client = discord.Client()
try:
  from tinydb import TinyDB, operations, Query
except ImportError:
  print("Sorry, but TinyDB needs to be installed to run ReddBot.")
  sys.exit(1)
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Bot Owner is ' + (await client.application_info()).owner.name + "#" + (await client.application_info()).owner.discriminator)
    print('------')
    await client.change_presence(game=(discord.Game(name="'rb!help' for help.")),status=discord.Status.online)
    await client.send_message((await client.application_info()).owner,"ReddBot has started up. :smile:")
@client.event
async def on_server_join(serv):
    #message owner an embed displaying new server
    print("***JOINED NEW SERVER*** " + serv.name)
    em = discord.Embed(title='Joined Server',description=serv.name)
    if len(serv.icon_url) != 0:
        em.set_image(url=serv.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message((await client.application_info()).owner,embed=em)

@client.event
async def on_server_update(servbef,servaf):
    #message owner an embed displaying updated
    print("***SERVER CHANGED*** " + servbef.name + "... Name after change: " + servaf.name)
    em = discord.Embed(title='Server Changed',description="Before: " + servbef.name +"\nAfter: " + servaf.name)
    if len(serv.icon_url) != 0:
        em.set_image(url=servaf.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message((await client.application_info()).owner,embed=em)

@client.event
async def on_server_remove(serv):
    #message owner an embed displaying removed server
    print("***SERVER REMOVED*** " + serv.name)
    em = discord.Embed(title='Server Removed',description=serv.name)
    if len(serv.icon_url) != 0:
        em.set_image(url=serv.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message((await client.application_info()).owner,embed=em)

@client.event
async def on_error(eve,*args,**kwargs):
    await client.send_message((await client.application_info()).owner,"ReddBot Error: ```Caused By: " + str(eve) + "```")
    strtosend = ""
    for agg in sys.exc_info():
        strtosend = strtosend + str(agg) + "\n"
    await client.send_message((await client.application_info()).owner,"```" + strtosend + "```")

@client.event
async def on_message(message):
    if message.content.startswith('rb!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
client.run("[insert token here]")