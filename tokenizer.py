from nltk import sent_tokenize
import os
import sys
import json

def main():
    texts = {}

    for root, dirs, files in os.walk(sys.argv[1]):
        print "Tokenizing " + root + " to sentences...",
        for file in files:
            if file[-4:] == ".txt":
                try:
                    inFile = open(os.path.join(root, file), 'r')
                    inText = inFile.read()

                    names = os.path.join(root, file).split("/")
                    docket = names[-1].split("_")[0]
                    page = names[-1].split("_")[-1][:-4]

                    year_dir = "sentences/" + names[-3] + "/"
                    if not os.path.exists(year_dir):
                        os.mkdir(year_dir)
                    session_dir = "sentences/" + names[-3] + "/" + names[-2] + "/"
                    if not os.path.exists(session_dir):
                        os.mkdir(session_dir)
                    baseName = "sentences/" + names[-3] + "/" + names[-2] + "/" + docket + ".json"

                    outText = inText.replace('\n', ' ').replace('\x13\x10', ' ').replace(' - ', '').replace(' -', '').replace(' -', '').replace('-', '')
                    outSentences = sent_tokenize(outText)

                    if baseName not in texts:
                        texts[baseName] = {}

                    texts[baseName][page] = outSentences
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    print("FAILED")
        print("done")


    for fileName, text in texts.iteritems():
        outFile = open(fileName, 'w')
        json.dump(text, outFile)

if __name__ == "__main__":
    main()