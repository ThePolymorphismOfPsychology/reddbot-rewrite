rbversion = "rewrite-0.0.5 Auspicious Anteater"
global client
import random
import sys
global foundoldrole
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
global queryer,db,prefixtable,botowner
queryer = Query()
db = TinyDB("C:\ReddBot\data.json")
#prefix db
prefixtable = db.table("prefixes")
#botowner stuff
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
    await client.send_message(botowner,client.user.name + " has started up. :smile:")
@client.event
async def on_server_join(serv):
    botowner = (await client.application_info()).owner
    #message owner an embed displaying new server
    print("***JOINED NEW SERVER*** " + serv.name)
    #create default serverside prefix
    prefixtable.insert({"sid": serv.id,"serverprefix": "rb!"})
    #create channel lists
    tmptbl = db.table(serv.id + "_chanperms")
    mygenchan = ""
    for chan in serv.channels:
        if chan.type is discord.ChannelType.text:
            tmptbl.insert({"cid": chan.id,"enabled":"true"})
            print("REGISTERED CHANNEL #" + chan.name)
            if chan.is_default is True:
                mygenchan = chan.id
    #create role lists
    tmptbl = db.table(serv.id + "_roleperms")
    for rolea in serv.roles:
        tmptbl.insert({"rid": rolea.id,"admin": "false","disable_botuse": "false"})
        print("REGISTERED ROLE @" + rolea.id)
    #register welcome message
    tmptbl = db.table("serverdata")
    #user.mention - replace with user mention
    #user.name - replace with user name
    #user.discrim - replace with user discriminator
    tmptbl.insert({"sid": serv.id, "welcomemessage": "hello, {user.mention}!","enabled":"false","cid": mygenchan,"dmMessage": "hello {user.name}#{user.discrim}","enableddm":"false","promoteladder":"[]"})
    print("Added data to global data table")
    em = discord.Embed(title='Joined Server',description=serv.name)
    if len(serv.icon_url) != 0:
        em.set_image(url=serv.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message(botowner,embed=em)

@client.event
async def on_channel_create(chan):
    if chan.is_private == False:
        tmptbl = db.table(chan.server.id + "_chanperms")
        tmptbl.insert({"cid": chan.id,"enabled":"true"})

@client.event
async def on_channel_delete(chan):
    if chan.is_private == False:
        tmptbl = db.table(chan.server.id + "_chanperms")
        tmptbl.remove(queryer.cid == chan.id)
    
@client.event
async def on_member_join(member):
    #send welcome message
    tmptbl = db.table("serverdata")
    az = tmptbl.get(queryer.sid == member.server.id)
    if az is None:
        print("**REGISTERED ORPHAN " + member.server.name + "**")
        tmptbl.insert({"sid": serv.id, "welcomemessage": "hello, {user.mention}!","enabled":"false","cid": mygenchan,"dmMessage": "hello {user.name}#{user.discrim}","enableddm":"false","promoteladder":"[]"})
    else:
        if az['enabled'] == "true":
            await client.send_message(discord.utils.get(member.server.channels, id=az['cid'], type=discord.ChannelType.text),az['welcomemessage'].replace("{user.mention}",member.mention).replace("{user.name}",member.name).replace("{user.discrim}",member.discriminator))
        if az['enableddm'] == "true":
            await asyncio.sleep(3)
            await client.send_message(member,az['dmMessage'].replace("{user.mention}",member.mention).replace("{user.name}",member.name).replace("{user.discrim}",member.discriminator))
    
@client.event
async def on_server_update(servbef,servaf):
    botowner = (await client.application_info()).owner
    #message owner an embed displaying updated
    print("***SERVER CHANGED*** " + servbef.name + "... Name after change: " + servaf.name)
    em = discord.Embed(title='Server Changed',description="Before: " + servbef.name +"\nAfter: " + servaf.name)
    if len(servaf.icon_url) != 0:
        em.set_image(url=servaf.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message(botowner,embed=em)
    
@client.event
async def on_server_role_create(role):
    tmptbl = db.table(role.server.id + "_roleperms")
    tmptbl.insert({"rid": role.id,"admin": "false","disable_botuse": "false"})

@client.event
async def on_server_role_remove(role):
    tmptbl = db.table(role.server.id + "_roleperms")
    tmptbl.remove(queryer.rid == role.id)
@client.event
async def on_server_remove(serv):
    botowner = (await client.application_info()).owner
    #message owner an embed displaying removed server
    print("***SERVER REMOVED*** " + serv.name)
    #cleanup serverside prefixes
    prefixtable.remove(queryer.sid == serv.id)
    #cleanup serverside permissions
    db.purge_table(serv.id + "_roleperms")
    db.purge_table(serv.id + "_chanperms")
    tmptbl = db.table("serverdata")
    tmptbl.remove(queryer.sid == serv.id)
    em = discord.Embed(title='Server Removed',description=serv.name)
    if len(serv.icon_url) != 0:
        em.set_image(url=serv.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message(botowner,embed=em)

@client.event
async def on_error(eve,*args,**kwargs):
    botowner = (await client.application_info()).owner
    if sys.exc_info()[0] is ImportError:
        await client.send_message(botowner,client.user.name + " has shutdown. :cry:")
        await asyncio.sleep(2)
        await client.logout()
        await asyncio.sleep(2)
        await client.close()
        await asyncio.sleep(2)
        db.close()
        await asyncio.sleep(2)
        raise Exception("Shutdown")
    elif sys.exc_info()[0] is discord.errors.Forbidden:
        print("403 forbidden")
        print(sys.exc_info()[2])
        return True
    await client.send_message(botowner,"ReddBot Error: ```Caused By: " + str(eve) + "```")
    strtosend = ""
    for agg in sys.exc_info():
        strtosend = strtosend + str(agg) + "\n"
    await client.send_message(botowner,"```" + strtosend + "```")
@client.event
async def on_message(message):
    #get botowner
    botowner = (await client.application_info()).owner
    prefix = ""
    #if the channel is a private message, then the prefix is default (rb!)
    if message.channel.is_private is True:
        prefix = "rb!"
    #if the channel is serverside, then the prefix is the server's.
    elif message.channel.is_private is False:
        prefixobj = prefixtable.get(queryer.sid == message.server.id)
        if prefixobj is None:
            prefixtable.insert({"sid": message.server.id,"serverprefix": "rb!"})
        prefix = prefixobj['serverprefix']
    if message.content.startswith(prefix + 'test'):
        if redutil.canUse(message,db) is True:
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    #change welcome/dm welcome message, enable or disable it
    elif message.content.startswith(prefix + 'welcomer'):
        if redutil.canUse(message,db) is True:
            if redutil.isAdmin(message,db) is True:
                tmptbl = db.table("serverdata")
                args = redutil.getargs(message)
                argcount = redutil.argcount(args)
                if argcount == 0:
                    await client.send_message(message.channel,"Invalid Syntax.")
                else:
                    if args[1] == "enable":
                        if argcount > 1:
                            if args[2] == "dm":
                                tmptbl.update(operations.set("enableddm","true"),queryer.sid == message.server.id)
                                await client.send_message(message.channel,"**Welcome DMs were enabled.**")
                            else:
                                tmptbl.update(operations.set("enabled","true"),queryer.sid == message.server.id)
                                await client.send_message(message.channel,"**Welcome Messages were enabled.**")
                        else:
                            tmptbl.update(operations.set("enabled","true"),queryer.sid == message.server.id)
                            await client.send_message(message.channel,"**Welcome Messages were enabled.**")
                    elif args[1] == "disable":
                        if argcount > 1:
                            if args[2] == "dm":
                                tmptbl.update(operations.set("enableddm","false"),queryer.sid == message.server.id)
                                await client.send_message(message.channel,"**Welcome DMs were enabled.**")
                            else:
                                tmptbl.update(operations.set("enabled","false"),queryer.sid == message.server.id)
                                await client.send_message(message.channel,"**Welcome Messages were enabled.**")
                        else:
                            tmptbl.update(operations.set("enabled","false"),queryer.sid == message.server.id)
                            await client.send_message(message.channel,"**Welcome Messages were enabled.**")
                    elif args[1] == "set":
                        if argcount > 2:
                            if args[2] == "dm":
                                tmptbl.update(operations.set("dmMessage", " ".join(args[3:])),queryer.sid == message.server.id)
                                await client.send_message(message.channel,"**The new welcome dm is set to**```" + " ".join(args[3:]) + "```")
                            elif args[2] == "channel":
                                if len(message.channel_mentions) > 1:
                                    await client.send_message(message.channel,"Invalid Syntax.")
                                elif len(message.channel_mentions) < 1:
                                    await client.send_message(message.channel,"Invalid Syntax.")
                                else:
                                    await client.send_message(message.channel,message.channel_mentions[0].name + " was set as the welcome channel.")
                                    tmptbl.update(operations.set("cid", message.channel_mentions[0].id),queryer.sid == message.server.id)
                            else:
                                tmptbl.update(operations.set("welcomemessage"," ".join(args[2:])),queryer.sid == message.server.id)
                                await client.send_message(message.channel,"**The new welcome message is set to**```" + " ".join(args[2:]) + "```")
                    elif args[1] == "view":
                        alex = tmptbl.get(queryer.sid == message.server.id)
                        await client.send_message(message.channel,"**The current welcome message is **```" + alex['welcomemessage'] + "```**The current DM message is **```" + alex['dmMessage'] + "```")
                    else:
                        await client.send_message(message.channel,"Invalid Syntax.")
            else:
                memsg = await client.send_message(message.channel,"**Sorry, " + message.author.mention + "!** You don't have proper permissions.")
                await asyncio.sleep(5)
                await client.delete_message(memsg)
    #set prefix for server (default is 'rb!')
    elif message.content.startswith(prefix + 'setprefix'):
        if redutil.canUse(message,db) is True:
            if redutil.isAdmin(message,db) is True:
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
        if redutil.canUse(message,db) is True:
            if redutil.isprivchan(message) is True:
                await client.send_message(message.channel,"**Prefix: **```rb!```")
            else:
                mypref = prefixtable.get(queryer.sid == message.server.id)
                if mypref is None:
                    prefixtable.insert({"sid": message.server.id,"serverprefix": "rb!"})
                    await client.send_message(message.channel,"**Recovery Complete. Default prefix set.**")
                else:
                    await client.send_message(message.channel,"**Prefix: **```" + mypref['serverprefix'] + "```")
#add bot administrator                    
    elif message.content.startswith(prefix + "addadmin"):
        if redutil.canUse(message,db) is True:
            if message.author == message.server.owner or message.author == (await client.application_info()).owner:
                tmptbl = db.table(message.server.id + "_roleperms")
                updstr = ""
                for re in message.role_mentions:
                    if re.is_everyone:
                        updstr = updstr + "**everyone** was not given Admin.\n"
                    else:
                        tmptbl.update(operations.set("admin","true"),queryer.rid == re.id)
                        updstr = updstr + "**" + re.name + "** was given Admin.\n"
                await client.send_message(message.channel,updstr)
#remove bot administrator                
    elif message.content.startswith(prefix + "deladmin"):
        if redutil.canUse(message,db) is True:
            if message.author == message.server.owner or message.author == (await client.application_info()).owner:
                tmptbl = db.table(message.server.id + "_roleperms")
                updstr = ""
                for re in message.role_mentions:
                    if re.is_everyone:
                        updstr = updstr + "**everyone** was unchanged.\n"
                    else:
                        tmptbl.update(operations.set("admin","false"), queryer.rid == re.id)
                        updstr = updstr + "**" + re.name + "** had Admin revoked.\n"
                if updstr == "":
                    await client.send_message("**The administrator list was unchanged.**")
                else:
                    await client.send_message(message.channel,updstr)
    elif message.content.startswith(prefix + "blacklist"):
        if redutil.canUse(message,db) is True:
            if message.author == message.server.owner or message.author == (await client.application_info()).owner:
                tmptbl = db.table(message.server.id + "_roleperms")
                updstr = ""
                args = redutil.getargs(message)
                if args[1] == "add":
                    for re in message.role_mentions:
                        if re.is_everyone:
                            updstr = updstr + "**everyone** was unchanged.\n"
                        else:
                            tmptbl.update(operations.set("disable_botuse","true"), queryer.rid == re.id)
                            updstr = updstr + "The role **" + re.name + "** was added to the blacklist.\n"
                    if updstr == "":
                        await client.send_message("**The blacklist was unchanged.**")
                    else:
                        await client.send_message(message.channel,updstr)
                elif args[1] == "remove":
                    for re in message.role_mentions:
                        if re.is_everyone:
                            updstr = updstr + "**everyone** was unchanged.\n"
                        else:
                            tmptbl.update(operations.set("disable_botuse","false"), queryer.rid == re.id)
                            updstr = updstr + "The role **" + re.name + "** was removed from the blacklist.\n"
                    if updstr == "":
                        await client.send_message("**The blacklist was unchanged.**")
                    else:
                        await client.send_message(message.channel,updstr)
    elif message.content.startswith(prefix + "testthis"):
        args = redutil.getargs(message)
        for i in args[1:]:
            print(i)
    #test permissions
    elif message.content.startswith(prefix + "whoami"):
        stra = ""
        tmptbl = db.table(message.server.id + "_roleperms")
        for role in message.author.roles:
            ax = tmptbl.get(queryer.rid == role.id)
            if ax is None:
                tmptbl.insert({"rid": role.id,"admin": "false","disable_botuse": "false"})
            else:
                stra = stra + "Role: " + role.name + "\nPermissions: A-" + ax['admin'] + " B-" + ax['disable_botuse'] + "\n"
        if redutil.canUse(message,db) is True:
            astra = stra + "**YOU ARE NOT BLACKLISTRED**\n"
        else:
            stra = stra + "**YOU ARE BLACKLISTED****\n"
        if redutil.isAdmin(message,db) is True:
            stra = stra + "**YOU ARE AN ADMIN**\n"
        else:
            stra = stra + "**YOU ARE NOT AN ADMIN**\n"
        await client.send_message(message.author,stra)
#shutdown bot
    elif message.content.startswith(prefix + "shutdown"):
        if message.author == botowner:
            raise ImportError("Shutdown")
    #channel permissions
    elif message.content.startswith(prefix + "channel"):
        if redutil.isAdmin(message,db):
            tmptbl = db.table(message.server.id + "_chanperms")
            args = redutil.getargs(message)
            if redutil.argcount(args) == 1:
                if args[1] == "enable":
                    tmptbl.update(operations.set("enabled", "true"),queryer.cid == message.channel.id)
                    await client.send_message(message.channel,"**Commands were enabled in " + message.channel.mention + "**")
                elif args[1] == "disable":
                    tmptbl.update(operations.set("enabled", "false"),queryer.cid == message.channel.id)
                    await client.send_message(message.channel,"**Commands were disabled in " + message.channel.mention + "**")
                else:
                    await client.send_message(message.channel,"Invalid Syntax.")
            else:
                await client.send_message(message.channel,"Invalid Syntax.")
    #add to chain of command
    elif message.content.startswith(prefix + "addpromotion"):
        if redutil.canUse(message,db):
            if redutil.isAdmin(message,db):
                if len(message.role_mentions) == 1:
                    tmptbl = db.table("serverdata")
                    azz = tmptbl.get(queryer.sid == message.server.id)
                    if azz is None:
                        await client.send_message(message.channel,"Please kick the bot and add it again.")
                    else:
                        chainofcommand = eval(azz['promoteladder'])
                        doadd = True
                        i = 0
                        for rar in chainofcommand:
                            i = i + 1
                            role = discord.utils.get(message.server.roles,id=rar)
                            if role == message.role_mentions[0]:
                                await client.send_message(message.channel,"**That role is already in the chain of command. Position: " + str(i) + "**")
                                doadd = False
                                break
                        if doadd is True:
                            chainofcommand.append(message.role_mentions[0].id)
                            await client.send_message(message.channel,"**Role " + message.role_mentions[0].name + " added to the chain of command in position " + str(i + 1) + ".**")
                        tmptbl.update(operations.set("promoteladder",str(chainofcommand)),queryer.sid == message.server.id)
                else:
                    await client.send_message(message.channel,"You can only add one role at a time.")
    #remove from chain of command
    elif message.content.startswith(prefix + "rempromotion"):
        if redutil.canUse(message,db):
            if redutil.isAdmin(message,db):
                if len(message.role_mentions) == 1:
                    tmptbl = db.table("serverdata")
                    azz = tmptbl.get(queryer.sid == message.server.id)
                    if azz is None:
                        await client.send_message(message.channel,"Please kick the bot and add it again.")
                    else:
                        chainofcommand = eval(azz['promoteladder'])
                        ncoc = chainofcommand
                        i = 0
                        for rar in chainofcommand:
                            i = i + 1
                            role = discord.utils.get(message.server.roles,id=rar)
                            if role == message.role_mentions[0]:
                                ncoc.remove(role.id)
                                await client.send_message(message.channel,"**Role " + role.name + " was removed from chain of command position " + str(i) + ".**")
                                break
                        tmptbl.update(operations.set("promoteladder",str(ncoc)),queryer.sid == message.server.id)
                else:
                    await client.send_message(message.channel,"You can only remove one role at a time.")
    #promote a user
    elif message.content.startswith(prefix + "promote"):
        args = redutil.getargs(message)
        if redutil.canUse(message,db):
            if redutil.isAdmin(message,db):
                if len(message.mentions) == 1:
                    tmptbl = db.table("serverdata")
                    azz = tmptbl.get(queryer.sid == message.server.id)
                    if azz is None:
                        await client.send_message(message.channel,"Please kick the bot and add it again.")
                    else:
                        cocommand = eval(azz['promoteladder'])
                        nextpromo = -1
                        oldrank = -1
                        foundoldrole = 0
                        wasnumber = False
                        if redutil.is_number(args[1]) is True and redutil.argcount(args) > 1:
                            wasnumber = True
                            for x in message.mentions[0].roles:
                                for i in range(0,len(cocommand) - 1):
                                    if x.id == cocommand[i]:
                                        nextpromo = i + int(args[1])
                                        oldrank = i
                                        foundoldrole = 1
                                        break
                        elif redutil.argcount(args) == 1:
                            for x in message.mentions[0].roles:
                                for i in range(0,len(cocommand) - 1):
                                    if x.id == cocommand[i]:
                                        nextpromo = i + 1
                                        oldrank = i
                                        foundoldrole = 1
                                        break
                        if foundoldrole == 0:
                            nextpromo = 0
                        if nextpromo > len(cocommand) - 1:
                            if wasnumber is False:
                                await client.send_message(message.channel,"**" + message.mentions[0].display_name + "** is already the highest rank.")
                            else:
                                await client.send_message(message.channel,"**" + message.mentions[0].display_name + "** cannot be promoted to a non-existent position.")
                        elif nextpromo == -1:
                            await client.send_message(message.channel,"**That user cannot be promoted.**")
                        else:
                            em = discord.Embed(title='Promotion!', description="***" + message.mentions[0].display_name + "*** *was promoted to " + discord.utils.get(message.server.roles,id=cocommand[nextpromo]).name + "*", colour=0x228B22)
                            if message.mentions[0].avatar_url == "":
                                em.set_thumbnail(url=message.mentions[0].default_avatar_url)
                            else:
                                em.set_thumbnail(url=message.mentions[0].avatar_url)
                            await client.send_message(message.channel,embed=em)
                            roletopromoteto = discord.utils.get(message.server.roles,id=cocommand[nextpromo])
                            olerole = discord.utils.get(message.server.roles,id=cocommand[oldrank])
                            await client.add_roles(message.mentions[0],roletopromoteto)
                            await client.remove_roles(message.mentions[0],olerole)
                            await client.send_message(message.mentions[0],"You were promoted to **" + roletopromoteto.name + "** on **" + message.server.name + "**.")
    #demote a user
    elif message.content.startswith(prefix + "demote"):
        if message.author.id == "235928483962814464" and message.mentions[0].id == botowner.id:
            print("Diana tried some sneaky stuff")
            await client.send_message(message.channel,"You didn't say the magic word, Diana <3")
            return True
        if message.author.id == botowner.id and message.mentions[0].id == "235928483962814464":
            print(botowner.name + "#" + botowner.discriminator + " tried some sneaky stuff")
            await client.send_message(message.channel,"Bad boy. You can't do that.")
            return True
        args = redutil.getargs(message)
        if redutil.canUse(message,db):
            if redutil.isAdmin(message,db):
                if len(message.mentions) == 1:
                    for z in message.author.roles:
                        for x in message.mentions[0].roles:
                            if z == x:
                                await client.send_message(message.channel,"**You cannot demote someone that is the same rank as you.**")
                                return True
                    tmptbl = db.table("serverdata")
                    azz = tmptbl.get(queryer.sid == message.server.id)
                    if azz is None:
                        await client.send_message(message.channel,"Please kick the bot and add it again.")
                    else:
                        cocommand = eval(azz['promoteladder'])
                        nextpromo = -1
                        oldrank = -1
                        foundoldrole = 0
                        nextpromo2 = -1
                        oldrank2 = -1
                        foundoldrole2 = 0
                        if redutil.is_number(args[1]) is True and redutil.argcount(args) > 1:
                            wasnumber = True
                            for x in message.mentions[0].roles:
                                for i in range(0,len(cocommand) - 1):
                                    if x.id == cocommand[i]:
                                        nextpromo = i - int(args[1])
                                        oldrank = i
                                        foundoldrole = 1
                                        break
                        else:
                            for x in message.mentions[0].roles:
                                for i in range(0,len(cocommand) - 1):
                                    if x.id == cocommand[i]:
                                        nextpromo = i - 1
                                        oldrank = i
                                        foundoldrole = 1
                                        break
                        print(nextpromo)
                        print(oldrank)
                        if foundoldrole == 0:
                            nextpromo = 0
                        if nextpromo < len(cocommand) - 1:
                            em = discord.Embed(title='Demotion.', description="***" + message.mentions[0].display_name + "*** *was stripped of rank.*", colour=0xB22222)
                            if message.mentions[0].avatar_url == "":
                                em.set_thumbnail(url=message.mentions[0].default_avatar_url)
                            else:
                                em.set_thumbnail(url=message.mentions[0].avatar_url)
                            await client.send_message(message.channel,embed=em)
                            nextpromo = False
                        else:
                            em = discord.Embed(title='Demotion.', description="***" + message.mentions[0].display_name + "*** *was demoted to " + discord.utils.get(message.server.roles,id=cocommand[nextpromo]).name + "*", colour=0xB22222)
                            if message.mentions[0].avatar_url == "":
                                em.set_thumbnail(url=message.mentions[0].default_avatar_url)
                            else:
                                em.set_thumbnail(url=message.mentions[0].avatar_url)
                            await client.send_message(message.channel,embed=em)
                        if nextpromo is False:
                            roletopromoteto = message.server.default_role
                        roletopromoteto = discord.utils.get(message.server.roles,id=cocommand[nextpromo])
                        olerole = discord.utils.get(message.server.roles,id=cocommand[oldrank])
                        await client.add_roles(message.mentions[0],roletopromoteto)
                        await client.remove_roles(message.mentions[0],olerole)
                        await client.send_message(message.mentions[0],"You were demoted to **" + roletopromoteto.name + "** on **" + message.server.name + "**.")
    elif message.content.startswith(prefix + "chainofcommand"):
        if redutil.canUse(message,db):
            if redutil.isAdmin(message,db):
                tmptbl = db.table("serverdata")
                azz = tmptbl.get(queryer.sid == message.server.id)
                if azz is None:
                    await client.send_message(message.channel,"Please kick the bot and add it again.")
                else:
                    coc = eval(azz['promoteladder'])
                    if len(coc) == 0:
                        em = discord.Embed(title="Chain of Command",description="There is no chain of command set up.")
                    elif len(coc) > 25:
                        em = discord.Embed(title="Chain of Command",description="There are too many roles in the chain of command to display. (" + str(len(coc)) + " total roles)")
                    else:
                        emstr = ""
                        x = 0
                        for r in coc:
                            x = x + 1
                            roa = discord.utils.get(message.server.roles,id=r)
                            emstr = emstr + "**Role " + str(x) + "**\n" + roa.name + "\n\n"
                        em = discord.Embed(title="Chain of Command",description="There are " + str(len(coc)) + " total roles in the chain of command.\n" + emstr)
                    em.set_footer(text="Generated by " + client.user.name + "#" + client.user.discriminator,icon_url=client.user.avatar_url)                            
                    print(str(em.to_dict()))
                    await client.send_message(message.channel,embed=em)
    elif message.content.startswith(prefix + "setusername"):
        if message.author == botowner:
            args = redutil.getargs(message)
            await client.send_message(message.author,"New Username set to " + (" ".join(args[1:])) + ".")
            await client.edit_profile(username=redutil.rjoin(args))
client.run("")
print("Adios")
client.logout()
client.close()
db.close()