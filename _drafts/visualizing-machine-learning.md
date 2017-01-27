# Visualizing Machine Learning: Scikit-Learn, Yellowbrick, and Deadly Fungi


# How to compare models for machine learning

In this lab, we are going to look at scores for a variety of models and compare them in order to select the best model for our data. We will build two pipelines- one that runs just a selected estimator and one that will include a SelectFromModel step prior to modeling our data. We will write our scores to a file that we can use for creating plots comparing the models.

This lab borrows heavily from the [Census notebook](https://github.com/georgetown-analytics/machine-learning/tree/master/examples/bbengfort/census) we reviewed at the end of the machine learning class. We did this to reinforce the concepts we went over in Machine Learning and to show you another way to adapt that code to different data. We are going to use a different UCI data set in this exercise-- the Mushroom Data Set. Our objective is to predict if a mushroom is poisionous or edible based on its characteristics.

Sources:

http://archive.ics.uci.edu/ml/machine-learning-databases/mushroom

https://github.com/gumption/Python_for_Data_Science

https://github.com/georgetown-analytics/machine-learning/tree/master/examples/bbengfort/census


```python
import json
import os
import pickle
import requests
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cross_validation import KFold, StratifiedKFold, train_test_split
from sklearn.datasets.base import Bunch
from sklearn.ensemble import BaggingClassifier, ExtraTreesClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import ElasticNetCV, LogisticRegressionCV, LogisticRegression, SGDClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, auc, roc_curve, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.svm import LinearSVC, NuSVC, SVC
```

    /Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/sklearn/cross_validation.py:44: DeprecationWarning: This module was deprecated in version 0.18 in favor of the model_selection module into which all the refactored classes and functions are moved. Also note that the interface of the new CV iterators are different from that of this module. This module will be removed in 0.20.
      "This module will be removed in 0.20.", DeprecationWarning)



```python
%matplotlib inline
pd.set_option('display.max_columns', 500)
```

## Fetch the data

We are going to use a **modified** version of the [Mushroom Dataset](https://archive.ics.uci.edu/ml/datasets/Mushroom) from the UCI machine learning library.

## Data Exploration

We have provided two files- agaricus-lepiota.data, and agaricus-lepiota.names. The names file provides us with the following information:

Relevant Information:
    This data set includes descriptions of hypothetical samples
    corresponding to 23 species of gilled mushrooms in the Agaricus and
    Lepiota Family (pp. 500-525).  Each species is identified as
    definitely edible, definitely poisonous, or of unknown edibility and
    not recommended.  This latter class was combined with the poisonous
    one.  The Guide clearly states that there is no simple rule for
    determining the edibility of a mushroom; no rule like ``leaflets
    three, let it be'' for Poisonous Oak and Ivy.

Number of Instances: 8124

Number of Attributes: 22 (all nominally valued)

**However**, for this exercise, we're going to use the class labels and the first three attributes.

Attribute Information: (classes: edible=e, poisonous=p)
     1. cap-shape:                bell=b,conical=c,convex=x,flat=f,
                                  knobbed=k,sunken=s
     2. cap-surface:              fibrous=f,grooves=g,scaly=y,smooth=s
     3. cap-color:                brown=n,buff=b,cinnamon=c,gray=g,green=r,
                                  pink=p,purple=u,red=e,white=w,yellow=y


Class Distribution:
    --    edible: 4208 (51.8%)
    -- poisonous: 3916 (48.2%)
    --     total: 8124 instances           


Let's load the data with pandas.


```python
names = [
    'class',
    'cap-shape',
    'cap-surface',
    'cap-color'
]

mushrooms = os.path.join('data','mushrooms','agaricus-lepiota.data')
data = pd.read_csv(mushrooms, usecols=['p','x','s','n'])
data.columns = names
data.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>class</th>
      <th>cap-shape</th>
      <th>cap-surface</th>
      <th>cap-color</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>e</td>
      <td>x</td>
      <td>s</td>
      <td>y</td>
    </tr>
    <tr>
      <th>1</th>
      <td>e</td>
      <td>b</td>
      <td>s</td>
      <td>w</td>
    </tr>
    <tr>
      <th>2</th>
      <td>p</td>
      <td>x</td>
      <td>y</td>
      <td>w</td>
    </tr>
    <tr>
      <th>3</th>
      <td>e</td>
      <td>x</td>
      <td>s</td>
      <td>g</td>
    </tr>
    <tr>
      <th>4</th>
      <td>e</td>
      <td>x</td>
      <td>y</td>
      <td>y</td>
    </tr>
  </tbody>
</table>
</div>



Our data, including the target, is categorical. We will need to change these values to numeric ones for machine learning.

But first, let's look at some plots of our features. Using what we learned about visualizations with Seaborn, we can quickly plot whether a mushroom is edible or poisonous by each feature.


```python
#seaborn factorplot to show edible/poisonous breakdown by different factors
for name in names[1:]:
    g = sns.factorplot("class", col=name, data=data,
                    kind="count", size=2.5, aspect=.8, col_wrap=7)

```


![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_7_0.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_7_1.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_7_2.png)


The factorplots show us how many mushrooms with each feature value are poisionous or edible. Only "gill color = b" seems to always indicate poisonous mushrooms.

## Data Management

We need to structure our data on disk in a way that we can load into Scikit-Learn in a repeatable fashion for continued analysis. As we have discussed before, we can use sklearn.datasets.base.Bunch object to load the data into data and target attributes respectively, similar to how Scikit-Learn's toy datasets are structured (see Machine Learning lectures and Census notebook).

In order to organize our data on disk, we'll need to add the following files:

README.md: a markdown file containing information about the dataset and attribution. Will be exposed by the DESCR attribute.

meta.json: a helper file that contains machine readable information about the dataset like target_names and feature_names.

The README.md file can be created directly using a text editor. Create your file with a link to the data set and some information on the source of the data as listed on the UCI page. For example, you could use the following information in your README file:

# Mushroom Data Set

Data downloaded from [UCI Machine Learning Repository- Mushroom Data Set](http://archive.ics.uci.edu/ml/machine-learning-databases/mushroom).

## Data Set Information

Origin:

Mushroom records drawn from The Audubon Society Field Guide to North American Mushrooms (1981). G. H. Lincoff (Pres.), New York: Alfred A. Knopf

Donor:

Jeff Schlimmer (Jeffrey.Schlimmer '@' a.gp.cs.cmu.edu)

Prediction task is to determine whether a mushroom is edible or poisonous.





We can write the meta.json file using the data frame that we already have. However, as we saw in the Census example, it is useful to obtain the unique values of categorical data when we have categorical values. It would be more meaningful if the attribute values were full words instead of single letters.

In order to facilitate this, create a file in your text editor called 'agaricus-lepiota.attributes' with the attribute information from the .names file and store it with your data. We will use this to create a dictionary of values for every attribute which we can use to map our values. Copy the attribues information from the .names file and edit the file so each line of the text file contains one attribute and its values. For example:

    class: edible=e, poisonous=p
    cap-shape: bell=b, conical=c, convex=x, flat=f, knobbed=k, sunken=s
    cap-surface: fibrous=f, grooves=g, scaly=y, smooth=s
    ...

When your file is complete, you can review the contents of the file in your notebook using the command below.

(! is a [cell magics](https://ipython.org/ipython-doc/dev/interactive/magics.html) that allows us to make calls to the shell. )


```python
# Run the command appropriate for your OS.

# OSX/ Linux
! cat data/mushrooms/agaricus-lepiota.attributes

# Windows
#! type data\mushrooms\agaricus-lepiota.attributes
```

    class: edible=e, poisonous=p
    cap-shape: bell=b, conical=c, convex=x, flat=f, knobbed=k, sunken=s
    cap-surface: fibrous=f, grooves=g, scaly=y, smooth=s
    cap-color: brown=n ,buff=b, cinnamon=c, gray=g, green=r, pink=p, purple=u, red=e, white=w, yellow=y

We can now use this file to create a list of dictionaries. This list will allow us to easily replace the single letters with the full word it represents.

Luckily, someone else has done the hardwork on this for us. The code below comes from [Python for Data Science](https://github.com/gumption/Python_for_Data_Science).


```python
def load_attribute_names_and_values(filename):
    '''Returns a list of attribute names and values in a file.

    This list contains dictionaries wherein the keys are names
    and the values are value description dictionariess.

    Each value description sub-dictionary will use
    the attribute value abbreviations as its keys
    and the attribute descriptions as the values.

    filename is expected to have one attribute name and set of values per line,
    with the following format:
        name: value_description=value_abbreviation[,value_description=value_abbreviation]*
    for example
        cap-shape: bell=b, conical=c, convex=x, flat=f, knobbed=k, sunken=s
    The attribute name and values dictionary created from this line would be the following:
        {'name': 'cap-shape',
         'values': {'c': 'conical',
                    'b': 'bell',
                    'f': 'flat',
                    'k': 'knobbed',
                    's': 'sunken',
                    'x': 'convex'}}
    '''
    attribute_names_and_values = []  # this will be a list of dicts
    with open(filename) as f:
        for line in f:
            attribute_name_and_value_dict = {}
            attribute_name_and_value_string_list = line.strip().split(':')
            attribute_name = attribute_name_and_value_string_list[0]
            attribute_name_and_value_dict['name'] = attribute_name
            if len(attribute_name_and_value_string_list) < 2:
                attribute_name_and_value_dict['values'] = None # no values for this attribute
            else:
                value_abbreviation_description_dict = {}
                description_and_abbreviation_string_list = attribute_name_and_value_string_list[1].strip().split(',')
                for description_and_abbreviation_string in description_and_abbreviation_string_list:
                    description_and_abbreviation = description_and_abbreviation_string.strip().split('=')
                    description = description_and_abbreviation[0]
                    if len(description_and_abbreviation) < 2: # assumption: no more than 1 value is missing an abbreviation
                        value_abbreviation_description_dict[None] = description
                    else:
                        abbreviation = description_and_abbreviation[1]
                        value_abbreviation_description_dict[abbreviation] = description
                attribute_name_and_value_dict['values'] = value_abbreviation_description_dict
            attribute_names_and_values.append(attribute_name_and_value_dict)
    return attribute_names_and_values


attribute_filename = os.path.join('data','mushrooms','agaricus-lepiota.attributes')
attribute_names_and_values = load_attribute_names_and_values(attribute_filename)

```

We now have a list that contains a dictionary for each column in our data. Take a look at the dictionaries.


```python
attribute_names_and_values[0]
```




    {'name': 'class', 'values': {'e': 'edible', 'p': 'poisonous'}}



We can use these dictionaries to replace our single letters with the full word it stands for and write our new dataframe to a txt file.


```python
# What does the while loop below do? Explain the code to your partner in plain english. Add extra cells to the notebook
# to test pieces of the code if that helps.

i = 0

while i < len(names):
    data.replace({names[i] : attribute_names_and_values[i]['values']}, inplace=True)
    i += 1

data.to_csv(os.path.join('data', 'mushrooms', 'agaricus-lepiota.txt'), header=None, index=False)
data.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>class</th>
      <th>cap-shape</th>
      <th>cap-surface</th>
      <th>cap-color</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>edible</td>
      <td>convex</td>
      <td>smooth</td>
      <td>yellow</td>
    </tr>
    <tr>
      <th>1</th>
      <td>edible</td>
      <td>bell</td>
      <td>smooth</td>
      <td>white</td>
    </tr>
    <tr>
      <th>2</th>
      <td>poisonous</td>
      <td>convex</td>
      <td>scaly</td>
      <td>white</td>
    </tr>
    <tr>
      <th>3</th>
      <td>edible</td>
      <td>convex</td>
      <td>smooth</td>
      <td>gray</td>
    </tr>
    <tr>
      <th>4</th>
      <td>edible</td>
      <td>convex</td>
      <td>scaly</td>
      <td>yellow</td>
    </tr>
  </tbody>
</table>
</div>



Now we can create our meta.json file and bunches.

We are going to reuse code from the [Census notebook](https://github.com/georgetown-analytics/machine-learning/tree/master/examples/bbengfort/census) we discussed in Machine Learning. It has been modified to work with our data here.

This code creates a `meta.json` file by inspecting the data frame that we have constructued. The `target_names` column, is just the two unique values in the `data['class']` series; by using the `pd.Series.unique` method - we're guarenteed to spot data errors if there are more or less than two values. The `feature_names` is simply the names of all the columns.

Then we get tricky &mdash; we want to store the possible values of each categorical field for lookup later, but how do we know which columns are categorical and which are not? Luckily, Pandas has already done an analysis for us, and has stored the column data type, `data[column].dtype`, as either `int64` or `object`. Here I am using a dictionary comprehension to create a dictionary whose keys are the categorical columns, determined by checking the object type and comparing with `object`, and whose values are a list of unique values for that field.



```python
json_file = os.path.join('data','mushrooms','meta.json')

meta = {
    'target_names': list(data['class'].unique()),
    'feature_names': list(data.columns),
    'categorical_features': {
        column: list(data[column].unique())
        for column in data.columns
        if data[column].dtype == 'object'
    },
}

with open(json_file, 'w') as f:
    json.dump(meta, f, indent=2)
```

### Imputation or Drop

According to the information we received with the dataset, there are missing values in the stalk-root feature. Missing values are indicated with '?', which we replaced with the value 'missing'.

Given our lack of subject matter expertise and the numer of instances available, we will drop instances where 'stalk-root' == 'missing'. We want to do that before we create the bunch. If we chose to impute the values, we would pass everything through to the bunch and deal with that value in our pipeline.

**Bonus:** At the end of the exercise, create a bunch with the instances we just dropped and run the data again to see what your scores look like if 'missing' is encoded as an accepted value.

Now that we have everything we need stored on disk, we can create a `load_data` function, which will allow us to load the training and test datasets appropriately from disk and store them in a `Bunch`:


```python
def load_data():
    root = os.path.join('data','mushrooms')
    # Load the meta data from the file
    with open(os.path.join(root, 'meta.json'), 'r') as f:
        meta = json.load(f)

    names = meta['feature_names']

    # Load the readme information
    with open(os.path.join(root, 'README.md'), 'r') as f:
        readme = f.read()

    # Load the data from the file where we updated the feature values
    mushrooms = pd.read_csv(os.path.join(root, 'agaricus-lepiota.txt'), names=names)

    # Remove the target from the categorical features
    meta['categorical_features'].pop('class')

    # Return the bunch with the appropriate data chunked apart
    return Bunch(
        data = mushrooms[names[1:]],
        target = mushrooms[names[0]],
        target_names = meta['target_names'],
        feature_names = meta['feature_names'],
        categorical_features = meta['categorical_features'],
        DESCR = readme,
    )

dataset = load_data()
```

Compare the code above to the load_data() function in the Census notebook. What was changed? Why?

## Feature Extraction

Unfortunately, the categorical values themselves are not useful for machine learning; we need a single instance table that contains _numeric values_. In order to extract this from the dataset, we'll have to use Scikit-Learn transformers to transform our input dataset into something that can be fit to a model. In particular, we'll have to do the following:

- encode the categorical labels as numeric data
- impute missing values with data (or remove)

Our first step is to get our data out of the object data type land and into a numeric type, since nearly all operations we'd like to apply to our data are going to rely on numeric types. Luckily, Sckit-Learn does provide a transformer for converting categorical labels into numeric integers: [`sklearn.preprocessing.LabelEncoder`](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html).

Unfortunately it can only transform a single vector at a time, so we'll have to adapt it in order to apply it to multiple columns. We can do this a couple of different ways: write code that uses a loop to encode each column or create a multicolumn LabelEncoder.

The ability to create custom transformers to use in a pipeline is a powerful skill to have. Let's use the LabelEncoder from the Census notebook and use it with the mushroom data.


```python
class EncodeCategorical(BaseEstimator, TransformerMixin):
    """
    Encodes a specified list of columns or all columns if None.
    """

    def __init__(self, columns=None):
        self.columns  = [col for col in columns]
        self.encoders = None

    def fit(self, data, target=None):
        """
        Expects a data frame with named columns to encode.
        """
        # Encode all columns if columns is None
        if self.columns is None:
            self.columns = data.columns

        # Fit a label encoder for each column in the data frame
        self.encoders = {
            column: LabelEncoder().fit(data[column])
            for column in self.columns
        }
        return self

    def transform(self, data):
        """
        Uses the encoders to transform a data frame.
        """
        output = data.copy()
        for column, encoder in self.encoders.items():
            output[column] = encoder.transform(data[column])

        return output
```

If we use the class as written, we will have the ability to use this to transform all of our features using the LabelEncoder. We will use it as part of our pipeline.

## Model Evaluation

Let's build a way to evaluate multiple estimators, both on their own and using [SelectFromModel](http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectFromModel.html).


```python
# set some things up for our function

if not os.path.exists(os.path.join('data', 'mushrooms', 'output')):
                      os.mkdir(os.path.join('data', 'mushrooms', 'output'))

OUTPATH = os.path.abspath(os.path.join('.', 'data', 'mushrooms', 'output'))
print(OUTPATH)
```

    /Users/rebeccabilbro/Desktop/stuff/XBUS-506-01.Visual_Analytics/select/data/mushrooms/output



```python
def model_selection(dataset, feature_model, model_estimator, fse_label, model_label):

    """
    Test various combinations of estimators for feature selection and modeling.
    The pipeline generates the dataset, encodes columns, then uses the encoded results for feature selection.
    Finally,the selected features are sent to the estimator model for scoring.
    """

    start  = time.time()

    # assign X
    X = dataset.data
    # assign y, encoding the target value
    y = LabelEncoder().fit_transform(dataset.target)

    if feature_model == 'none':
        # use the pipeline that does not use SelectFromModel
        model = Pipeline([
                 ('label_encoding', EncodeCategorical(dataset.categorical_features.keys())),
                 ('one_hot_encoder', OneHotEncoder()),
                 ('estimator', model_estimator)
            ])
    else:
        #use the pipeline that has SelectFromModel
        model = Pipeline([
                         ('label_encoding', EncodeCategorical()),
                         ('one_hot_encoder', OneHotEncoder()),
                         ('estimator', model_estimator),
                         ('feature_selection', SelectFromModel(feature_model)),
                         ('estimator', model_estimator)
                          ])

    """
    Train and test the model using StratifiedKFold cross validation. Compile the scores for each iteration of the model.
    """
    scores = {'accuracy':[], 'auc':[], 'f1':[], 'precision':[], 'recall':[]}

    for train, test in StratifiedKFold(y, n_folds=4, shuffle=True):  # Ben says always use 12 folds! We cheat a bit here...
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

        model.fit(X_train, y_train)
        expected  = y_test
        predicted = model.predict(X_test)

        ## Visualize scores
        fpr, tpr, thresholds = roc_curve(expected, predicted)
        roc_auc = auc(fpr, tpr)
        plt.figure()
        plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC-AUC for {}'.format(model_label))
        plt.legend(loc="lower right")
        plt.show()

        ## Record scores
        scores['accuracy'].append(accuracy_score(expected, predicted))
        scores['f1'].append(f1_score(expected, predicted, average='binary'))
        scores['precision'].append(precision_score(expected, predicted, average='binary'))
        scores['recall'].append(recall_score(expected, predicted, average='binary'))

        """
        AUC cannot be computed if only 1 class is represented in the data. When that happens, record an AUC score of 0.
        """
        try:
            scores['auc'].append(roc_auc_score(expected, predicted))
        except:
            scores['auc'].append(0)

    """
    Print the modeling details and the mean score.
    """
    print("\nBuild and Validation of took {:0.3f} seconds\n".format(time.time()-start))
    print("Feature Selection Estimator: {}\n".format(fse_label))
    print("Estimator Model: {}\n".format(model_label))
    print("Validation scores are as follows:\n")
    print(pd.DataFrame(scores).mean())

    """
    Create a data frame with the mean score and estimator details.
    """
    df = pd.DataFrame(scores).mean()
    df['SelectFromModel'] =  fse_label
    df['Estimator']  = model_label

    """
    Write official estimator to disk
    """
    estimator = model
    estimator.fit(X,y)

    pickle_path = os.path.join(OUTPATH + "/", fse_label.lower().replace(" ", "-") + "_" + model_label.lower().replace(" ", "-") + ".pickle")
    with open(pickle_path, 'wb') as f:
        pickle.dump(estimator, f)

    print("\nFitted model written to:\n{}".format(os.path.abspath(pickle_path)))

    return df
```

Read through the function and make sure you understand what it is doing.

First, it uses the pipeline based on whether or not there is a SelectFromModel estimator provided.

It then splits the data runs the model multiple times on different sets of data. It creates a dictionary of scores for each model, printing the mean of each set of scores.

Next, the estimator is fit with all the data and saved to a pickle file on your drive.

Last, the function returns a dataframe object with the mean scores from modeling and the label for each of the estimators.

When we call the function, we are transposing the returned dataframe and appending it to a new dataframe. Once we are done doing the calls we want, we save the final dataframe as a csv file. We can review this manually and also use it to plot information about how our models perform.

Below, we are making the calls. Use the examples provided to add additional items to model including calls with an estimator to use for SelectFromModel. As an example:

evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, LogisticRegression(), LinearSVC(), "LogisticRegression", "LinearSVC")).T)


```python
evaluation = pd.DataFrame()

evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", LogisticRegression(), "none", "LogisticRegression")).T)
evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", KNeighborsClassifier(), "none", "KNeighborsClassifier")).T)
evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", BaggingClassifier(KNeighborsClassifier()), "none", "BaggedKNeighborsClassifier")).T)
evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", RandomForestClassifier(), "none", "RandomForestClassifier")).T)
evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", ExtraTreesClassifier(), "none", "ExtraTreesClassifier")).T)
evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", SGDClassifier(), "none", "SGDClassifier")).T)
evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", LinearSVC(), "none", "LinearSVC")).T)

evaluation.to_csv(os.path.join('data', 'mushrooms', 'model_comparison.csv'), index=False)
```


![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_0.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_1.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_2.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_3.png)



    Build and Validation of took 0.784 seconds

    Feature Selection Estimator: none

    Estimator Model: LogisticRegression

    Validation scores are as follows:

    accuracy     0.662066
    auc          0.662157
    f1           0.658520
    precision    0.650940
    recall       0.666383
    dtype: float64

    Fitted model written to:
    /Users/rebeccabilbro/Desktop/stuff/XBUS-506-01.Visual_Analytics/select/data/mushrooms/output/none_logisticregression.pickle



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_5.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_6.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_7.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_8.png)



    Build and Validation of took 2.969 seconds

    Feature Selection Estimator: none

    Estimator Model: KNeighborsClassifier

    Validation scores are as follows:

    accuracy     0.689948
    auc          0.689310
    f1           0.671074
    precision    0.691185
    recall       0.658451
    dtype: float64

    Fitted model written to:
    /Users/rebeccabilbro/Desktop/stuff/XBUS-506-01.Visual_Analytics/select/data/mushrooms/output/none_kneighborsclassifier.pickle



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_10.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_11.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_12.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_13.png)



    Build and Validation of took 20.096 seconds

    Feature Selection Estimator: none

    Estimator Model: BaggedKNeighborsClassifier

    Validation scores are as follows:

    accuracy     0.703749
    auc          0.702855
    f1           0.687697
    precision    0.701511
    recall       0.677895
    dtype: float64

    Fitted model written to:
    /Users/rebeccabilbro/Desktop/stuff/XBUS-506-01.Visual_Analytics/select/data/mushrooms/output/none_baggedkneighborsclassifier.pickle



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_15.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_16.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_17.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_18.png)



    Build and Validation of took 0.958 seconds

    Feature Selection Estimator: none

    Estimator Model: RandomForestClassifier

    Validation scores are as follows:

    accuracy     0.708971
    auc          0.707930
    f1           0.691967
    precision    0.711885
    recall       0.677105
    dtype: float64

    Fitted model written to:
    /Users/rebeccabilbro/Desktop/stuff/XBUS-506-01.Visual_Analytics/select/data/mushrooms/output/none_randomforestclassifier.pickle



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_20.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_21.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_22.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_23.png)



    Build and Validation of took 1.010 seconds

    Feature Selection Estimator: none

    Estimator Model: ExtraTreesClassifier

    Validation scores are as follows:

    accuracy     0.704681
    auc          0.703320
    f1           0.684392
    precision    0.705801
    recall       0.664862
    dtype: float64

    Fitted model written to:
    /Users/rebeccabilbro/Desktop/stuff/XBUS-506-01.Visual_Analytics/select/data/mushrooms/output/none_extratreesclassifier.pickle



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_25.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_26.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_27.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_28.png)



    Build and Validation of took 0.750 seconds

    Feature Selection Estimator: none

    Estimator Model: SGDClassifier

    Validation scores are as follows:

    accuracy     0.612645
    auc          0.616083
    f1           0.586991
    precision    0.592620
    recall       0.647934
    dtype: float64

    Fitted model written to:
    /Users/rebeccabilbro/Desktop/stuff/XBUS-506-01.Visual_Analytics/select/data/mushrooms/output/none_sgdclassifier.pickle



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_30.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_31.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_32.png)



![png](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2017-01-29-model_selection_28_33.png)
