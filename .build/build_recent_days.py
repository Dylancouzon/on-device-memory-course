"""Build ro_shared_data/recent_days.json: a few weeks of text/voice notes before "today".

Gives the L5 capstone a realistic history to search, so the finished assistant
feels lived-in. Photos stay in the curated ro_shared_data/images set: this file is text
and voice only. The hero day (ro_shared_data/memories.json, 42 memories) is untouched, so
L2/L4 payoffs and spoken counts hold. Read by L3 §8 and the L5 capstone.

Timestamps share memories.json's BASE ("today 00:00 UTC"); `day` is days before
today, `h` is the hour of day. Ids start at 1000, clear of the hero day's 0-41.
Edit HISTORY and re-run: `python .build/build_recent_days.py`.
"""
import json
from pathlib import Path

BASE = 1_699_920_000  # today 00:00:00 UTC, matches build_memories.py
START_ID = 1000

# (day, h, source_type, content, category, location, price, store)
# content -> note (text) or transcript (voice). One coherent life: the same
# people and anchors as the hero day (Sarah, Alex, Mum, book club, the bike,
# the coast trip), so the history reads as continuous, not a grab-bag.
HISTORY = [
    (-21, 7.5, 'text', 'Coffee at Blue Cup, espresso, $5', 'food', '5th St', 5.0, 'Blue Cup'),
    (-21, 9.0, 'text', 'Standup at 9:30, review dashboard update', 'work', 'Office', None, None),
    (-21, 14.0, 'text', 'Sarah says the kitchen refactor PR is live', 'work', 'Office', None, None),
    (-21, 18.5, 'voice', 'Note to self, buy milk and bread on the way home', 'errands', 'Station', None, None),
    (-20, 6.5, 'text', 'Gym early, shoulders and back day', 'health', 'Gym', None, None),
    (-20, 10.0, 'text', 'Meeting with Alex about the coast trip weekend', 'social', 'Office', None, None),
    (-20, 12.0, 'text', 'Lunch at Ramen-ya, tonkotsu broth, $14', 'food', 'Downtown', 14.0, 'Ramen-ya'),
    (-20, 15.0, 'text', 'Book club Friday, new sci-fi novel starts', 'social', 'Home', None, None),
    (-20, 19.0, 'voice', "Reminder, Mum's birthday, she wants a scarf", 'social', None, None, None),
    (-20, 22.0, 'text', 'Fixed the dripping kitchen tap finally', 'home', 'Home', None, None),
    (-19, 7.0, 'text', 'Commute took 35 min, bike path was blocked', 'travel', None, None, None),
    (-19, 9.5, 'text', 'Debug production issue in user auth service', 'work', 'Office', None, None),
    (-19, 13.0, 'text', 'Sandwich from deli, turkey Swiss, $8.50', 'food', 'Office', 8.5, None),
    (-19, 16.0, 'voice', 'Quick memo, need to buy new lightbulbs for the living room', 'errands', 'Home', None, None),
    (-18, 8.0, 'text', 'Coffee with Alex at Park, meeting was good', 'social', 'Park', None, None),
    (-18, 11.0, 'text', 'Stakeholder meeting about Q3 roadmap', 'work', 'Office', None, None),
    (-18, 14.5, 'text', 'Groceries, $52, including meat for Sunday roast', 'errands', 'Downtown', 52.0, None),
    (-18, 18.0, 'voice', 'Note to self, landlord says rent stays same next year', 'home', 'Home', None, None),
    (-18, 21.0, 'text', 'Planted basil in kitchen window, hoping it survives', 'home', 'Home', None, None),
    (-17, 9.0, 'text', 'Finished sci-fi book, really gripping', 'social', 'Home', None, None),
    (-17, 12.0, 'text', 'Lunch special at Ramen-ya, $11.50 with tea', 'food', 'Downtown', 11.5, 'Ramen-ya'),
    (-17, 15.0, 'text', "Sarah's PR review needs one more iteration", 'work', 'Office', None, None),
    (-17, 17.5, 'voice', 'Reminder, bike needs new chain soon, check pressure', 'travel', 'Home', None, None),
    (-17, 20.0, 'text', 'Flu shot appointment next Tuesday at 3pm', 'health', None, None, None),
    (-16, 6.5, 'text', 'Gym session, legs, feeling strong today', 'health', 'Gym', None, None),
    (-16, 10.0, 'text', 'Code review for new API endpoints done', 'work', 'Office', None, None),
    (-16, 15.5, 'text', 'Planning items for weekend coast trip', 'travel', 'Home', None, None),
    (-16, 19.0, 'voice', 'Note to self, return library books tomorrow morning', 'errands', 'Home', None, None),
    (-16, 21.0, 'text', 'Mum called, she likes the scarf idea', 'social', 'Home', None, None),
    (-15, 8.0, 'text', 'Morning coffee, oat milk cappuccino, $6', 'food', '5th St', 6.0, 'Blue Cup'),
    (-15, 10.5, 'text', 'Team standup, release planned for Friday', 'work', 'Office', None, None),
    (-15, 13.0, 'text', 'Lunch meeting with Alex at downtown spot', 'social', 'Downtown', None, None),
    (-15, 16.0, 'text', 'Bought scarf for Mum, blue wool, $45', 'shopping', 'Mall', 45.0, None),
    (-15, 18.5, 'voice', 'Quick memo, locker code at the gym is 2280', 'health', 'Gym', None, None),
    (-15, 22.0, 'text', 'Packed for coast trip, leaving tomorrow', 'travel', 'Home', None, None),
    (-14, 7.0, 'text', 'Coast trip day, early morning departure', 'travel', 'Station', None, None),
    (-14, 12.0, 'text', 'Lunch at beach cafe, fish and chips, $16', 'food', None, 16.0, None),
    (-14, 15.0, 'voice', 'Note to self, Alex found great hiking trail near coast', 'travel', None, None, None),
    (-14, 19.0, 'text', 'Hotel dinner, local seafood place, $38', 'food', None, 38.0, None),
    (-14, 21.0, 'text', 'Sunset walk along the beach with Alex', 'social', None, None, None),
    (-13, 8.0, 'text', 'Breakfast at cafe, avocado toast, $12', 'food', None, 12.0, None),
    (-13, 11.0, 'text', 'Hiking trail with Alex, saw three deer', 'travel', None, None, None),
    (-13, 16.0, 'text', 'Bought local pottery, $28, hand wash only', 'shopping', None, 28.0, None),
    (-13, 19.5, 'voice', "Reminder, the pottery can't go in the dishwasher", 'home', 'Home', None, None),
    (-13, 21.0, 'text', 'Evening at hotel, wine and board games', 'social', None, None, None),
    (-12, 8.0, 'text', 'Last morning at coast, relaxed breakfast', 'food', None, None, None),
    (-12, 13.0, 'text', 'Drove back, stopped at roadside market', 'errands', None, None, None),
    (-12, 18.0, 'text', 'Back home, unpacking from the trip', 'home', 'Home', None, None),
    (-12, 20.0, 'voice', 'Note to self, do laundry tomorrow morning', 'errands', 'Home', None, None),
    (-11, 9.0, 'text', 'Back at work, caught up on emails', 'work', 'Office', None, None),
    (-11, 11.0, 'text', 'Sarah wants to pair program on auth service', 'work', 'Office', None, None),
    (-11, 15.0, 'text', 'Finished laundry, put pottery on shelf', 'home', 'Home', None, None),
    (-11, 18.5, 'voice', 'Quick reminder, book club Friday night, bring wine', 'social', 'Home', None, None),
    (-11, 20.0, 'text', 'Gym session, arms and core work', 'health', 'Gym', None, None),
    (-10, 10.0, 'text', 'Pair programming with Sarah, fixed bug', 'work', 'Office', None, None),
    (-10, 16.0, 'text', 'Shopping for book club wine, red blend, $18', 'shopping', 'Mall', 18.0, None),
    (-10, 19.0, 'voice', 'Reminder, basil on windowsill needs water today', 'home', 'Home', None, None),
    (-9, 8.0, 'text', 'Commute smooth, bike path working again', 'travel', None, None, None),
    (-9, 10.5, 'text', 'Release prep meeting, everything good', 'work', 'Office', None, None),
    (-9, 12.5, 'text', 'Team lunch at sandwich place, $9.50', 'food', 'Downtown', 9.5, None),
    (-9, 15.0, 'text', 'Doctor appointment confirmed, Tuesday 2pm', 'health', None, None, None),
    (-9, 18.0, 'voice', 'Note to self, Mum got the scarf, she loves it', 'social', 'Home', None, None),
    (-9, 20.0, 'text', 'Evening jog around the park, 3 miles', 'health', 'Park', None, None),
    (-8, 6.5, 'text', 'Gym early, chest and triceps day', 'health', 'Gym', None, None),
    (-8, 9.0, 'text', 'Final release tests passing, shipping Friday', 'work', 'Office', None, None),
    (-8, 14.0, 'text', 'Alex texted, wants to hike again next month', 'social', 'Office', None, None),
    (-8, 17.0, 'voice', 'Reminder, need to prep something nice for book club', 'social', 'Home', None, None),
    (-7, 8.0, 'text', 'Friday coffee, celebrating the release', 'food', '5th St', 6.0, 'Blue Cup'),
    (-7, 10.0, 'text', 'Release deployed successfully, no issues', 'work', 'Office', None, None),
    (-7, 12.0, 'text', 'Celebration lunch with Sarah and team', 'food', 'Downtown', 15.0, None),
    (-7, 15.0, 'text', 'Left work early, heading to book club', 'social', 'Home', None, None),
    (-7, 19.0, 'voice', 'Book club night, great discussion, wine perfect', 'social', 'Home', None, None),
    (-6, 10.0, 'text', 'Book club moves to Alex place next time, 22 Birch Lane', 'social', 'Home', None, None),
    (-6, 12.0, 'text', 'Brunch at the cafe, pancakes and coffee, $14', 'food', 'Downtown', 14.0, None),
    (-6, 15.0, 'text', 'Grocery shopping, ingredients for new recipe', 'errands', 'Downtown', 38.0, None),
    (-6, 18.0, 'voice', 'Note to self, try the Thai curry recipe this week', 'food', 'Home', None, None),
    (-6, 20.0, 'text', 'Gym session, cardio and weights', 'health', 'Gym', None, None),
    (-5, 7.0, 'text', 'Morning bike ride, clearing my head', 'travel', 'Park', None, None),
    (-5, 10.0, 'text', 'Monday standup, planning next sprint', 'work', 'Office', None, None),
    (-5, 13.0, 'text', 'Lunch, tried Thai curry, really good, $11', 'food', 'Office', 11.0, None),
    (-5, 15.5, 'text', 'Sarah wants to discuss refactoring payment module', 'work', 'Office', None, None),
    (-5, 19.0, 'voice', 'Reminder, doctor appointment tomorrow, bring insurance card', 'health', 'Home', None, None),
    (-4, 11.0, 'text', 'Code review for payment refactoring PR', 'work', 'Office', None, None),
    (-4, 13.5, 'text', 'Quick lunch, sandwich from deli, $9', 'food', 'Office', 9.0, None),
    (-4, 14.0, 'voice', 'Quick memo, doctor appointment in an hour', 'health', 'Office', None, None),
    (-4, 16.0, 'text', 'Doctor visit went well, all clear', 'health', None, None, None),
    (-4, 18.5, 'text', 'Made Thai curry at home, turned out great', 'food', 'Home', None, None),
    (-3, 7.5, 'text', 'Gym session, back to routine', 'health', 'Gym', None, None),
    (-3, 10.0, 'text', 'Payment refactoring PR approved, merging today', 'work', 'Office', None, None),
    (-3, 12.0, 'text', 'Lunch with Alex, planning next coast trip', 'social', 'Downtown', None, None),
    (-3, 15.0, 'text', 'Bike chain needs replacing, will do this weekend', 'travel', 'Home', None, None),
    (-3, 18.0, 'voice', 'Note to self, buy new bike chain at the station shop', 'shopping', 'Station', None, None),
    (-3, 20.0, 'text', 'Evening walk with Alex around neighborhood', 'social', 'Home', None, None),
    (-2, 11.0, 'text', 'Sprint planning session for next cycle', 'work', 'Office', None, None),
    (-2, 16.0, 'text', 'Bought new bike chain, $32 at station shop', 'shopping', 'Station', 32.0, None),
    (-2, 19.5, 'voice', 'Reminder, replace the bike chain tomorrow afternoon', 'travel', 'Home', None, None),
    (-2, 21.0, 'text', 'Watched sci-fi movie, good one', 'social', 'Home', None, None),
    (-1, 7.0, 'text', 'Office wifi password is on the whiteboard by the kitchen', 'work', 'Office', None, None),
    (-1, 10.0, 'text', 'Final checks on deployed feature, no issues', 'work', 'Office', None, None),
    (-1, 15.0, 'text', 'Replaced bike chain finally, runs smooth', 'travel', 'Home', None, None),
    (-1, 18.0, 'voice', 'Note to self, Alex wants to hike again next weekend', 'social', 'Home', None, None),
    (-1, 20.0, 'text', 'Evening gym session, finished strong', 'health', 'Gym', None, None),
]


def build():
    out = []
    for i, (day, h, kind, content, cat, loc, price, store) in enumerate(HISTORY):
        m = {
            "id": START_ID + i,
            "source_type": kind,
            "category": cat,
            "location": loc,
            "timestamp": BASE + day * 86_400 + int(h * 3600),
        }
        m["note" if kind == "text" else "transcript"] = content
        if price is not None:
            m["price"] = price
        if store is not None:
            m["store"] = store
        out.append(m)
    return out


def main():
    memories = build()
    Path("ro_shared_data/recent_days.json").write_text(json.dumps(memories, indent=2) + "\n")

    from collections import Counter
    print(f"wrote ro_shared_data/recent_days.json: {len(memories)} notes")
    print("by source:", dict(Counter(m["source_type"] for m in memories)))
    print("by category:", dict(Counter(m["category"] for m in memories)))


if __name__ == "__main__":
    main()
