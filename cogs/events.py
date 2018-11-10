import logging

import discord
from discord.ext import commands
from tinydb import Query, TinyDB
from tinydb.operations import delete

from CustomImports import variables

# File with events

class Events:
    def __init__(self, bot):
        self.bot = bot
        self.Users = Query()

    #When member is banned remove from db and log it
    async def on_member_ban(self, member):
        db = TinyDB(variables.db_location, default_table=variables.table_name)
        if db.contains(self.Users.discord_id == member.id):
            db.remove(self.Users.discord_id == member.id)
            logging.info((str(member) + ' was banned').encode("utf-8"))
        db.close()

    # When member leaves remove from db and log it
    async def on_member_remove(self, member):
        db = TinyDB(variables.db_location, default_table=variables.table_name)
        channel = discord.utils.get(member.server.channels, id=variables.club_invite_channel)
        mod = discord.utils.get(member.server.roles, name=variables.mod_role)
        if db.contains(self.Users.discord_id == member.id):
            db_ret = db.get(self.Users.discord_id == member.id)
            league_name = db_ret.get('league_name')
            db.remove(self.Users.discord_id == member.id)
            fmt = 'User left discord {0} ({1.id}) : {2} {3.mention}'
            await self.bot.send_message(channel, fmt.format(member, member, league_name, mod))
            logging.info((str(member) + ' left / was kicked').encode("utf-8"))
            db.close()
        else:
            fmt = 'User left discord {0} ({1.id}) : Not verified {2.mention}'
            await self.bot.send_message(channel, fmt.format(member, member, mod))
            logging.info((str(member) + ' left / was kicked').encode("utf-8"))
            db.close()
    
    # Send pm to newcomers with what to do
    async def on_member_join(self, member):
        current_role = discord.utils.get(member.roles, name=variables.verified)
        default_role = discord.utils.get(member.server.roles, name=variables.not_verified)
        try:
            await self.bot.add_roles(member, default_role)
        except Exception as e:
            logging.error(('[' + str(member) + ']: ' + str(e) + ' default role').encode("utf-8"))
        if current_role is None:
            try:
                await self.bot.send_message(member, variables.rules)
                await self.bot.send_message(member, variables.instructions)
            except Exception as e:
                channel = discord.utils.get(member.server.channels, id=variables.verify_channel_id)
                mod_role = discord.utils.get(member.server.channels, name=variables.mod_role)
                fmt = "Yo {0.mention}, Wumpus says you're a retard, why do you have direct messages turned off ? {1.mention}"
                await self.bot.send_message(channel, fmt.format(member, mod_role))
                logging.error((str(e) + " " + str(member) + ' with id ' + str(member.id)).encode("utf-8"))
        logging.info((str(member) + ' has joined').encode("utf-8"))
    # On error
    async def on_error(self, e):
        logging.error(str(e).encode("utf-8"))

    

def setup(bot):
    bot.add_cog(Events(bot))
