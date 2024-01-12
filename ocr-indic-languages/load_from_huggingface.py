!pip install datasets
import datasets

#Lets download this dataset using Python https://huggingface.co/datasets/wikimedia/wikipedia/tree/main/20231101.or
#This download has tons of languages, but we only want Odia language.

wiki_df = datasets.load_dataset('wikimedia/wikipedia', 
                                '20231101.or', #Passing language code, as mentioned in the website
                                ) #This is a dictionary with 'train' as its only key
wiki_df = wiki_df['train'] #selecting the train split

wiki_df = wiki_df.to_pandas() #Converting it to pandas dataframe.

#From here, all pandas operations can be applied to wiki_df.

