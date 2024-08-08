alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def substitution_encode(message, codebet):
    codebetDict = {}
    for i in range(len(codebet)):
        codebetDict[alphabet[i]] = codebet[i]
    newMessage = ""
    for i in message.upper():
        if(i in alphabet):
            newMessage += codebetDict[i]
        else:
            newMessage += i
    return newMessage



def substitution_decode(message, codebet):
    codebetDict = {}
    for i in range(len(codebet)):
        codebetDict[codebet[i]] = alphabet[i]
    newMessage = ""
    for i in message.upper():
        if(i in alphabet):
            newMessage += codebetDict[i]
        else:
            newMessage += i
    return newMessage

new_codebet = "XRPHIWGSONFQDZEYVJKMATUCLB"
print(substitution_encode("Hello Students", new_codebet))
print(substitution_decode(substitution_encode("Hello Students", new_codebet), new_codebet))
