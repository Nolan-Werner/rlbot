# This is the main file where you control your bot's strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits

class Bot(BotCommandAgent):
    # This function runs every in-game tick (every time the game updates anything)
    CHAT_COMMS = {
        'kickoff': "Let's go!",
        'at_opponent_goal': "I'm attacking!",
        'away_from_my_net': "Defending!",
        'boosting': "Grabbing boost!",
        'need_support': "Need backup!",
        'goal_scored': "What a save!",
    } 
    def run(self):
        available_boosts = [boost for boost in self.boosts if boost.large and boost.active]
        if self.get_intent() is not None:
            return
        if self.kickoff_flag:
            self.set_intent(kickoff())
            return
        
        if self.is_in_front_of_ball():
            self.set_intent(goto(available_boosts[0].location))
            print('going for boost', available_boosts[0].index)
            self.set_intent(goto(self.friend_goal.location))
            print('rotating to goal')

        if self.ball.location.y-self.me.location.y > 300:
            self.controller.boost = True


        targets = {
            'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post), 
        }
        hits = find_hits(self,targets)
        if len(hits['at_opponent_goal']) > 0:
            self.set_intent(hits['at_opponent_goal'][0])
            print('at their goal')
            return
        
        #get boost
        if self.me.boost <1:
            closest_boost = self.get_closest_large_boost()
            if closest_boost is not None:
                boost_location = closest_boost.location
                self.set_intent(goto(boost_location))
                print('going for boost', available_boosts[0].index)
        
        if self.has_scored_goal():  # Replace with your actual goal check method
            self.send_custom_chat(self.CHAT_COMMS['goal_scored'])
            print("What a save!")
            self.send_custom_chat(self.CHAT_COMMS['goal_scored'])
            print("What a save!")
            self.send_custom_chat(self.CHAT_COMMS['goal_scored'])
            print("What a save!")
        
