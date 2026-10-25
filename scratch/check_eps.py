# Script to summarize the core events of each episode
import re

episodes = {}

for ep in range(60, 73):
    with open(f"volumen_6/transcripciones/limpias/episodio_{ep}.txt") as f:
        t = f.read()
    episodes[ep] = t

# Let's write a script that outputs summaries for each ep
print("Loaded all 13 episodes.")
