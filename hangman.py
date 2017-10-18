# CSE 250A, HW1, 1.9 Hangman
# Xuan Zhu, A53234451

from heapq import heappush
from heapq import nlargest
from heapq import nsmallest

# (a) find 15 most and 14 least frequent words
count_total = 0;
dictionary = {}
h = []
f = open("hw1_word_counts_05.txt", 'r')
for line in f:
	key, value = line.split(' ')
	value = int(value)
	dictionary[key] = value
	count_total += value
f.close()

for w in dictionary:
	dictionary[w] = float(dictionary[w])/float(count_total)
	heappush(h, (dictionary[w], w))

print "15 most frequent words: "
print nlargest(15, h), '\n'
print "14 least frequent words: "
print nsmallest(14, h) ,'\n'

# input: string word, list incorrect guess
# output: char res, double prob
def hangman(word, incguess):
	# correct guess in word
	cguess = []
	# positions that has and has not been guessed
	right_pos = []
	empty_pos = []
	for i in range(5):
		c= word[i]
		if(c=='-'):
			empty_pos.append(i)
		else:
			right_pos.append(i)
			if (c not in cguess):
				cguess.append(c)
	# init parameters
	den = 0
	letters = {}
	for i in range(ord('A'), ord('Z')+1):
		letters[chr(i)] = 0
	# see if this word valid
	for w in dictionary:
		valid = True
		# 1. make suire the word has the correct guesses
		for i in right_pos:
			if(w[i]!=word[i]):
				valid = False
		if(not valid):
			continue
		# 2. make sure the word does not have already guessed char in empty positions
		for i in empty_pos:
			if(w[i] in cguess or w[i] in incguess):
				valid = False
		if(not valid):
			continue
		# valid, then add to denominator
		den += dictionary[w]
		# check for each letter
		for c in letters:
			if(c in cguess or c in incguess):
				continue
			curr_c = False
			for i in empty_pos:
				if(w[i]==c):
					curr_c = True
			# curr letter exists in the word, add the P(w)
			if(curr_c):
				letters[c] += dictionary[w]
	# now find the best guess
	prob = 0
	for c in letters:
		letters[c] /= den
		if(letters[c]>prob):
			prob = letters[c]
			res = c
	print "For ", word, " with incorrect guesses: ", incguess
	print "Best next guess: ", res, ";"
	print "Prob: ", prob, ".\n" 

print "#1"
hangman('-----',[])
print "#2"
hangman('-----',['E','A'])
print "#3"
hangman('A---S',[])
print "#4"
hangman('A---S',['I'])
print "#5"
hangman('--O--',['A','E','M','N','T'])

print "Test cases: "
print "#6"
hangman('-----',['E','O'])
print "#7"
hangman('D--I-',[])
print "#8"
hangman('D--I-',['A'])
print "#9"
hangman('-U---',['A','E','I','O','S'])
'''
# (b)(1) P(Li = l | E)
letters = {}
for i in range(ord('A'), ord('Z')+1):
	letters[chr(i)] = 0

for w in dictionary:
	for c in letters:
		if(w[0]==c or w[1]==c or w[2]==c or w[3]==c or w[4]==c):
			# P(Li=l) += P(w)
			letters[c] += dictionary[w]
max_freq = letters['A']
max_char = 'A'
for c in letters:
	if(letters[c]>max_freq):
		max_freq = letters[c]
		max_char = c
print "#1"
print "Best next guess: ", max_char, ";"
print "Prob: ", max_freq, "."


# (b)(2) no EA
# init as 0s
den = 0
for c in letters:
	letters[c] = 0
for w in dictionary:
	if(w[0]=='A' or w[1]=='A' or w[2]=='A' or w[3]=='A' or w[4]=='A'):
			continue
	if(w[0]=='E' or w[1]=='E' or w[2]=='E' or w[3]=='E' or w[4]=='E'):
			continue
	else:
		den+=dictionary[w]	
	for c in letters:
		if(w[0]==c or w[1]==c or w[2]==c or w[3]==c or w[4]==c):
			letters[c]+=dictionary[w]

max_freq = 0
for c in letters:
	letters[c] /= den
	if(letters[c]>max_freq):
		max_freq = letters[c]
		max_char = c
print "#2"
print "Best next guess: ", max_char, ";"
print "Prob: ", max_freq, "."

# (b)(3) A---S, no incorrect guess
# init as 0s
den = 0
for c in letters:
	letters[c] = 0
for w in dictionary:
	if(w[0]!='A' or w[4]!='S'):
		continue
	if(w[1]=='A' or w[2]=='A'or w[3]=='A'):
		continue
	if(w[1]=='S' or w[2]=='S'or w[3]=='S'):
		continue
	den+=dictionary[w]
	for c in letters:
		if(c=='A' or c=='S'):
			continue
		if(w[1]==c or w[2]==c or w[3]==c):
			letters[c]+=dictionary[w]


max_freq = 0
for c in letters:
	letters[c] /= den
	if(letters[c]>max_freq):
		max_freq = letters[c]
		max_char = c
print "#3"
print "Best next guess: ", max_char, ";"
print "Prob: ", max_freq, "."


# (b)(4) A---S, incorrect: {I}
# init as 0s
den = 0
for c in letters:
	letters[c] = 0
for w in dictionary:
	if(w[0]!='A' or w[4]!='S'):
		continue
	if(w[1]=='A' or w[2]=='A'or w[3]=='A'):
		continue
	if(w[1]=='S' or w[2]=='S'or w[3]=='S'):
		continue
	if(w[1]=='I' or w[2]=='I'or w[3]=='I'):
		continue
	den+=dictionary[w]
	for c in letters:
		if(c=='A' or c=='S' or c=='I'):
			continue
		if(w[1]==c or w[2]==c or w[3]==c):
			letters[c]+=dictionary[w]

max_freq = 0
for c in letters:
	letters[c] /= den
	if(letters[c]>max_freq):
		max_freq = letters[c]
		max_char = c
print "#4"
print "Best next guess: ", max_char, ";"
print "Prob: ", max_freq, "."

# (b)(5) --O--, incorrect: {A,E,M,N,T}
# init as 0s
den = 0
for c in letters:
	letters[c] = 0
for w in dictionary:
	if(w[2]!='O'):
		continue
	if(w[0]=='O' or w[1]=='O' or w[3]=='O' or w[4]=='O'):
		continue
	if(w[0]=='A' or w[1]=='A' or w[3]=='A' or w[4]=='A'):
		continue
	if(w[0]=='E' or w[1]=='E' or w[3]=='E' or w[4]=='E'):
		continue		
	if(w[0]=='M' or w[1]=='M' or w[3]=='M' or w[4]=='M'):
		continue	
	if(w[0]=='N' or w[1]=='N' or w[3]=='N' or w[4]=='N'):
		continue
	if(w[0]=='T' or w[1]=='T' or w[3]=='T' or w[4]=='T'):
		continue
	den += dictionary[w]
	for c in letters:
		if(c=='O' or c=='A' or c=='E' or c=='M' or c=='N' or c=='T'):
			continue
		if(w[0]==c or w[1]==c or w[3]==c or w[4]==c):
			letters[c]+=dictionary[w]

max_freq = 0
for c in letters:
	letters[c] /= den
	if(letters[c]>max_freq):
		max_freq = letters[c]
		max_char = c
print "#5"
print "Best next guess: ", max_char, ";"
print "Prob: ", max_freq, "." 


# test
# (b)(6)
den = 0;
for c in letters:
	letters[c] = 0
for w in dictionary:
	if(w[0]=='O' or w[1]=='O' or w[2]=='O' or w[3]=='O' or w[4]=='O'):
			continue
	if(w[0]=='E' or w[1]=='E' or w[2]=='E' or w[3]=='E' or w[4]=='E'):
			continue
	else:
		den+=dictionary[w]
	for c in letters:
		if(w[0]==c or w[1]==c or w[2]==c or w[3]==c or w[4]==c):
			letters[c]+=dictionary[w]
max_freq = 0
for c in letters:
	letters[c] /= den
	if(letters[c]>max_freq):
		max_freq = letters[c]
		max_char = c
print "#6"
print "Best next guess: ", max_char, ";"
print "Prob: ", max_freq, "."

# (b)(3) D--I-, no incorrect guess
# init as 0s
den = 0
for c in letters:
	letters[c] = 0
for w in dictionary:
	if(w[0]!='D' or w[3]!='I'):
		continue
	if(w[1]=='D' or w[2]=='D'or w[4]=='D'):
		continue
	if(w[1]=='I' or w[2]=='I'or w[4]=='I'):
		continue
	den+=dictionary[w]
	for c in letters:
		if(c=='D' or c=='I'):
			continue
		if(w[1]==c or w[2]==c or w[4]==c):
			letters[c]+=dictionary[w]


max_freq = 0
for c in letters:
	letters[c] /= den
	if(letters[c]>max_freq):
		max_freq = letters[c]
		max_char = c
print "#7"
print "Best next guess: ", max_char, ";"
print "Prob: ", max_freq, "."


# (b)(8) D--I-, incorrect: {A}
# init as 0s
den = 0
for c in letters:
	letters[c] = 0
for w in dictionary:
	if(w[0]!='D' or w[3]!='I'):
		continue
	if(w[1]=='D' or w[2]=='D'or w[4]=='D'):
		continue
	if(w[1]=='I' or w[2]=='I'or w[4]=='I'):
		continue
	if(w[1]=='A' or w[2]=='A'or w[4]=='A'):
		continue
	den+=dictionary[w]
	for c in letters:
		if(c=='D' or c=='I' or c=='A'):
			continue
		if(w[1]==c or w[2]==c or w[4]==c):
			letters[c]+=dictionary[w]

max_freq = 0
for c in letters:
	letters[c] /= den
	if(letters[c]>max_freq):
		max_freq = letters[c]
		max_char = c
print "#8"
print "Best next guess: ", max_char, ";"
print "Prob: ", max_freq, "."

# (b)(9) -U---, incorrect: {A,E,I,O,S}
# init as 0s
den = 0
for c in letters:
	letters[c] = 0
for w in dictionary:
	if(w[1]!='U'):
		continue
	if(w[0]=='U' or w[2]=='U' or w[3]=='U' or w[4]=='U'):
		continue
	if(w[0]=='A' or w[2]=='A' or w[3]=='A' or w[4]=='A'):
		continue
	if(w[0]=='E' or w[2]=='E' or w[3]=='E' or w[4]=='E'):
		continue		
	if(w[0]=='I' or w[2]=='I' or w[3]=='I' or w[4]=='I'):
		continue	
	if(w[0]=='O' or w[2]=='O' or w[3]=='O' or w[4]=='O'):
		continue
	if(w[0]=='S' or w[2]=='S' or w[3]=='S' or w[4]=='S'):
		continue
	den += dictionary[w]
	for c in letters:
		if(c=='U' or c=='A' or c=='E' or c=='I' or c=='O' or c=='S'):
			continue
		if(w[0]==c or w[2]==c or w[3]==c or w[4]==c):
			letters[c]+=dictionary[w]

max_freq = 0
for c in letters:
	letters[c] /= den
	if(letters[c]>max_freq):
		max_freq = letters[c]
		max_char = c
print "#9"
print "Best next guess: ", max_char, ";"
print "Prob: ", max_freq, "." 
'''