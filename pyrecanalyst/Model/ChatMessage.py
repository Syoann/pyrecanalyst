from pyrecanalyst.Model.Player import Player


class ChatMessage:
    """
    The ChatMessage class represents a single chat message sent before or during
    the game.
    """

    def __init__(self, time=0, player=None, msg='', group=''):
        # Sent time in milliseconds since the start of the game.
        self.time = time

        # Player who sent this message.
        #
        # This might be a player that is not actually in the game, if they joined
        # the lobby but left before the game started. In that case the Player
        # object will be empty except for 'name'.
        self.player = player

        # Message text
        self.msg = msg

        # Group at which this chat is directed (<Team>, <Enemy>, <All>), if any
        self.group = group

    def __str__(self):
        return f">{self.player_name}:{self.msg}"

    @staticmethod
    def create(time, player, chat):
        """
        Helper method to create a chat message from a chat string more easily.

        Messages actually have the player name and sometimes a group specifier
        (<Team>, <Enemy>, etc) included in their message body which is lame.
        Sometimes players that don't end up in the player info blocks of the
        recorded games sent messages anyway (particularly pre-game chat by people
        who joined the multiplayer lobby and then left) so we deal with that too.
        """
        group = ''

        # This is directed someplace (@All, @Team, @Enemy, etc.)
        # Voobly adds @Rating messages too, which we might wish to parse into
        # the player objects later as a 'rating' property.
        if chat.startswith('<'):
            # Standard directed chat messages have a format like:
            #   <All>PlayerName: message
            # Voobly rating messages however:
            #   <Rating> PlayerName: message
            # ...adds a space character before the name, so we deal with it
            # separately.
            if chat.startswith('<Rating> '):
                group = 'Rating'
                chat = chat[9:]
            else:
                end = chat.index('>')
                group = chat[1:end]
                chat = chat[end+1:]

        if not player:
            player = Player()

            try:
                player.name = chat[:chat.index(': ')].strip()
            # Empty message ?
            except:
                player.name = chat[:chat.index(':')].strip()

        # Cut the player name out of the message contents.
        chat = chat[len(player.name) + 2:].strip()

        return ChatMessage(time, player, chat, group)
