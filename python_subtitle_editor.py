### http://www.tutorialspoint.com/python/python_reg_expressions.htm
#coding: utf8
import re

def my_time_difference(prevTimeEnd,currTimeStart):

    prevTimeEndMillisecs = 0
    currTimeStartMillisecs = 0
    
    prevTimeEnd=prevTimeEnd.replace(',', ":")
    timeParts = prevTimeEnd.split(":")
    prevTimeEndMillisecs = int(timeParts[0])*60*60*1000 + int(timeParts[1])*60*1000 + int(timeParts[2])*1000 + int(timeParts[3])
    
    currTimeStart = re.sub(r',', ":", currTimeStart)
    timeParts = currTimeStart.split(':')
    currTimeStartMillisecs = int(timeParts[0])*60*60*1000 + int(timeParts[1])*60*1000 + int(timeParts[2])*1000 + int(timeParts[3])
    
    print("difference:")    
    print (str(int(currTimeStartMillisecs) - int(prevTimeEndMillisecs)))
    #input()
    
    return int(currTimeStartMillisecs) - int(prevTimeEndMillisecs)


def calculateTimeWithDiff(time,difference):

    timeInMillisecs = 0
    differenceInMillisecs = int(difference)
    
    time=time.replace(',', ":")
    timeParts = time.split(":")
    timeInMillisecs = int(timeParts[0])*60*60*1000 + int(timeParts[1])*60*1000 + int(timeParts[2])*1000 + int(timeParts[3])
    
    calculatedTimeInMillisecs = timeInMillisecs + differenceInMillisecs
    
    hours = int(calculatedTimeInMillisecs / (60*60*1000))
    minutesRemainedInMillisecs = calculatedTimeInMillisecs % (60*60*1000)
    minutes = int(minutesRemainedInMillisecs / (60*1000))
    secondsRemainedInMillisecs = minutesRemainedInMillisecs % (60*1000)
    seconds = int(secondsRemainedInMillisecs / 1000)
    milliseconds = secondsRemainedInMillisecs % 1000
    
    return str(hours).zfill(2)+":"+str(minutes).zfill(2)+":"+str(seconds).zfill(2)+","+str(milliseconds).zfill(3)
    
def calculate_previos_timeline(previousTimeLine,currentTimeLine):
    searchObj=re.search(r'^(.*\s+-->\s+)(.*)', previousTimeLine, re.M|re.I)
    prevTimeEnd = "0";
    currTimeStart = "0";
    if searchObj:
        prevTimePart1=searchObj.group(1)
        prevTimeEnd=searchObj.group(2)
    searchObj=re.search(r'^(.*)(\s+-->\s+.*)', currentTimeLine, re.M|re.I)
    if searchObj:
        currTimeStart=searchObj.group(1)
        currTimePart2=searchObj.group(2)
    myTimeDiff = my_time_difference(prevTimeEnd,currTimeStart)
    if (myTimeDiff > 10):
        if (myTimeDiff < 1500):
            print("myTimeDiff:" + str(myTimeDiff))
            #input()
            #prevTimeEnd = currTimeStart
            calculatedPrevTimeEnd=calculateTimeWithDiff(currTimeStart,"-10")
            previousTimeLine = prevTimePart1 + calculatedPrevTimeEnd + "\n"
        else:
            calculatedPrevTimeEnd=calculateTimeWithDiff(prevTimeEnd,"1500")
            previousTimeLine = prevTimePart1 + calculatedPrevTimeEnd + "\n"
    elif (myTimeDiff == 0):
        print("!!!WARNING - almost overlaping 0");
        calculatedPrevTimeEnd=calculateTimeWithDiff(currTimeStart,"-10")

        previousTimeLine = prevTimePart1 + calculatedPrevTimeEnd + "\n"
    return previousTimeLine

    
def extend_durations(sourceFile):
    destinationFile = sourceFile + '.new'
    fs = open(sourceFile, 'r', encoding="utf8")
    #fs = open(sourceFile, 'r', encoding='cp1250')
    lineNr = 0
    previousTimeLineNr=0
    listWithLines=[]
    while 1:                
        line = fs.readline()        
        if not line: break
        listWithLines.append(line)
        searchObj=re.search(r'^.*\s+-->\s+.*', line, re.M|re.I)
        if searchObj:
            if previousTimeLineNr!=0:
                listWithLines[previousTimeLineNr]=calculate_previos_timeline(listWithLines[previousTimeLineNr],line)
                previousTimeLineNr=lineNr
            previousTimeLineNr=lineNr
            #print(line)
        lineNr=lineNr+1    
    fs.close()
    fd = open(destinationFile, 'w', encoding="utf8")
    #fd = open(destinationFile, 'w', encoding="cp1250")
    for line in listWithLines:
        fd.write(line)
    fd.close()
    return

    
extend_durations("Amongst_White_Clouds.srt")