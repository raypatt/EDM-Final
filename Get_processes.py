#The whole survey is in one column that’s “text; text; dialogEmotionEMOTION1; dialogEmotionEMOTION2; dialogConf3”. Had to parse over that string with a window that looks for “dialogEmotion” and gets the word that comes before the next “;”  So I store the emotions in a dictionary of levels nested in participants (e.g., AA01 : [LVL1 : “Sad”, “happy”, LVL2 : “angry”], AA02 : [LVL1 : …]). Then I go through and convert the emotions to one hot encoding so if the set of emotions is “Happy” “Sad” “Angry” and they say theyre “Happy” they’d get a value of [1,0,0] vs “Happy”, “Sad” getting [1,1,0]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:29:24 2022

@author: raypatt
"""

# Frustrated, Curious, Confused, Interested, Happy, Angry, Anxious, Calm, Proud, Ashamed, Bored
import csv
import time
import re

store = {}
data= []
files = ["/Users/raypatt/Desktop/Fox and Field Logs/01AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01BA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01BB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01BD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01BE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01BF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01BG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01BJ.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01CA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01CC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01CE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01CF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01CG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/01CI.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03BA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03BB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03BC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03BD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03BE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03BF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03BH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03BJ.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03CA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03CB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03CC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03CD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03CE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03CF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03CG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03CH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/03CI.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09BA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09BB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09BC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09BD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09BE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09BF.csv",
# NOT COMPLETE: "/Users/raypatt/Desktop/Fox and Field Logs/09BG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09CB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09CC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09CD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09CE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09CF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09CG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/09CH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11AA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11BA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11BB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11BC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11BD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11BG.csv",
##NOT COMPLETE: "/Users/raypatt/Desktop/Fox and Field Logs/11BH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11BJ.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11CA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11CB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11CC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11CD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11CE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11CF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/11CG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25AA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25BA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25BB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25BC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25BF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25BG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25BI.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25CA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25CB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25CC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25CD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25CE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25CG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/25CH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27AA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27BA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27BB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27BC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27BD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27BE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27BF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27BG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27BH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27CA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27CB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27CC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27CD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27CE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27CF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27CG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/27CH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33AA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33BA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33BC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33BD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33BG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33BI.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33CA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33CB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33CF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33CG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/33CH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35AA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35BA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35BB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35BC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35BD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35BF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35BG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35BH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35BI.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35CA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35CB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35CC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35CD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35CE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35CG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35CH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/35CI.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41AA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41BB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41BC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41BD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41BE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41BF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41BH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41BJ.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41CA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41CB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41CC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41CD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41CE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41CF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41CG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/41CH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43AA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43BF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43BG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43BH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43BI.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43CB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43CC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43CD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43CE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43CG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/43CH.csv",
##NOT COMPLETE "/Users/raypatt/Desktop/Fox and Field Logs/44AH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57BA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57BB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57BC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57BD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57BI.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57CA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57CB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57CC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57CD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57CE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57CG.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57CH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/57CI.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59AA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59AB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59BA.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59BB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59BC.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59BD.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59BF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59BG.csv",
##NOT COMPLETE "/Users/raypatt/Desktop/Fox and Field Logs/59BH.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59BI.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59CB.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59CE.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59CF.csv",
"/Users/raypatt/Desktop/Fox and Field Logs/59CI.csv"]

sequence_idx = 1

def parseNested(text, left=r'[{,@]', right=r'[},~]', sep=r';'):
    text = text.replace('[', '@')
    text = text.replace(']', '~')
    text = text.replace('\n', '')
    """ Based on https://stackoverflow.com/a/17141899/190597 (falsetru) """
    pat = r'({}|{}|{})'.format(left, right, sep)
    tokens = re.split(pat, text)    
    stack = [[]]
    for x in tokens:
        if not x or re.match(sep, x): continue
        if re.match(left, x):
            stack[-1].append([])
            stack.append(stack[-1][-1])
        elif re.match(right, x):
            stack.pop()
            if not stack:
                raise ValueError('error: opening bracket is missing')
        else:
            stack[-1].append(x)
    if len(stack) > 1:
        print(text)
        raise ValueError('error: closing bracket is missing')
    return stack.pop()
def getInsideIdx(code): 
    code_sansText = re.sub(r'[A-Za-z,;,(,),0-9,\n,=,+, ,<,.]', '', code)
    tmp = []
    for i in code_sansText: 
        tmp.append(i)
        if(i == "{"): tmp.append("F")
    tmp = ("".join(tmp))
    
    tmp2 = parseNested(tmp)
    inside_idx = 0
    found = False
    for idx, i in enumerate(tmp2):
        if "F" in i: 
            inside_idx = idx
            found = True
    if not(found): 
        inside_idx = -9
    return inside_idx
                    ######## Redefine Block Action ########
                    ##Block_Move_In
                    ##Block_Move_Out
                    ##Block_Move_OutOf
                    ##Block_Move_Into
                    ###Block_Move_Chunk
                    
                    ##Block_Change
                    ##Block_Delete
                    ##Block_Delete_Chunk
                    ##Block_Create
                    
#Produces edit which is an array [0,0] where array[0] is whether the change was outside run code and array[1] is inside runcode
def edit_block(currentCode, nextCode):
    code1 = parseNested(currentCode)
    code2 = parseNested(nextCode)
    
    inside1 = getInsideIdx(currentCode)
    inside2 = getInsideIdx(nextCode)

    edit = [0,0]
   # if inside1 != -9 and inside2 != -9: 
    #    if str(code1[inside1]) !=
    #if inside1 == inside2: 
     #   if inside1 != -9 and inside2 != -9:
      #      if str(code1[inside1]) == str(code2[inside2]): 
       #         edit[0] = 1
        #    else:
         #       edit[1] = 1
        #else:
         #   edit[0] = 0
    return edit
    
def move_block(currentCode, nextCode):
    
    code_parsed = parseNested(currentCode)
    code2_parsed = parseNested(nextCode)
    
    code_in_idx = getInsideIdx(currentCode)
    code2_in_idx = getInsideIdx(nextCode)
    
    move_block_out = False #Moving a block out of run code
    move_block_in = False #Moving a block into run code
    move_block = False #Just moving a block within a chunk of code
    move_block_inside = False
    move_block_outside = False
    move_block_nowhere = False
    
    if str(currentCode == nextCode): 
        move_block_nowhere = True
    else: 
        if code_in_idx != -9 and code2_in_idx != -9:
            if (code_in_idx < len(code_parsed) or code2_in_idx < len(code2_parsed)):
                if (len(str(code_parsed[code_in_idx]))) > (len(str(code2_parsed[code2_in_idx]))): move_block_out = True
                if (len(str(code_parsed[code_in_idx]))) < (len(str(code2_parsed[code2_in_idx]))): move_block_in = True
        if code_in_idx == -9 and code2_in_idx != -9: 
           # print("DICK")
            move_block_in = True
        if code_in_idx != 0 and code2_in_idx ==-9: 
            #print("DICK2")
            move_block_out = True
        if code_in_idx == code2_in_idx and len(code_parsed) > len(code2_parsed):
            move_block_in = True
        if code_in_idx == code2_in_idx and len(code_parsed) < len(code2_parsed):
            move_block_out = True
        
        if not(move_block_out) and not(move_block_in): move_block = True
        
        #first we want to get moving from only block on field to inside
        
        
        move_block_outside = False
        move_block_inside = False
        if len(code_parsed) == len(code2_parsed) and code_in_idx != code2_in_idx: move_block_outside = True
        if move_block:
            if (code_in_idx != -9 and code2_in_idx != -9):
                if ((code_in_idx < len(code_parsed) or code2_in_idx < len(code2_parsed))):
                    if ((str(code_parsed[code_in_idx])) != (str(code2_parsed[code2_in_idx]))): 
                        move_block_inside = True
                else: print("poop")
            else: move_block_outside = True
        
        move_block_nowhere = False
   # if currentCode == nextCode: move_block_nowhere = True
    
    ####IF just moved onto playing field will be the same
    
    
    ret = [0,0,0,0,0]
    if move_block_in: ret[0] = 1
    if move_block_out: ret[1] = 1
    if move_block_inside: ret[2] = 1
    if move_block_outside: ret[3] = 1
    if move_block_nowhere: ret[4] = 1
    
    
    #Investigating why there are so many [0,0,0,0]s
    #if ret == [0,0,0,0]: 
     #   if code_in_idx != code2_in_idx:
      #      print("====")
       #     print(str(code_in_idx) + " | " + str(code2_in_idx))
        #    print(code_parsed)
         #   print(code2_parsed)
          #  print("====")
    return ret

TESTVAR = 0 
import datetime

for fileName in files: 
    ID = fileName[42:46]
    store[ID] = {}

    storedLines = []
    with open(fileName, mode ='r')as file:
        csvFile = csv.reader(file)
        rows =[]
        for idx, lines in enumerate((csvFile)):
            storedLines.append(lines)

    with open(fileName, mode ='r')as file:
        csvFile = csv.reader(file)
        
        levelStart = 0 
        levelidx = 0
        
        for idx, lines in enumerate((csvFile)):
            if idx == 0: 
                header = lines
                type_idx = header.index("Type")
                level_idx = header.index("Level")
                attempt_idx = header.index("Attempt")
                editType_idx = header.index("EditType")
                time_idx = header.index("Local EDT")
                code_idx = header.index("Code")
                editedBlock_idx = header.index("EditedBlock")
                correct_idx = header.index("Correct")
                gameStartTime = datetime.datetime.strptime(storedLines[idx+1][time_idx], "%Y-%m-%d %H:%M:%S")
                
                
                
            else: 
                if lines[type_idx] == 'Process':
                    level = lines[level_idx]
                    attempt = lines[attempt_idx]
                    editType = lines[editType_idx]
                    time = lines[time_idx]
                    code = lines[code_idx]
                    previousCode = storedLines[idx][code_idx]
                    nextCode = storedLines[idx+1][code_idx]
                    editedBlock = lines[editedBlock_idx]
                    
                    timeSinceGameStart = (datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") - gameStartTime).seconds
                    
                    if storedLines[idx-1][level_idx] != level: 
                        levelStartTime = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                    #if storedLines[idx-1][level_idx] != level and level == "111": print("OK")
                    
                    timeSinceLevelStart = (datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") - levelStartTime).seconds
                    
                    if timeSinceGameStart == 0 and timeSinceLevelStart == 0:
                        timeSinceLastAction = 0
                    else:
                        if storedLines[idx-1][time_idx] == "Local EDT": 
                            timeSinceLastAction = 0
                        else:
                            timeSinceLastAction = (datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(storedLines[idx-1][time_idx], "%Y-%m-%d %H:%M:%S")).seconds
                  
                    
                    move = [0, 0, 0, 0, 0]
                    create = [0]
                    delete = [0]
                    edit = [0]
                    chunk = [0]
                    
                    #Identify if editblock is a chunk
                    #print(code)
                    editedBlock = editedBlock.split(',')
                    if len(editedBlock) > 1: chunk[0] = 1
                    if editType == "Block_Move": 
                        move = move_block(code, nextCode)
                        #if move == [0,0,0,0]: 
                            #data.append([editType, code, lines[0], storedLines[idx+1][0], nextCode, storedLines[idx+1][editType_idx]])
                            #data.append([ID, lines[0], code, editType,storedLines[idx+1][0], nextCode, storedLines[idx+1][editType_idx]])
                            
                    if editType == "Block_Create": create[0] = 1 
                    if editType == "Block_Delete": delete[0] = 1
                    if editType == "Block_Change": edit[0] = 1
                    ret = move + edit + delete + create + chunk


                    string = ""
                    if ret[0] == 1: string += "MoveIn_"
                    if ret[1] == 1: string += "MoveOut_"
                    if ret[2] == 1: string += "MoveInside_"
                    if ret[3] == 1: string += "MoveOutside_"
                    if ret[4] == 1: string += "MoveNowhere_"
                    if ret[5] == 1: string += "Edit_"
                    if ret[6] == 1: string += "Delete_"
                    if ret[7] == 1: string += "Create_"
                    if ret[7] == 1: string += "Chunk_"
                    
                    
                    if storedLines[idx-1][level_idx] != level: 
                        levelidx = 1
                        sequence_idx += 1
                    else: 
                        levelidx += 5
                    data.append([sequence_idx] + [level] + [ID] + [levelidx] + [string])
                    
                    #data.append(ret)
csvLines = []
            
# name of csv file 
filename = "/Users/raypatt/Desktop/EDM Final Project/process.csv"
#fields = ["Level", "ID", "Frustrated", "Curious", "Confused", "Interested", "Happy", "Angry", "Anxious", "Calm", "Proud", "Ashamed", "Bored", "Confidence"]
    
# writing to csv file 
with open(filename, 'w+') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    #csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerow(["seqId", "level", "ID", "levelID", "action"])
    for ID in data: 
        csvwriter.writerow(ID)



            
            