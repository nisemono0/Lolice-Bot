import logging
from datetime import datetime

import discord
from discord.ext import commands

from CustomImports import variables

# Initialize bot
bot = commands.Bot(command_prefix=variables.bot_prefix, description=variables.bot_description)

# Initialize logging
logging.basicConfig(format='[%(asctime)s] [%(levelname)s]:%(message)s', filename=variables.logger_location, level=logging.INFO)

# On bot start
@bot.event
async def on_ready():
	# Prints
	print('-----------------------------------------------------------')
	print('Logged in at : ' + str(datetime.now()))
	print('Name: ' + str(bot.user))
	print('Id: ' + bot.user.id)
	print('discord.py version: ' + discord.__version__)
	print('-----------------------------------------------------------\n')
	print('STARTED LOGGING')

	# File Logging
	logging.info('----------------------------------------------------')
	logging.info('Logged in at : ' + str(datetime.now()))
	logging.info('Name: ' + str(bot.user))
	logging.info('Id: ' + bot.user.id)
	logging.info('discord.py version: ' + discord.__version__)
	logging.info('----------------------------------------------------\n')
	logging.info('STARTED LOGGING')

# Load all cogs and start the bot
if __name__ == '__main__':
	for extension in variables.extensions:
		try:
			bot.remove_command('help')
			bot.load_extension(extension)
			print('[INFO]:Loaded extention: ' + str(extension))
			logging.info('Loaded extension: ' + str(extension))
		except Exception as e:
			fmt = '{0} cannot be loaded: [{1}]'
			print('[ERROR]:' + fmt.format(extension, e))
			logging.error(fmt.format(extension, e))
	bot.run(variables.bot_token)
