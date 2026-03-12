from OSRSBytes import Hiscores
from rates import rates
import streamlit as st
import pandas as pd

LEVEL_99_XP = 13034431
ALL_SKILLS = []

for skill in  Hiscores('Lynx Titan').getSkillsGenerator():
    ALL_SKILLS.append(skill)


def get_rate(skill, level):
    table = rates[skill]
    best = table[0][0]
    for lvl, rate in table:
        if level >= lvl:
            best = rate
    return best


def hours_to_target(skill, start_xp):
    global LEVEL_99_XP
    xp = start_xp
    hours = 0

    while xp < LEVEL_99_XP:
        rate = get_rate(skill, xp)
        xp += rate   # simulate 1 hour
        hours += 1

    return hours

def safe_skill(acc, skill, field):
    try:
        return acc.skill(skill, field)
    except:
        # Unranked → default
        if field == 'level':
            return 1
        if field == 'experience':
            return 0
        return None


st.set_page_config(layout="wide")
st.title("Race to Max Comparison")

col1_in, col2_in = st.columns([1,1])

with col1_in:
    user1 = st.text_input("Account 1")

with col2_in:
    user2 = st.text_input("Account 2")

col1_out, col2_out = st.columns([1,1])

if st.button("Compare"):

    acc1 = Hiscores(user1)
    acc2 = Hiscores(user2)

    # try:
    df_user1 = pd.DataFrame([{"skill": skill, "level1": safe_skill(acc1, skill, 'level'), "xp1": safe_skill(acc1, skill, 'experience'), 'xp_to-max1' : LEVEL_99_XP - min(safe_skill(acc1, skill, 'experience'), LEVEL_99_XP), 'hours_to_max1': hours_to_target(skill, safe_skill(acc1, skill, 'experience')) } for skill in ALL_SKILLS])
    df_user2 = pd.DataFrame([{"skill": skill, "level2": safe_skill(acc2, skill, 'level'), "xp2": safe_skill(acc2, skill, 'experience'), 'xp_to-max2' : LEVEL_99_XP - min(safe_skill(acc2, skill, 'experience'), LEVEL_99_XP), 'hours_to_max2': hours_to_target(skill, safe_skill(acc2, skill, 'experience')) } for skill in ALL_SKILLS])
# except Exception as e:
    # print('user is unranked in skills, exiting')
    # exit()

    df_user1['level_99_xp'] = LEVEL_99_XP
    df_user2['level_99_xp'] = LEVEL_99_XP

    df_user1 = df_user1.sort_values("skill")
    df_user2 = df_user2.sort_values("skill")

    df_user1_display = df_user1[["skill", "level1", "xp1", 'hours_to_max1']].copy()
    df_user2_display = df_user2[["skill", "level2", "xp2", 'hours_to_max2']].copy()

    df_user1_display["xp1"] = df_user1_display["xp1"].apply(lambda x: f"{x:,}")
    df_user2_display["xp2"] = df_user2_display["xp2"].apply(lambda x: f"{x:,}")

    diff = pd.merge(df_user1, df_user2, on="skill")
    diff['Level Diff'] = diff['level1'] - diff['level2']
    diff['xp_diff'] = diff['xp1'] - diff['xp2']
    #diff['hours_to_max']  = diff['hours_to_max1'] - diff['hours_to_max2']

    #diff['EXP To Max Diff'] = diff['xp_to-max1'] - diff['xp_to-max2']

    total_hours = df_user1_display['hours_to_max1'].sum() - df_user2_display['hours_to_max2'].sum()

    display_diff = diff[['Level Diff','hours_to_max1', 'hours_to_max2', 'skill']]

    df_user1_display.rename(columns={'level1': user1 + "'s Level", 'xp1': user1 + "'s Exp", 'hours_to_max1': user1 + "'s Hours to Max"}, inplace=True)
    df_user2_display.rename(columns={'level2': user2 + "'s Level", 'xp2': user2 + "'s Exp", 'hours_to_max2': user2 + "'s Hours to Max"}, inplace=True)

 
    
    #display_diff['EXP To Max Diff'] = display_diff['EXP To Max Diff'].apply(lambda x: f"{x:,}")
    #display_diff['Hours Ahead/Behind'] = display_diff['hours_diff'].apply(lambda x: f"{x:,.2f}")

    df_out = df_user1_display.merge(df_user2_display, on="skill")#.merge(display_diff, on="skill")
    df_out.rename(columns={'skill': 'Skill', 'hours_diff': 'Hours Ahead/Behind'}, inplace=True)
    df_out['Skill'] = df_out['Skill'].str.capitalize()

    st.dataframe(df_out.style.set_properties(**{'text-align': 'left'}), hide_index=True, width='stretch', height=875)

    st.write(f"{user1} is {df_user1_display[user1 + "'s Hours to Max"].sum()} hours away from maxing")
    st.write(f"{user2} is {df_user2_display[user2 + "'s Hours to Max"].sum()} hours away from maxing")

    if df_user1_display[user1 + "'s Hours to Max"].sum() == 0 and df_user2_display[user2 + "'s Hours to Max"].sum() == 0:
        st.write(f"There is no race, both players are already maxed")
    elif df_user1_display[user1 + "'s Hours to Max"].sum() == 0:
        st.write(f"{user1} has won the race to max!")
    elif df_user2_display[user2 + "'s Hours to Max"].sum() == 0:
        st.write(f"{user2} has won the race to max!")
    elif total_hours > 0:
        st.write(f"{user1} is {abs(total_hours)} hours behind {user2} in the race to max")
    else:
        st.write(f"{user1} is {abs(total_hours)} hours ahead of {user2} in the race to max")


