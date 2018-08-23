import os
import zipfile
import requests
import pandas as pd

WALKING_DATASET = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00286/User%20Identification%20From%20Walking%20Activity.zip",
)

def download_data(path='data', urls=WALKING_DATASET):
    if not os.path.exists(path):
        os.mkdir(path)

    for url in urls:
        response = requests.get(url)
        name = os.path.basename(url)
        with open(os.path.join(path, name), 'wb') as f:
            f.write(response.content)

if __name__ == "__main__":
    download_data()
    z = zipfile.ZipFile(os.path.join('data', 'User%20Identification%20From%20Walking%20Activity.zip'))
    z.extractall(os.path.join('data', 'walking'))

    # Concatenate all the separate files into a single file
    PATH = os.path.join('data', 'walking','User Identification From Walking Activity')
    columns = ["timestep", "x acceleration", "y acceleration", "z acceleration"]

    allwalkers = pd.DataFrame(columns=columns)

    for root, dirs, files in os.walk(PATH):
        for file in files:
            if file.endswith(".csv"):
                walker = pd.read_csv(os.path.join(PATH, file), header=None)
                walker.columns = columns
                walker["walker_id"] = int(os.path.splitext(file)[0])
                allwalkers = pd.concat([allwalkers, walker])

    allwalkers.to_csv(os.path.join(PATH, "all_walkers.csv"), index=False)
