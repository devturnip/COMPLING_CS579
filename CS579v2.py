import json
from stanfordcorenlp import StanfordCoreNLP
import PyPDF2
from nltk import tokenize

pdfFileObject = open(r"SOFTWARE_REQUIREMENT_SPECIFICATION_SRS_O.pdf", 'rb')
#pdfFileObject = open(r"2007_puget_sound.pdf", 'rb')
#pdfFileObject = open(r"EM-SRS-ReviewSoftRightHospitalManagementSystemSRS.pdf", 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
# print(" No. Of Pages :", pdfReader.numPages)
# pageObject = pdfReader.getPage(10)

nlp = StanfordCoreNLP(r'http://localhost', port=9000)
allSentence = []
verb = []
frequencyVerb = []
full_sentence = []
obligation_sentence = []
acp_sentence = []
props = {'annotators': 'tokenize,ssplit,pos', 'pipelineLanguage': 'en', 'outputFormat': 'xml'}
obligation_modal = ['must', 'have to', 'should' , 'need to', 'needs to']
acp_model = ['access', 'allow', 'deny']
#cp_model = ['allow', 'disallow', 'access', 'responsible for', 'able to', 'prevent']


def checkingSentence(sentence):
    isThereSubject = False
    isThereVerb = False
    isThereModal = False
    for word in sentence:
        if (word[1] == "NN") or (word[1] == "NNS") or (word[1] == "NNP") or (word[1] == "NNPS"):
            isThereSubject = True
        if word[1] == "MD":
            isThereModal = True
        if (word[1] == "VB") or (word[1] == "VBD") or (word[1] == "VBG") or (word[1] == "VBN") or (
                word[1] == "VBP") or (word[1] == "VBZ"):
            isThereVerb = True

    if (isThereSubject == True) and (isThereModal == True) and (isThereVerb == True):
        return True
    else:
        return False

def preprocessing2(allSentence):
    result = []
    for sentence in allSentence:  # filter the sentences that have a modal verb
        # print(sentence)
        flag = False
        if (checkingSentence(sentence) == True):
            flag = True
        if (flag == True):
            result.append(sentence)
    return result


def resolve_coref(sentence):
    words = ""
    o = nlp.annotate(sentence, properties={'annotators': 'dcoref', 'outputFormat': 'json', 'ner.useSUTime': 'false'})
    output = json.loads(o)
    if 'corefs' in output:
        # print(output)
        for coref in output['corefs']:
            mentions = output['corefs'][coref]
            antecedent = mentions[0]  # the antecedent is the first mention in the coreference chain
            for j in range(1, len(mentions)):
                mention = mentions[j]
                if mention['type'] == 'PRONOMINAL':
                    # get the attributes of the target mention in the corresponding sentence
                    target_sentence = mention['sentNum']
                    target_token = mention['startIndex'] - 1
                    # transfer the antecedent's word form to the appropriate token in the sentence
                    output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']
                    #print(output)

        """ Print the "resolved" output """
        possessives = ['hers', 'his', 'their', 'theirs']
        for sentence in output['sentences']:
            for token in sentence['tokens']:
                output_word = token['word']
                # check lemmas as well as tags for possessive pronouns in case of tagging errors
                if token['lemma'] in possessives or token['pos'] == 'PRP$':
                    output_word += "'s"  # add the possessive morpheme
                output_word += token['after']
                words += output_word

    return words


def print_sentence(element):
    for i in element:
        print(i)


def print_clean(element):
    for i in element:
        clean_words = ""
        for y in i:
            clean_words += (y[0] + " ")
        # clean_words += "\n"
        getObligationPolicy(clean_words)
        full_sentence.append(clean_words)
        # print(clean_words)


def getAccessControlPolicy():
    for i in full_sentence:
        for o in obligation_sentence:
            if i not in obligation_sentence:
                for acp in acp_model:
                    if acp in i:
                        if i not in acp_sentence:
                            acp_sentence.append(i)



def getObligationPolicy(sentence):
    for md in obligation_modal:
        if md in sentence:
            if sentence not in obligation_sentence:
                obligation_sentence.append(sentence)


def checkingverb(checkingVerb):
    if (checkingVerb[1] == "MD" or checkingVerb[1] == "VB"):
        verb.append(checkingVerb[0])

    if (checkingVerb[1] == "VB" or checkingVerb[1] == "VBG" or checkingVerb[1] == "VBN" or checkingVerb[1] == "VBP" or
            checkingVerb[1] == "VBZ"):
        return True
    else:
        return False


def getSentence(sentence):
    flag = False
    for element in sentence:
        if (checkingverb(element) == True):
            flag = True
    if (flag == True):
        temp = []
        # for i in sentence:
        #     temp.append(i[0])
        allSentence.append(sentence)
        # result.append(temp)


def pickTop10():  # pick the most frequently verbs top 10
    pick = []
    uniqueVerb = list(set(verb))
    for i in uniqueVerb:
        frequencyVerb.append((i, verb.count(i)))
    frequencyVerb.sort(key=lambda element: element[1], reverse=True)
    # print(frequencyVerb)
    for i in range(0, 15):
        pick.append(frequencyVerb[i][0])  # append top 10
    return pick


def pdf2txt():
    for i in range(0, pdfReader.numPages):
        pageObject = pdfReader.getPage(i)
        txt = pageObject.extractText()
        txt = tokenize.sent_tokenize(txt)
        for sentence in txt:
            new_sentence = resolve_coref(sentence)
            posTaggedSentence = nlp.pos_tag(new_sentence)
            getSentence(posTaggedSentence)
            # result.append(getAccessControlPolicy(posTaggedSentence))
            # result.append(getObligationPolicy(posTaggedSentence))


def checkingWord(word):
    if (word[1] == "MD"):
        return True
    else:
        return False


def preprocessing(allSentence):
    result = []
    for sentence in allSentence:
        # print(sentence)
        flag = False
        for word in sentence:
            if (checkingWord(word) == True):
                flag = True
            if (flag == True):
                result.append(sentence)
                break
    return result


pdf2txt()
# picked = pickTop10()
processedSentence = preprocessing2(allSentence)
#print_sentence(processedSentence)

print_clean(processedSentence)

# print("PRINTING FULL LIST...........\n")
# for f in full_sentence:
#     print(f.center(40))


print("\n")
print("PRINTING OBLIGATIONS...........\n")
for o in obligation_sentence:
    print(o.center(40))

getAccessControlPolicy()
print("\n")
print("PRINTING ACPs...........\n")
for a in acp_sentence:
    print(a.center(40))

pdfFileObject.close()
nlp.close()
