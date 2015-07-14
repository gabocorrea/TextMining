import re

fileName = 'textMining01.csv-testSet'

### replace all   \n and \t    with   a blankspace
regexStr = r'\\n|\\t'
regexObj = re.compile(regexStr)
with open('temp.arff','w') as fdout:
	with open(fileName+'.arff') as fdin:
		for line in fdin:
			outLine = regexObj.sub(' ', line)
			fdout.write(outLine)



### replace all file paths (such as ../../bin/)  with _OSPathElement_   .   Does not support paths with \ separator
regexStr = r'([\w\-\.:]+/)+'
regexObj = re.compile(regexStr)
with open('temp2.arff','w') as fdout:
	with open('temp.arff') as fdin:
		i=1
		DoModifyLine=False
		for line in fdin:
			if line=='@data\n':
				DoModifyLine=True
				i+=1
				fdout.write(line)
				continue
			if DoModifyLine:
				outLine = regexObj.sub('_OSPathElement_', line)
				fdout.write(outLine)
			else:
				fdout.write(line)
			i+=1




### replace all class paths (such as java.util.Collection)  with _ClassPathElement_
regexStr = r'(\w+\.)+\w+'
regexObj = re.compile(regexStr)
with open('temp3.arff','w') as fdout:
	with open('temp2.arff') as fdin:
		i=1
		DoModifyLine=False
		for line in fdin:
			if line=='@data\n':
				DoModifyLine=True
				i+=1
				fdout.write(line)
				continue
			if DoModifyLine:
				outLine = regexObj.sub('_ClassPathElement_', line)
				fdout.write(outLine)
			else:
				fdout.write(line)
			i+=1




### replace all camel-case words with _ClassElement_
regexStr = r'\b([A-Z][a-z\d]+){2,}\b|\b([a-z]+[A-Z][a-z\d]+)+\b'# add the following to the regexStr to include words like ALLCAPSLOCK  and  CONSTANT   |(\b[A-Z]{2,}\b)
regexObj = re.compile(regexStr)			
with open(fileName+'---camelcaseWords_replaced_by_classmemberelement.arff','w') as fdout:
	with open('temp3.arff') as fdin:
		i=1
		DoModifyLine=False
		for line in fdin:
			if line=='@data\n':
				DoModifyLine=True
				i+=1
				fdout.write(line)
				continue
			if DoModifyLine:
				outLine = regexObj.sub('_ClassElement_', line)
				fdout.write(outLine)
			else:
				fdout.write(line)
			i+=1

import os
os.remove('temp.arff')
os.remove('temp2.arff')
os.remove('temp3.arff')