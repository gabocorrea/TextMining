"""	Lee como input un archivo .csv con header id,sub_id,comment__class,type,path,text.
	El output es un archivo .csv con header text,comment__class con la diferencia que los
	caracteres " fueron reemplazados por \" y que comment__class ahora corresponde a un string
	(antes correspondia a un int)
	"""
import sys,re

def usage(): #this usage text is not finished. not even correct by now. 
	print("""
Usage:
	python 3_leave_only_text_and_class_in_the_csv.py <file_name_in>

Description:
	Lee como input un archivo .csv con header id,sub_id,comment__class,type,path,text.
	El output es un archivo .csv con header text,comment__class

Options:
	-h, --help
		print help and usage of this script

	-c, --classifier
		Must be NONE or KEYWORDS. If NONE, phrases won't be given a color (or a type of comment).
		If KEYWORDS, phrases with at least one keyword - see keywords below - will be given a yellow color (directive-type comment).
		NONE is the default if option is left blank.

		keywords:
			call*,invo*,before,after,between,once,prior,must,mandat*,require*,shall,
			should,encourage*,recommend*,may,assum*,only,debug*,restrict*,never,
			condition*,strict*,necessar*,portab*,strong*,performan*,efficien*,fast,
			quick,better,best,concurren*,synchron*,lock*,thread*,simultaneous*,
			desir*,alternativ*,addition*,extend*,overrid*,overload*,overwrit*,
			reimplement*,subclass*,super*,inherit*,warn*,aware*,error*,note*

	-m, --minlines
		Sets the minimum lines a javadoc comment nees to have in ordered to be included in the output file.
		(IMPORTANT:)By default is 4. For example, the following javadoc comment has 4 lines:
			/** Returns a {@link Set} of unique elements in the Bag.
			 * 
			 * @return the Set of unique Bag elements
			 */
			
Examples:
	python 1_convert-comments-in-many-files-to-one-csv___separated_by_phrases folderIn out.csv
	python 1_convert-comments-in-many-files-to-one-csv___separated_by_phrases folderIn out.csv -c KEYWORDS
	python 1_convert-comments-in-many-files-to-one-csv___separated_by_phrases folderIn out.csv -c KEYWORDS --minlines=3
	
Details:
	The output .csv file has the following header:
		id,sub_id,comment__class,type,path,text

		""")



filename_in=sys.argv[1]
fdout = open(filename_in[:-4]+'_(only comments and class).csv','w')

linesNotCorrectlyFormated = 0
with open(filename_in) as fdin:
	i=0
	for line in fdin:
		splitted = line.split(',',5)
		if len(splitted) == 6:
			if i<=0:
				fdout.write(splitted[5][:-1]+','+splitted[2]+'\n')
			else:
				
				# Replace all " with \"
				p=re.compile(r'"')
				s=p.sub( r'\"', splitted[5] )

				
				
				s=s[:-1]
				fdout.write('"'+s+'"'+',')
				if(splitted[2]=='0'):
					fdout.write('non-directive\n')
				elif(splitted[2]=='1'):
					fdout.write('directive\n')
				elif(splitted[2]=='2'):
					fdout.write('semi-directive\n')#('semi-directive\n')
				elif(splitted[2]=='3'):
					fdout.write('null-directive\n')#('null-directive\n')
				else:
					print('Error, read a number out of range in the directive types')
					sys.exit()
		else:
			linesNotCorrectlyFormated += 1
		i+=1

print('linesNotCorrectlyFormated='+str(linesNotCorrectlyFormated))