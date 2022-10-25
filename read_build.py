import time
import pyttsx3
from typing import List
import datetime
from dataclasses import dataclass, field
from rich.console import Console
from rich.markdown import Markdown
from rich.style import Style

@dataclass
class BuildOrder:
    """Docstring"""
    civ: str
    name: str
    description: str
    
    timestamps: List[int] = field(default_factory=list) # in seconds
    text: List[List[str]] = field(default_factory=list)
    
    def read_aloud(self):
        # speech engine
        engine = pyttsx3.init()

        # printing engine
        console = Console()
        header_style = Style(color='#D300FF', bold=True)   

        # Cycle through building tips
        time_spent_giving_tips = 0
        for i,s in enumerate(self.timestamps):
            # sleep for <gap> seconds
            # the first instructions will play immediately
            gap = 0
            if i > 0:
                gap = self.timestamps[i] - self.timestamps[i-1]
            time.sleep(gap-time_spent_giving_tips)              

            # Print tips to console
            # The first and second set of tips will be displayed immediately for
            #   the player to look forward
            if i == 0: # Print the first tip
                # format time and display across top
                s_formatted = str(datetime.timedelta(seconds=s))
                timeline_md = f'## ~~~~~~~~~~ {s_formatted[3:]} ~~~~~~~~~~'
                console.print(Markdown(timeline_md), style=header_style)
                for tip in self.text[0]:
                    console.print(tip, justify='center')
                console.print('\n')
            
            # Print the subsequent tips
            if i < len(self.timestamps) - 1:
                s_formatted = str(datetime.timedelta(
                                        seconds=self.timestamps[i+1]
                                        ))
                timeline_md = f'## ~~~~~~~~~~ {s_formatted[3:]} ~~~~~~~~~~'
                console.print(Markdown(timeline_md), style=header_style)
                for tip in self.text[i+1]:
                    console.print(tip, justify='center')
                console.print('\n')

            start = time.time()
            for utt in self.text[i]:
                engine.say(utt)
                engine.runAndWait()
                time.sleep(1.5)
            end = time.time()
            time_spent_giving_tips = end - start


if __name__ == '__main__':

    # English 2 | 2 | 2
    b = BuildOrder(
        civ = 'English',
        name = '2 2 2',
        description = 'description',
        timestamps = [0, 25, 95, 125, 240, 340, 365, 480],
        text = [
            [
                'Send the scout running to find sheep, send 2 vills to sheep, 2 vills to wood, and 2 vills to Gold',
                'build a lumber camp with a wood vill, and a mining camp with a mining vill',
                'send a sheep vill to make a house, then a mill, behind  the  TC, then send back to sheep'
             ],
            [
                'Send the first created villager to Gold',
                'Send the rest of the new villagers to gather food from farms near the mill\'s influence'
            ],
            [
                'Research wheelbarrow from the mill'
            ],
            [
                'Build a farm with a food vill',
                'Rally vills to sheep, transfer them from sheep to farm once you have 37 wood'
            ],
            [
                'Age up with council hall',
            ],
            [
                'Build a barracks once the council hall is getting close to finished',
                'Train spearman with the barracks',
            ],
            [
                'Once in the Feudal Age, get 6 vills on Gold, ten vills on Wood',
                'Continue building Farms around mills, build more mills if needed',
                'Research Double Broadaxe at the lumber camp',
                'Train longbows at the council hall'
            ],
            [
                'Build a blacksmith'
            ]
        ],
    )

    b.read_aloud()  
