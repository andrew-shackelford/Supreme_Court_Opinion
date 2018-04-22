from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import sys
import json

def main():
    sid = SentimentIntensityAnalyzer()

    for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            if file[-5:] == ".json":
                try:
                    print "Analyzing " + os.path.join(root, file) + " for sentiment...",
                    inFile = open(os.path.join(root, file), 'r')
                    sentences = json.load(inFile)

                    names = os.path.join(root, file).split("/")

                    year_dir = "sentiments/" + names[-3] + "/"
                    if not os.path.exists(year_dir):
                        os.mkdir(year_dir)
                    session_dir = "sentiments/" + names[-3] + "/" + names[-2] + "/"
                    if not os.path.exists(session_dir):
                        os.mkdir(session_dir)
                    baseName = "sentiments/" + names[-3] + "/" + names[-2] + "/" + names[-1]

                    outSentiments = {}
                    totals = {}
                    num = 0

                    for pageNum, pageData in sentences.iteritems():
                        sentiments = []
                        for sent in pageData:
                            scores = sid.polarity_scores(sent)
                            num += 1
                            for label, score in scores.iteritems():
                                if label not in totals:
                                    totals[label] = score
                                else:
                                    totals[label] += score
                            sentiments.append(scores)
                        outSentiments[pageNum] = sentiments

                    for label, score in totals.iteritems():
                        totals[label] = score/num

                    outSentiments["all"] = totals
                    outFile = open(baseName, 'w')
                    json.dump(outSentiments, outFile)
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    print("FAILED")
                print("done")

if __name__ == "__main__":
    main()