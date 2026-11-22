# world-news-20261122
[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/sastra-wev/world-news-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/sastra-wev/world-news-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

**The World in One Page** — the whole of Sunday 22 November 2026's world
news summed up in a single 1024×1024 newspaper front page. The hero story
is the COP31 climate summit in Antalya running into a second day of
overtime, deadlocked over fossil fuels; alongside it, Iran's strike on a
Bahrain industrial site and Mexico's capture of cartel boss "El Chapo
Isidro" as illustrated panels, ten more numbered stories from every
region, and a "day in numbers" strip.

The page is drawn programmatically with PIL (`render.py`) from the day's
verified reporting and committed as `entry.png`; `main.py` copies that
asset byte-for-byte to the output path, so the entry is fully
deterministic and needs nothing beyond the Python standard library.

## Run it

```sh
python3 main.py   # writes /output/entry.png
```

To regenerate the artwork from source (requires Pillow):

```sh
python3 render.py # rewrites entry.png next to the script
```
