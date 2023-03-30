import random
games = {}
class HangmanGame:
    def __init__(self, channel):
        self.channel = channel
        self.word = self.get_random_word()
        self.guesses = []
        self.max_guesses = 6


    async def start_game(self):
        await self.channel.send('Starting a new game of Hangman! The word has {} letters.'.format(len(self.word)))
        await self.channel.send(self.get_board())
        await self.channel.send('Make a guess by using !guess.')

    def get_random_word(self):
        word_list = ['aatrox', 'ahri', 'akali', 'akshan', 'alistar', 'amumu', 'anivia', 'annie', 'aphelios', 'ashe', 'aurelion', 'sol', 'azir', 'bard', "belveth", 'blitzcrank', 'brand', 'braum', 'caitlyn', 'camille', 'cassiopeia', "chogath", 'corki', 'darius', 'diana', 'drmundo', 'draven', 'ekko', 'elise', 'evelynn', 'ezreal', 'fiddlesticks', 'fiora', 'fizz', 'galio', 'gangplank', 'garen', 'gnar', 'gragas', 'graves', 'gwen', 'hecarim', 'heimerdinger', 'illaoi', 'irelia', 'ivern', 'janna', 'jarvaniv', 'jax', 'jayce', 'jhin', 'jinx', "kaisa", 'kalista', 'karma', 'karthus', 'kassadin', 'katarina', 'kayle', 'kayn', 'kennen', "khazix", 'kindred', 'kled', "kogmaw", "ksante", 'leblanc', 'leesin', 'leona', 'lillia', 'lissandra', 'lucian', 'lulu', 'lux', 'malphite', 'malzahar', 'maokai', 'masteryi', 'milio', 'missfortune', 'mordekaiser', 'morgana', 'nami', 'nasus', 'nautilus', 'neeko', 'nidalee', 'nilah', 'nocturne', 'nunuwillump', 'olaf', 'orianna', 'ornn', 'pantheon', 'poppy', 'pyke', 'qiyana', 'quinn', 'rakan', 'rammus', "resai", 'rell', 'renataglasc', 'renekton', 'rengar', 'riven', 'rumble', 'ryze', 'samira', 'sejuani', 'senna', 'seraphine', 'sett', 'shaco', 'shen', 'shyvana', 'singed', 'sion', 'sivir', 'skarner', 'sona', 'soraka', 'swain', 'sylas', 'syndra', 'tahmkench', 'taliyah', 'talon', 'taric', 'teemo', 'thresh', 'tristana', 'trundle', 'tryndamere', 'twistedfate', 'twitch', 'udyr', 'urgot', 'varus', 'vayne', 'veigar', "velkoz", 'vex', 'vi', 'viego', 'viktor', 'vladimir', 'volibear', 'warwick', 'wukong', 'xayah', 'xerath', 'xinzhao', 'yasuo', 'yone', 'yorick', 'yuumi', 'zac', 'zed', 'zeri', 'ziggs', 'zilean', 'zoe', 'zyra', "ksante", 'milio']
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
    
    def end_game(self, id):
        del games[id]