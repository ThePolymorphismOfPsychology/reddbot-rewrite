#collection of simplicity tools/permissions helpers
import asyncio
from tinydb import Query
queryer = Query()
#check if channel is private
def isprivchan(message):
    if message.channel.is_private is True:
        return True
    else:
        return False
#check if user is allowed to use bot
def canUse(message,db):
    print("PERMCHECK ON " + message.server.name + " BY " + message.author.name + "#" + message.author.discriminator)
    if isprivchan(message) is True:
        print("    PRIVATE MESSAGE: RETURN TRUE")
        return True
    else:
        serverchanperms = db.table(message.server.id + "_chanperms")
        myshit = serverchanperms.get(queryer.cid == message.channel.id)
        if myshit is None:
            serverchanperms.insert({"cid": message.channel.id, "enabled": true})
            print("**Recovery Action performed on Server " + message.server.name + ".**")
            print("    CHANNEL NOT RECORDED, ADDED TO DATABASE")
        else:
            if myshit["enabled"] == "false":
                print("    CHANNEL DISABLED, RETURN FALSE.")
                return False
        serveradminroles = db.table(message.server.id + "_roleperms")
        if message.server.owner == message.author:
            print("    AUTHOR IS SERVER OWNER. RETURN TRUE.")
            return True
        for rolez in message.server.roles:
            serveradmins = serveradminroles.get(queryer.rid == rolez.id)
            if serveradmins is not None:
                for role2 in message.author.roles:
                    if rolez.id == role2.id:
                        if serveradmins["admin"] == "true":
                            print("    AUTHOR IS ADMIN. RETURN TRUE.")
                            return True
                        elif serveradmins["disable_botuse"] == "true":
                            print("    AUTHOR IS ON BLACKLIST. RETURN FALSE.")
                            return False
            else:
                print("**Recovery Action performed on Server " + message.server.name + ".**")
                serveradminroles.insert({"rid": rolez.id,"admin": "false","disable_botuse": "false"})
        return True
#check if user is bot admin
def isAdmin(message,db):
    if isprivchan(message) is True:
        return False
    else:
        serveradminroles = db.table(message.server.id + "_roleperms")
        if message.server.owner == message.author:
            return True
        for role in message.server.roles:
            serveradmins = serveradminroles.get(queryer.rid == role.id)
            if serveradmins is not None:
                for role2 in message.author.roles:
                    if role.id == role2.id:
                        if serveradmins["admin"] == "true":
                            return True
            else:
                serveradminroles.insert({"rid": role.id,"admin": "false","disable_botuse": "false"})
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

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
        return False