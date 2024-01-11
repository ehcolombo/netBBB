The repository contains two mains scripts:

getParedao.py
getQueridometro.py

Both developed during the Big Brother Brasil (2021 edition) in collaboration with [quaseobjeto]([https://link-url-here.org](https://linktr.ee/quaseobjeto)https://linktr.ee/quaseobjeto).
This two scripts were part of a mock science project to quantify the interactions among BBB participants using the daily emoji votes (queridometro) and the votes during the elimination round (paredao).
Fights, friendshipts, love stories, and all the drama is quantified by means of networks.

**getParedao.py**
Usage:

Create a file "BBB Stats - paredao-atual.csv" in the data folder. This csv file contains two column who voted in who (as an example see data from BBB2021 in the data folder)
Then, from the netBB folder, the script can be ran on the terminal with the command:
`python getParedao.py`
the output is an image "paredao_atual.png" in the plot folder.

**getQueridometro.py**
Usage:

Create a file "BBB Stats - DAY.csv" where DAY is a number (1,2,3,...). This csv file contains the adjancy matrix of the emoji votes (who gave which emoji to which participant). For details see data from BBB21 on the data folder.
Then, from the netBB folder, the script can be ran on the terminal with command:
`python getQueridometro DAY` where again DAY is a number for the day you want the queridometro network.
The output is a network with the votes given. The image is saved in the plot folder with name "queridometro_dia_DAY.png".

**NOTES:**
The code and data is free to use and adapt given that the authors are credited.
For code ehcolombo should be credited and for data (BBB21) [quaseobjeto]([https://link-url-here.org](https://linktr.ee/quaseobjeto)https://linktr.ee/quaseobjeto) should be credited (data was collected manually over the whole 2021 edition).

Python packages need are:
numpy,os,igraph,PIL
