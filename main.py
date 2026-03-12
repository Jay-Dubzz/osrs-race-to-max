from OSRSBytes import Hiscores
import streamlit as st
import pandas as pd

LEVEL_99_XP = 13034431

st.set_page_config(layout="wide")
st.title("Race to Max Comparison")

col1_in, col2_in = st.columns([1,1])

with col1_in:
    user1 = st.text_input("Account 1")

with col2_in:
    user2 = st.text_input("Account 2")

col1_out, col2_out = st.columns([1,1])


rates = {'attack': 100000, 'defense': 100000, 'strength': 100000, 'hitpoints': 25000, 'ranged': 100000, 'prayer': 400000, 'magic': 150000, 'cooking': 400000, 'woodcutting': 60000, 'fletching': 125000, 'fishing': 80000, 'firemaking': 200000, 'crafting': 200000, 'smithing': 150000, 'mining': 45000, 'herblore': 200000, 'agility': 60000, 'thieving': 150000, 'slayer': 40000, 'farming': 150000, 'runecrafting': 45000, 'hunter': 150000, 'construction': 200000, 'sailing': 150000}

if st.button("Compare"):
    acc1 = Hiscores(user1)
    acc2 = Hiscores(user2)

    df_user1 = pd.DataFrame([{"skill": skill, "level1": acc1.skill(skill, 'level'), "xp1": acc1.skill(skill, 'experience'), 'xp_to-max1' : min(acc1.skill(skill, 'experience'), LEVEL_99_XP)} for skill in acc1.getSkillsGenerator()])
    df_user2 = pd.DataFrame([{"skill": skill, "level2": acc2.skill(skill, 'level'), "xp2": acc2.skill(skill, 'experience'), 'xp_to-max2' : min(acc2.skill(skill, 'experience'), LEVEL_99_XP)} for skill in acc2.getSkillsGenerator()])

    df_user1 = df_user1.sort_values("skill")
    df_user2 = df_user2.sort_values("skill")

    df_user1_display = df_user1[["skill", "level1", "xp1"]].copy()
    df_user2_display = df_user2[["skill", "level2", "xp2"]].copy()

    df_user1_display["xp1"] = df_user1_display["xp1"].apply(lambda x: f"{x:,}")
    df_user2_display["xp2"] = df_user2_display["xp2"].apply(lambda x: f"{x:,}")

    diff = pd.merge(df_user1, df_user2, on="skill")
    diff['Level Diff'] = diff['level1'] - diff['level2']
    diff['xp_diff'] = diff['xp1'] - diff['xp2']
    diff['xp_per_hr'] = diff['skill'].map(rates)
    diff['EXP To Max Diff'] = diff['xp_to-max1'] - diff['xp_to-max2']
    diff['hours_diff'] = diff['EXP To Max Diff'] / diff['xp_per_hr']


    df_user1_display.rename(columns={'level1': user1 + "'s Level", 'xp1': user1 + "'s Exp"}, inplace=True)
    df_user2_display.rename(columns={'level2': user2 + "'s Level", 'xp2': user2 + "'s Exp"}, inplace=True)

    display_diff = diff[['Level Diff','EXP To Max Diff','hours_diff', 'skill']]
    total_hours = display_diff['hours_diff'].sum().round()
    display_diff['EXP To Max Diff'] = display_diff['EXP To Max Diff'].apply(lambda x: f"{x:,}")
    #display_diff['Hours Ahead/Behind'] = display_diff['hours_diff'].apply(lambda x: f"{x:,.2f}")

    df_out = df_user1_display.merge(df_user2_display, on="skill").merge(display_diff, on="skill")
    df_out.rename(columns={'skill': 'Skill', 'hours_diff': 'Hours Ahead/Behind'}, inplace=True)
    df_out['Skill'] = df_out['Skill'].str.capitalize()

    st.dataframe(df_out.style.set_properties(**{'text-align': 'left'}), hide_index=True, width='stretch', height=875)



