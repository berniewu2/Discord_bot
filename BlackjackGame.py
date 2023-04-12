import random
games = {}
def calculate_score(hand):
    # Calculate the score of a hand
    score = 0
    num_aces = 0
    for card in hand:
        rank = card[0]
        if rank in ["J", "Q", "K"]:
            score += 10
        elif rank == "A":
            num_aces += 1
            score += 11
        else:
            score += int(rank)
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score

class Blackjack:
    def __init__(self, players, channel):
        self.channel = channel
        self.deck = self.create_deck()
        self.players = players
        self.hands = {}
        self.hand = []
        self.bets = {}

        self.hand.append(self.draw_card())
        # Deal the initial cards
        for player in self.players:
            self.hands[player] = [self.draw_card(), self.draw_card()]
            self.bets[player] = 0
        self.hand.append('Unknown')
        # Check for blackjack
        """
        for player in self.players:
            if calculate_score(self.hands[player]) == 21:
                return "{} got blackjack! They win.".format(player)
        """


        # Return the initial state of the game
    

    def draw_card(self):
        # Draw a card from the deck
        card = self.deck.pop()
        return card

    def create_deck(self):
        # Create a standard 52-card deck
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        deck = []
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades","Hearts", "Diamonds", "Clubs", "Spades"]:
            for rank in ranks:
                deck.append((rank, suit))
        random.shuffle(deck)
        return deck
    
    def calculate(self,hand):
        score = 0
        num_aces = 0
        for card in hand:
            rank = card[0]
            if rank in ["J", "Q", "K"]:
                score += 10
            elif rank == "A":
                num_aces += 1
                score += 11
            else:
                score += int(rank)
        while score > 21 and num_aces > 0:
            score -= 10
            num_aces -= 1
        return score
        
    def end(self, bot):
        self.hand.remove('Unknown')
        self.hand.append(self.draw_card())
        winner = []
        no_one_win = True
        max = self.calculate(self.hand)

        if len(self.hands)==0:
            winner.append(bot)
        else:
            while(max < 17):
                self.hand.append(self.draw_card())
                max = self.calculate(self.hand)
            if max < 21 :
                winner.append(bot)
            else:
                max = 0
            
            
            for k,v in self.hands.items():
                no_one_win = False
                if max < self.calculate(v):
                    max = self.calculate(v)
                    winner = [k]
                if max == self.calculate(v):
                    if k in winner:
                        continue
                    winner.append(k)

        winner = [i.name for i in winner]
        result = "```\n"
        result += "{}{}\n\n".format(", ".join(winner),'の勝利', )
        result += "```"
        return result, no_one_win





    def get_game_state(self):
        # Return the current state of the game
        state = "```\n"
        for player in self.hands:
            state += "{}: {}\n\n".format('百鬼あやめ', ", ".join(str(card) for card in self.hand))
            state += "{}: {}\n".format(player.name, ", ".join(str(card) for card in self.hands[player]))
            state += "Bet: {}\n\n".format(self.bets[player])
        state += "```"
        return state
    
    async def hit(self, player):
        self.hands[player].append(self.draw_card())
        if calculate_score(self.hands[player])>21:
            await self.channel.send(self.get_game_state())
            await self.channel.send(f'busts! {player.name} lose!')
            del self.hands[player]



