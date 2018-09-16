---
layout: post
title:  SPARQL from Python
image:
  feature: pepper_crop.png
tags:   programming
date:   2018-07-05 14:42
---

`SPARQLWrapper` is a simple Python wrapper around a SPARQL service for remote query execution. Not only does it enable us to write more complex queries to extract information from RDF than those exposed through a library like `rdflib`, it can also convert query results into other formats like JSON and CSV!

## First, what is SPARQL?

SPARQL ("SPARQL Protocol And RDF Query Language") is a W3C standard for querying [RDF](https://rebeccabilbro.github.io/rdf-basics/) and can be used to express queries across diverse data sources, whether the data is stored natively as RDF or viewed as RDF via middleware. SPARQL contains capabilities for querying required and optional graph patterns along with their conjunctions and disjunctions. SPARQL also supports extensible value testing and constraining queries by source RDF graph. The results of SPARQL queries can be results sets or RDF graphs.

SPARQL allows us to express queries as three-part statements:

    """
    PREFIX ... // identifies & nicknames namespace URIs of desired variables
    SELECT ... // lists variables to be returned (start with a ?)
    WHERE  ... // contains restrictions on variables expressed as triples
    """

## `SPARQLWrapper`

The Python library `SPARQLWrapper` (which can be installed via `pip`) enables us to use the SPARQL query language to interact with remote or local SPARQL endpoints, such as [DBPedia](http://wiki.dbpedia.org/):


```python
from SPARQLWrapper import SPARQLWrapper, JSON

# Specify the DBPedia endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# Query for the description of "Capsaicin", filtered by language
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?comment
    WHERE { <http://dbpedia.org/resource/Capsaicin> rdfs:comment ?comment
    FILTER (LANG(?comment)='en')
    }
""")

# Convert results to JSON format
sparql.setReturnFormat(JSON)
result = sparql.query().convert()

# The return data contains "bindings" (a list of dictionaries)
for hit in result["results"]["bindings"]:
    # We want the "value" attribute of the "comment" field
    print(hit["comment"]["value"])
```

    Capsaicin (/kæpˈseɪ.ᵻsɪn/ (INN); 8-methyl-N-vanillyl-6-nonenamide) is an active component of chili peppers, which are plants belonging to the genus Capsicum. It is an irritant for mammals, including humans, and produces a sensation of burning in any tissue with which it comes into contact. Capsaicin and several related compounds are called capsaicinoids and are produced as secondary metabolites by chili peppers, probably as deterrents against certain mammals and fungi. Pure capsaicin is a volatile, hydrophobic, colorless, odorless, crystalline to waxy compound.


## Querying Wikidata

We can also use the Wikidata Query Service (WDQS) endpoint to query [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page).

Let's say we want to continue our research into spicy things by searching for information about hot sauces in Wikidata. The first step is to find the unique identifier that Wikidata uses to reference "hot sauce", which we can do by searching on Wikidata. It turns out to be "Q522171", which is an "`entity`", which corresponds to the "`wd`" prefix in Wikidata.

If we want to get back results for all of the kinds of hot sauces cataloged in Wikidata, we want to query for the results that have the direct property -- or "`wdt`" in Wikidata prefix speak -- "`<subclasses of>`", which is encoded as "P279" in Wikidata.

_NOTE: For simple WDQS triples, items should be prefixed with `wd:`, and properties with `wdt:`. We don't need to explicitly alias any prefixes in this case because WDQS already knows many shortcut abbreviations commonly used externally (e.g. rdf, skos, owl, schema, etc.) as well as ones internal to Wikidata, such as:_

    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wds: <http://www.wikidata.org/entity/statement/>
    PREFIX wdv: <http://www.wikidata.org/value/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>

More on prefixes [here](https://en.wikibooks.org/wiki/SPARQL/Prefixes).


```python
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Below we SELECT both the hot sauce items & their labels
# in the WHERE clause we specify that we want labels as well as items
sparql.setQuery("""
SELECT ?item ?itemLabel

WHERE {
  ?item wdt:P279 wd:Q522171.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
```

Let's use `pandas` to review the results as a dataframe:

```python
import pandas as pd

results_df = pd.io.json.json_normalize(results['results']['bindings'])
results_df[['item.value', 'itemLabel.value']]
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
      <th>item.value</th>
      <th>itemLabel.value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>http://www.wikidata.org/entity/Q249114</td>
      <td>salsa</td>
    </tr>
    <tr>
      <th>1</th>
      <td>http://www.wikidata.org/entity/Q335016</td>
      <td>Tabasco sauce</td>
    </tr>
    <tr>
      <th>2</th>
      <td>http://www.wikidata.org/entity/Q360459</td>
      <td>Adobo</td>
    </tr>
    <tr>
      <th>3</th>
      <td>http://www.wikidata.org/entity/Q460439</td>
      <td>Blair's 16 Million Reserve</td>
    </tr>
    <tr>
      <th>4</th>
      <td>http://www.wikidata.org/entity/Q966327</td>
      <td>harissa</td>
    </tr>
    <tr>
      <th>5</th>
      <td>http://www.wikidata.org/entity/Q1026822</td>
      <td>Chili oil</td>
    </tr>
    <tr>
      <th>6</th>
      <td>http://www.wikidata.org/entity/Q1392674</td>
      <td>sriracha sauce</td>
    </tr>
    <tr>
      <th>7</th>
      <td>http://www.wikidata.org/entity/Q2227032</td>
      <td>mojo</td>
    </tr>
    <tr>
      <th>8</th>
      <td>http://www.wikidata.org/entity/Q2279518</td>
      <td>Shito</td>
    </tr>
    <tr>
      <th>9</th>
      <td>http://www.wikidata.org/entity/Q2402909</td>
      <td>Valentina</td>
    </tr>
    <tr>
      <th>10</th>
      <td>http://www.wikidata.org/entity/Q3273096</td>
      <td>Doubanjiang</td>
    </tr>
    <tr>
      <th>11</th>
      <td>http://www.wikidata.org/entity/Q3474141</td>
      <td>sauce samouraï</td>
    </tr>
    <tr>
      <th>12</th>
      <td>http://www.wikidata.org/entity/Q3474250</td>
      <td>Q3474250</td>
    </tr>
    <tr>
      <th>13</th>
      <td>http://www.wikidata.org/entity/Q4922876</td>
      <td>Nam phrik</td>
    </tr>
    <tr>
      <th>14</th>
      <td>http://www.wikidata.org/entity/Q5104402</td>
      <td>Cholula Hot Sauce</td>
    </tr>
    <tr>
      <th>15</th>
      <td>http://www.wikidata.org/entity/Q6961170</td>
      <td>Nam chim</td>
    </tr>
    <tr>
      <th>16</th>
      <td>http://www.wikidata.org/entity/Q16628511</td>
      <td>Q16628511</td>
    </tr>
    <tr>
      <th>17</th>
      <td>http://www.wikidata.org/entity/Q16642516</td>
      <td>Q16642516</td>
    </tr>
  </tbody>
</table>
</div>

Success!

### More on SPARQL & SPARQL Endpoints

 - [Learning SPARQL, 2nd Edition, by Bob DuCharme](https://www.amazon.com/Learning-SPARQL-Querying-Updating-1-1/dp/1449371434).
 - Querying Wikidata with SPARQL [tutorial](https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial).
 - [Video tutorial](https://youtu.be/1jHoUkj_mKw) on using Wikidata Query Service.
 - Test out Wikidata SPARQL queries [here](https://query.wikidata.org/).
 - Using DBPedia with SPARQL [video](https://youtu.be/BmHKb0kLGtA).
 - Cool site for finding [live SPARQL endpoints](http://sparqles.ai.wu.ac.at/availability).
