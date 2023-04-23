import random
import pandas as pd
import asyncio 
games = {}

class Blackjack:
    def __init__(self, channel, bot, five, ten):
        self.channel = channel
        self.player = bot
        self.deck = self.create_deck()
        self.hand = []
        self.hands = []
        self.need_split = False
        self.bet = 0
        self.not_finish = True
        

        for user in five:
            self.hands.append(Hand(user, 5))
        for user in ten:
            self.hands.append(Hand(user, 10))

        self.hand.append(self.draw_card(self.deck))
        self.hand.append('Unknown')

        # Deal the initial cards
        for h in self.hands:
            h.hand = [self.draw_card(self.deck), self.draw_card(self.deck)]
            if h.check_split():
                h.need_split = True
                self.need_split = False


    async def start_game(self):
        while len(self.hands)>0 and self.not_finish:
            self.not_finish = False
            await self.channel.send(self.get_game_state())
            for h in self.hands:
                await self.channel.send(h.get_game_state())
                async for msg in self.channel.history(limit=1):
                    h.message_id = msg.id
                    if not h.stand:
                        await msg.add_reaction('🇭')
                        await msg.add_reaction('🇸')
                    if h.need_split:
                        await msg.add_reaction('🃏')
            await asyncio.sleep(5)
            for h in self.hands:
                if not h.stand:
                    if h.message_id == 0:
                        continue
                    h.stand = True
                    msg = await self.channel.fetch_message(h.message_id)
                    if h.need_split:
                        split = [user async for user in msg.reactions[2].users()]
                        if len(split) > 1:
                            h.stand = False
                            self.not_finish = True
                            h.need_split = False
                            new_hand = Hand(h.player, h.bet)
                            self.hands.insert(self.hands.index(h) + 1, new_hand)
                            new_hand.hand.append(h.hand.pop(1))
                            new_hand.message_id = 0
                            h.hand.append(self.draw_card(self.deck))
                            if h.check_split():
                                h.need_split = True
                            new_hand.hand.append(self.draw_card(self.deck))
                            if new_hand.check_split():
                                new_hand.need_split = True
                            continue
                    users = [user async for user in msg.reactions[0].users()]
                    if len(users)>1:
                        h.stand = False
                        self.not_finish = True
                        for user in users:
                            if user != h.player:
                                continue
                        if await h.hit(self.deck):
                            await self.channel.send(h.get_game_state())
                            await self.channel.send(f'busts! {h.player.name} loses {h.bet} credits!')
                            self.hands.remove(h)
            

    def draw_card(self,deck):
        card = deck.pop()
        random.shuffle(deck)
        return card
    
    def create_deck(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] #
        deck = []
        for suit in ["♥️", "♦️", "♣️", "♠️", "♥️", "♦️", "♣️", "♠️"]:
            for rank in ranks:
                deck.append((rank, suit))
        random.shuffle(deck)
        return deck
    
    def calculate(self):
        score = 0
        num_aces = 0
        for card in self.hand:
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
    
    async def hit(self, deck):
        data = pd.read_csv('credit.csv')
        data = data.set_index('ID')
        self.hand.append(self.draw_card(deck))
        if self.calculate()>21:
            data.loc[self.player.id].values[0] -= self.bet
            data.to_csv('credit.csv')
            return True
        return False

    async def end(self):
        data = pd.read_csv('credit.csv')
        data = data.set_index('ID')
        result = "```\n"
        self.hand.remove('Unknown')
        self.hand.append(self.draw_card(self.deck))
        no_one_win = True
        max = self.calculate()

        if len(self.hands) == 0:
            result += "百鬼あやめ最高"

        else:
            while(max < 17):
                self.hand.append(self.draw_card(self.deck))
                max = self.calculate()
            if max > 21:
                max = 0
            
            for h in self.hands:
                no_one_win = False
                if max < h.calculate():
                    data.loc[h.player.id].values[0] += h.bet
                    result += f"{h.player.name} wins {h.bet} credits\n"
                else:
                    data.loc[h.player.id].values[0] -= h.bet
                    result += f"{h.player.name} loses {h.bet} credits\n"
        result += "```"
        data.to_csv('credit.csv')
        if not no_one_win:
            await self.channel.send(self.final_game_state())
        return result, no_one_win

    def final_game_state(self):
        state = "```\n"
        state += "{}: {}\n\n".format('百鬼あやめ', ", ".join(str(card) for card in self.hand))
        for h in self.hands:
            state += "{}: {}\n".format(h.player.name, ", ".join(str(card) for card in h.hand))
            state += "Bet: {}\n\n".format(h.bet)
        state += "```"
        return state

    def get_game_state(self):
        state = "```\n"
        state += "{}: {}\n\n".format(self.player.name, ", ".join(str(card) for card in self.hand))
        state += "Bet: {}\n\n".format(self.bet)
        state += "```"
        return state
    
    def check_split(self):
        return (self.hand[0][0]) == (self.hand[1][0])

class Hand(Blackjack):
    def __init__(self, player, bet) -> None:
        self.player = player
        self.hand = []
        self.bet = bet
        self.need_split = False
        self.message_id = 0
        self.stand = False