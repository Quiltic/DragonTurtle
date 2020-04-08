#this is so that the IDE doesent yell at me for not having this in the file.
if __name__ == "__main__":  
    from bs4 import BeautifulSoup
    import requests
    import JTools as jt

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Monster Tools ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def findMonster(NAME = 'Dragon turtle'):
    '''
    Given a name it will give you basics on a monster and a url to its page
    findMonster(NAME = 'Dragon turtle'): gives basic stats and a url (dict)
    '''
    name = NAME.lower().replace(' ','%20') # no spaces only %20
    url = "https://roll20.net/compendium/dnd5e/"+name # url
    r  = requests.get(url) # get info
    data = r.text # get data
    soup = BeautifulSoup(data,features="lxml") # soup

    # this is if it is not appart of the normal stuff or non existant
    if ('You do not own' in str(soup)):
        print("Cant get creature: link given.")
        return(url)
    elif 'Page Not Found' in str(soup):
        print('Not found.')
        return(None)
    
    # proper looking name
    name = soup.find('h1',{'class':'page-title'}).get_text().replace('\n','').replace('\t','')

    # achual info lies
    top = soup.find('div',{"class":"col-md-12 attrList"})
    stuff = top.find_all('div')

    # basicly this does all the work it is in an unusual div structure but makes this work nicely
    Monster = {'Name': name,'url': url}
    for a in range(1,len(stuff)-1,4):
        Monster[stuff[a].get_text()] = stuff[a+1].get_text().replace('\n',' ').replace(' + ','+')

    
    return(Monster)



def cleanPrint(Monster):
    '''
    Prints out basic monster stuff
    cleanPrint(Monster): gives true or error: prints data/url
    '''
    if type(Monster) == str:
        print('Not found. Go to: {}'.format(Monster['url']))
        return('Not found. Go to: {}'.format(Monster['url']))
    elif Monster == None:
        print('Not found. No page.')
        return('Not found. No page.')
    print('For more go to: {}'.format(Monster['url']))
    
    
    print(Monster['Name'])
    print(Monster['Size']+Monster['Type']+':'+Monster['Alignment'])
    print()

    print('AC:'+Monster['AC'])
    print('HP:'+Monster['HP'])
    print('Speed:'+Monster['Speed'])
    print()

    print('STR','DEX','CON','INT','WIS','CHA')
    print(Monster['STR']+Monster['DEX']+Monster['CON']+Monster['INT']+Monster['WIS']+Monster['CHA'])
    print()

    # some have this some dont
    #print('Saving Throws:'+Monster['Saving Throws'])
    #print('Resistances:'+Monster['Resistances'])
    #print('Senses:'+Monster['Senses'])
    #print('Languages:'+Monster['Languages'])
    
    print('Challenge Rating:'+Monster['Challenge Rating'])
    print()
    print('For more go to: {}'.format(Monster['url']))
    return(True) # worked

if __name__ == "__main__":    
    name = "cat"
    cleanPrint(findMonster(name))
