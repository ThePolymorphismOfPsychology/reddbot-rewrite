#collection of simplicity tools/permissions helpers
import asyncio
#check if channel is private
def isprivchan(message):
    if message.channel.is_private is True:
        return True
    else:
        return False
#check if user is allowed to use bot
def canUse(message,db):
    if isprivchan(message) is True:
        return True
    else:
        serveradminroles = db.table(message.server.id + "_roleperms")
        if message.server.owner == message.author:
            return True
        for role in message.server.Roles:
            serveradmins = serveradminroles.get(queryer.rid == role.id)
            if serveradmins is not None:
                for role2 in message.author.Roles:
                    if role.id == role2.id:
                        if serveradmins["admin"] == "true":
                            return True
                        elif serveradmins["disable_botuse"] == "true":
                            return False
            else:
                serveradminroles.insert({"rid": role.id,"admin": "false","disable_botuse": "false"})
        return True
#check if user is bot admin
def isAdmin(message,db):
    if isprivchan(message) is True:
        return False
    else:
        serveradminroles = db.table(message.server.id + "_roleperms")
        if message.server.owner == message.author:
            return True
        for role in message.server.Roles:
            serveradmins = serveradminroles.get(queryer.rid == role.id)
            if serveradmins is not None:
                for role2 in message.author.Roles:
                    if role.id == role2.id:
                        if serveradmins["admin"] == "true":
                            return True
            else:
                serveradminroles.insert({"rid": role.id,"admin": "false","disabled": "false"})
        return False
    return False
async def msgowner(msg):
    await client.send_message(botowner,msg)
    return True

def getargs(message):
    return message.content.split(" ")

def argcount(arglist):
    if len(arglist) == 1:
        return 0
    else:
        return len(arglist[1:])
def rjoin(arglist):
    if len(arglist) == 1:
        return ""
    else:
        return " ".join(arglist[1:])