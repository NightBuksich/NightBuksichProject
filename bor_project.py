import discord
from discord import utils
import helper_for_bot


class Bot(discord.Client):
    async def bot_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == helper_for_bot.id_post:
            channel = self.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member = utils.get(message.guild.members, id=payload.user_id)
            try:
                emoji = str(payload.emoji)
                role = utils.get(message.guild.roles, id=helper_for_bot.games[emoji])
                if len(member.roles) <= helper_for_bot.max_games_for_one_user:
                    await member.add_roles(role)
                    print('[Success] Пользователь получил роль!'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Ошибка слишуом много ролей!'.format(member))
            except KeyError as e:
                print('[ERROR] Не нашлось роли с таким эмодзи')

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)
        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=helper_for_bot.games[emoji])
            await member.remove_roles(role)
            print('[SUCCESS] Роль убрана!'.format(member, role))
        except KeyError as e:
            print('[ERROR] Не налось роли с таким эмодзи')


client = Bot()
client.run('ODM3NTY4MDU1ODgyMTUzOTg0.YIucCQ.biFy1_qQHKC4FtMuq0KOvfpa7B4')
