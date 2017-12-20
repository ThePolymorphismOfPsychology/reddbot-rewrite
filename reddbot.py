rbversion = "rewrite-0.0.1 Auspicious Anteater"
global client
import random
import sys
try:
  import discord
except ImportError:
  print("Sorry, but Discord.PY needs to be installed to run ReddBot.")
  sys.exit(1)
import asyncio
client = discord.Client()
try:
  from tinydb import TinyDB, operations, Query
except ImportError:
  print("Sorry, but TinyDB needs to be installed to run ReddBot.")
  sys.exit(1)
global db
global prefixtable
global profiletable
global queryer
queryer = Query()
db = TinyDB("C:\ReddBot\data.json")
#prefix db
prefixtable = db.table("prefixes")
#botowner stuff
global botowner 
botowner = ""
import redutil
@client.event
async def on_ready():
    botowner = (await client.application_info()).owner
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Bot Owner is ' + botowner.name + "#" + botowner.discriminator)
    print('------')
    await client.change_presence(game=(discord.Game(name="'rb!help' for help.")),status=discord.Status.online)
    await client.send_message(botowner,"ReddBot has started up. :smile:")
@client.event
async def on_server_join(serv):
    #message owner an embed displaying new server
    print("***JOINED NEW SERVER*** " + serv.name)
    #create default serverside prefix
    prefixtable.insert({"sid": serv.id,"serverprefix": "rb!"})
    #create role lists
    tmptbl = db.table(serv.id + "_perms")
    for rolea in serv.Roles:
        tmptbl.insert({"rid": rolea.id,"admin": "false","disable_botuse": "false"})
    em = discord.Embed(title='Joined Server',description=serv.name)
    if len(serv.icon_url) != 0:
        em.set_image(url=serv.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message(botowner,embed=em)

@client.event
async def on_server_update(servbef,servaf):
    #message owner an embed displaying updated
    print("***SERVER CHANGED*** " + servbef.name + "... Name after change: " + servaf.name)
    em = discord.Embed(title='Server Changed',description="Before: " + servbef.name +"\nAfter: " + servaf.name)
    if len(servaf.icon_url) != 0:
        em.set_image(url=servaf.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message(botowner,embed=em)

@client.event
async def on_server_remove(serv):
    #message owner an embed displaying removed server
    print("***SERVER REMOVED*** " + serv.name)
    #cleanup serverside prefixes
    prefixtable.remove(queryer.sid == serv.id)
    #cleanup serverside permissions
    db.purge_table(serv.id + "_perms")
    em = discord.Embed(title='Server Removed',description=serv.name)
    if len(serv.icon_url) != 0:
        em.set_image(url=serv.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message(botowner,embed=em)

@client.event
async def on_error(eve,*args,**kwargs):
    await client.send_message(botowner,"ReddBot Error: ```Caused By: " + str(eve) + "```")
    strtosend = ""
    for agg in sys.exc_info():
        strtosend = strtosend + str(agg) + "\n"
    await client.send_message(botowner,"```" + strtosend + "```")
@client.event
async def on_message(message):
    prefix = ""
    if message.channel.is_private is True:
        prefix = "rb!"
    elif message.channel.is_private is False:
        prefixobj = prefixtable.get(queryer.sid == message.server.id)
        if prefixobj is None:
            prefixtable.insert({"sid": serv.id,"serverprefix": "rb!"})
        prefix = prefixobj['serverprefix']
    if message.content.startswith(prefix + 'test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    #set prefix for server (default is 'rb!')
    elif message.content.startswith(prefix + 'setprefix'):
        if redutil.isAdmin(message) is True:
            args = redutil.getargs(message)
            if redutil.isprivchan(message) is True:
                await client.send_message(message.channel,"**You cannot set a prefix for dms**")
            else:
                if redutil.argcount(args) == 0:
                    prefixtable.update(operations.set("serverprefix","rb!"),queryer.sid == message.server.id)
                    memsg = await client.send_message(message.channel,"**PREFIX SET TO: ** ```rb!```")
                    await asyncio.sleep(5)
                    await client.delete_message(memsg)
                else:
                    prefixtable.update(operations.set("serverprefix",redutil.rjoin(args).replace("\r","").replace("\n","").replace(" ","")),queryer.sid == message.server.id)
                    memsg = await client.send_message(message.channel,"**PREFIX SET TO: **```" + redutil.rjoin(args).replace("\r","").replace("\n","").replace(" ","") + "```")
                    await asyncio.sleep(5)
                    await client.delete_message(memsg)
        else:
            memsg = await client.send_message(message.channel,"**Sorry, " + message.author.mention + "!** You don't have proper permissions.")
            await asyncio.sleep(5)
            await client.delete_message(memsg)
    #show prefix
    elif message.content.startswith(prefix + "defprefix"):
        if redutil.isprivchan(message) is True:
            await client.send_message(message.channel,"**Prefix: **```rb!```")
        else:
            mypref = prefixtable.get(queryer.sid == message.server.id)
            if mypref is None:
                prefixtable.insert({"sid": message.server.id,"serverprefix": "rb!"})
                await client.send_message(message.channel,"**Recovery Complete. Default prefix set.**")
            else:
                await client.send_message(message.channel,"**Prefix: **```" + mypref['serverprefix'] + "```")
client.run("")