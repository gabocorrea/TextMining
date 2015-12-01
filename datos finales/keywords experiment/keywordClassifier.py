import sys, collections, re

def usage():
	return """
	Usage: python <nombrePrograma> <file_in.arff>
	
	Example: python <nombrePrograma> in.arff > in_keywordClassifierResults.csv

	Tests the keyword Classifier on <file_in.arff> prints to stdout the values of the
	confusion matrix in csv style

	Asumes an input file with:
		@ATTRIBUTE text string
		@ATTRIBUTE comment__class {directive,non-directive}

	Also asumes that input file has an empty line as the last line of the file
	"""


classes = collections.OrderedDict()
classes['directive']=0
classes['non-directive']=0

matrix = collections.OrderedDict()
matrix['vp']=0
matrix['fn']=0
matrix['fp']=0
matrix['vn']=0



if len(sys.argv)<2 or len(sys.argv)>3:
	print(usage())
	sys.exit()








regexKeywords = r"\bcall\w*\b" + r"|" + r"\binvo\w*\b" + r"|" + r"\bbefore\b" + r"|" + r"\bafter\b" + r"|" + r"\bbetween\b" + r"|" + r"\bonce\b" + r"|" + r"\bprior\b" + r"|" + r"\bmust\b" + r"|" + r"\bmandat\w*\b" + r"|" + r"\brequire\w*\b" + r"|" + r"\bshall\b" + r"|" + r"\bshould\b" + r"|" + r"\bencourage\w*\b" + r"|" + r"\brecommend\w*\b" + r"|" + r"\bmay\b" + r"|" + r"\bassum\w*\b" + r"|" + r"\bonly\b" + r"|" + r"\bdebug\w*\b" + r"|" + r"\brestrict\w*\b" + r"|" + r"\bnever\b" + r"|" + r"\bcondition\w*\b" + r"|" + r"\bstrict\w*\b" + r"|" + r"\bnecessar\w*\b" + r"|" + r"\bportab\w*\b" + r"|" + r"\bstrong\w*\b" + r"|" + r"\bperforman\w*\b" + r"|" + r"\befficien\w*\b" + r"|" + r"\bfast\b" + r"|" + r"\bquick\b" + r"|" + r"\bbetter\b" + r"|" + r"\bbest\b" + r"|" + r"\bconcurren\w*\b" + r"|" + r"\bsynchron\w*\b" + r"|" + r"\block\w*\b" + r"|" + r"\bthread\w*\b" + r"|" + r"\bsimultaneous\w*\b" + r"|" + r"\bdesir\w*\b" + r"|" + r"\balternativ\w*\b" + r"|" + r"\baddition\w*\b" + r"|" + r"\bextend\w*\b" + r"|" + r"\boverrid\w*\b" + r"|" + r"\boverload\w*\b" + r"|" + r"\boverwrit\w*\b" + r"|" + r"\breimplement\w*\b" + r"|" + r"\bsubclass\w*\b" + r"|" + r"\bsuper\w*\b" + r"|" + r"\binherit\w*\b" + r"|" + r"\bwarn\w*\b" + r"|" + r"\baware\w*\b" + r"|" + r"\berror\w*\b" + r"|" + r"\bnote\w*\b"

#igual a regexKeywords pero le agregue 'null'
regexKeywords_custom_01 =  r"\bnull\b"    + r"|" + r"\bcall\w*\b" + r"|" + r"\binvo\w*\b" + r"|" + r"\bbefore\b" + r"|" + r"\bafter\b" + r"|" + r"\bbetween\b" + r"|" + r"\bonce\b" + r"|" + r"\bprior\b" + r"|" + r"\bmust\b" + r"|" + r"\bmandat\w*\b" + r"|" + r"\brequire\w*\b" + r"|" + r"\bshall\b" + r"|" + r"\bshould\b" + r"|" + r"\bencourage\w*\b" + r"|" + r"\brecommend\w*\b" + r"|" + r"\bmay\b" + r"|" + r"\bassum\w*\b" + r"|" + r"\bonly\b" + r"|" + r"\bdebug\w*\b" + r"|" + r"\brestrict\w*\b" + r"|" + r"\bnever\b" + r"|" + r"\bcondition\w*\b" + r"|" + r"\bstrict\w*\b" + r"|" + r"\bnecessar\w*\b" + r"|" + r"\bportab\w*\b" + r"|" + r"\bstrong\w*\b" + r"|" + r"\bperforman\w*\b" + r"|" + r"\befficien\w*\b" + r"|" + r"\bfast\b" + r"|" + r"\bquick\b" + r"|" + r"\bbetter\b" + r"|" + r"\bbest\b" + r"|" + r"\bconcurren\w*\b" + r"|" + r"\bsynchron\w*\b" + r"|" + r"\block\w*\b" + r"|" + r"\bthread\w*\b" + r"|" + r"\bsimultaneous\w*\b" + r"|" + r"\bdesir\w*\b" + r"|" + r"\balternativ\w*\b" + r"|" + r"\baddition\w*\b" + r"|" + r"\bextend\w*\b" + r"|" + r"\boverrid\w*\b" + r"|" + r"\boverload\w*\b" + r"|" + r"\boverwrit\w*\b" + r"|" + r"\breimplement\w*\b" + r"|" + r"\bsubclass\w*\b" + r"|" + r"\bsuper\w*\b" + r"|" + r"\binherit\w*\b" + r"|" + r"\bwarn\w*\b" + r"|" + r"\baware\w*\b" + r"|" + r"\berror\w*\b" + r"|" + r"\bnote\w*\b"






mode='waitingfor@dataline'

with open(sys.argv[1]) as fdin:
	currentline = 0

	for line in fdin:
		currentline += 1
		if str.lower(line)=='@data\n':
			mode='readingdata'
			continue
		if mode=='readingdata':
			start = line.index('"')+1
			end = line.rindex('"')
			comment = line[start:end]
			classStr = line[line.rindex(',')+1:-1]

			p = re.compile(regexKeywords_custom_01, re.IGNORECASE)
			if p.search(comment) == None:
				if classStr == 'non-directive': #Verdadero Negativo (VN)
					matrix['vn']+=1
				elif classStr == 'directive': #Falso Negativo (FN)
					matrix['fn']+=1
				else:
					print ("error con la clase de la linea {0} del archivo {1}".format(currentline,sys.argv[1]))
			else:
				if classStr == 'directive': #Verdadero Positivo (VP)
					matrix['vp']+=1
				elif classStr == 'non-directive': #Falso Positivo (FP)
					matrix['fp']+=1
				else:
					print ("error con la clases de la  linea {0} del archivo {1}".format(currentline,sys.argv[1]))


i=0
for key,val in matrix.items():
	sys.stdout.write(str(key))
	if i<len(matrix.keys())-1:
		sys.stdout.write(',')
	else:
		sys.stdout.write('\n')
	i+=1
i=0
for key,val in matrix.items():
	sys.stdout.write(str(val))
	if i<len(matrix.keys())-1:
		sys.stdout.write(',')
	else:
		sys.stdout.write('\n')
	i+=1