import discord
from discord.ext import commands


class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self):
        embed=discord.Embed(title="Help", description="This is the lolice", color=0x763030)
        embed.add_field(name="$lolname | $lolname [user]", value="Get your own or someone's league name", inline=False)
        embed.add_field(name="$whois [league name]", value="Get someone's discord name", inline=False)
        embed.add_field(name="$update [new name]", value="Update your league name", inline=False)
        embed.add_field(name="$pervert", value="Gives or removes the NSFW role", inline=False)
        embed.add_field(name="$help | $commands", value="Show this message", inline=False)
        await self.bot.say(embed=embed)

    @commands.command()
    async def commands(self):
        embed=discord.Embed(title="Help", description="This is the lolice", color=0x763030)
        embed.add_field(name="$lolname | $lolname [user]", value="Get your own or someone's league name", inline=False)
        embed.add_field(name="$whois [league_name]", value="Get someone's discord name", inline=False)
        embed.add_field(name="$update [new name]", value="Update your league name", inline=False)
        embed.add_field(name="$pervert", value="Gives or removes the NSFW role", inline=False)
        embed.add_field(name="$help | $commands", value="Show this message", inline=False)
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
