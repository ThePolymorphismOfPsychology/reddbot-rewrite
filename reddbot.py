rbversion = "1.5.1 Brave Boar"
import random
import discord
import asyncio
import sys
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    ownerid = (await client.application_info()).owner.id
    print(ownerid)
    print('------')
    await client.change_presence(game=(discord.Game(name="'rb!help' for help.")),status=discord.Status.online)
    await client.send_message((await client.application_info()).owner,"ReddBot has started up. :smile:")
@client.event
async def on_server_join(serv):
    print("***JOINED NEW SERVER*** " + serv.name)
    em = discord.Embed(title='Joined Server',description=serv.name)
    if len(serv.icon_url) != 0:
        em.set_image(url=serv.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message((await client.application_info()).owner,embed=em)

@client.event
async def on_server_update(servbef,servaf):
    print("***SERVER CHANGED*** " + servbef.name + "... Name after change: " + servaf.name)
    em = discord.Embed(title='Server Changed',description="Before: " + servbef.name +"\nAfter: " + servaf.name)
    if len(serv.icon_url) != 0:
        em.set_image(url=serv.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message((await client.application_info()).owner,embed=em)

@client.event
async def on_server_remove(serv):
    print("***SERVER REMOVED*** " + serv.name)
    em = discord.Embed(title='Server Removed',description=serv.name)
    if len(serv.icon_url) != 0:
        em.set_image(url=serv.icon_url)
    em.set_author(name="ReddBot",icon_url=client.user.default_avatar_url)
    await client.send_message((await client.application_info()).owner,embed=em)

@client.event
async def on_error(eve,*args,**kwargs):
    print(sys.exc_info()[1])
    if sys.exc_info()[1] == "Shutdown":
        raise Exception("Shutdown2")
    else:
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
    elif message.content.startswith('rb!mkvote'):
        if type(message.channel) == discord.channel.PrivateChannel:
            await client.send_message(message.author,"**ERROR**```Cannot run command in DM.```")
        else:
            do_we_allow = False
            for role in message.author.roles:
                if role.name == "ReddBot Administrator":
                    do_we_allow = True
            if do_we_allow == True:
                print(message.server.name + ": " + message.author.name + " has begun making a vote in " + message.channel.name)
                #ask what the title for the vote should be
                askmsg = await client.send_message(message.channel, '**What should the title be?**')
                #get message from orignal author
                titlemsg = await client.wait_for_message(author=message.author)
                if titlemsg.mention_everyone == True:
                    #delete all messages if it mentions everyone owo
                    await client.send_message(message.channel, ':angry: You cannot mention everyone in a title. **Command Cancelled.**')
                    await client.delete_message(askmsg)
                    await client.delete_message(titlemsg)
                    await client.delete_message(message)
                else:
                    print(message.server.name + ": " + message.author.name + " has chosen '" + titlemsg.content + "' as the title for the new vote.")
                    promask = await client.send_message(message.channel, "**What should the prompt be?**")
                    prom = await client.wait_for_message(author=message.author)
                    if titlemsg.mention_everyone == True:
                        #delete all messages if it mentions everyone owo
                        await client.send_message(message.channel, ':angry: You cannot mention everyone in a title. **Command Cancelled.**')
                        await client.delete_message(askmsg)
                        await client.delete_message(titlemsg)
                        await client.delete_message(message)
                        await client.delete_message(prom)
                        await client.delete_message(promask)
                    else:
                        print(message.server.name + ": " + message.author.name + " has finished making a vote in " + message.channel.name)
                        em = discord.Embed(title=titlemsg.content,description="**" + prom.content + "**",colour=0x7f0000)
                        em.set_author(name="Please vote now.", icon_url=client.user.default_avatar_url)
                        await client.delete_message(askmsg)
                        await client.delete_message(titlemsg)
                        await client.delete_message(message)
                        await client.delete_message(prom)
                        await client.delete_message(promask)
                        await client.send_message(message.channel,"@everyone")
                        #thanks to DianaWinters
                        diana = await client.send_message(message.channel,embed=em)
                        await client.add_reaction(diana,"yes:391705849661358082")
                        await client.add_reaction(diana,"no:391705816438145024")
                        await client.send_message(message.author,"**Done processing your vote in " + message.server.name + ".**")
            else:
                tmp = await client.send_message(message.channel,"Sorry, " + message.author.mention + ". You do not have valid permissions for this command.")
                await asyncio.sleep(5)
                await client.delete_message(tmp)
    elif message.content.startswith('rb!shutdown'):
        if message.author.id == (await client.application_info()).owner.id:
            await client.change_presence(game=None,status=discord.Status.offline)
            print("ReddBot Shutting Down :'(")
            await client.send_message((await client.application_info()).owner,"ReddBot has shutdown. :cry:")
            await client.logout()
            await client.close()
        else:
            await client.send_message(message.author,"Nice try, **ACCESS DENIED**")
    elif message.content.startswith('rb!version'):
        em = discord.Embed(description="**" + rbversion + "**",colour=0x00ff00)
        em.set_author(name="ReddBot Version",icon_url=client.user.default_avatar_url)
        await client.send_message(message.channel,embed=em)
    elif message.content.startswith('rb!help'):
        #check if help was sent in dms or in server chat
        if not type(message.channel) == discord.channel.PrivateChannel:
            await client.send_message(message.channel,"**Check your dms ;)**")
        await client.send_message(message.author,"***ReddBot Help***```Make Vote - rb!mkvote (requires 'ReddBot Administrator' role)\nGet current version - rb!version\nDisplay this help prompt - rb!help\nkiss someone - rb!kiss\nhug someone - rb!hug\nsmooch someone - rb!smooch\nslap someone - rb!slap\nshoot someone - rb!shoot\npat someone - rb!pat\ngive someone a cookie - rb!cookie```")
    elif message.content.startswith('rb!invite'):
        await client.delete_message(message)
        if message.author.id == (await client.application_info()).owner.id:
            await client.send_message(message.author,"https://discordapp.com/api/oauth2/authorize?client_id=392099253180170250&permissions=1275590736&scope=bot")
    elif message.content.startswith('rb!slap'):
        args = message.content.split(' ')
        if len(args) == 1:
            await client.send_message(message.channel,"**SLAP only takes 1 argument. You gave 0.**")
        elif len(args) > 2:
            await client.send_message(message.channel,"**SLAP only takes 1 argument. You gave " + str(len(args) - 1) + ".**")
        else:
            #placeholder, add randomized choices
            await client.delete_message(message)
            myreplies = ["%s slapped **%s!**", "Ouch! %s slapped **%s!**", "%s slapped **%s!** That looked painful!", "%s attempted to slap **%s** but missed."]
            selrep = random.choice(myreplies)
            await client.send_message(message.channel,selrep % (message.author.mention,message.mentions[0].display_name))
    #shoot command
    elif message.content.startswith('rb!shoot'):
        args = message.content.split(' ')
        if len(args) == 1:
            await client.send_message(message.channel,"**SHOOT only takes 1 argument. You gave 0.**")
        elif len(args) > 2:
            await client.send_message(message.channel,"**SHOOT only takes 1 argument. You gave " + str(len(args) - 1) + ".**")
        else:
            #placeholder, add randomized choices
            await client.delete_message(message)
            myreplies = ["%s shot at **%s!**", "%s shot at **%s!** Ow! Right in the leg!", "%s shot at **%s!** They missed!", "%s attempted to shoot **%s** but hit a wall instead."]
            selrep = random.choice(myreplies)
            await client.send_message(message.channel,selrep % (message.author.mention,message.mentions[0].display_name))
    #hug command
    elif message.content.startswith('rb!hug'):
        args = message.content.split(' ')
        if len(args) == 1:
            await client.send_message(message.channel,"**HUG only takes 1 argument. You gave 0.**")
        elif len(args) > 2:
            await client.send_message(message.channel,"**HUG only takes 1 argument. You gave " + str(len(args) - 1) + ".**")
        else:
            #placeholder, add randomized choices
            await client.delete_message(message)
            myreplies = ["%s hugged **%s!** xoxo", "%s hugged **%s!** Awww!", "%s hugged **%s!** <3", "%s hugged **%s**."]
            selrep = random.choice(myreplies)
            await client.send_message(message.channel,selrep % (message.author.mention,message.mentions[0].display_name))
    elif message.content.startswith('rb!kiss'):
        args = message.content.split(' ')
        if len(args) == 1:
            await client.send_message(message.channel,"**KISS only takes 1 argument. You gave 0.**")
        elif len(args) > 2:
            await client.send_message(message.channel,"**KISS only takes 1 argument. You gave " + str(len(args) - 1) + ".**")
        else:
            #placeholder, add randomized choices
            await client.delete_message(message)
            myreplies = ["%s kissed **%s!**", "OwO... %s kissed **%s!**", "%s kissed **%s!** Awww!", "%s attempted to kiss **%s**."]
            selrep = random.choice(myreplies)
            await client.send_message(message.channel,selrep % (message.author.mention,message.mentions[0].display_name))
    elif message.content.startswith('rb!smooch'):
        args = message.content.split(' ')
        if len(args) == 1:
            await client.send_message(message.channel,"**SMOOCH only takes 1 argument. You gave 0.**")
        elif len(args) > 2:
            await client.send_message(message.channel,"**SMOOCH only takes 1 argument. You gave " + str(len(args) - 1) + ".**")
        else:
            #placeholder, add randomized choices
            await client.delete_message(message)
            myreplies = ["%s smooched **%s!**", "Awww! %s smooched **%s!**", "%s smooched **%s!** That looked intense!", "%s attempted to smooch **%s** but fell on their face instead."]
            selrep = random.choice(myreplies)
            await client.send_message(message.channel,selrep % (message.author.mention,message.mentions[0].display_name))
    elif message.content.startswith('rb!cookie'):
        args = message.content.split(' ')
        if len(args) == 1:
            await client.send_message(message.channel,"**COOKIE only takes 1 argument. You gave 0.**")
        elif len(args) > 2:
            await client.send_message(message.channel,"**COOKIE only takes 1 argument. You gave " + str(len(args) - 1) + ".**")
        else:
            #placeholder, add randomized choices
            await client.delete_message(message)
            myreplies = ["%s gave **%s** a cookie! :cookie:", "%s gave a cookie to **%s!** :cookie:", "%s sent **%s** a cookie! :cookie:"]
            selrep = random.choice(myreplies)
            await client.send_message(message.channel,selrep % (message.author.mention,message.mentions[0].display_name))
    elif message.content.startswith('rb!pat'):
        args = message.content.split(' ')
        if len(args) == 1:
            await client.send_message(message.channel,"**PAT only takes 1 argument. You gave 0.**")
        elif len(args) > 2:
            await client.send_message(message.channel,"**PAT only takes 1 argument. You gave " + str(len(args) - 1) + ".**")
        else:
            #placeholder, add randomized choices
            await client.delete_message(message)
            myreplies = ["%s patted **%s!**", "Awww! %s patted **%s!**", "%s patted **%s!** That looked intense!", "%s attempted to pat **%s** but fell on their face instead."]
            selrep = random.choice(myreplies)
            await client.send_message(message.channel,selrep % (message.author.mention,message.mentions[0].display_name))
    elif message.content.startswith('rb!profile'):
        args = message.content.split(' ')
        if len(args) == 1:
            await client.send_message(message.channel,"**There is no spoon.**")
        elif len(args) == 2:
            await client.send_message(message.channel,"**Coming Soon**")
        else:
            await client.send_message(message.channel,"**Not Yet Implemented**")
client.run("MzkyMDk5MjUzMTgwMTcwMjUw.DRiTXQ.38djgoReh6Hk9Ryj4oFjbCkp2sU")