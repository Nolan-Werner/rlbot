# This is the main file where you control your bot's strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits

class Bot(BotCommandAgent):
    # Predefined chat messages
    CHAT_COMMS = {
        'kickoff': "Let's go!",
        'at_opponent_goal': "I'm attacking!",
        'away_from_my_net': "Defending!",
        'boosting': "Grabbing boost!",
        'need_support': "Need backup!",
        'goal_scored': "Goal!",
    }
    
    def run(self):
        
        if self.get_intent() is not None:
            return
        
        if self.kickoff_flag:
            self.send_custom_chat(self.CHAT_COMMS['kickoff'])
            self.set_intent(kickoff())
            return
        
        targets = {
            'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
            'away_from_my_net': (self.friend_goal.right_post, self.friend_goal.left_post) 
        }
        hits = find_hits(self, targets)
        
        if len(hits['at_opponent_goal']) > 0:
            self.set_intent(hits['at_opponent_goal'][0])
            self.send_custom_chat(self.CHAT_COMMS['at_opponent_goal'])
            print('at their goal')
            return
            
        if len(hits['away_from_my_net']) > 0:
            self.set_intent(hits['away_from_my_net'][0])
            self.send_custom_chat(self.CHAT_COMMS['away_from_my_net'])
            print('away from our goal')
            return
        
        available_boosts = [boost for boost in self.boosts if boost.large and boost.active]
        if len(available_boosts) > 0:
            self.set_intent(goto(available_boosts[0].location))
            self.send_custom_chat(self.CHAT_COMMS['boosting'])
            print('going for boost', available_boosts[0].index)
            return
        
        # Check for goal scored condition
        if self.has_scored_goal():  # Replace with your actual goal check method
            self.send_custom_chat(self.CHAT_COMMS['goal_scored'])

    def send_custom_chat(self, message):
        # Implement this method to send chat messages to your team
        print("Chat to team:", message)  # Placeholder for actual chat function
    
    def has_scored_goal(self):
        # Implement your logic to check if the bot's team has scored a goal
        return False  # Placeholder; update with actual logic