import sys; sys.path.insert(0, 'D:\\forge')
from forge_prototype import load_exercises
exs = load_exercises()
targets = ['bodyweight/db', 'db/bodyweight', 'bodyweight/light db', 'band + strap']
for e in exs:
    et = e.equipment.lower().replace(' ','')
    if any(t in et for t in targets):
        print(f'{e.name:40s} eq="{e.equipment}" lv={e.min_equip_level()} bw={e.equip_ok(0)}')
