from django.shortcuts import render
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tensorflow
import tflearn
import json
import random
from .models import Conversation
stemmer = None
model = None
words = []
labels = []
docs_x = []
docs_y = []
data = []
conversations = []
def train(request):
	global model
	if model != None:
		return render(request, 'home.html', {'answer':''})
	global stemmer
	stemmer = LancasterStemmer()
	
	global data
	with open('E:\\MAIN\\intents.json') as file:
		data = json.load(file)
	global words
	global labels
	global docs_x
	global docs_y
	for intent in data['intents']:
		for pattern in intent['patterns']:
			wrds = nltk.word_tokenize(pattern)
			words.extend(wrds)
			docs_x.append(wrds)
			docs_y.append(intent['tag'])
		if intent['tag'] not in labels:
			labels.append(intent['tag'])
	
	words = [stemmer.stem(w.lower()) for w in words if w not in '?']
	words = sorted(list(set(words)))
	labels = sorted(labels)
	training = []
	output = []
	out_empty = [0 for _ in range(len(labels))]
	for x, doc in enumerate(docs_x):
		bag = []
		wrds = [stemmer.stem(w) for w in doc]
		for w in words:
			if w in wrds:
				bag.append(1)
			else:
				bag.append(0)
		output_row = out_empty[:]
		output_row[labels.index(docs_y[x])] = 1
		training.append(bag)
		output.append(output_row)

	training = numpy.array(training)
	output = numpy.array(output)
	
	tensorflow.reset_default_graph()
	net = tflearn.input_data(shape = [None, len(training[0])])
	net = tflearn.fully_connected(net, len(training)/2)
	net = tflearn.fully_connected(net, 20)
	net = tflearn.fully_connected(net, len(output[0]), activation = 'softmax')
	net = tflearn.regression(net)

	model = tflearn.DNN(net)
	model.fit(training, output, n_epoch = 1000, batch_size = 8)

	return render(request, 'home.html')

def home(request):
	global conversations
	conversations = []
	return render(request, 'home.html')

def bag_of_words(s, words):
	bag = [0 for  _ in range(len(words))]
	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]
	for se in s_words:
		for i, w in enumerate(words):
			if w == se:
				bag[i] = 1
			
	return numpy.array(bag)

def display(request):
	question = request.GET['question']
	global model
	global words
	global labels
	global data
	results = model.predict([bag_of_words(question, words)])[0]
	result_index = numpy.argmax(results)
	tag = labels[result_index]
	answer = ""
	if tag != 'specific':
		if results[result_index] > 0.5:
			for tg in data['intents']:
				if tg['tag'] == tag:
					responses = tg['responses']
					answer = random.choice(responses)
					break
		else:
			answer = "I did not get that. Please try again."
	else:
		if 'engineering' in question:
			answer += '\nFollowing are the top scholarships in India:\n1. LIC Golden Jubilee Scholarships\n2. NTPC Scholarship Scheme\n3. VIT University Ignite Scholarships\n4. Merit-Cum-Means based Scholarships\nPlease visit out page to get detailed information.'
		if 'commerce' in question:
			answer += '\nFollowing are the top scholarships in India:\n1. Sarla Devi Scholarship\n2. CLP India Scholarship Theme\n3. IIM Calcutta Fellow Program\n4. South India Bank Scholarship Theme.\nPlease visit out page to get detailed information.'
		if 'physically challenged' in question:
			answer += '\nStudents with 40% or more disability whose monthly family income does not exceed Rs. 15,000/-are eligible for scholarship. A scholarship of Rs. 700/- per month to day scholars and Rs. 1,000/- per month to hostellers is provided to the students pursuing Graduate and Post Graduate level technical or professional courses. A scholarship or Rs. 400/- per month to day scholars and Rs. 700/- per month to hostellers is provided for pursuing diploma and certificate level professional courses. In addition to the scholarship, the students are reimbursed the course fee subject to a ceiling of Rs. 10,000/- per year. Financial assistance under the scheme is also given for computer with editing software for blind/ deaf graduate and postgraduate students pursuing professional courses and for support access software for cerebral palsied students'
			answer += "You could find many more scholarships in different fields. Just check out our scholarships page."
	conv = Conversation()
	conv.question = question
	conv.answer = answer
	conversations.append(conv)
	return render(request, 'home.html', {'conversations': conversations})