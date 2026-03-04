"""Visual demo of all nayan_tqdm themes."""
import time
from nayan_tqdm import tqdm
from nayan_tqdm.registry import list_themes

THEMES = list_themes()
N = 80
DELAY = 0.02

for theme in THEMES:
    print(f"\n  === {theme} ===\n")
    for _ in tqdm(range(N), theme=theme):
        time.sleep(DELAY)
    time.sleep(0.5)

print()
