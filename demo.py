"""Visual demo of all nyanbar themes."""
import time
from nyanbar import tqdm
from nyanbar.registry import list_themes

THEMES = list_themes()
N = 80
DELAY = 0.02

for theme in THEMES:
    print(f"\n  === {theme} ===\n")
    for _ in tqdm(range(N), theme=theme):
        time.sleep(DELAY)
    time.sleep(0.5)

print()
