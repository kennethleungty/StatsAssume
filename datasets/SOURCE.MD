## Data Sources

Here is a list of toy datasets available for usage in StatsAssume

| Name | Info | Task | Source |
| --- | --- | --- | --- |
| **Auto** | Gas mileage, horsepower, and other information for cars | Regression | [:link:](https://www.statlearning.com/s/Auto.csv) |
| **College** | Demographic characteristics, tuition, and more for USA colleges | Regression | [:link:](https://github.com/nguyen-toan/ISLR/blob/master/dataset/College.csv) |
| **Credit** | Information about credit card debt for 10,000 customers | Regression | [:link:](https://github.com/nguyen-toan/ISLR/blob/master/dataset/Credit.csv) |
| **Fish** | Fish Market Dataset. 'Fish_processed.csv' is pre-processed (one-hot encoded) version of Fish.csv | Regression | [:link:](https://www.kaggle.com/aungpyaeap/fish-market)|
| **Heart** | Heart disease dataset | Classification | [:link:](https://www.statlearning.com/s/Heart.csv) |
| **Income2** | Income data based on education and seniority  | Regression | [:link:](https://github.com/nguyen-toan/ISLR/blob/master/dataset/Income2.csv) |
| **Insurance** | Personal medical insurance costs | Regression | [:link:](https://github.com/stedy/Machine-Learning-with-R-datasets/blob/master/insurance.csv) |

To load the toy dataset in the Jupyter notebook, use the `load_data` function with the dataset name as the parameter (WITHOUT the .csv suffix) e.g. 
```python 
df = load_data('Auto')
```

We are open to contributions of more toy datasets!