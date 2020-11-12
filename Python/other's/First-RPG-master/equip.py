#!/usr/bin/env python
import items, classes

def equip_Item(char, inventory, pos, item="Empty", object="Null"):
    if object == "Null":
        new_equip = items.get_Item(item)
    else:
        new_equip = object

    if pos == 'main':
        cur_equip = char.equip['main']
        char.equip['main'] = new_equip
        char.skills.change_Useable(char, 'main', new_equip, cur_equip)
        if new_equip['type'] in ['Staff', '2H Sword', '2H Axe', 'Spear', 'Bow']:
            equip_Item(char, inventory, 'offh', 'Empty')
    elif pos == 'offh':
        cur_equip = char.equip['offh']
        char.equip['offh'] = new_equip
        char.skills.change_Useable(char, 'offh', new_equip, cur_equip)
        if char.equip['main']['type'] in ['Staff', '2H Sword', '2H Axe', 'Spear', 'Bow'] and new_equip['name'] != "Empty":
            equip_Item(char, inventory, 'main', 'Empty')
    else:
        cur_equip = char.equip[pos]
        char.equip[pos] = new_equip

    inventory.rem_Avail(item,1)
    inventory.add_Avail(cur_equip['name'],1)

    a = 'curr'
    for each in ('maxhp','maxmp','str','dex','agi',
                 'spd','int','wsd','lck','pow','mpow',
                 'def','mdef'):
        if each == 'str':
            char.stats[a][each] -= int(cur_equip[each])
            char.stats[a]['pow'] -= int(cur_equip[each])
            char.stats[a][each] += int(new_equip[each])
            char.stats[a]['pow'] += int(new_equip[each])
        elif each == 'int':
            char.stats[a][each] -= int(cur_equip[each])
            char.stats[a]['mpow'] -= int(cur_equip[each])
            char.stats[a][each] += int(new_equip[each])
            char.stats[a]['mpow'] += int(new_equip[each])
        else:
            char.stats[a][each] -= int(cur_equip[each])
            char.stats[a][each] += int(new_equip[each])

def load_Stats(char):
    for each in [char.equip['main'],char.equip['offh'],char.equip['head'],char.equip['body'],char.equip['legs'],char.equip['hand'],char.equip['feet'],char.equip['acc1'],char.equip['acc2'],char.equip['acc3']]:
        for stat in ['maxhp','maxmp','str','dex','agi','spd','int','wsd','pow','mpow','def','mdef']:
            char.stats['curr'][stat] += int(each[stat])