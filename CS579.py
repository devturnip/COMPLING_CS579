from stanfordcorenlp import StanfordCoreNLP
import PyPDF2
from nltk import tokenize


pdfFileObject = open(r"C:\Users\user\Downloads\2007_puget_sound.pdf", 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
# print(" No. Of Pages :", pdfReader.numPages)
# pageObject = pdfReader.getPage(10)

nlp = StanfordCoreNLP(r'http://localhost', port=9000)
result = []
verb = []
frequencyVerb = []
props={'annotators': 'tokenize,ssplit,pos','pipelineLanguage':'en','outputFormat':'xml'}

def print_sentence(element):
    for i in element:
        print(i)

def getAccessControlPolicy(sentence):

    return sentence

def getObligationPolicy(sentence):

    return sentence

def checkingverb(checkingVerb):
    if(checkingVerb[1] == "MD" or checkingVerb[1] == "VB"):
        verb.append(checkingVerb[0])

    if (checkingVerb[1] == "VB"  or checkingVerb[1] == "VBG" or checkingVerb[1] == "VBN" or checkingVerb[1] == "VBP" or checkingVerb[1] == "VBZ"):
        return True
    else: return False

def getSentence(sentence):
    flag = False
    for element in sentence:
        if (checkingverb(element) == True):
            flag = True
    if (flag == True):
        temp = []
        # for i in sentence:
        #     temp.append(i[0])
        result.append(sentence)

        #result.append(temp)

for i in range(0,pdfReader.numPages):
    pageObject = pdfReader.getPage(i)
    txt = pageObject.extractText()
    txt = tokenize.sent_tokenize(txt)
    for sentence in txt:
        posTaggedSentence = nlp.pos_tag(sentence)
        getSentence(posTaggedSentence)
        #result.append(getAccessControlPolicy(posTaggedSentence))
        #result.append(getObligationPolicy(posTaggedSentence))


uniqueVerb = list(set(verb))
for i in uniqueVerb:
    frequencyVerb.append((i, verb.count(i)))


frequencyVerb.sort(key=lambda element : element[1],reverse=True)
print(frequencyVerb)
#print_sentence(result)
pdfFileObject.close()
nlp.close()


