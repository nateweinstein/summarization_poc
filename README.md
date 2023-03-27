# summarization_poc

<!-- Make sure that you have conda (python env and package manager) installed -->
https://docs.conda.io/en/latest/miniconda.html

<!-- Create the conda environment -->
conda env create --name envname --file=environments.yml

<!-- To create the model -->
run ``jupyter-notebook``

-This will open your browser
-In the top menu, under Cells, hit "Run all cells"


<!-- The repo already has the content, but to recreate it-->
open ```main.py```: 
    1. tweak the inputs 
    2. update the get_web.py/parseContent if you change the site to crawl
    3. uncomment `generateArticles()`

run ```python main.py```


<!-- To test summarization of local content -->
open ```main.py```: 
    1. uncomment `testSummarizer()
run ```python main.py```
