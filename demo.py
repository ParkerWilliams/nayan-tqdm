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

# ── Indeterminate mode (total=None) ─────────────────────────────────────────

print("\n  === Indeterminate Mode (total=None) ===\n")
print("  Note: Shows current behavior with total=None.\n")

for theme in ("nyan", "wizard", "disco"):
    print(f"\n  --- {theme} (total=None) ---\n")
    bar = tqdm(total=None, theme=theme, desc=theme)
    for i in range(60):
        time.sleep(0.03)
        bar.update(1)
    bar.close()
    time.sleep(0.3)

print()
