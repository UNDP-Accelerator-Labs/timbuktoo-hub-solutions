# About
This project computes a description of the entries in a dataset of grassroots innovations mapped on the African continent. The description consists of a 10-dimensional vector of scores from 0 to 4 and a text comment. The descriptions are then visualized as a radar diagram.

## Data
The data consists of the 6,297 grassroots innovations mapped by the [UNDP Accelerator Labs](https://acceleratorlabs.undp.org) and published in structured form in the [SDG Commons](https://sdg-innovation-commons.org) platform as of February 2025. Mapping is, by default, care of UNDP Accelerator Labs staff. However, the dataset includes about 2,300 solutions mapped by the UNDP Zambia Accelerator Lab through self-reporting via a third-party digital platform, and then imported onto the Commons. 

## Methods

The method we followed consists of a quantitative analysis meant to generate long lists of grassroots innovations classified according to (exogenous) thematic areas. These areas are meant to mirror the mission of [Timbuktoo](https://www.undp.org/africa/projects/timbuktoo), an initiative by the United Nations Development programme meant to incubate African startups. To this end, Timbuktoo has planned to launch eleven hubs, each dedicated to a specific economic sector, from agriculture to logistics, from mining to the creative sector. 

Innovations in those lists were then examined qualitatively to detect patterns. By "pattern" we mean here either that multiple innovators were independently addressing the same need, or that multiple innovators (such as "clean cooking") were independently deploying the same technological strategy (such as "connect a machine to a solar panel for off-grid use").

### Quantitative analysis to get to a thematically coherent long list of solutions

* We first filtered the solutions by location, selecting those that had been mapped in the countries listed in the [United Nations Geoscheme for Africa](https://en.wikipedia.org/wiki/United_Nations_geoscheme_for_Africa). This left us with 2,996 solutions.
* Next, we acquired from Timbuktoo official documents descriptions of the mission of each hub.
* We used these descriptions to craft a prompt that instructed a Large Language Model – previously trained on Accelerator labs data – to go through the solutions and assign a proximity score of the textual description of each solution to each of the eleven descriptions of the different hubs. Each solution was hence associated with a 11-dimensions vector, whose elements are integers from 0 (indicating no mention at all of the sector in question in the solution) to 4 (indicating that the sector in question is a major topic of the solution). The model was instructed to assign the value 4 to at most one single sector.
* We then chose the two economic sectors that were most represented in the solutions (in terms of the mean score across the 2,996 solutions): agri-tech and green/climate/energy. We took the solutions that had scored the highest proximity (=4) to each of these two sectors, and assigned them to specially created boards in the [SDG Commons platform](https://sdg-innovation-commons.org). 709 solutions scored 4 for proximity to agri-tech; 340 for proximity to green/climate/energy.
* 288 solutions scored proximity = 0 to *all* of the sectors.
* The LLM assigned with a U-shaped pattern: the most frequently assigned value is 0, followed by 4, then 3, then 2, then 1. Additionally, almost all elements in the correlation coefficient matrix have a low absolute value, and most are negative. This is compatible with the existence of technological tradeoffs, such as that, for example, an innovation highly relevant to agri-tech is unlikely to have additional uses in mining. There are a few exceptions: the main notable one is the positive correlation between `cities and mobility` and `e-commerce and logistics`.

![image](https://github.com/user-attachments/assets/7319e312-5e96-43b1-a0da-e6bfc67ae3a4)

This work produces an interactive visualization, through which you can explore the solutions. 

### Qualitative analysis to validate and score

* Next, we went through 108 solutions for each of the two sectors in the analysis. We removed false positives, replacing them wih extra solutions from the respective long lists until we reached the number of 108. We encountered about 30 false positives in agri-tech and 6 in green/climate/energy.
* We also tried to detect patterns in the sense mentioned above. For each pattern, we created a board on the SDG Commons.
* In some cases, we encountered clearly defined technological tropes, like biodigesters and dryers. In these cases we searched the SDG Commons for the appropriate search terms in both English and French, and were able to identify some false negatives and add them to long list board. The two long list boards also provided false negatives from one another: solutions that had been assigned to `green/climate/energy`, but could as well have been assigned to `agri-tech` and viceversa. These were 34 for `green/climate/energy` and 104 for `agri-tech`, leading to grand totals of 388 and 783 respectively.
* The correlation coefficient between the proximity scores of solutions to `agri-tech` and those to `green/climate/energy` is about 0.01. This suggests that the high number of false negatives was *not* caused by the restriction we placed on the LLM that it only assign score equal to 4 to one of the sectors – a more fundamental misalignment seems at work. Hence, we recommend taking these results with a higher-than-usual degree of caution.
