---
layout: post
title:  Tailored Learning
image:
  feature: pepper_crop.png
tags:   machine_learning
date:   2020-12-08 8:27
---

In this series on multilingual models, we'll construct a pipeline that leverages a transfer learning model to train a text classifier using text in *one* language, and then apply that trained model to predictions for text in *another* language. In our [first post](https://rebeccabilbro.github.io/small-data-delegated-literacy/), we considered the rise of small data and the role of transfer learning in delegated literacy. In this post, we'll prepare our domain-specific training corpus and construct our tailored learning pipeline using Multilingual BERT.

## Language, Forwards and Backwards

The transfer learning model we'll be using to bootstrap our multilingual complaint detector is based on a transformer model architecture called [BERT, or Bidirectional Encoder Representations from Transformers](https://arxiv.org/abs/1810.04805), which was originally published in 2018.

BERT models learn all sentences in the corpus twice &mdash; first left-to-right as we typically read most romance languages, and then with the order of all sentences reversed. They do so in a so-called "self-supervised" fashion using (1) attention masks, where the model masks 15% of the input words at random, and then iteratively learns to predict the missing words and (2) next sentence prediction, where the sentences are reordered at random and the model learns to predict the sentences which actually preceed each other.

The model we'll be using here is mBert, or Multilingual BERT, a variant that was pretrained on a large [multilingual](https://github.com/google-research/bert/blob/master/multilingual.md#list-of-languages) corpus from Wikipedia. We'll be using the version of the model published in the `transformers` library by [Hugging Face](https://huggingface.co/models). Make sure you have `pip installed` the following libraries: `transformers`, `torch`, and `tensorflow`.


## Prepare the Data

This project requires two datasets, both containing reviews of books. The first dataset contains Hindi-language book reviews, and was originally gathered from Raghvendra Pratap Singh
([MrRaghav](https://github.com/MrRaghav)) via [his GitHub repository](https://github.com/MrRaghav/Complaints-mining-from-Hindi-product-reviews) concerning complaint-mining in product reviews.

### Prepare the Hindi Data

This dataset includes both book and phone reviews. Let's keep only the book reviews, which will leave us with 2839 instances.

```python
hindi_reviews = pd.read_excel(
    "amazon-youtube-hindi-complaints-data.xlsx",
    sheet_name="Sheet1"
)

hindi_reviews = hindi_reviews[hindi_reviews.Category == "Book"]
hindi_reviews = hindi_reviews.drop(columns=["Category"])
hindi_reviews.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Label</th>
      <th>Reviews</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>किंडल आपके साथ इस किताब को पढ़ने में मुझे कंटि...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>मुस्लिम शासकों उनके अत्याचारों से हिन्दू जनता ...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>पर नशा है आईएएस की तैयारी</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0</td>
      <td>एकदम जबरदस्त किताब है</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0</td>
      <td>एक जबरदस्त कहानी</td>
    </tr>
  </tbody>
</table>
</div>

### Prepare the English Data

The second dataset contains English-language book reviews, and is a subset of the [Amazon product review corpus](https://registry.opendata.aws/amazon-reviews-ml/), a (unfortunately English-only, to my knowledge) portion of which is available from [Julian McAuley at UCSD](https://cseweb.ucsd.edu/~jmcauley/) [here](http://jmcauley.ucsd.edu/data/amazon/).

Note that it's a 3 gig file, compressed, so we'll add a parameter to our parsing function to allow us to limit the number of rows we parse from the training data and shorten the training time. We'll also create a function that will examine the numeric review rating, which is between 1 and 5, and label as a "complaint" any review with a score of less than 2.


```python
def parse(path, n_rows=10000):
    g = gzip.open(path, 'rb')
    idx = 0
    for line in g:
        if idx > n_rows:
            break
        else:
            idx += 1
            yield eval(line)

def make_dataframe(path):
    idx = 0
    df = {}
    for dictionary in parse(path):
        df[idx] = dictionary
        idx += 1
    return pd.DataFrame.from_dict(df, orient='index')

def get_complaints(rating):
    if rating > 2:
        return 0
    else:
        return 1
```

```python
english_reviews = make_dataframe("reviews_Books_5.json.gz")

english_reviews["Score"] = english_reviews["overall"].apply(get_complaints)

english_reviews = english_reviews.drop(
    columns=[
        "reviewerID", "asin", "reviewerName", "helpful",
        "summary", "unixReviewTime", "reviewTime", "overall"
    ]
)
english_reviews.columns = ["Reviews", "Label"]
english_reviews.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Reviews</th>
      <th>Label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Spiritually and mentally inspiring! A book tha...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>This is one my must have books. It is a master...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>This book provides a reflection that you can a...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>I first read THE PROPHET in college back in th...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A timeless classic.  It is a very demanding an...</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>


## Set up Model Architecture

Now that the data is loaded into dataframes, we'll start setting up the model architecture.

---

**NOTE**: The architecture for this model was inspired by [emarkou's WIP Text classification using multilingual BERT](https://github.com/emarkou/multilingual-bert-text-classification), which attempts to reproduce the results presented in [Beto, Bentz, Becas: The Surprising Cross-Lingual Effectiveness of BERT](https://www.aclweb.org/anthology/D19-1077.pdf), a zero-shot text classification with BERT.

---

With deep learning models, the first step is to establish a few fixed variables for the number of epochs, the maximum length of sequences, the batch size, a random seed for training, , and the path to where we'd like to store the trained model. Given that these values are hard-coded and won't change, I'm configuring them as global variables.


```python
EPOCHS = 3
MAX_LEN = 128
BATCH_SIZE = 32
RANDOM_SEED = 38

STORE_PATH = os.path.join("..", "results")

if not os.path.exists(STORE_PATH):
    os.makedirs(STORE_PATH)
```

### Tokenizing and Masking the Data

Now we need functions that can take in the dataframes and return tokenized feature vectors and attention masks.


```python
def prep(df):
    """
    This prep function will take the feature dataframe as input,
    perform tokenization, and return the encoded feature vectors
    """
    sentences = df.values
    tokenizer = BertTokenizer.from_pretrained(
        'bert-base-multilingual-cased', do_lower_case=True
    )

    encoded_sentences = []
    for sent in sentences:
        encoded_sent = tokenizer.encode(
            sent,
            add_special_tokens=True,
            truncation=True,
            max_length=MAX_LEN
        )

        encoded_sentences.append(encoded_sent)

    encoded_sentences = pad_sequences(
        encoded_sentences,
        maxlen=MAX_LEN,
        dtype="long",
        value=0,
        truncating="post",
        padding="post"
    )

    return encoded_sentences


def attn_mask(encoded_sentences):
    """
    This function takes the encoded sentences as input and returns
    attention masks ahead of BERT training.

    A 0 value corresponds to padding, and a value of 1 is an actual token.
    """

    attention_masks = []
    for sent in encoded_sentences:
        att_mask = [int(token_id > 0) for token_id in sent]
        attention_masks.append(att_mask)
    return attention_masks
```

We can use these functions after splitting our training data to preprocess it:


```python
X = english_reviews["Reviews"]
y = english_reviews["Label"]

# Create train and test splits
X_train, X_test, y_train, y_test = tts(
    X, y, test_size=0.20, random_state=38, shuffle=True
)

X_train_encoded = prep(X_train)
X_train_masks = attn_mask(X_train_encoded)

X_test_encoded = prep(X_test)
X_test_masks = attn_mask(X_test_encoded)
```

### Convert the input layer to tensors

BERT models expect tensors as inputs rather than arrays, so we'll convert everything to tensors next:

```python
train_inputs = torch.tensor(X_train_encoded)
train_labels = torch.tensor(y_train.values)
train_masks = torch.tensor(X_train_masks)

validation_inputs = torch.tensor(X_test_encoded)
validation_labels = torch.tensor(y_test.values)
validation_masks = torch.tensor(X_test_masks)
```


### Configure Data Loaders for Training and Validation

Our next step is to create `DataLoaders` capable of sequentially feeding the data into the BERT model.

```python
train_data = TensorDataset(
    train_inputs,
    train_masks,
    train_labels
)
train_sampler = SequentialSampler(train_data)
trainer = DataLoader(
    train_data,
    sampler=train_sampler,
    batch_size=BATCH_SIZE
)

# data loader for validation
validation_data = TensorDataset(
    validation_inputs,
    validation_masks,
    validation_labels
)
validation_sampler = SequentialSampler(validation_data)
validator = DataLoader(
    validation_data,
    sampler=validation_sampler,
    batch_size=BATCH_SIZE
)
```

### Load the BERT Model

Now we'll load the pre-trained BERT model, prepare the optimizer (the mechanism by which the model will improve incrementally over the course of training), and the scheduler:

```python
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)

model = BertForSequenceClassification.from_pretrained(
    "bert-base-multilingual-cased",
    num_labels=2,   # we are doing binary classification
    output_attentions=False,
    output_hidden_states=False,
)

optimizer = AdamW(
    model.parameters(),
    lr=3e-5,
    eps=1e-8,
    weight_decay=0.01
)

total_steps = len(trainer) * EPOCHS
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=0,
    num_training_steps=total_steps
)
```

## Tailored Learning

Now we're almost ready to start the augmented training of the pre-trained BERT model so that it will be able to identify the critical book reviews. The last two things we need are a method for computing the model's accuracy, which will tell us how we're doing over the course of training, and a training function that will trigger BERT's internal training mechanisms.

```python
def compute_accuracy(y_pred, y_true):
    """
    Compute the accuracy of the predicted values
    """
    predicted = np.argmax(y_pred, axis=1).flatten()
    actual = y_true.flatten()
    return np.sum(predicted==actual)/len(actual)


def train_model(train_loader, test_loader, epochs):
    losses = []
    for e in range(epochs):
        print('======== Epoch {:} / {:} ========'.format(e + 1, epochs))
        start_train_time = time.time()
        total_loss = 0
        model.train()
        for step, batch in enumerate(train_loader):

            if step%10 == 0:
                elapsed = time.time() - start_train_time
                print(
                    "{}/{} --> Time elapsed {}".format(
                        step, len(train_loader), elapsed
                    )
                )

            input_data, input_masks, input_labels = batch
            input_data = input_data.type(torch.LongTensor)
            input_masks = input_masks.type(torch.LongTensor)
            input_labels = input_labels.type(torch.LongTensor)

            model.zero_grad()

            # forward propagation
            out = model(
                input_data,
                token_type_ids=None,
                attention_mask=input_masks,
                labels=input_labels
            )
            loss = out[0]
            total_loss = total_loss + loss.item()

            # backward propagation
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1)
            optimizer.step()

        epoch_loss = total_loss/len(train_loader)
        losses.append(epoch_loss)
        print("Training took {}".format(
            (time.time() - start_train_time)
        ))

        # Validation
        start_validation_time = time.time()
        model.eval()
        eval_loss, eval_acc = 0, 0
        for step, batch in enumerate(test_loader):
            eval_data, eval_masks, eval_labels = batch
            eval_data = input_data.type(torch.LongTensor)
            eval_masks = input_masks.type(torch.LongTensor)
            eval_labels = input_labels.type(torch.LongTensor)

            with torch.no_grad():
                out = model(
                    eval_data,
                    token_type_ids=None,
                    attention_mask=eval_masks
                )
            logits = out[0]

            batch_acc = compute_accuracy(
                logits.numpy(), eval_labels.numpy()
            )

            eval_acc += batch_acc

        print(
            "Accuracy: {}, Time elapsed: {}".format(
                eval_acc/(step + 1),
                time.time() - start_validation_time
            )
        )

    return losses
```

Now we're ready to train:

```python
losses = train_model(trainer, validator, EPOCHS)
```

    ======== Epoch 1 / 3 ========
    0/250 --> Time elapsed 0.007717132568359375
    10/250 --> Time elapsed 327.6781442165375
    20/250 --> Time elapsed 671.3720242977142
    30/250 --> Time elapsed 980.1099593639374
    40/250 --> Time elapsed 1277.7987241744995
    50/250 --> Time elapsed 1568.9109942913055
    ...
    ...
    ...
    Training took 9373.865983963013
    Accuracy: 1.0, Time elapsed: 705.2603988647461

We then serialize and save the model:

```python
model_to_save = model.module if hasattr(model, 'module') else model
model_to_save.save_pretrained(STORE_PATH)
```

### Results

In my experiments, where I used only the first 10k rows of the English-language reviews, and only 3 epochs, the total training time on my 4-year-old Macbook Air (i.e. CPUs only and not a ton of horsepower) was just over 7 hours.

To really evaluate our tailored BERT model though, we need to evaluate it on a different dataset, which is where our Hindi-language book reviews come in. Here's how we'll set up our validation function:

```python
def test_model(new_df):
    """
    Test the trained model on a dataset in another language.
    This function assumes the input dataframe contains two columns
    "Reviews" (the text of the review) and "Labels" (the score for
    the review, where a 0 represents no complaint and a 1 represents
    a complaint.)
    """
    X = new_df["Reviews"]
    y = new_df["Label"]

    X_test_encoded = prep(X)
    X_test_masks = attn_mask(X_test_encoded)

    test_inputs = torch.tensor(X_test_encoded)
    test_labels = torch.tensor(y.values)
    test_masks = torch.tensor(X_test_masks)

    test_data = TensorDataset(
        test_inputs,
        test_masks,
        test_labels
    )
    test_sampler = SequentialSampler(test_data)
    tester = DataLoader(
        test_data,
        sampler=test_sampler,
        batch_size=BATCH_SIZE
    )

    model.eval()
    eval_loss, eval_acc = 0, 0

    for step, batch in enumerate(tester):
        eval_data, eval_masks, eval_labels = batch
        eval_data = eval_data.type(torch.LongTensor)
        eval_masks = eval_masks.type(torch.LongTensor)
        eval_labels = eval_labels.type(torch.LongTensor)

        with torch.no_grad():
            out = model(
                eval_data,
                token_type_ids=None,
                attention_mask=eval_masks
            )
        logits = out[0]
        logits = logits.detach().cpu().numpy()
        eval_labels = eval_labels.to('cpu').numpy()
        batch_acc = compute_accuracy(logits, eval_labels)
        eval_acc += batch_acc
    print("Accuracy: {}".format(eval_acc/(step + 1)))
```

Now we can run our validation function over our Hindi-language book reviews, and see how accurately the model is able to predict whether it is reading a critical review, or not:

```python
test_model(hindi_reviews)
```

    Accuracy: 0.9507053004396678

## Conclusion

That's a pretty high score, and in terms of next steps, we should take a look at the predictions coming out of our newly bootstrapped model for both English and Hindi-language reviews, and see if they make sense. For that, I'll have to check with some of my colleagues in India, but will plan to circle back in a future post to discuss the results, including issues such as overfit or imbalance, and next steps for model tuning and deployment.

## Resources

- emarkou, [WIP Text classification using multilingual BERT (mBert)](https://github.com/emarkou/multilingual-bert-text-classification)
- Google Research, [BERT](https://github.com/google-research/bert)
- Hugging Face, [BERT multilingual base model (cased)](https://huggingface.co/bert-base-multilingual-cased)
- Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova, [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)
- Julian McAuley, [Amazon product data](http://jmcauley.ucsd.edu/data/amazon/)
- Jindřich Libovický, Rudolf Rosa, Alexander Fraser, [How Language-Neutral is Multilingual BERT?](https://arxiv.org/abs/1911.03310)
- MrRaghav, [Identifying Complaints from Product Reviews: A Case Study on Hindi](https://github.com/MrRaghav/Complaints-mining-from-Hindi-product-reviews)
- Shijie Wu and Mark Dredze, [Beto, Bentz, Becas: The Surprising Cross-Lingual Effectiveness of BERT](https://www.aclweb.org/anthology/D19-1077.pdf)
- Shijie Wu, Mark Dredze, [Are All Languages Created Equal in Multilingual BERT?](https://arxiv.org/abs/2005.09093)
- Wikipedia, [Domain Adaptation](https://en.wikipedia.org/wiki/Domain_adaptation)
