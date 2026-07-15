"""Build data/memories.json: one person's day, shared across L2-L5.

Text and voice notes plus photo captures, each with metadata the labs filter on
(category, location, timestamp, price). Photo entries point at files in
data/images. Edit the DAY list and re-run: `python .build/build_memories.py`.

Timestamps are epoch seconds. BASE is "today 00:00 UTC"; `h` is the hour of day
(negative = yesterday), so the data reads as times, not raw integers.
"""
import json
from pathlib import Path

BASE = 1_699_920_000  # today 00:00:00 UTC (2023-11-14)

# (h, source_type, content, category, location, price, store)
# content -> note (text), transcript (voice), or image filename (photo).
DAY = [
    # --- text notes ---
    (8.3, "text", "Great little coffee place on 5th with outdoor seating and fast wifi", "food", "5th St", None, None),
    (10.0, "text", "Standup with Sarah moved to Thursday to review the Q3 roadmap", "work", "Office", None, None),
    (9.0, "text", "Pick up dry cleaning before Friday, ticket is on the fridge", "errands", "Home", None, None),
    (11.5, "text", "Idea: batch the weekly report so it drafts itself every Monday", "work", "Office", None, None),
    (19.0, "text", "Mum's new address is 14 Elm Court, buzzer 3", "social", "Home", None, None),
    (15.3, "text", "Liked the black and white running shoes at the mall, about $45", "shopping", "Mall", 45.0, None),
    (21.0, "text", "Book club is reading the new sci-fi novel, we meet next Tuesday", "social", "Home", None, None),
    (12.0, "text", "Dentist appointment confirmed for next Wednesday at 2pm", "health", "Home", None, None),
    (12.5, "text", "Try the new ramen place downtown, everyone raves about the tonkotsu", "food", "Downtown", None, None),
    (17.5, "text", "Water the plants twice a week while the amaryllis is blooming", "home", "Home", None, None),
    (7.5, "text", "Renewed the gym membership, locker code is 4471", "health", "Gym", 40.0, None),
    (16.0, "text", "Found a quiet cafe with good wifi to work from near the park", "work", "Park", None, None),
    (20.0, "text", "Remember to call the landlord about the leaking tap", "errands", "Home", None, None),
    (8.0, "text", "New bakery on the corner does an amazing morning cronut", "food", "5th St", 4.0, None),
    (22.0, "text", "Parking permit renewal is due at the end of the month", "errands", "Home", None, None),
    (14.0, "text", "Meeting notes: ship the edge demo before the conference", "work", "Office", None, None),
    (18.0, "text", "Bought a new houseplant for the kitchen windowsill", "home", "Home", 12.0, None),
    (21.5, "text", "Weekend trip: check train times to the coast on Saturday", "travel", "Station", None, None),
    # --- yesterday, for time-window filters ---
    (-7.0, "text", "Coffee run to the espresso bar near the office", "food", "Office", 3.0, None),
    (-4.0, "text", "Late night fixing the deploy pipeline, finally green", "work", "Home", None, None),
    # --- voice notes (on-device transcript) ---
    (13.4, "voice", "Note to self, the ramen downtown was incredible, fourteen dollars and worth it, sat right by the window", "food", "Downtown", 14.0, "Ramen-ya"),
    (15.5, "voice", "Reminder, buy a birthday present for Alex this week, maybe those headphones he mentioned", "shopping", "Mall", None, None),
    (10.1, "voice", "Quick memo, the standup is moved to Thursday, tell the rest of the team", "work", "Office", None, None),
    (9.2, "voice", "Parked the bike near the station, second rack from the entrance", "travel", "Station", None, None),
    (19.5, "voice", "Just remembered, we are low on coffee at home, grab a bag on the way back", "errands", "Home", None, None),
    # --- photo captures (point at data/images) ---
    (8.2, "photo", "coffee.jpg", "food", "5th St", None, "Blue Cup"),
    (8.1, "photo", "bakery.jpg", "food", "5th St", 4.0, None),
    (13.0, "photo", "restaurant.jpg", "food", "Downtown", None, "Elizabeth's"),
    (13.2, "photo", "ramen.jpg", "food", "Downtown", 14.0, "Ramen-ya"),
    (20.0, "photo", "pizza.jpg", "food", "Home", 18.0, None),
    (15.3, "photo", "sneakers.jpg", "shopping", "Mall", 45.0, "SportsWorld"),
    (9.1, "photo", "bicycle.jpg", "travel", "5th St", None, None),
    (21.6, "photo", "train.jpg", "travel", "Station", None, None),
    (16.2, "photo", "street.jpg", "travel", "Downtown", None, None),
    (16.5, "photo", "park.jpg", "travel", "Park", None, None),
    (17.6, "photo", "plant.jpg", "home", "Home", 12.0, None),
    (18.2, "photo", "kitchen.jpg", "home", "Home", None, None),
    (17.0, "photo", "dog.jpg", "social", "Park", None, None),
    (15.8, "photo", "book.jpg", "shopping", "Mall", 15.0, None),
    (16.1, "photo", "laptop.jpg", "work", "Park", None, None),
    (10.0, "photo", "meeting.jpg", "work", "Office", None, None),
    (7.4, "photo", "gym.jpg", "health", "Gym", None, None),
]

# Voice notes carry the audio file L4 transcribes on-device. The stored
# transcript is the fallback text L2/L3/L5 read; L4 replaces it with what its
# Whisper model produces from these clips (see .build/utils/audio.py).
VOICE_AUDIO = {
    "Note to self, the ramen downtown was incredible, fourteen dollars and worth it, sat right by the window": "ramen.wav",
    "Reminder, buy a birthday present for Alex this week, maybe those headphones he mentioned": "birthday.wav",
    "Quick memo, the standup is moved to Thursday, tell the rest of the team": "standup.wav",
    "Parked the bike near the station, second rack from the entrance": "bike.wav",
    "Just remembered, we are low on coffee at home, grab a bag on the way back": "coffee.wav",
}


def build():
    out = []
    for i, (h, kind, content, category, location, price, store) in enumerate(DAY):
        m = {
            "id": i,
            "source_type": kind,
            "category": category,
            "location": location,
            "timestamp": BASE + int(h * 3600),
        }
        m["note" if kind == "text" else "transcript" if kind == "voice" else "file"] = content
        if kind == "voice":
            m["audio_file"] = VOICE_AUDIO[content]
        if price is not None:
            m["price"] = price
        if store is not None:
            m["store"] = store
        out.append(m)
    return out


def main():
    memories = build()
    # every photo must point at a real file
    imgs = {p.name for p in Path("data/images").glob("*.jpg")}
    missing = [m["file"] for m in memories
               if m["source_type"] == "photo" and m["file"] not in imgs]
    assert not missing, f"photo entries with no image on disk: {missing}"
    # every voice note must point at a real audio clip
    clips = {p.name for p in Path("data/audio").glob("*.wav")}
    missing_audio = [m["audio_file"] for m in memories
                     if m["source_type"] == "voice" and m["audio_file"] not in clips]
    assert not missing_audio, f"voice entries with no audio on disk: {missing_audio}"
    Path("data/memories.json").write_text(json.dumps(memories, indent=2) + "\n")

    from collections import Counter
    cats = Counter(m["category"] for m in memories)
    kinds = Counter(m["source_type"] for m in memories)
    print(f"wrote data/memories.json: {len(memories)} memories")
    print("by source:", dict(kinds))
    print("by category:", dict(cats))


if __name__ == "__main__":
    main()
