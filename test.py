from OSRSBytes import Hiscores

user1 = Hiscores('Icy Tires')

print(user1.skill('sailing', 'level'))

for skill in user1.getSkillsGenerator():
    print(skill)