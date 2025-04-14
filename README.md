
# Weather trends in Tromsø region

This is a project looking at the weather of Tromsø and the surrounding area to look at how it's changed over the years, how long the data has been collected and how the quality of the data has changed over time, using data collected from the [FROST API](https://frost.met.no/index.html). This is part of the exam for HEL-8048, a UiT course in the spring of 2025.


## Installation

This project requires specific modules to run properly. Below are the instructions to set up the environment using **conda**. If you want to use something else
the packages and their version can be found in the *environment.yml* file.

To set up the environment, you need to have [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed.

### Create the Environment

Run the following command in your terminal to create the conda environment where it will be named **troms_weather**:
```
conda env create -f environment.yml
```
Activate said environment with the code:
```
conda activate troms_weather
```

### Obtaining the client files

To use the FROST API you also need additional client files when collecting the data. To obtain these cliend IDs go to click [here](https://frost.met.no/howto.html) and click on *CREATE A USER* and follow the instructions. You will then recive a client ID and a secret client ID. These will need to be put in two text files names 'client_id.txt' and 'client_secret.txt' within the 'client_files' folder with nothing else in them.

When all this is done, you can now run the scripts in this project. 

## Overview 

This project is in several folders and organized in this manner:
<pre>'''
.
├── LICENSE
├── README.md
├── client_files
├── data
│   ├── Basisdata_55_Troms_25833_N1000Hoyde_GML.gfs
│   ├── Basisdata_55_Troms_25833_N1000Hoyde_GML.gml
│   └── Kommuner-L.geojson
├── docs
│   ├── iTromso-februar-newspaper.pdf
│   ├── Justifications and Descisions.pdf
│   ├── main_project.html
│   └── main_project.pdf
├── environment.yml
├── scripts
│   ├── main_project.ipynb
│   ├── reading_data.py
│   └── supporting_information.ipynb
''' </pre>

'client_files' should contain two files called 'client_id.txt' and client_secret.txt' with information given in the installation section. 
'data' includes data needed to make certain plots and figures in addition to the gathered data from the FROST API.
'docs' contain a newspaper related to the main project as well as the justification document and a htlm and pdf version of the main project file. 
'scripts' contains all the scripts for this project
- 'main_project.ipynb' is the main project for the exam is found. 
- 'reading_data.py' is a supporting module to the main project, used to collect the information from the API
- 'supporting_information.ipynb' is a jupyter notebook containing other scripts and work not included in the main project file. 
'environment.yml' is an environment file containing all necessary dependencies
'LICENSE' includes the terms and conditions for the lisence used for this project

## Sources 

Geojson of Norway found in 'data' is gathered from [fylker-og-kommuner](https://github.com/robhop/fylker-og-kommuner) github.  
Basisdata found in 'data' is gathered from [Kartkatalog Norge](https://kartkatalog.geonorge.no/).  
Newspaper from 1975 is from the national library in Norway.   

## Authors

- ([@trhaugen](https://github.com/trhaugen))

## Contributing

Contributions are always welcome, big and small. If you have any suggestions for further use and development they are also welcome. 

## How to cite

If you use this project in your research or publication, please cite it as:
'''
@misc{tromsweather,
  author       = {Tonje R. Haugen},
  title        = {Weather trends in Tromsø region},
  year         = {2025},
  url          = {https://github.com/trhaugen/troms_weather},
  note         = {GitHub repository}
}
'''
Alternatively, mention the repository link directly in your work:

    Haugen, T.R. Weather trend in Tromsø. GitHub, 2025. Available at: https://github.com/trhaugen/troms_weather

## License

[GNU GPLv3 ](https://choosealicense.com/licenses/gpl-3.0/)

