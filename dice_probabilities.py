import streamlit as st
import itertools
import pandas as pd

# Remove top padding via CSS
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Calculate individual number probabilities
number_counts = {n: 0 for n in all_numbers}
for gatherable in roll_to_gather:
    for n in all_numbers:
        if n in gatherable:
            number_counts[n] += 1

single_probs = {
    n: number_counts[n] / len(roll_to_gather)
    for n in all_numbers
}

# Display single number probabilities on the left
st.sidebar.markdown("### Single Number Probabilities")
df_single = pd.DataFrame({
    "Number": list(single_probs.keys()),
    "P": [f"{p:.2f}" for p in single_probs.values()]
})
st.sidebar.dataframe(df_single.set_index("Number"), use_container_width=True)


st.title("4d6 Dice Combination Probabilities")
st.write(
    "Calculate the probability of hitting pairs or triplets of numbers in a custom dice game. "
    "Adjust filters to explore different combinations."
)

# All possible 4d6 rolls
all_rolls = list(itertools.product(range(1,7), repeat=4))

# For each roll, what are the possible numbers you can pick?
roll_to_gather = []
for roll in all_rolls:
    a,b,c,d = roll
    pairs = [
        (a+b, c+d),
        (a+c, b+d),
        (a+d, b+c)
    ]
    gatherable = set()
    for p in pairs:
        gatherable.add(p[0])
        gatherable.add(p[1])
    roll_to_gather.append(gatherable)

all_numbers = list(range(2, 13))

def calc_probs(combos, roll_to_gather, all_rolls, pow_max=10):
    result = []
    for combo in combos:
        success = sum(
            any(num in gatherable for num in combo)
            for gatherable in roll_to_gather
        )
        prob = success / len(all_rolls)
        row = [combo, prob] + [prob**n for n in range(2, pow_max+1)]
        result.append(row)
    result.sort(key=lambda x: -x[1])
    return result

# Sidebar filters
combo_type = st.sidebar.radio("Show combinations of...", ("Pairs (2 numbers)", "Triplets (3 numbers)"))

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

min_p, max_p = st.sidebar.slider(
    "Probability range (P):",
    min_value=0.0, max_value=1.0,
    value=(0.0, 1.0),
    step=0.01
)

comb_size = 2 if combo_type.startswith("Pairs") else 3
combos = list(itertools.combinations(all_numbers, comb_size))

# Apply include filter
if must_include:
    combos = [
        combo for combo in combos
        if all(num in combo for num in must_include)
    ]

# Apply exclude filter
if must_exclude:
    combos = [
        combo for combo in combos
        if all(num not in combo for num in must_exclude)
    ]

results = calc_probs(combos, roll_to_gather, all_rolls)

# Convert to DataFrame for better display and filtering
columns = ["Numbers", "P"] + [f"P^{i}" for i in range(2, 11)]
df = pd.DataFrame(results, columns=columns)

# Apply probability filter
df = df[(df["P"] >= min_p) & (df["P"] <= max_p)]

# Format numbers for nicer display
df["Numbers"] = df["Numbers"].apply(lambda x: ", ".join(map(str, x)))
for col in df.columns[1:]:
    df[col] = df[col].apply(lambda x: f"{x:.2f}")

# Display table larger vertically
st.dataframe(df.reset_index(drop=True), use_container_width=True, height=700)
