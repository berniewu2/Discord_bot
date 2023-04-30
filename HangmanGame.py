import random
import discord
games = {}
class HangmanGame:
    def __init__(self, channel):
        self.channel = channel
        self.word = self.get_random_word()
        self.guesses = []
        self.max_guesses = 6


    async def start_game(self):
        await self.channel.send(self.get_board())
        await self.channel.send('Make a guess by using /g.')

    def get_random_word(self):
        word_list = ['aatrox', 'ahri', 'akali', 'akshan', 'alistar', 'amumu', 'anivia', 'annie', 'aphelios', 'ashe', 'aurelionsol', 'azir', 'bard', "belveth", 'blitzcrank', 'brand', 'braum', 'caitlyn', 'camille', 'cassiopeia', "chogath", 'corki', 'darius', 'diana', 'drmundo', 'draven', 'ekko', 'elise', 'evelynn', 'ezreal', 'fiddlesticks', 'fiora', 'fizz', 'galio', 'gangplank', 'garen', 'gnar', 'gragas', 'graves', 'gwen', 'hecarim', 'heimerdinger', 'illaoi', 'irelia', 'ivern', 'janna', 'jarvaniv', 'jax', 'jayce', 'jhin', 'jinx', "kaisa", 'kalista', 'karma', 'karthus', 'kassadin', 'katarina', 'kayle', 'kayn', 'kennen', "khazix", 'kindred', 'kled', "kogmaw", "ksante", 'leblanc', 'leesin', 'leona', 'lillia', 'lissandra', 'lucian', 'lulu', 'lux', 'malphite', 'malzahar', 'maokai', 'masteryi', 'milio', 'missfortune', 'mordekaiser', 'morgana', 'nami', 'nasus', 'nautilus', 'neeko', 'nidalee', 'nilah', 'nocturne', 'nunuandwillump', 'olaf', 'orianna', 'ornn', 'pantheon', 'poppy', 'pyke', 'qiyana', 'quinn', 'rakan', 'rammus', "resai", 'rell', 'renataglasc', 'renekton', 'rengar', 'riven', 'rumble', 'ryze', 'samira', 'sejuani', 'senna', 'seraphine', 'sett', 'shaco', 'shen', 'shyvana', 'singed', 'sion', 'sivir', 'skarner', 'sona', 'soraka', 'swain', 'sylas', 'syndra', 'tahmkench', 'taliyah', 'talon', 'taric', 'teemo', 'thresh', 'tristana', 'trundle', 'tryndamere', 'twistedfate', 'twitch', 'udyr', 'urgot', 'varus', 'vayne', 'veigar', "velkoz", 'vex', 'vi', 'viego', 'viktor', 'vladimir', 'volibear', 'warwick', 'wukong', 'xayah', 'xerath', 'xinzhao', 'yasuo', 'yone', 'yorick', 'yuumi', 'zac', 'zed', 'zeri', 'ziggs', 'zilean', 'zoe', 'zyra', "ksante", 'milio']
        return random.choice(word_list)

    def get_board(self):
        board = ''
        for letter in self.word:
            if letter in self.guesses:
                board += letter + ' '
            else:
                board += '_ '
        return '```\n{}\n{}```'.format(board, self.get_hangman())
    
    
    def get_hangman(self):
        stages = [
            ' _________     \n|         |    \n|         O    \n|        /|\\  \n|        / \\  \n|               \n|',
            ' _________     \n|         |    \n|         O    \n|        /|\\  \n|        /    \n|               \n|',
            ' _________     \n|         |    \n|         O    \n|        /|\\  \n|               \n|               \n|',
            ' _________     \n|         |    \n|         O    \n|        /|   \n|               \n|               \n|',
            ' _________     \n|         |    \n|         O    \n|         |   \n|               \n|               \n|',
            ' _________     \n|         |    \n|         O    \n|               \n|               \n|               \n|',
            ' _________     \n|         |    \n|               \n|               \n|               \n|               \n|'
        ]
        return stages[self.max_guesses]
    
    async def guess(self, guess):
        if guess == self.word:
            await self.channel.send('Congratulations! You won!')
            end = discord.File('ayame_image\\ayame(hangman_end).jpg', filename='ayame.gif')
            await self.channel.send(file = end)
            self.end_game(self.channel.id)
        elif guess in self.guesses:
            await self.channel.send('You already guessed that letter.')
        elif guess in self.word:
            self.guesses.append(guess)
            await self.channel.send(self.get_board())
            if '_' not in self.get_board():
                await self.channel.send('Congratulations!')
                end = discord.File('ayame_image\\ayame(hangman_end).jpg', filename='ayame.gif')
                await self.channel.send(file = end)
        else:
            self.guesses.append(guess)
            self.max_guesses-=1
            if self.max_guesses == 0:
                await self.channel.send(f'You are bad\n The answer is {self.word}')
                self.end_game(self.channel.id)
                return
            await self.channel.send(self.get_board())



    def end_game(self, id):
        del games[id]
