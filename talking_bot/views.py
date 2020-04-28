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

#Text Reading
from django.http import HttpResponse
import pytesseract as tess
from PIL import Image
import re

def show(request):
	tess.pytesseract.tesseract_cmd = r'C:\Users\Admin\AppData\Local\Tesseract-OCR\tesseract.exe'
	img = Image.open('media/res.png')
	text = tess.image_to_string(img)
	lines = [el.strip().lower() for el in text.split('\n') if len(el.strip()) > 0]
	text = ' '.join(lines)
	# print(text)
	phone = None
	pattern = re.compile(r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}')
	m = re.finditer(pattern, text)
	for match in m:
		phone = match.group(0)
	print(phone)

	email = None
	pattern = re.compile(r'(\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+)')
	m = re.finditer(pattern, text)
	for match in m:
		email = match.group(0)
	print(email)

	education = []
	pattern = re.compile(r"(be|me|bsc|msc|btech|ba|ma|bachelor|bachelor's degree|master|master's degree|doctorate)\s?(of|in)\s?(\w+)")
	m = re.finditer(pattern, text)
	for match in m:
		education.append(match.group(3))
	print(education)

	scores = []
	pattern = re.compile(r'(cgpa|c.g.p.a.)\s*(\d+.?\d+)')
	m = re.finditer(pattern, text)
	for match in m:
		scores.append(match.group(2))
	pattern = re.compile(r'(\d+.?\d+)%')
	m = re.finditer(pattern, text)
	for match in m:
		scores.append(match.group(1))
	pattern = re.compile(r'(\d+.?\d+)(/\d+.?\d+)?\s*(cgpa|c.g.p.a.)')
	m = re.finditer(pattern, text)
	for match in m:
		scores.append(match.group(1))

	print(scores)

	return HttpResponse('Text Read Successfully')

from django.shortcuts import render, redirect
from .models import Images
from .forms import ImagesForm

def home_view(request):
    context = {}
    if request.method == "POST":
        form = ImagesForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("img")
            obj = Images.objects.create(
                                 name = name,
                                 img = img
                                 )
            obj.save()
            return redirect('show')
    else:
        form = ImagesForm()
    context['form']= form
    return render(request, "resume.html", context)