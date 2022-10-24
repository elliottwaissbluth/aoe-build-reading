from email import header
import os
import sys
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
        # The gaps in time determine when the actions are read
        gaps = [self.timestamps[t+1] - self.timestamps[t] 
                for t in range(len(self.timestamps[1:]))]
        gaps.insert(0, 0)
        
        # speech engine
        engine = pyttsx3.init()

        # printing engine
        console = Console()
        header_style = Style(color='#D300FF', bold=True)   

        # Cycle through building tips
        for i,g in enumerate(gaps):
            # sleep for <gap> seconds
            time.sleep(g)

            # Print tips to console
            # Get time in readable format
            if i == 0:
                g_formatted = str(datetime.timedelta(seconds=self.timestamps[i]))
                timeline_md = f'## Timeline for {g_formatted} seconds'
                console.print(Markdown(timeline_md), style=header_style)
                for tip in self.text[i]:
                    console.print(tip, justify='center')
                console.print('\n')
            
            if i != len(gaps)-1:
                g_formatted = str(datetime.timedelta(seconds=self.timestamps[i+1]))
                timeline_md = f'## Timeline for {g_formatted} seconds'
                console.print(Markdown(timeline_md), style=header_style)
                for tip in self.text[i+1]:
                    console.print(tip, justify='center')
                console.print('\n')

            # Save utterance to file and immediately open and read
            full_utterance = [x + ' ' for x in self.text[i]]
            for utt in full_utterance:
                engine.say(utt)
                engine.runAndWait()
                time.sleep(1.5)

if __name__ == '__main__':

    # English 2 | 2 | 2
    b = BuildOrder(
        civ = 'English',
        name = '2 2 2',
        description = 'description',
        timestamps = [0, 95, 125, 240, 340, 365, 480],
        text = [
            ['Send the scout running to find sheep',
            '2 vills to wood, 2 vills to gold (build lumber camp and mining camp',
            '1 vill to make house then mill behind TC, then back to sheep)'],
            ['Research wheelbarrow'],
            ['Build a farm with a food vill',
            'Rally vills to sheep, transfer them from sheep to farm once you have \
            37 wood'],
            ['With three food, age up with council hall',
            'send the 4 food vills on sheep to wood',
            'rally to wood, slowly add some farms'],
            ['Build a barracks once the council hall is getting close to finished'],
            ['Research Double Broadaxe',
            'Produce longbows and spears and begin to push'],
            ['Build a blacksmith']
        ],
    )

    b.read_aloud()  
