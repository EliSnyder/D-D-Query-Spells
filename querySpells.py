import csv
import re
import textwrap

def printDic(dic):
	keyList = sorted(list(dic.keys()))
	for key in keyList:
		print(textwrap.fill((str(key) + ":" + str(dic[key])), width=180))

def listAllSpells():
	print (spellDict)
	spellList = list(spellDict.keys())
	for spell in sorted(spellList):
		print (spellList)
		
def regexSearchSpells(regExp):
	regExp =  re.compile(regExp)
	spellList = list(spellDict.keys())
	for spell in sorted(spellList):
		if re.search(regExp, spell):
			print(spell)
		
def printSpellDetails(spellName):
	try:
		printDic(spellDict[querySpell])
	except KeyError:
		print("The spell entered does not exist")

def printSpellByLevel(levelNum):
	queryLevel = int(levelNum)
	for spell, attributes in list(spellDict.items()):
		if int(attributes["Level"]) == queryLevel:
			print(spell)

def printSpellByRange(spellRange):
	spellRange = int(spellRange)
	for spell in spellDict:
		try:
			if int(spellDict[spell]["Range"]) > spellRange:
				print (spell)
		except:
			pass

def querySpellList(queryString):
	queryMatches = []
	for spell in spellDict.keys():
		if queryString.lower() in spell.lower():
			queryMatches.append(spell)
		queryMatches.sort()
	for spell in queryMatches:
		print (spell)

def constructSpellDict():
	spellDict = {}
	SPELL_NAME_INDEX = 2
	
	dictKeys = []
	
	with open("5e Spells.csv", 'r') as spellsFile:
		counter = 0
		junk = csv.reader(spellsFile)
		for row in junk:
			if counter == 0:
				dictKeys = row
				counter += 1
			elif counter > 0:
				if row[SPELL_NAME_INDEX] not in spellDict:
					spellDict[row[SPELL_NAME_INDEX]] = {}
				
				components = []
				for i in range(6, 9):
					components.append(row[i])
				spellDict[row[SPELL_NAME_INDEX]]["Components"] = components
				
				spellDict[row[SPELL_NAME_INDEX]]["Classes"] = row[20].split(',')
				for i in [x for x in range(1, 20) if x != SPELL_NAME_INDEX and x not in range(6,9)]:
					spellDict[row[SPELL_NAME_INDEX]][dictKeys[i]] = row[i]
					
	for spell in spellDict.keys():
		spellDict[spell]["Range"] = re.sub("Touch", "0", spellDict[spell]["Range"])
		spellDict[spell]["Range"] = re.sub("'", "", spellDict[spell]["Range"])
		spellDict[spell]["Range"] = re.sub("Personal", "Self", spellDict[spell]["Range"])
		if "miles" in spellDict[spell]["Range"] and "Self" not in spellDict[spell]["Range"]:
			spellDict[spell]["Range"] = str(int(re.sub(" miles", "", spellDict[spell]["Range"]))*5280)
		elif "mile" in spellDict[spell]["Range"] and "Self" not in spellDict[spell]["Range"]:
			spellDict[spell]["Range"] = str(int(re.sub(" mile", "", spellDict[spell]["Range"]))*5280)
			
		try:      
			spellDict[spell]["Range"] = int(spellDict[spell]["Range"])
		except ValueError:
			pass
		
	return spellDict

spellDict = constructSpellDict()


if __name__ == '__main__':
	done = False
		
	while not done:
		inputValid = False
		
		mode = None
		changeMode = False
		
		while not inputValid:
			mode = input("What would you like to do? \n 1:List all the spells \n 2:Learn about a spell \n 3:List spells by level \n 4:List spells by range \n 5:Search spells by keyword \n 6:Search spells using regex\n 7:Exit \n")
			if "1" <= mode <= "7":
				inputValid = True
				
		mode = int(mode)
		
		#List Spells
		if mode == 1:
			listAllSpells()
			print ("\n")
		
		#Learn details about a spell
		while mode == 2 and not changeMode:
			querySpell = input("Select spell:")
			if querySpell != "":
				printSpellDetails(querySpell)
			else:
				changeMode = True
			print ("\n")
		   
		#list spells by level
		while mode == 3 and not changeMode:
			queryLevel = input("Please enter the level:")
			if queryLevel != "":
				printSpellByLevel(queryLevel)
			else:
				changeMode = True
			print ("\n")
					
		#list spells by range
		if mode == 4:
			desiredSpellRange = input("Desired spell range in feet:")
			printSpellByRange(desiredSpellRange)
			print ("\n")
			
		#spell keyword search                
		while mode == 5 and not changeMode:
			queryString = input("What keyword would you like to search for?:")
			if queryString != "":
				querySpellList(queryString)
			else:
				changeMode = True
			print ("\n")
			
		if mode == 6:
			regExp = input("Regex Expression:")
			regexSearchSpells(regExp)
			print ("\n")
			
		if mode == 7:
			print ("Here")
			done == True
