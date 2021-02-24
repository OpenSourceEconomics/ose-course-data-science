<a href="https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics-course-project-Pascalheid/blob/master/Angrist_1990.ipynb"
   target="_parent">
   <img src="https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.png"
      width="109" height="20">
</a>
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics-course-project-Pascalheid/master?filepath=%2FAngrist_1990.ipynb)
</a>
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/HumanCapitalAnalysis/template-course-project/blob/master/LICENSE)
</a>
[![Build Status](https://travis-ci.org/HumanCapitalAnalysis/microeconometrics-course-project-Pascalheid.svg?branch=master)](https://travis-ci.org/HumanCapitalAnalysis/microeconometrics-course-project-Pascalheid)

## Replication Project on Lifetime Earnings and the Vietnam Era Draft Lottery: Evidence from Social Security Administrative Records by Joshua Angrist (1990)

The notebook [Angrist_1990.ipynb](https://github.com/HumanCapitalAnalysis/microeconometrics-course-project-Pascalheid/blob/master/Angrist_1990.ipynb) contains a project by [Pascal Heid](https://github.com/Pascalheid) for the 2020 iteration of the [Mircoeconometrics](https://microeconometrics.readthedocs.io/) Master class at the university of Bonn. It replicates the results of the following paper:

> Angrist, Joshua. (1990). [Lifetime Earnings and the Vietnam Era Draft Lottery: Evidence from Social Security Administrative Records](https://www.jstor.org/stable/2006669?seq=1#metadata_info_tab_contents). *American Economic Review*. 80. 313-36.

In his landmark paper, Angrist (1990) discusses steps to overcome bias prevalent in the previous literature when estimating the effect of veteran status on subsequent earnings. He does so by suggesting the use of the Vietnam war draft lottery as an instrument for veteran status. Hereby he exploits the generally random nature of the draft lottery to obtain estimates of the treatment effect of being a veteran on lifetime earnings. He finds that the earnings of white veterans are around fifteen percent lower than those of comparable nonveterans. Less importantly, Angrist (1990) attributes that to the loss of working experience due to military service by estimating a simple structural model. 

### Structure of the Repository

In the [data repository](https://github.com/HumanCapitalAnalysis/microeconometrics-course-project-Pascalheid/tree/master/data) the replication data which has been used to create the [replication notebook](https://github.com/HumanCapitalAnalysis/microeconometrics-course-project-Pascalheid/blob/master/Angrist_1990.ipynb) can be found. The folder [auxiliary](https://github.com/HumanCapitalAnalysis/microeconometrics-course-project-Pascalheid/tree/master/auxiliary) contains several modules with the core functions creating the figures and tables in Angrist (1990) as well as some extra visualizations and extensions. Lastly, the causal graphs are stored in the [material repo](https://github.com/HumanCapitalAnalysis/microeconometrics-course-project-Pascalheid/tree/master/material).
