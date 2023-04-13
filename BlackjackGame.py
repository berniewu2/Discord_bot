import random
from credit import credits
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
    def __init__(self, channel, five, ten):
        self.channel = channel
        self.deck = self.create_deck()
        self.hands = {}
        self.hand = []
        self.bets = {}
        self.players = five + ten


        self.hand.append(self.draw_card())

        for player in five:
            self.bets[player] = 5
        for player in ten:
            self.bets[player] = 10

        # Deal the initial cards
        for player in self.players:
            self.hands[player] = [self.draw_card(), self.draw_card()]
        self.hand.append('Unknown')


    def draw_card(self):
        # Draw a card from the deck
        card = self.deck.pop()
        return card

    def create_deck(self):
        # Create a standard 52-card deck
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        deck = []
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades", "Hearts", "Diamonds", "Clubs", "Spades"]:
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
        
    async def end(self, bot):
        result = "```\n"
        self.hand.remove('Unknown')
        self.hand.append(self.draw_card())
        winner = []
        tie = []
        no_one_win = True
        max = self.calculate(self.hand)

        if len(self.hands)==0:
            winner.append(bot)
        else:
            while(max < 17):
                self.hand.append(self.draw_card())
                max = self.calculate(self.hand)
            if max > 21:
                max = 0
            
            for k,v in self.hands.items():
                no_one_win = False
                if max < self.calculate(v):
                    credits[k.id] += self.bets[k]
                    print(self.bets[k])
                    result += f"{k.name} wins {self.bets[k]} credits"
                elif max > self.calculate(v):
                    credits[k.id] -= self.bets[k]
                    result += f"{k.name} loses {self.bets[k]} credits"

        result += "```"
        return result, no_one_win


    def get_game_state(self):
        # Return the current state of the game
        state = "```\n"
        state += "{}: {}\n\n".format('百鬼あやめ', ", ".join(str(card) for card in self.hand))
        for player in self.hands:
            state += "{}: {}\n".format(player.name, ", ".join(str(card) for card in self.hands[player]))
            state += "Bet: {}\n\n".format(self.bets[player])
        state += "```"
        return state
    
    async def hit(self, player):
        self.hands[player].append(self.draw_card())
        if calculate_score(self.hands[player])>21:
            await self.channel.send(self.get_game_state())
            await self.channel.send(f'busts! {player.name} lose!')
            credits[player.id] -= self.bets[player]
            del self.hands[player]




