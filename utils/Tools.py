import json, sys, os
import aiosqlite
import redis.asyncio as redis
import discord
from discord.ext import commands
from core import Context

ANTINUKE_DB_PATH = os.getenv("ANTINUKE_DB_PATH", "antinuke.db")
REDIS_URL = os.getenv("REDIS_URL")
_redis_client = None


def _get_redis_client():
    global _redis_client
    if not REDIS_URL:
        return None
    if _redis_client is None:
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client


async def _ensure_antinuke_schema(db: aiosqlite.Connection) -> None:
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS antinuke_settings (
            guild_id INTEGER PRIMARY KEY,
            status TEXT NOT NULL
        )
        """
    )
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS antinuke_events (
            guild_id INTEGER PRIMARY KEY,
            data TEXT NOT NULL
        )
        """
    )
    await db.commit()


def _default_antinuke_events():
    return {
        "antinuke": {
            "antirole-delete": True,
            "antirole-create": True,
            "antirole-update": True,
            "antichannel-create": True,
            "antichannel-delete": True,
            "antichannel-update": True,
            "antiban": True,
            "antikick": True,
            "antiwebhook": True,
            "antibot": True,
            "antiserver": True,
            "antiping": True,
            "antiprune": True,
            "antiemoji-delete": True,
            "antiemoji-create": True,
            "antiemoji-update": True,
            "antimemberrole-update": True,
        }
    }

def getIgnore(guildID):
    with open("ignore.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "channel": [],
            "role": None,
            "user": [],
            "bypassrole": None,
            "bypassuser": [],
            "commands": []
            
            
        }
        updateignore(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]



def updateignore(guildID, data):
    with open("ignore.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("ignore.json", "w") as config:
        config.write(newdata)
################

def getExtra(guildID):
    with open("extra.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "owners": [],
            "antiSpam": False,
            "antiLink": False,
            "antiinvites": False,
            "punishment": "mute",
            "whitelisted": [],
            "channel": None,
            "mods": [],
            "modrole": None,
            "ignorechannels": []
            
        }
        updateExtra(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateExtra(guildID, data):
    with open("extra.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("extra.json", "w") as config:
        config.write(newdata)






###########autorole###########
def updateautorole(guildID, data):
    with open("autorole.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("autorole.json", "w") as config:
        config.write(newdata)


def getautorole(guildID):
    with open("autorole.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "bots": [],
            "humans": []
        }
        updateautorole(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]
#######################vcrole ############   


def updatevcrole(guildID, data):
    with open("vcrole.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("vcrole.json", "w") as config:
        config.write(newdata)


def getvcrole(guildID):
    with open("vcrole.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "bots": "",
            "humans": ""
        }
        updatevcrole(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]  
    
#######################welcome############


def updategreet(guildID, data):
    with open("greet.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("greet.json", "w") as config:
        config.write(newdata)


def getgreet(guildID):
    with open("greet.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
                "autodel": None,
                "channel": [],
                "color": None,
                "embed": False,
                "footer": "",
                "image": "",
                "message": "<<user.mention>> Welcome To <<server.name>>",
                "ping": False,
                "title": "",
                "thumbnail": ""
        }
        updategreet(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]  




#######################config############


   
    
def getConfig(guildID):
    with open("config.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "whitelisted": [],
            "admins": [],
            "adminrole": None,
            "punishment": "ban",
            "prefix": ".",
            "staff": None,
            "vip": None,
            "girl": None,
            "guest": None,
            "frnd": None,
            "wlrole": None,
            "reqrole": None
        }
        updateConfig(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]

###############
def updateConfig(guildID, data):
    with open("config.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("config.json", "w") as config:
        config.write(newdata)


def add_user_to_blacklist(user_id: int) -> None:
    with open("blacklist.json", "r") as file:
        file_data = json.load(file)
        if str(user_id) in file_data["ids"]:
            return

        file_data["ids"].append(str(user_id))
    with open("blacklist.json", "w") as file:
        json.dump(file_data, file, indent=4)


def remove_user_from_blacklist(user_id: int) -> None:
    with open("blacklist.json", "r") as file:
        file_data = json.load(file)
        file_data["ids"].remove(str(user_id))
    with open("blacklist.json", "w") as file:
        json.dump(file_data, file, indent=4)




def blacklist_check():

    def predicate(ctx):
        with open("blacklist.json") as f:
            data = json.load(f)
            if str(ctx.author.id) in data["ids"]:
                return False
            return True

    return commands.check(predicate)


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)





async def getanti(guildid):
    redis_client = _get_redis_client()
    cache_key = f"antinuke:status:{guildid}"
    if redis_client:
        cached = await redis_client.get(cache_key)
        if cached is not None:
            return cached
    async with aiosqlite.connect(ANTINUKE_DB_PATH) as db:
        await _ensure_antinuke_schema(db)
        cursor = await db.execute(
            "SELECT status FROM antinuke_settings WHERE guild_id = ?",
            (guildid,),
        )
        row = await cursor.fetchone()
        if row is None:
            default = "off"
            await db.execute(
                "INSERT INTO antinuke_settings (guild_id, status) VALUES (?, ?)",
                (guildid, default),
            )
            await db.commit()
            if redis_client:
                await redis_client.set(cache_key, default)
            return default
        status = row[0]
        if redis_client:
            await redis_client.set(cache_key, status)
        return status


async def updateanti(guildid, data):
    async with aiosqlite.connect(ANTINUKE_DB_PATH) as db:
        await _ensure_antinuke_schema(db)
        await db.execute(
            """
            INSERT INTO antinuke_settings (guild_id, status)
            VALUES (?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET status = excluded.status
            """,
            (guildid, data),
        )
        await db.commit()
    redis_client = _get_redis_client()
    if redis_client:
        await redis_client.set(f"antinuke:status:{guildid}", data)



def ignore_check():

    def predicate(ctx):
            data = getIgnore(ctx.guild.id)
            ch = data["channel"]
            iuser = data["user"]
            irole = data["role"]
            buser = data["bypassuser"]
            brole = data["bypassrole"]
            if str(ctx.author.id) in buser:
                return True            
            elif str(ctx.author.id) in iuser or str(ctx.channel.id) in ch:
                return False
            else:
                return True
            

    return commands.check(predicate)



async def updateHacker(guildID, data):
    payload = json.dumps(data, ensure_ascii=False)
    async with aiosqlite.connect(ANTINUKE_DB_PATH) as db:
        await _ensure_antinuke_schema(db)
        await db.execute(
            """
            INSERT INTO antinuke_events (guild_id, data)
            VALUES (?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET data = excluded.data
            """,
            (guildID, payload),
        )
        await db.commit()
    redis_client = _get_redis_client()
    if redis_client:
        await redis_client.set(f"antinuke:events:{guildID}", payload)


async def getHacker(guildID):
    redis_client = _get_redis_client()
    cache_key = f"antinuke:events:{guildID}"
    if redis_client:
        cached = await redis_client.get(cache_key)
        if cached is not None:
            return json.loads(cached)
    async with aiosqlite.connect(ANTINUKE_DB_PATH) as db:
        await _ensure_antinuke_schema(db)
        cursor = await db.execute(
            "SELECT data FROM antinuke_events WHERE guild_id = ?",
            (guildID,),
        )
        row = await cursor.fetchone()
        if row is None:
            defaultConfig = _default_antinuke_events()
            payload = json.dumps(defaultConfig, ensure_ascii=False)
            await db.execute(
                "INSERT INTO antinuke_events (guild_id, data) VALUES (?, ?)",
                (guildID, payload),
            )
            await db.commit()
            if redis_client:
                await redis_client.set(cache_key, payload)
            return defaultConfig
        data = json.loads(row[0])
        if redis_client:
            await redis_client.set(cache_key, row[0])
        return data



def getLogging(guildID):
    with open("logging.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "mod": None,
            "role": None,
            "message": None,
            "member": None,
            "channel": None,
            "server": None,
            "voice": None
        }
        updateLogging(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateLogging(guildID, data):
    with open("logging.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("logging.json", "w") as config:
        config.write(newdata)
