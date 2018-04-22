import PyPDF2
import os
import sys

def main():
    for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            if file[-4:] == ".pdf":
                try:
                    print "Converting " + os.path.join(root, file) + " to text...",
                    pdfFile = open(os.path.join(root, file), 'rb')
                    pdfReader = PyPDF2.PdfFileReader(pdfFile)

                    names = os.path.join(root, file).split("/")
                    year_dir = "txts/" + names[-3] + "/"
                    if not os.path.exists(year_dir):
                        os.mkdir(year_dir)
                    session_dir = "txts/" + names[-3] + "/" + names[-2] + "/"
                    if not os.path.exists(session_dir):
                        os.mkdir(session_dir)
                    baseName = "txts/" + names[-3] + "/" + names[-2] + "/" + file[:-4] + "_"

                    for i in range(pdfReader.numPages):
                        outName = baseName + str(i) + ".txt"
                        outFile = open(outName, "w")
                        outUnicode = pdfReader.getPage(i).extractText()
                        outASCII = outUnicode.encode('ascii', 'ignore')
                        outFile.write(outASCII)
                        outFile.close()

                    print("done")
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    print("FAILED")


if __name__ == "__main__":
    main()