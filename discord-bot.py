from configparser import ConfigParser
from terminaltables import AsciiTable
import discord
import logging
import os
import edscc


client = discord.Client()
debug = False
token = ""
api_key = ""
api_url = ""
valid_verb = []

config = ConfigParser()
dirPath = os.path.dirname(os.path.realpath(__file__))
config_file = dirPath + '/config.ini'

try:
    print("Loading configurations")
    os.stat(config_file)
    config.read(config_file)
except IOError:
    print(f"Unable to open {config_file}")
    exit(code=0)

try:
    token = config.get('General', 'Discord_Token')
    api_key = config.get('General', 'EDSCC_API')
    api_url = config.get('General', 'API_URL')
except (RuntimeError, TypeError, NameError):
    print(f"{RuntimeError}: {TypeError} {NameError}")
    exit(code=0)

debug = config.getboolean('General', 'debug')

if debug:
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=dirPath + '/discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    logger2 = logging.getLogger('urllib3')
    logger2.setLevel(logging.DEBUG)
    logger2.propagate = True
    handler2 = logging.FileHandler(filename=dirPath + '/edscc.log', encoding='utf-8', mode='w')
    handler2.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger2.addHandler(handler2)

    try:
        edscc_client = edscc.ApiClient(api_key=api_key, api_url=api_url)
        edscc_client.auth()
        valid_verb = edscc_client.valid_verb
        print(valid_verb)
    except Exception:
        print("Connection to EDSCC Server failed.")
        exit(-1)

@client.event
async def on_ready():
    print(f'Discord package version: {discord.__version__}')
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):  # event that happens per any message.
    global valid_verb

    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    elif message.content.startswith('!'):
        tuples = message.content[1:].split(' ')
        command = tuples[0]
        params = tuples[1:]
        msg = '{0.author.mention} Command issued: {1} Params: {2}'.format(message, command, params)
        print(msg)
        print(valid_verb)
        if command in valid_verb:
            reply = {
                'message': '',
                'app_code': '200',
                'error': ''
            }
            if command == 'link':
                try:
                    reply = edscc_client.post('link', discord_name=message.author, discord_id=message.author.id)
                except Exception:
                    print("Exception!")
            else:
                try:
                    reply = edscc_client.post(command, discord_name=message.author, discord_id=message.author.id,
                                              params=params)
                except Exception:
                    print(f"Command '{command}' failed.")
                    msg = 'Command {0} failed. Internal Error.'.format(command)
                    await message.channel.send(msg)

            if reply['app_code'] == 200:
                msg = '{0.author.mention} {1}'.format(message, reply['message'])
                if 'table' in reply:
                    table = AsciiTable(reply['table']['data'])
                    msg = msg + '```' + reply['table']['title'] + '\n' + table.table + '```'
                await message.channel.send(msg)
            else:
                msg = '{0.author.mention} {1}'.format(message, reply['error'])
                await message.channel.send(msg)
        else:
            msg = '{0.author.mention} Unknown command. `!commands` for a list of valid commands.'.format(message)
            await message.channel.send(msg)

    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")


# @client.event
# async def on_typing(channel, user, when):
#     if channel.name == "bot" and user.id != client.user.id:
#         print(f"sending a message to {user}")
#         msg = '{0.mention}, who said you can type in here?'.format(user)
#         await channel.send(msg)

client.run(token)
