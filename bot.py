"""
bruh
"""

import discord

def readToken():
    with open("TOKEN", 'r') as f:
        return f.read()

TOKEN = readToken()

class Bruh(discord.Client):
    voice_handles = {}

    def setTraining():
        pass

    async def on_message(self, message):
        """
        Handle messages
        """

        if message.author == self.user:
            return
        elif message.channel.name != "bruh":
            return

        if message.content != "bruh":
            # Invalid message. Remove and replace
            await self.send_message(message.channel, "bruh")
            await self.delete_message(message)

    async def on_message_edit(self, before, after):
        if after != "bruh":
            await self.send_message(after.channel, "bruh")
            await self.delete_message(after)

    # async def on_reaction_add(self, reaction, user):
    #     if not len(reaction.message.reactions) < 4:
    #         # message is complete, timme to verify
    #         for i in range(4):

    async def on_voice_state_update(self, before, after):
        # prevent recursion
        if after == self.user:
            return

        channel = after.voice.voice_channel
        if type(channel) == type(None):
            # User left channel
            channel = before.voice.voice_channel
        elif channel.name == "bruh":
            vc = await self.join_voice_channel(channel)
            self.voice_handles[channel.id] = vc
            return

        # Check if channel empty
        if len(channel.voice_members) <= 1:
            # channel is empty
            handle = self.voice_handles[channel.id]
            await handle.disconnect()

    async def on_ready(self):
        print("ready")

if __name__ == "__main__":
    client = Bruh()

    client.run(TOKEN)