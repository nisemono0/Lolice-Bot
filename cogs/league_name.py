import logging
import re

import discord
from discord.ext import commands
from tinydb import Query, TinyDB
from tinydb.operations import delete, increment

from CustomImports import variables

# File for league-names commands

class LeagueNames():
    """League name commands"""
    def __init__(self, bot):
        # Instantiate the bot and the query for db
        self.bot = bot
        self.Users = Query()

    # Checks if user DOES NOT have the not verified role
    def check_update(self):
        def predicate(context):
            Users = Query()
            db = TinyDB(variables.db_location, default_table=variables.table_name)
            if db.contains(Users.discord_id == context.message.author.id):
                db.close()
                return True
            db.close()
            return False
        return commands.check(predicate)

    # Verify command
    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_role(variables.not_verified)
    async def verify(self, context, *, league_name: str=None):
        """$verify [league name]: Add league name, and confirms you agree to rules"""
        # if no name given, do nothing
        if league_name == None:
            return
        db = TinyDB(variables.db_location, default_table=variables.table_name)
        # if db contains user already do nothing
        if db.contains(self.Users.discord_id == context.message.author.id):
            db.close()
            return
        try:
            # if all above are false get mod role and verified role and the mod notif channel
            mod_notif_channel = discord.utils.get(context.message.server.channels, id=variables.club_invite_channel)
            verified_role = discord.utils.get(context.message.author.server.roles, name=variables.verified)
            mod_role = discord.utils.get(context.message.server.roles, name=variables.mod_role)
            lol_names_channel = discord.utils.get(context.message.server.channels, id=variables.verify_channel_id)
            # delete the ~verify command
            await self.bot.delete_message(context.message)
            # replace everything with the verified role
            await self.bot.replace_roles(context.message.author, verified_role)
            # pm's the welcome message
            fmt = '{0.mention} : {1}'
            await self.bot.send_message(lol_names_channel, fmt.format(context.message.author, league_name))
            # notify mods user needs an invite
            fmt = '{0.mention} needs a club invite, {1.mention}'
            await self.bot.send_message(mod_notif_channel, fmt.format(context.message.author, mod_role))
            # pm the user the welcome message
            await self.bot.send_message(context.message.author, variables.welcome_message)
            # add user into db
            db.insert({'discord_id': context.message.author.id, 'discord_name': str(context.message.author), 'league_name': league_name})
            db.close()
            # cli/file logging
            print('[INFO]:' + str(context.message.author) + ' is verified')
            print('[INFO]:' + str(context.message.author) + ' == ' + league_name)
            logging.info((str(context.message.author) + ' is verified').encode("utf-8"))
            logging.info((str(context.message.author) + ' == ' + league_name).encode("utf-8"))
        except Exception as e:
            # if bot has error, log it
            print('[ERROR]:' + '[' + str(context.message.channel) + ']: ' + str(e) + ' for verify')
            logging.error(('[' + str(context.message.channel) + ']: ' + str(e) + ' for verify').encode("utf-8"))
            db.close()
    # if the user has verified role do nothing
    @verify.error
    async def verify_error(self, error, context):
        return
    
    # Update name command
    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @check_update(None)
    async def update(self, context, *, league_name: str=None):
        """$update [new name]: Update your league name"""
        # verify check with roles
        user_roles = [role.name for role in context.message.author.roles]
        if variables.not_verified in user_roles:
            raise Exception('User not verified')
        elif league_name != None:
            db = TinyDB(variables.db_location, default_table=variables.table_name)
            db_ret = db.get(self.Users.discord_id == context.message.author.id)
            old_name = db_ret.get('league_name')
            # update new name
            db.update({'league_name': league_name}, self.Users.discord_id == context.message.author.id)
            db.close()
            fmt = '{0.mention} successfully updated your league name: {1} -> {2}'
            await self.bot.say(fmt.format(context.message.author, old_name, league_name))
            # send new name for logging into the league-name channel
            channel = discord.utils.get(context.message.author.server.channels, id = variables.verify_channel_id)
            fmt = '{0.mention} : {1} -> {2}'                
            await self.bot.send_message(channel, fmt.format(context.message.author, old_name, league_name))
            # CLI, file logging
            print('[INFO]:' + str(context.message.author) + ' updated league name: ' + old_name + ' -> ' + league_name)
            logging.info((str(context.message.author) + ' updated league name: ' + old_name + ' -> ' + league_name).encode("utf-8"))
            return
        else: 
            await self.bot.say('No name given')
    # If user is not verified
    @update.error
    async def update_error(self, error, context):
        # if the user is not verified then do nothing 
        return

    @commands.command(pass_context=True)
    async def lolname(self, context, user: discord.Member=None):
        """$lolname | $lolname [user]: Get your own or someone's league name"""
        if user is None:
            db = TinyDB(variables.db_location, default_table=variables.table_name)
            # Get your own lolname if you're in the db
            db_ret = db.search(self.Users.discord_id.search(context.message.author.id, flags=re.IGNORECASE))
            if not db_ret:
                await self.bot.say('User not found')
                db.close()
                return
            else:
                embed=discord.Embed(title="", description="", color=0x763030)
                league_name = db_ret[0].get('league_name')
                embed.add_field(name="Discord name: {0} (Id: {1})".format(context.message.author, context.message.author.id), value="League name: {0}".format(league_name), inline=False)
                await self.bot.say(embed=embed)
                db.close()
                return
        else:
            # Get another user's lolname
            db = TinyDB(variables.db_location, default_table=variables.table_name)
            db_ret = db.search(self.Users.discord_id.search(user.id, flags=re.IGNORECASE))
            if not db_ret:
                await self.bot.say('User not found')
                db.close()
                return
            else:
                embed=discord.Embed(title="", description="", color=0x763030)
                league_name = db_ret[0].get('league_name')
                embed.add_field(name="Discord name: {0} (Id: {1})".format(user, user.id), value="League name: {0}".format(league_name), inline=False)
                await self.bot.say(embed=embed)
                db.close()
                return

    @commands.command(pass_context=True)
    async def whois(self, context, *, league_name):
        """$whois [league name]: Get your own or someone's league name"""
        db = TinyDB(variables.db_location, default_table=variables.table_name)
        db_ret = db.search(self.Users.league_name.search(league_name, flags=re.IGNORECASE))
        if not db_ret:
            await self.bot.say("User not found")
            db.close()
            return
        else:
            embed=discord.Embed(title="", description="", color=0x763030)
            for ret in db_ret:
                discord_id = ret.get('discord_id')
                discord_name = ret.get('discord_name')
                league_name = ret.get('league_name')
                member = discord.utils.get(context.message.author.server.members, id=discord_id)
                if member is None:
                    embed.add_field(name="Discord name: {0} (Id: {1})".format(discord_name, discord_id), value="League name: {0}".format(league_name), inline=False)
                else:
                    embed.add_field(name="Discord name: {0} (Id: {1})".format(member, discord_id), value="League name: {0}".format(league_name), inline=False)
            await self.bot.say(embed=embed)
            db.close()
            return




def setup(bot):
    bot.add_cog(LeagueNames(bot))
