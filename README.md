# PPL model


![](/_readme/logo-ppl.png)    ![](/_readme/DSKC_logo.png)

### Project Structure

(based on [Cookiecutter](https://drivendata.github.io/cookiecutter-data-science/)) 

+ src
    
    + data_curation
    
        Cleaning and pre processing methods, 
        this code creates a train and test dataset.
    
    + modeling
    
        Scripts to train models and then use trained models to make predictions
         
+ model

   Trained and serialized models, model predictions, or model summaries

+ notebooks

    Jupyter notebooks. Naming convention is a number (for ordering), 
    a short `_` delimited description, e.g.
    `1.0_data_curation.ypynb`.
    
+ reports

    
    
### Installation

`pip install -r requirements.txt`

`python -m spacy download en `