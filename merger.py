import os
import sys
import json
import csv

def main_by_docket():
    mergedSents = []
    for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            if file[-5:] == ".json":
                try:
                    print "Merging " + os.path.join(root, file) + "...",
                    inFile = open(os.path.join(root, file), 'r')
                    sentiments = json.load(inFile)
                    names = os.path.join(root, file).split("/")

                    totalSent = sentiments["all"]
                    outSentiments = []
                    outSentiments.append(names[-3])
                    outSentiments.append(names[-2])
                    outSentiments.append(names[-1].split(".")[0])
                    outSentiments.append(totalSent["neg"])
                    outSentiments.append(totalSent["neu"])
                    outSentiments.append(totalSent["pos"])
                    outSentiments.append(totalSent["compound"])

                    mergedSents.append(outSentiments)
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    print("FAILED")
                print("done")

    outFile = open("data_by_case.csv", 'w')
    writer = csv.writer(outFile)
    writer.writerow(["Year", "Session", "Docket", "Negative", "Neutral", "Positive", "Compound"])
    for sent in mergedSents:
        writer.writerow(sent)

def main():
    mergedSents = {}
    for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            if file[-5:] == ".json":
                try:
                    print "Merging " + os.path.join(root, file) + "...",
                    inFile = open(os.path.join(root, file), 'r')
                    sentiments = json.load(inFile)
                    names = os.path.join(root, file).split("/")
                    year = names[-3]

                    totalSent = sentiments["all"]
                    if year not in mergedSents:
                        mergedSents[year] = totalSent
                        mergedSents[year]["num_cases"] = 1
                    else:
                        for key, val in totalSent.iteritems():
                            mergedSents[year][key] += val
                        mergedSents[year]["num_cases"] += 1
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    print("FAILED")
                print("done")

    outFile = open("data_by_year.csv", 'w')
    writer = csv.writer(outFile)
    writer.writerow(["Year", "Negative", "Neutral", "Positive", "Compound"])
    for key in sorted(mergedSents.keys()):
        year = key
        num_cases = mergedSents[key]["num_cases"]
        neg = mergedSents[key]["neg"]/num_cases
        neu = mergedSents[key]["neu"]/num_cases
        pos = mergedSents[key]["pos"]/num_cases
        compound = mergedSents[key]["compound"]/num_cases
        writer.writerow([year, neg, neu, pos, compound])

if __name__ == "__main__":
    main()