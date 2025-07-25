import streamlit as st
import itertools
import pandas as pd

st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
        }
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)


st.title("4d6 Dice Combination Probabilities")
st.write(
    "Calculate the probability of hitting pairs or triplets of numbers in a custom dice game. "
    "Adjust filters to explore different combinations."
)

# All possible 4d6 rolls
all_rolls = list(itertools.product(range(1, 7), repeat=4))

# For each roll, determine the possible numbers that can be gathered
roll_to_gather = []
for roll in all_rolls:
    a, b, c, d = roll
    pairs = [
        (a + b, c + d),
        (a + c, b + d),
        (a + d, b + c)
    ]
    gatherable = set()
    for p in pairs:
        gatherable.add(p[0])
        gatherable.add(p[1])
    roll_to_gather.append(gatherable)

all_numbers = list(range(2, 13))

# Sidebar filters
combo_type = st.radio(
    "Combinations",("Pairs","Triplets"),
    index=1,
    horizontal=True# Triplets selected by default
)

must_include = st.sidebar.multiselect(
    "Show combinations that contain (optional):",
    options=all_numbers,
    default=[]
)

must_exclude = st.sidebar.multiselect(
    "Exclude combinations that contain (optional):",
    options=all_numbers,
    default=[]
)

# Build and filter combinations
comb_size = 2 if combo_type.startswith("Pairs") else 3
combos = list(itertools.combinations(all_numbers, comb_size))

if must_include:
    combos = [
        combo for combo in combos
        if all(num in combo for num in must_include)
    ]

if must_exclude:
    combos = [
        combo for combo in combos
        if all(num not in combo for num in must_exclude)
    ]

# Function to calculate combo probabilities AND number frequencies
def calc_probs(combos, roll_to_gather, all_rolls, pow_max=10):
    results = []
    number_hits = {n: 0 for n in all_numbers}

    for combo in combos:
        success_count = 0
        for gatherable in roll_to_gather:
            if any(num in gatherable for num in combo):
                success_count += 1
                for num in combo:
                    if num in gatherable:
                        number_hits[num] += 1
        prob = success_count / len(all_rolls)
        row = [combo, prob] + [prob ** n for n in range(2, pow_max + 1)]
        results.append(row)

    results.sort(key=lambda x: -x[1])

    # Normalize single number hits
    total_rolls = len(all_rolls)
    number_probs = {n: number_hits[n] / total_rolls for n in all_numbers}

    return results, number_probs

# Compute results and dynamic single number probabilities
results, number_probs = calc_probs(combos, roll_to_gather, all_rolls,pow_max = 20)

# Format and display single number probabilities
st.sidebar.markdown("### Dynamic Single Number Probabilities")
df_single = pd.DataFrame({
    "Number": list(number_probs.keys()),
    "P": [f"{p:.1f}" for p in number_probs.values()]
})
st.sidebar.dataframe(df_single.set_index("Number"), use_container_width=True, height=330)

# Format results into DataFrame
columns = ["Numbers", "P"] + [f"P^{i}" for i in range(2, 21)]
df = pd.DataFrame(results, columns=columns)

# Clean display
df["Numbers"] = df["Numbers"].apply(lambda x: ", ".join(map(str, x)))
for col in df.columns[1:]:
    df[col] = df[col].apply(lambda x: f"{x:.2f}")

# Show main table
styled_df = df.style.background_gradient(
    subset=df.columns[1:],  # Apply to P, P^2, ..., P^15
    cmap="Greens",
    axis=None,
    gmap=None
)

st.dataframe(styled_df, use_container_width=True, height=700)
#st.dataframe(df.reset_index(drop=True), use_container_width=True, height=700)
