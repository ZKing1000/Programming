import classes, items

def inventory_Init(inventory):
    inventory.add_Item('Copper Longsword', 1)
    inventory.add_Item('Tanto',1)
    inventory.add_Item('Dragonscale Helm', 1)
    inventory.add_Item('Dragonscale Vest', 1)
    inventory.add_Item('Dragonscale Leggings', 1)
    inventory.add_Item('Dragonscale Gloves', 1)
    inventory.add_Item('Dragonscale Boots', 1)
    inventory.add_Item('Rose Amulet', 1)
    inventory.add_Item('Potion', 10)
    inventory.add_Item('Ether', 5)
    inventory.add_Item('Copper Buckler', 1)
    inventory.add_Item('Seashell', 1)
    
def magic_Init(party):
    party[1].magic.add_Spell('Fire I')
    party[1].magic.add_Spell('Ice I')
    party[1].magic.add_Spell('Lightning I')
    party[1].magic.add_Spell('Wind I')
    party[1].magic.add_Spell('Fire II')
    party[1].magic.add_Spell('Ice II')
    party[1].magic.add_Spell('Lightning II')
    party[1].magic.add_Spell('Wind II')
    party[1].magic.add_Spell('Fire III')
    party[1].magic.add_Spell('Ice III')
    party[1].magic.add_Spell('Lightning III')
    party[1].magic.add_Spell('Wind III')
    party[1].magic.add_Spell('Heal I')
    party[1].magic.add_Spell('Heal II')
    party[1].magic.add_Spell('Heal III')
    party[1].magic.add_Spell('Life I')
    party[1].magic.add_Spell('Life II')
    party[1].magic.add_Spell('Life Wave')
    party[1].magic.add_Spell('Strength+')
    party[1].magic.add_Spell('Strength-')
    party[1].magic.add_Spell('Dexterity+')
    party[1].magic.add_Spell('Dexterity-')
    party[1].magic.add_Spell('Agility+')
    party[1].magic.add_Spell('Agility-')
    party[1].magic.add_Spell('Speed+')
    party[1].magic.add_Spell('Speed-')
    party[1].magic.add_Spell('Intelligence+')
    party[1].magic.add_Spell('Intelligence-')
    party[1].magic.add_Spell('Wisdom+')
    party[1].magic.add_Spell('Wisdom-')
    party[1].magic.add_Spell('Defense+')
    party[1].magic.add_Spell('Defense-')
    party[1].magic.add_Spell('Mag Defense+')
    party[1].magic.add_Spell('Mag Defense-')

def equip_Init(index, inventory):
    tempdict = {}

    if index == 1:
        temp = items.get_Item('Dagger')
        tempdict['main'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Dagger')
        tempdict['offh'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Hat')
        tempdict['head'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Doublet')
        tempdict['body'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Trousers')
        tempdict['legs'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Halfgloves')
        tempdict['hand'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Shoes')
        tempdict['feet'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc1'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc2'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc3'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
    elif index == 2:
        temp = items.get_Item('Light Staff')
        tempdict['main'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['offh'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Hat')
        tempdict['head'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Doublet')
        tempdict['body'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Trousers')
        tempdict['legs'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Halfgloves')
        tempdict['hand'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Shoes')
        tempdict['feet'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc1'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc2'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc3'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
    elif index == 3:
        temp = items.get_Item('Copper Longsword')
        tempdict['main'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['offh'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Leather Helm')
        tempdict['head'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Leather Vest')
        tempdict['body'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Leather Leggings')
        tempdict['legs'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Leather Gloves')
        tempdict['hand'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Leather Boots')
        tempdict['feet'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc1'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc2'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc3'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
    elif index == 4:
        temp = items.get_Item('Dagger')
        tempdict['main'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['offh'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Hat')
        tempdict['head'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Doublet')
        tempdict['body'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Trousers')
        tempdict['legs'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Halfgloves')
        tempdict['hand'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Nettled Shoes')
        tempdict['feet'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc1'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc2'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
        temp = items.get_Item('Empty')
        tempdict['acc3'] = temp
        inventory.add_Item(temp['name'],1)
        inventory.rem_Avail(temp['name'],1)
        
    return tempdict

def equip_Avail_Init(index):
    tempdict = {}
    if index == 1:
        tempdict['main'] = ['Dagger','1H Sword','1H Axe','Bow']
        tempdict['offh'] = ['Dagger','1H Sword','1H Axe','Light Shield','Heavy Shield']
        tempdict['head'] = ['Light Head Armor', 'Medium Head Armor', 'Heavy Head Armor']
        tempdict['body'] = ['Light Body Armor', 'Medium Body Armor', 'Heavy Body Armor']
        tempdict['legs'] = ['Light Leg Armor', 'Medium Leg Armor', 'Heavy Leg Armor']
        tempdict['hand'] = ['Light Hand Armor', 'Medium Hand Armor', 'Heavy Hand Armor']
        tempdict['feet'] = ['Light Feet Armor', 'Medium Feet Armor', 'Heavy Feet Armor']
        tempdict['acc'] = ['Accessories1','Accessories2']
    elif index == 2:
        tempdict['main'] = ['Dagger','1H Sword','1H Axe','Staff','Bow']
        tempdict['offh'] = ['Light Shield']
        tempdict['head'] = ['Light Head Armor', 'Medium Head Armor']
        tempdict['body'] = ['Light Body Armor', 'Medium Body Armor']
        tempdict['legs'] = ['Light Leg Armor', 'Medium Leg Armor']
        tempdict['hand'] = ['Light Leg Armor', 'Medium Hand Armor']
        tempdict['feet'] = ['Light Feet Armor', 'Medium Feet Armor']
        tempdict['acc'] = ['Accessories1','Accessories3']
    elif index == 3:
        tempdict['main'] = ['1H Sword','1H Axe','2H Sword','2H Axe','Bow']
        tempdict['offh'] = ['Light Shield', 'Heavy Shield']
        tempdict['head'] = ['Medium Head Armor', 'Heavy Head Armor']
        tempdict['body'] = ['Medium Body Armor', 'Heavy Body Armor']
        tempdict['legs'] = ['Medium Leg Armor', 'Heavy Leg Armor']
        tempdict['hand'] = ['Medium Hand Armor', 'Heavy Hand Armor']
        tempdict['feet'] = ['Medium Feet Armor', 'Heavy Feet Armor']
        tempdict['acc'] = ['Accessories1','Accessories3']
    elif index == 4:
        tempdict['main'] = ['Dagger','1H Sword','1H Axe','Spear','Bow']
        tempdict['offh'] = ['Light Shield']
        tempdict['head'] = ['Light Head Armor', 'Medium Head Armor']
        tempdict['body'] = ['Light Body Armor', 'Medium Body Armor']
        tempdict['legs'] = ['Light Leg Armor', 'Medium Leg Armor']
        tempdict['hand'] = ['Light Hand Armor', 'Medium Hand Armor']
        tempdict['feet'] = ['Light Feet Armor', 'Medium Feet Armor']
        tempdict['acc'] = ['Accessories1','Accessories4']
    return tempdict

def stat_Init(index):
    tempdict = {}
    if index == 1:
        tempdict['base'] = {
            'maxhp': 100.00,'maxmp': 50.00,
            'str': 10.00,'dex': 11.00,
            'agi': 11.00,'spd': 11.00,
            'int': 9.00,'wsd': 8.00,
            'lck': 8.00
        }
        tempdict['mult'] = {
            'maxhp': 1.0,'maxmp': 0.9,
            'str': 1.0,'dex': 1.1,
            'agi': 1.1,'spd': 1.1,
            'int': 0.9,'wsd': 0.9,
            'lck': 0.9
        }
        tempdict['curr'] = {
            'lvl': 1,
            'hp': 40,'maxhp': 100,
            'mp': 40,'maxmp': 50,
            'str': 10,'dex': 11,
            'agi': 11,'spd': 10,
            'int': 9,'wsd': 8,
            'lck': 8,'energy': 0,
            'exp': 0,'exn': 10,
            'ext': 0,
            'm_fire': 0, 'm_ice': 0,
            'm_wind': 0, 'm_lightning': 0,
            'd_fire': 0, 'd_ice': 0,
            'd_wind': 0, 'd_lightning': 0,
            'pow': 10,'mpow': 9,
            'def': 0,'mdef': 0
        }
    elif index == 2:
        tempdict['base'] = {
            'maxhp': 90.00,'maxmp': 70.00,
            'str': 7.00,'dex': 8.00,
            'agi': 0.90,'spd': 12.00,
            'int': 13.00,'wsd': 10.00,
            'lck': 9.00
        }
        tempdict['mult'] = {
            'maxhp': 0.9,'maxmp': 1.2,
            'str': 0.8,'dex': 0.8,
            'agi': 0.9,'spd': 1.1,
            'int': 1.2,'wsd': 1.1,
            'lck': 1.0
        }
        tempdict['curr'] = {
            'lvl': 1,
            'hp': 80,'maxhp': 90,
            'mp': 40,'maxmp':70,
            'str': 7,'dex': 8,
            'agi': 9,'spd': 12,
            'int': 13,'wsd': 10,
            'lck': 9,'energy': 0,
            'exp': 0,'exn': 10,
            'ext': 0,
            'm_fire': 0, 'm_ice': 0,
            'm_wind': 0, 'm_lightning': 0,
            'd_fire': 0, 'd_ice': 0,
            'd_wind': 0, 'd_lightning': 0,
            'pow': 7,'mpow': 13,
            'def': 0,'mdef': 0
        }
    elif index == 3:
        tempdict['base'] = {
            'maxhp': 110.00,'maxmp': 40.00,
            'str': 12.00,'dex': 9.00,
            'agi': 10.00,'spd': 9.00,
            'int': 7.00,'wsd': 6.00,
            'lck': 8.00
        }
        tempdict['mult'] = {
            'maxhp': 1.1,'maxmp': 0.80,
            'str': 1.15,'dex': 1.12,
            'agi': 1.05,'spd': 1.05,
            'int': 0.79,'wsd': 0.78,
            'lck': 0.81
        }
        tempdict['curr'] = {
            'lvl': 1,
            'hp': 110,'maxhp': 110,
            'mp': 40,'maxmp': 40,
            'str': 12,'dex': 9,
            'agi': 10,'spd': 9,
            'int': 7,'wsd': 6,
            'lck': 8,'energy': 0,
            'exp': 0,'exn': 10,
            'ext': 0,
            'm_fire': 0, 'm_ice': 0,
            'm_wind': 0, 'm_lightning': 0,
            'd_fire': 0, 'd_ice': 0,
            'd_wind': 0, 'd_lightning': 0,
            'pow': 12,'mpow': 7,
            'def': 0,'mdef': 0
        }
    elif index == 4:
        tempdict['base'] = {
            'maxhp': 100.00,'maxmp': 40.00,
            'str': 10.00,'dex': 10.00,
            'agi': 10.00,'spd': 10.00,
            'int': 7.00,'wsd': 6.00,
            'lck': 8.00
        }
        tempdict['mult'] = {
            'maxhp': 1.05,'maxmp': 0.85,
            'str': 1.15,'dex': 1.08,
            'agi': 1.09,'spd': 1.05,
            'int': 0.75,'wsd': 0.75,
            'lck': 0.85
        }
        tempdict['curr'] = {
            'lvl': 1,
            'hp': 100,'maxhp': 100,
            'mp': 40,'maxmp': 40,
            'str': 10,'dex': 10,
            'agi': 10,'spd': 10,
            'int': 7,'wsd': 6,
            'lck': 8,'energy': 0,
            'exp': 0,'exn': 10,
            'ext': 0,
            'm_fire': 0, 'm_ice': 0,
            'm_wind': 0, 'm_lightning': 0,
            'd_fire': 0, 'd_ice': 0,
            'd_wind': 0, 'd_lightning': 0,
            'pow': 10,'mpow': 7,
            'def': 0,'mdef': 0
        }
    return tempdict

'''
for targetting info below:
    TARGET_TYPE
    'single' = one target
    'mult' = one or multiple targets
    'all' = all targets
    TARGET_LIMIT
    'self' = self only
    'not self' = allies only, but not self
    'ally' = allies only
    'enemy' = enemies only
    'any' = either allies or enemies
    TARGET_DEFAULT
    'ally'
    'enemy'
'''

def init_Spells():
    def basic_spell(name, type, effect_name, effect_value, cost, target_type, target_limit, target_default, desc):
        temp_list = list()
        temp_dict = {effect_name: effect_value}
        temp_list.append(temp_dict)
        temp = {
            'name': name,
            'type': type,
            'effect': temp_list,
            'cost': cost,
            'target_type': target_type,
            'target_limit': target_limit,
            'target_default': target_default,
            'desc': desc
        }
        return temp

    def add_spell_effect(spell, effect_name, effect_value):
        temp_dict = {effect_name: effect_value}
        spell['effect'].append(temp_dict)

    temp_dict = dict()

    #basic elemental spells
    temp_dict['Fire I'] = basic_spell('Fire I', 'damage', 'fire', 50, 12, 'mult', 'any', 'enemy', 'A basic fire spell')
    temp_dict['Ice I'] = basic_spell('Ice I', 'damage', 'ice', 50, 12, 'mult', 'any', 'enemy', 'A basic ice spell')
    temp_dict['Lightning I'] = basic_spell('Lightning I', 'damage', 'lightning', 50, 12, 'mult', 'any', 'enemy', 'A basic lightning spell')
    temp_dict['Wind I'] = basic_spell('Wind I', 'damage', 'wind', 50, 12, 'mult', 'any', 'enemy', 'A basic wind spell')
    temp_dict['Fire II'] = basic_spell('Fire II', 'damage', 'fire', 250, 40, 'mult', 'any', 'enemy', 'A powerful fire spell')
    temp_dict['Ice II'] = basic_spell('Ice II', 'damage', 'ice', 250, 40, 'mult', 'any', 'enemy', 'A powerful ice spell')
    temp_dict['Lightning II'] = basic_spell('Lightning II', 'damage', 'lightning', 250, 40, 'mult', 'any', 'enemy', 'A powerful lightning spell')
    temp_dict['Wind II'] = basic_spell('Wind II', 'damage', 'wind', 250, 40, 'mult', 'any', 'enemy', 'A powerful wind spell')
    temp_dict['Fire III'] = basic_spell('Fire III', 'damage', 'fire', 1000, 90, 'mult', 'any', 'enemy', 'A devastating fire spell')
    temp_dict['Ice III'] = basic_spell('Ice III', 'damage', 'ice', 1000, 90, 'mult', 'any', 'enemy', 'A devastating ice spell')
    temp_dict['Lightning III'] = basic_spell('Lightning III', 'damage', 'lightning', 1000, 90, 'mult', 'any', 'enemy', 'A devastating lightning spell')
    temp_dict['Wind III'] = basic_spell('Wind III', 'damage', 'wind', 1000, 90, 'mult', 'any', 'enemy', 'A devastating wind spell')

    #basic healing spells
    temp_dict['Heal I'] = basic_spell('Heal I', 'healing', 'heal', 50, 12, 'mult', 'any', 'ally', 'A basic healing spell')
    temp_dict['Heal II'] = basic_spell('Heal II', 'healing', 'heal', 250, 40, 'mult', 'any', 'ally', 'A powerful healing spell')
    temp_dict['Heal III'] = basic_spell('Heal III', 'healing', 'heal', 1000, 90, 'mult', 'any', 'ally', 'A miraculous healing spell')
    temp_dict['Life I'] = basic_spell('Life I', 'healing', 'revive', 50, 25, 'single', 'any', 'ally', 'Brings a character back to life with half health.')
    temp_dict['Life II'] = basic_spell('Life II', 'healing', 'revive', 100, 100, 'single', 'any', 'ally', 'Brings a character back to life with full health.')
    temp_dict['Life Wave'] = basic_spell('Life Wave', 'healing', 'revive', 50, 200, 'all', 'ally', 'ally', 'Brings all characters back to life with half health. Only useable in battle.')

    #basic utility spells
    temp_dict['Strength+'] = basic_spell('Strength+', 'utility', 'enhance', 'str', 10, 'single', 'any', 'ally', 'Increases the strength of the target.')
    temp_dict['Strength-'] = basic_spell('Strength-', 'utility', 'cripple', 'str', 10, 'single', 'any', 'enemy', 'Decreases the strength of the target.')
    temp_dict['Dexterity+'] = basic_spell('Dexterity+', 'utility', 'enhance', 'dex', 10, 'single', 'any', 'ally', 'Increases the dexterity of the target.')
    temp_dict['Dexterity-'] = basic_spell('Dexterity-', 'utility', 'cripple', 'dex', 10, 'single', 'any', 'enemy', 'Decreases the dexterity of the target.')
    temp_dict['Agility+'] = basic_spell('Agility+', 'utility', 'enhance', 'agi', 10, 'single', 'any', 'ally', 'Increases the agility of the target.')
    temp_dict['Agility-'] = basic_spell('Agility-', 'utility', 'cripple', 'agi', 10, 'single', 'any', 'enemy', 'Decreases the agility of the target.')
    temp_dict['Speed+'] = basic_spell('Speed+', 'utility', 'enhance', 'spd', 10, 'single', 'any', 'ally', 'Increases the speed of the target.')
    temp_dict['Speed-'] = basic_spell('Speed-', 'utility', 'cripple', 'spd', 10, 'single', 'any', 'enemy', 'Decreases the speed of the target.')
    temp_dict['Intelligence+'] = basic_spell('Intelligence+', 'utility', 'enhance', 'int', 10, 'single', 'any', 'ally', 'Increases the intelligence of the target.')
    temp_dict['Intelligence-'] = basic_spell('Intelligence-', 'utility', 'cripple', 'int', 10, 'single', 'any', 'enemy', 'Decreases the intelligence of the target.')
    temp_dict['Wisdom+'] = basic_spell('Wisdom+', 'utility', 'enhance', 'wsd', 10, 'single', 'any', 'ally', 'Increases the wisdom of the target.')
    temp_dict['Wisdom-'] = basic_spell('Wisdom-', 'utility', 'cripple', 'wsd', 10, 'single', 'any', 'enemy', 'Decreases the wisdom of the target.')
    temp_dict['Defense+'] = basic_spell('Defense+', 'utility', 'enhance', 'def', 10, 'single', 'any', 'ally', 'Increases the defense of the target.')
    temp_dict['Defense-'] = basic_spell('Defense-', 'utility', 'cripple', 'def', 10, 'single', 'any', 'enemy', 'Decreases the defense of the target.')
    temp_dict['Mag Defense+'] = basic_spell('Mag Defense+', 'utility', 'enhance', 'mdef', 10, 'single', 'any', 'ally', 'Increases the magic defense of the target.')
    temp_dict['Mag Defense-'] = basic_spell('Mag Defense-', 'utility', 'cripple', 'mdef', 10, 'single', 'any', 'enemy', 'Decreases the magic defense of the target.')

    return temp_dict

def init_Skills(equip_avail):
    def basic_skill(name, weapon, level, type, effect_name, effect_value, cost, curr_prog, total_prog, target_type, target_limit, target_default, desc):
        temp_list = list()
        temp_dict = {effect_name: effect_value}
        temp_list.append(temp_dict)
        temp = {
            'name': name,
            'weapon': weapon,
            'level': level,
            'type': type,
            'effect': temp_list,
            'cost': cost,
            'progress': curr_prog,
            'progress_cap': total_prog,
            'target_type': target_type,
            'target_limit': target_limit,
            'target_default': target_default,
            'desc': desc
        }
        return temp

    def add_skill_effect(skill, effect_name, effect_value):
        temp_dict = {effect_name: effect_value}
        skill['effect'].append(temp_dict)

    tempdict = {}

    if 'Dagger' in equip_avail['main']:
        tempdict['Knife Twist'] = basic_skill('Knife Twist', 'Dagger', 1, 'damage', 'physical', 20, 15, 0, 100, 'single', 'enemy', 'enemy', 'Inflicts a bleeding wound')
        add_skill_effect(tempdict['Knife Twist'], 'bleed', 10)
    if '1H Sword' in equip_avail['main']:
        tempdict['Double Cut'] = basic_skill('Double cut', '1H Sword', 1, 'damage', 'physical', 15, 20, 0, 100, 'single', 'enemy', 'enemy', 'Two is better than one.')
        add_skill_effect(tempdict['Double Cut'], 'physical', 15)
    if '2H Sword' in equip_avail['main']:
        tempdict['Heavy Blow'] = basic_skill('Heavy Blow', '2H Sword', 1, 'damage', 'physical', 40, 20, 0, 100, 'single', 'enemy', 'enemy', 'A full-force slash, ignores some defense.')
        add_skill_effect(tempdict['Heavy Blow'], 'ignore def', 10)
    if '1H Axe' in equip_avail['main']:
        tempdict['Cleave'] = basic_skill('Cleave', '1H Axe', 1, 'damage', 'physical', 30, 15, 0, 100, 'single', 'enemy', 'enemy', 'A powerful blow.')
    if '2H Axe' in equip_avail['main']:
        tempdict['Heavy Cleave'] = basic_skill('Heavy Cleave', '2H Axe', 1, 'damage', 'physical', 40, 20, 0, 100, 'single', 'enemy', 'enemy', 'A very powerful blow, ignores some defense.')
        add_skill_effect(tempdict['Heavy Blow'], 'ignore def', 10)
    if 'Staff' in equip_avail['main']:
        tempdict['Bash'] = basic_skill('Bash', 'Staff', 1, 'damage', 'physical', 15, 15, 0, 100, 'single', 'enemy', 'enemy', 'Use your staff to brain someone, might cause confusion.')
        add_skill_effect(tempdict['Bash'], 'confuse', 10)
    if 'Spear' in equip_avail['main']:
        tempdict['Double Thrust'] = basic_skill('Double Thrust', 'Spear', 1, 'damage', 'physical', 20, 20, 0, 100, 'single', 'enemy', 'enemy', 'Try and hit the same spot twice.')
        add_skill_effect(tempdict['Double Thrust'], 'physical', 20)
    if 'Bow' in equip_avail['main']:
        tempdict['Dual Shot'] = basic_skill('Dual Shot', 'Bow', 1, 'damage', 'physical', 15, 20, 0, 100, 'single', 'enemy', 'enemy', 'A skilled shot with two arrows.')
        add_skill_effect(tempdict['Dual Shot'], 'physical', 15)
    return tempdict