# NOT USED

from JTools import find_all
spell = {'name': 'Ice Knife', 'school': 'Conjuration', 'cast': {'level': ' 1', 'casting time': '1 Action', 'range': '60 feet', 'components': 'S, M', 'duration': 'Instantaneous'}, 'does': '|n (a drop of water or piece of ice) |nYou create a shard of ice and fling it at one creature within range. Make a ranged spell attack against the target. On a hit, the target takes 1d10 piercing damage. Hit or miss, the shard then explodes. The target and each creature within 5 feet of the point where the ice exploded must succeed on a Dexterity saving throw or take 2d6 cold damage. |nAt Higher Levels. When you cast this spell using a spell slot of 2nd level or higher, the cold damage increases by 1d6 for each slot level above 1st. |n', 'page': 'Page: 19  from EE Players Companion      ', 'classes': ['Druid', 'Sorcerer', 'Wizard'], 'url': 'https://www.dnd-spells.com/spell/ice-knife'}
spell = {'name': 'Darkness', 'school': 'Evocation', 'cast': {'level': ' 2', 'casting time': '1 Action', 'range': '60 feet', 'components': 'V, M (bat fur and a drop of pitch or piece of coal)', 'duration': 'Concentration, up to 10 minutes'}, 'does': "|n Magical darkness spreads from a point you choose within range to fill a 15-foot radius sphere for the duration. |nThe darkness spreads around corners. A creature with darkvision can't see through this darkness, and nonmagical light can't illuminate it. |n|nIf the point you choose is on an object you are holding or one that isn't being worn or carried, the darkness emanates from the object and moves with it. Completely covering the source of the darkness with an opaque object, such as a bowl or a helm, blocks the darkness.|n|nIf any of this spell's area overlaps with an area of light created by a spell of 2nd level or lower, the spell that created the light is dispelled. |n", 'page': 'Page: 230  Players Handbook     ', 'classes': ['Sorcerer', 'Warlock', 'Wizard'], 'url': 'https://www.dnd-spells.com/spell/darkness'}
#spell = {'name': 'Fireball', 'school': 'Evocation', 'cast': {'level': ' 3', 'casting time': '1 Action', 'range': '150 feet', 'components': 'V, S, M (a tiny ball of bat guano and sulfur)', 'duration': 'Instantaneous'}, 'does': "|n A bright streak flashes from your pointing finger to a point you choose within range then blossoms with a low roar into an explosion of flame. |nEach creature in a 20-foot radius must make a Dexterity saving throw. A target takes 8d6 fire damage on a failed save, or half as much damage on a successful one. The fire spreads around corners. It ignites flammable objects in the area that aren't being worn or carried. |n    When you cast this spell using a spell slot of 4th level or higher, the damage increases by 1d6 for each slot level above 3rd.        ", 'page': 'Page: 241  Players Handbook     ', 'classes': ['Sorcerer', 'Wizard'], 'url': 'https://www.dnd-spells.com/spell/fireball'}

def OffenceSpell(spell):
    '''
    Given a spell (dict) it will try to give you its damage and other helpfull bits relting to casting a damage spell
    '''
    offencive = {'damage':[], 'type':'area', 'save':None, 'higherLvl':None}

    # get the damages and there types cold lightning pearcing ect
    places = find_all(spell['does'],'take')
    for a in places:
        p1 = spell['does'][a:].index(' ') # could be takes witch would leave an s
        p2 = spell['does'][a:].index(' damage')

        offencive['damage'] += [spell['does'][a+p1+1:p2+a].split(' ')]

    if len(offencive['damage']): # if it does no damage its not an offencive spell no need to do the rest
        try:
            # get the type of spell ie ranged melee something else
            place = spell['does'].index('spell attack') # not achualy needed
            offencive['type'] = 'ranged' if 'ranged' in spell['does'][:place] else 'melee' if 'melee' in spell['does'][:place] else 'NO IDEA'
            #print(tpe)
        except ValueError:
            #print('area?')
            pass
        except Exception as e:
            print('Spell attack error: {}'.format(e))


        try:
            # if it has a saving through
            place = spell['does'].index(' saving throw')
            offencive['save'] = spell['does'][find_all(spell['does'][:place],' ')[-1]+1:place]
        except ValueError:
            #print('no save')
            pass
        except Exception as e:
            print('Save throw error: {}'.format(e))

        try:
            # if it has a saving through
            place = spell['does'].index("increases by ")
            #print(place+13,spell['does'][place+13:].index(' ')+place+13)
            offencive['higherLvl'] = spell['does'][place+13:spell['does'][place+13:].index(' ')+place+13] # +13 is from "increases by "
        except ValueError:
            #print('no save')
            pass
        except Exception as e:
            print('Save throw error: {}'.format(e))


    print(offencive)
    return(offencive)