    with open(r"C:\Users\MASSON\Desktop\ChatBot\intents.json",encoding="utf-8") as file:
        self.data = json.load(file)

    try:
        with open(r"C:\Users\MASSON\Desktop\ChatBot\data.pickle","rb") as f:
            words, labels,training,output = pickle.load(f)

    except:
        words = []
        labels = []
        docs_x = []
        docs_y = []
        for intent in self.data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern,language='french')
                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

        words = [stemmer.stem(w.lower()) for w in words if w != "?"]
        words = sorted(list(set(words)))
        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            bag = []
            wrds = [stemmer.stem(w.lower()) for w in doc]

            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1
            training.append(bag)
            output.append(output_row)

        training = np.array(training)
        output = np.array(output)

        with open(r"C:\Users\MASSON\Desktop\ChatBot\data.pickle","wb") as f:
            pickle.dump((words, labels,training,output),f)

    self.net = tflearn.input_data(shape = [None,len(training[0])])
    self.net = tflearn.fully_connected(self.net,8)
    self.net = tflearn.fully_connected(self.net,8)
    self.net = tflearn.fully_connected(self.net,len(output[0]),activation = "softmax")
    self.net = tflearn.regression(self.net)
    self.model = tflearn.DNN(self.net)

    try:
        self.model.load(r"C:\Users\MASSON\Desktop\ChatBot\model.tflearn")
    except:
        self.model.fit(training,output,n_epoch = 1000,batch_size = 8,show_metric=True)
        self.model.save(r"C:\Users\MASSON\Desktop\ChatBot\model.tflearn")