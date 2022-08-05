'''
Python script that reads a Fritzing file and returns the expected eletrical connection
'''
def getInstances(f):
    '''
    Returns tag 'chunk' list of connections from the Fritzing file; takes in .fz file as input
    '''
    curr_line, chunk = f.readline(), []
    while curr_line:
        if '<instances>' in curr_line:
            curr_line = f.readline()
            #We'll keep iterating through all instances, but we also need to package each instance into its own list
            while '</instances>' not in curr_line:
                temp = []
                while '</instance>' not in curr_line:
                    temp.append(curr_line.strip())
                    curr_line = f.readline()
                curr_line = f.readline()
                chunk.append(temp)
            return chunk
        else:
            curr_line = f.readline()
def getPinout(chunk):
    '''
    Returns dictionary pinout mapping; takes in tag connection 'chunk' list as input
    The following is the format of the mapping dictionary:

    (dict) => {component_type: {to:from}}
    e.g. 
        {'resistor': {'A3': 'A4', 'B7': 'B20}, 'wire': {'F5': 'H7' ...} ...}    
    '''

    pinout, pairs = {}, []

    for instance in chunk:
        temp, type = [], ''
        for line in instance:
            #Let's skip if the module is a breadboard, but record other types
            if ' moduleIdRef="Breadboard' in line or ' moduleIdRef="TwoLayerRectanglePCB' in line:
                #print("should have moved on to next instance")
                break
            elif 'moduleIdRef' in line:
                start = line.find('Ref') + 5

                while line[start] != '"':
                    type += line[start]
                    start +=1
                type = type.replace('ModuleID', '')
            if 'connectorId="pin' in line:
                #Before appending to temp, let's remove all the tag bloat from the file formatting
                #Start by looking for where the 'pin' substring ends, and hence where the actual location begins
                index, loc = line.find('pin') + 3, ''
                while line[index] != '"':
                    loc += line[index]
                    index +=1
                if loc not in temp:
                    temp.append(loc)
        if temp:
            temp.append(type)
            pairs.append(temp)
            if type not in pinout:
                pinout[type] = []
    #Now that we have the location pairs, let's map one to the other using the pinout dict.
    for pair in pairs:
        pins, comp = pair.copy()[:-1], pair[-1]
        pinout[comp].append(pins)
    return pinout

print(getPinout(getInstances(open("testFile.fz", 'r'))))