#!/usr/bin/env python
def get_Item(name):
# START WEAPONS
    if name == 'Dagger':
        temp = {
            'name': 'Dagger',
            'type': 'Dagger',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 5,
            'mpow': 3,
            'def': 0,
            'mdef': 0,
            'desc': "A cheap copper dagger.",
            'value': 100
        }
    elif name == 'Tanto':
        temp = {
            'name': 'Tanto',
            'type': 'Dagger',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 5,
            'agi': 2,
            'spd': 3,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 45,
            'mpow': 20,
            'def': 0,
            'mdef': 0,
            'desc': "Razor sharp and light as a feather.",
            'value': 15000
        }
    elif name == 'Copper Longsword':
        temp = {
            'name': 'Copper Longsword',
            'type': '1H Sword',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 8,
            'mpow': 4,
            'def': 0,
            'mdef': 0,
            'desc': 'Long, but not very strong.',
            'value': 150
        }
    elif name == 'Light Staff':
        temp = {
            'name': 'Light Staff',
            'type': 'Staff',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 5,
            'mpow': 10,
            'def': 0,
            'mdef': 0,
            'desc': 'A small wooden staff.',
            'value': 200
        }
# START SHIELDS
    elif name == 'Copper Buckler':
        temp = {
            'name': 'Copper Buckler',
            'type': 'Light Shield',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 3,
            'mdef': 1,
            'desc': 'A small copper shield.',
            'value': 150
        }
# START ARMOR
    elif name == 'Nettled Hat':
        temp = {
            'name': 'Nettled Hat',
            'type': 'Light Head Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 1,
            'mdef': 1,
            'desc': 'A plain hat made of woven nettles.',
            'value': 75
        }
    elif name == 'Nettled Doublet':
        temp = {
            'name': 'Nettled Doublet',
            'type': 'Light Body Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 3,
            'mdef': 3,
            'desc': 'A plain doublet made of woven nettles.',
            'value': 150
        }
    elif name == 'Nettled Trousers':
        temp = {
            'name': 'Nettled Trousers',
            'type': 'Light Leg Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 2,
            'mdef': 2,
            'desc': 'A pair of leggings made of woven nettles.',
            'value': 115
        }
    elif name == 'Nettled Halfgloves':
        temp = {
            'name': 'Nettled Halfgloves',
            'type': 'Light Hand Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 1,
            'mdef': 1,
            'desc': 'A pair of gloves made of woven nettles.',
            'value': 75
        }
    elif name == 'Nettled Shoes':
        temp = {
            'name': 'Nettled Shoes',
            'type': 'Light Feet Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 1,
            'mdef': 1,
            'desc': 'A pair of shoes made of woven nettles.',
            'value': 75
        }
    elif name == 'Leather Helm':
        temp = {
            'name': 'Leather Helm',
            'type': 'Medium Head Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 2,
            'mdef': 1,
            'desc': 'A plain helm made of leather.',
            'value': 100
        }
    elif name == 'Leather Vest':
        temp = {
            'name': 'Leather Vest',
            'type': 'Medium Body Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 5,
            'mdef': 2,
            'desc': 'A vest made of leather.',
            'value': 200
        }
    elif name == 'Leather Leggings':
        temp = {
            'name': 'Leather Leggings',
            'type': 'Medium Leg Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 3,
            'mdef': 1,
            'desc': 'A pair of leather leggings.',
            'value': 150
        }
    elif name == 'Leather Gloves':
        temp = {
            'name': 'Leather Gloves',
            'type': 'Medium Hand Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 2,
            'mdef': 1,
            'desc': 'A pair of leather gloves.',
            'value': 100
        }
    elif name == 'Leather Boots':
        temp = {
            'name': 'Leather Boots',
            'type': 'Medium Feet Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 2,
            'mdef': 1,
            'desc': 'A plain pair of leather boots.',
            'value': 100
        }
    elif name == 'Dragonscale Helm':
        temp = {
            'name': 'Dragonscale Helm',
            'type': 'Medium Head Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 3,
            'agi': 4,
            'spd': 3,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 16,
            'mdef':14,
            'desc': "Helm made from a black dragon's scales.",
            'value': 10000
        }
    elif name == 'Dragonscale Vest':
        temp = {
            'name': 'Dragonscale Vest',
            'type': 'Medium Body Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 5,
            'agi': 6,
            'spd': 5,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 21,
            'mdef':19,
            'desc': "Vest made from a black dragon's scales.",
            'value': 20000
        }
    elif name == 'Dragonscale Leggings':
        temp = {
            'name': 'Dragonscale Leggings',
            'type': 'Medium Leg Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 4,
            'agi': 4,
            'spd': 5,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 19,
            'mdef':17,
            'desc': "Leggings made from a black dragon's scales.",
            'value': 15000
        }
    elif name == 'Dragonscale Gloves':
        temp = {
            'name': 'Dragonscale Gloves',
            'type': 'Medium Hand Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 3,
            'agi': 2,
            'spd': 2,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 15,
            'mdef':13,
            'desc': "Gloves made from a black dragon's scales.",
            'value': 10000
        }
    elif name == 'Dragonscale Boots':
        temp = {
            'name': 'Dragonscale Boots',
            'type': 'Medium Feet Armor',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 2,
            'agi': 2,
            'spd': 3,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 15,
            'mdef':13,
            'desc': "Boots made from a black dragon's scales.",
            'value': 10000
        }
# START GET ACCESSORIES
    elif name == 'Seashell':
        temp = {
            'name': 'Seashell',
            'type': 'Accessory',
            'maxhp': 10,
            'maxmp': 10,
            'str': 1,
            'dex': 1,
            'agi': 1,
            'spd': 1,
            'int': 1,
            'wsd': 1,
            'lck': 1,
            'pow': 1,
            'mpow': 1,
            'def': 1,
            'mdef': 1,
            'desc': 'Sounds like the ocean.',
            'value': 200
        }
    elif name == 'Rose Amulet':
        temp = {
            'name': 'Rose Amulet',
            'type': 'Accessory',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 1,
            'lck': 5,
            'pow': 0,
            'mpow': 1,
            'def': 0,
            'mdef': 0,
            'desc': "Rose's amulet, given to her a long time ago.",
            'value': 0
        }
    elif name == 'Fang Necklace':
        temp = {
            'name': 'Fang Necklace',
            'type': 'Accessory',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'def': 1,
            'mdef': 1,
            'desc': "Made from a wolf's tooth.",
            'value': 200
        }
    elif name == 'Shiny Rock':
        temp = {
            'name': 'Shiny Rock',
            'type': 'Accessory',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 3,
            'int': 0,
            'wsd': 0,
            'lck': 5,
            'pow': 0,
            'mpow': 0,
            'def': 0,
            'mdef': 0,
            'desc': 'Oooh, shiny!',
            'value': 0
        }
# START GET CONSUMABLES
    elif name == 'Potion':
        temp = {
            'name': 'Potion',
            'effect': list(),
            'target_type': 'single',
            'target_limit': 'all',
            'target_default': 'ally',
            'desc': 'Heals 50 HP for a single character.',
            'value': 50
        }
        temp['effect'].append(dict({'heal hp': 50}))
    elif name == 'Super Potion':
        temp = {
            'name': 'Super Potion',
            'effect': list(),
            'target_type': 'single',
            'target_limit': 'all',
            'target_default': 'ally',
            'desc': 'Heals 250 HP for a single character.',
            'value': 500
        }
        temp['effect'].append(dict({'heal hp': 250}))
    elif name == 'Ether':
        temp = {
            'name': 'Ether',
            'effect': list(),
            'target_type': 'single',
            'target_limit': 'all',
            'target_default': 'ally',
            'desc': 'Heals 100 MP for a single character.',
            'value': 500
        }
        temp['effect'].append(dict({'heal mp': 100}))
    elif name == 'Super Ether':
        temp = {
            'name': 'Super Ether',
            'effect': list(),
            'target_type': 'single',
            'target_limit': 'all',
            'target_default': 'ally',
            'desc': 'Heals 500 MP for a single character.',
            'value': 5000
        }
        temp['effect'].append(dict({'heal mp': 500}))
    else:
        temp = {
            'name': 'Empty',
            'type': 'Empty',
            'maxhp': 0,
            'maxmp': 0,
            'str': 0,
            'dex': 0,
            'agi': 0,
            'spd': 0,
            'int': 0,
            'wsd': 0,
            'gsp': 0,
            'def': 0,
            'mdef': 0,
            'res': 0,
            'lck': 0,
            'pow': 0,
            'mpow': 0,
            'desc': 'None',
            'value': 0
        }
    return temp

def get_Type(name): #check to see the category an item belongs to
    daggers = ['Dagger','Rondel','Stiletto',
               'Dirk','Kukri','Tanto']
    onehswords = ['Copper Longsword','Bronze Longsword','Iron Longsword',
                  'Steel Longsword','Jeweled Longsword','Obsidian Longsword']
    staves = ['Light Staff','Fire Staff','Ice Staff','Lightning Staff','Wind Staff',
              'Twisted Staff','Searing Staff','Frozen Staff','Shock Staff','Gale Staff',
              'Jeweled Staff','Ancient Staff']
    lshields = ['Copper Buckler','Bronze Buckler','Iron Bucker',
                'Steel Buckler','Jeweled Buckler','Obsidian Buckler']
    lhelm = ['Nettled Hat','Linen Hat','Cotton Hat',
              'Wool Hat','Silk Hat','Cashmere Hat']
    mhelm = ['Leather Helm','Thick Leather Helm','Lizardshell Helm',
              'Beetleshell Helm','Scorpionshell Helm','Dragonscale Helm']
    lbody = ['Nettled Doublet','Linen Doublet','Cotton Doublet',
              'Wool Doublet','Silk Doublet','Cashmere Doublet']
    mbody = ['Leather Vest','Thick Leather Vest','Lizardshell Vest',
              'Beetleshell Vest','Scorpionshell Vest','Dragonscale Vest']
    llegs = ['Nettled Trousers','Linen Trousers','Cotton Trousers',
              'Wool Trousers','Silk Trousers','Cashmere Trousers']
    mlegs = ['Leather Leggings','Thick Leather Leggings','Lizardshell Leggings',
              'Beetleshell Leggings','Scorpionshell Leggings','Dragonscale Leggings']
    lhand = ['Nettled Halfgloves','Linen Halfgloves','Cotton Halfgloves',
              'Wool Halfgloves','Silk Halfgloves','Cashmere Halfgloves']
    mhand = ['Leather Gloves','Thick Leather Gloves','Lizardshell Gloves',
              'Beetleshell Gloves','Scorpionshell Gloves','Dragonscale Gloves']
    lfeet = ['Nettled Shoes','Linen Shoes','Cotton Shoes',
              'Wool Shoes','Silk Shoes','Cashmere Shoes']
    mfeet = ['Leather Boots','Thick Leather Boots','Lizardshell Boots',
              'Beetleshell Boots','Scorpionshell Boots','Dragonscale Boots']
    acc1 = ['Seashell','Fang Necklace']
    acc2 = ['Shiny Rock']
    acc3 = ['Rose Amulet']
    cons = ['Potion', 'Super Potion', 'Ether', 'Super Ether']
    
    if name in daggers:
        return 'Dagger'
    elif name in onehswords:
        return '1H Sword'
    elif name in staves:
        return 'Staff'
    elif name in lshields:
        return 'Light Shield'
    elif name in lhelm:
        return 'Light Head Armor'
    elif name in lbody:
        return 'Light Body Armor'
    elif name in llegs:
        return 'Light Leg Armor'
    elif name in lhand:
        return 'Light Hand Armor'
    elif name in lfeet:
        return 'Light Feet Armor'
    elif name in mhelm:
        return 'Medium Head Armor'
    elif name in mbody:
        return 'Medium Body Armor'
    elif name in mlegs:
        return 'Medium Leg Armor'
    elif name in mhand:
        return 'Medium Hand Armor'
    elif name in mfeet:
        return 'Medium Feet Armor'
    elif name in acc1:
        return 'Accessories1'
    elif name in acc2:
        return 'Accessories2'
    elif name in acc3:
        return 'Accessories3'
    elif name in cons:
        return 'Consumable'
    else:
        return 'Empty'

def get_Cat(name):
    temp_type = get_Type(name)
    if temp_type == 'Consumable':
        return 'CONS'
    elif temp_type in ['Accessories1','Accessories2','Accessories3',
                       'Accessories4','Accessories5','Accessories6']:
        return 'ACC'
    elif temp_type in ['Dagger','1H Sword','1H Axe',
                     '2H Sword','2H Axe','Bow',
                     'Staff','Light Shield','Heavy Shield']:
        return 'WEAP'
    elif temp_type in ['Light Head Armor','Light Body Armor','Light Leg Armor',
                       'Light Hand Armor','Light Feet Armor','Medium Head Armor',
                       'Medium Body Armor','Medium Leg Armor','Medium Hand Armor',
                       'Medium Feet Armor','Heavy Head Armor','Heavy Body Armor',
                       'Heavy Leg Armor','Heavy Hand Armor','Heavy Feet Armor']:
        return 'ARM'
    else:
        return None