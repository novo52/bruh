"""
bruh
"""

import discord
import re # Regex for dynamic bruh emoji acceptance

def readToken():
    with open("TOKEN", 'r') as f:
        return f.read()

TOKEN = readToken()

class Bruh(discord.Client):
    voice_handles = {}

    def setTraining():
        pass

    
    # Python can't deal with emojis, convert to unicode codes
    def convertToUnicode(self, emoji):
        return emoji.encode('unicode-escape').decode('utf-8')

    def isValidMessage(self, message):
        
        # Plain bruh
        if message == "bruh":
            return True

        # Dynamic bruhs (only 'bruh', ':bruh:', and ' ' are allowed)
        if message != message.lstrip(" "): # No leading whitespace
            return False
        if "bruhbruh" in message: # No double bruh
            return False
        if "     " in message: # No more than 4 spaces in a row
            return False

        message = re.sub("<:bruh:\d+>", "", message) # Bruh emoji is allowed
        message = message.replace("bruh", "") # Bruh is allowed
        message = message.replace(" ", "") # Single space allowed
        if message == "":
            return True

        return False # DESTROY

    def isValidReaction(self, reaction):
        
        reactions = reaction.message.reactions

        # A default unicode emoji
        if not reaction.custom_emoji:
            # Allow a custom bruh emoji to be before the unicode bruhs
            reactionOffset = 1
            if reactions[0].custom_emoji:
                reactionOffset = 2

            # bruh only
            regional_indicator_bruh = [
                '\U0001f1e7', #B
                '\U0001f1f7', #R
                '\U0001f1fa', #U
                '\U0001f1ed'] #H
            
            emoji = self.convertToUnicode(reaction.emoji)
            properEmoji = self.convertToUnicode(regional_indicator_bruh[(len(reactions) % 4) - reactionOffset])

            if emoji == properEmoji: # Valid reaction
                return True
            
            return False # Invalid

        # A custom bruh emoji
        if len(reactions) == 1 or len(reactions) == 5: # Allow a unicode bruh sequence
            validEmojiNames = [                        # to be followed by a custom bruh
                'bruh']
            valid = False
            for validEmojiName in validEmojiNames:
                
                if reaction.emoji.name == validEmojiName:
                    return True

        return False
        

    async def validateMessage(self, message):
        print("\"" + message.content + "\"")
        print("message sent by: " + message.author.name + " (" + message.author.nick + ")")
        if self.isValidMessage(message.content):
            print("valid")
            return
        
        # Invalid message. Delete
        print("invalid")
        channel = message.channel
        await message.delete()

    async def validateReaction(self, reaction, user):
        print("\"" + self.convertToUnicode(reaction.emoji) + "\"")
        print("reaction sent by: " + user.name + " (" + user.display_name + ")")
        if self.isValidReaction(reaction):
            print("valid")
            return

        # Invalid reaction. Delete
        print("invalid")
        await reaction.remove(user)

    # Sent messages
    async def on_message(self, message):

        if message.author == self.user:
            return

        if message.channel.name != "bruh":
            return

        await self.validateMessage(message)

    # Edits
    async def on_message_edit(self, before, after):
        await self.validateMessage(after)

    # Reactions
    async def on_reaction_add(self, reaction, user):
        await self.validateReaction(reaction, user)

    # Voice
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
