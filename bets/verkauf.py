import streamlit as st
from statistics import mean

def recommend_bid(table_cards, seen_cards=[]):
    if len(table_cards) != 5:
        return "Error: Provide exactly 5 table cards for this round."

    all_cards = set(range(1, 31))
    unseen_cards = list(all_cards - set(seen_cards) - set(table_cards))

    top = max(table_cards)
    second = sorted(table_cards)[-2]
    worst = min(table_cards)

    unseen_avg = mean(unseen_cards) if unseen_cards else 15.5

    top_delta = top - unseen_avg
    second_delta = second - unseen_avg
    spread = top - worst

    score = top_delta + 0.5 * second_delta + 0.1 * spread

    if score >= 12:
        return 4
    elif score >= 8:
        return 2
    elif score >= 4:
        return 1
    else:
        return 0

# Streamlit app
st.set_page_config(page_title="For Sale Bid Advisor", page_icon="🏠")

st.title("🏠 For Sale: Bidding Recommendation")
st.markdown("Enter the 5 property cards revealed this round and any cards already seen in previous rounds.")

# Input: current table cards
table_cards = st.text_input("Cards this round (5 cards, comma-separated)", "4, 9, 17, 21, 28")
seen_cards = st.text_input("Seen cards (comma-separated)", "1, 3, 6, 8, 10, 12, 14")

try:
    table_list = sorted([int(x.strip()) for x in table_cards.split(",") if x.strip()])
    seen_list = sorted([int(x.strip()) for x in seen_cards.split(",") if x.strip()])

    if len(table_list) != 5:
        st.error("Please enter exactly 5 cards for the current round.")
    else:
        bid = recommend_bid(table_list, seen_list)
        st.success(f"💡 Recommended Bid: **{bid}**")
except ValueError:
    st.error("Please enter valid integers separated by commas.")
