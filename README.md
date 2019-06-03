# Microeconometrics

... introductory course to microeconmetrics. The course is designed as to supplement and emphasize selected topics from the two textbooks below. As such, it is important that students read the relevant chapters in advance to get most out of the class.

Throughout the course we will make heavy use of [Python](https://www.python.org) and its [SciPy ecosystem](https://www.scipy.org) and [Jupyter Notebooks](https://jupyter.org) throughout the course and so we provide some useful resources below. For further information, please do not hesitate to [contact us](https://join.slack.com/t/humancapitalanalysis/shared_invite/enQtNDQ0ODkyODYyODA2LWEyZjdlNWYwYmUyNzlkOWFkNWJkMGI5M2M4ZWUyMThhNWNiMmJhY2ZjY2E4YzE3NGQ5MzcxZTRhN2QxYjgxYWY).

## Counterfactual approach to causal analysis

* Winship, C., and Morgan, S. L. (2014). [*Counterfactuals and causal inference: Methods and principles for social research (Analytical methods for social research)*](https://www.cambridge.org/de/academic/subjects/sociology/sociology-general-interest/counterfactuals-and-causal-inference-methods-and-principles-social-research-2nd-edition?format=PB). Cambridge, England: Cambridge University Press.

* Frölich, M., and Sperlich, S. (2019). [*Impact evaluation: Treatment effects and causal analysis*](https://www.cambridge.org/core/books/impact-evaluation/F07A859F06FF131D78DA7FC81939A6DC). Cambridge, England: Cambridge University Press.

### Potential outcome model

*  Heckman, J. J., and Vytlacil, E. J. (2007a). [Econometric evaluation of social programs, part I: Causal effects, structural models and econometric policy evaluation.](https://www.sciencedirect.com/science/article/pii/S1573441207060709) In J. J. Heckman, and E. E. Leamer (Eds.), *Handbook of Econometrics* (Vol. 6B, pp. 4779–4874). Amsterdam, Netherlands: Elsevier Science.

*  Imbens G. W., and Rubin D. B. (2015). [Causal inference for statistics, social, and biomedical sciences: An introduction.](https://www.cambridge.org/core/books/causal-inference-for-statistics-social-and-biomedical-sciences/71126BE90C58F1A431FE9B2DD07938AB). Cambridge, England: Cambridge University Press.

### Directed graphs

* Pearl, J. (2014). [*Causality*](https://www.cambridge.org/core/books/causality/B0046844FAE10CBF274D4ACBDAEB5F5B). Cambridge, England: Cambridge University Press.

* Peters, J., Janzig, D., and Schölkopf, B. (2018) [Elements of causal inference: Foundations and learning algorithms](https://mitpress.mit.edu/books/elements-causal-inference). Cambridge, MA: The MIT Press.

Please use the table of content to navigate the rest of the material.

1. [Lectures](#lectures)
2. [Special Focus](#focus)
3. [Resources](#resources)
4. [Iterations](#iterations)

We collect a list of additional, more general, reading recommendations [here](https://github.com/HumanCapitalAnalysis/general-resources).

## Lectures <a name="lectures"></a>

We provide the lectures in the form of a Jupyter notebook.

#### [Introduction](https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics/blob/master/lectures/01_introduction/lecture.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics/master?filepath=lectures%2F01_introduction%2Flecture.ipynb)

We briefly introduce the course and discuss some basic ideas about counterfactuals and causal inference.

#### [Tools for data science](https://nbviewer.jupyter.org/github/OpenSourceEconomics/tutorials/blob/master/tools_for_data_science/tutorial.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/OpenSourceEconomics/tutorials/master?filepath=tools_for_data_science%2Ftutorial.ipynb)

This guest lecture by the team of [OpenSourceEconomics](https://github.com/OpenSourceEconomics) presents a basic overview on the scientific Python ecosystem as we will heavily rely on it throughout the course.

#### [Potential outcome model](https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics/blob/master/lectures/02_potential_outcome_model/lecture.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics/master?filepath=lectures%2F02_potential_outcome_model%2Flecture.ipynb)

We discuss the core model of the course.

#### [Causal graphs](https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics/blob/master/lectures/03_causal_graphs/lecture.ipynb)  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics/master?filepath=lectures%2F03_causal_graphs%2Flecture.ipynb)

We explore the usefulness of causal graphs for the visualization of complex causal systems and the clarification of alternative identification strategies for causal effects. After establishing their basic notation and some key concepts, we link them to structural equations and the potential outcome model.

#### [Models of causal exposure and identification criteria for conditioning estimators](https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics/blob/master/lectures/04_criteria_conditioning_estimators/lecture.ipynb)  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics/master?filepath=lectures%2F04_criteria_conditioning_estimators%2Flecture.ipynb)

We study the basic conditioning strategy for the estimation of causal effects.

#### [Matching estimators of causal effects](https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics/blob/master/lectures/05_matching_estimators/lecture.ipynb)  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics/master?filepath=lectures%2F05_matching_estimators%2Flecture.ipynb)

We review the fundamental concepts of matching such as stratification of data, weighting to achieve balance, and propensity scores.

#### [Regression estimators of causal effects](https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics/blob/master/lectures/06_regression_estimators/lecture.ipynb)  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics/master?filepath=lectures%2F06_regression_estimators%2Flecture.ipynb)

We study the most common form of data analysis.

#### [Self-selection, heterogeneity, and causal graphs](https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics/blob/master/lectures/07_selection_heterogeneity_graphs/lecture.ipynb)  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics/master?filepath=lectures%2F07_selection_heterogeneity_graphs%2Flecture.ipynb)

We lay the groundwork to estimate causal effects if simple conditioning on observed variables that lie along all back-door paths will not suffice.

#### [Instrumental variable estimators of causal effects](https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics/blob/master/lectures/08_instrumental_variable/lecture.ipynb)  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics/master?filepath=lectures%2F08_instrumental_variable%2Flecture.ipynb)

We study the use of instrumental variable estimators.

#### [Mechanisms and causal explanation](https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics/blob/master/lectures/09_mechanisms_causal_explanation/lecture.ipynb)  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics/master?filepath=lectures%2F09_mechanisms_causal_explanation%2Flecture.ipynb)

We study front-door identification that allow (under certain conditions) to provide a causal account of the effect of D on Y.

#### [Repeated observations and the estimation of causal effects](https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics/blob/master/lectures/10_repeated_observations/lecture.ipynb)  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics/master?filepath=lectures%2F10_repeated_observations%2Flecture.ipynb)

We now explore models in which we have multiple observations at different points in time. Due to its similar structure, we also look at the sharp and fuzzy regression discontinuity design.

## Special focus <a name="focus"></a>

We discuss selected topics in more details based on student demands.

#### [Regression discontinuity design](https://github.com/HumanCapitalAnalysis/microeconometrics/blob/master/lectures/11_regression_discontinuity/slides.pdf)

We study regression discontinuity design in more detail. We discuss identification, issues in interpretation, and challenges to application based on the seminal review by [Lee & Lemieux (2010)](https://www.aeaweb.org/articles?id=10.1257/jel.48.2.281).

## Resources <a name="resources"></a>

We provide some additional resources that are useful for our course work.

#### Textbooks

* Angrist, J. D., and Pischke, J. (2009). [*Mostly harmless econometrics: An empiricists companion*](https://press.princeton.edu/titles/8769.html). Princeton, NJ: Princeton University Press.

* Wooldridge, J. M. (2009). [*Econometric analysis of cross section and panel data*](https://mitpress.mit.edu/books/econometric-analysis-cross-section-and-panel-data). Cambridge, MA: The MIT Press.

#### Datasets

The two textbooks above provide an impressive amount of data from research articles. We provide them in a central place [here](https://github.com/HumanCapitalAnalysis/microeconometrics/tree/master/datasets).

#### Tools

* Rossant, C. (2018). [*IPython interactive computing and visualization cookbook*](https://www.packtpub.com/big-data-and-business-intelligence/ipython-interactive-computing-and-visualization-cookbook-second-e). Birmingham, England: Packt Publishing.

* VanderPlas, J. (2016). [*Python data science handbook*](https://www.oreilly.com/library/view/python-data-science/9781491912126/). Sebastopol, CA: O'Reilly Media, Inc.

* Varoquaux, G., Haenel, V., Gouillart, E., Jędrzejewski-Szmek, Z., Gommers, R., Pedregosa, F., … yasutomo57jp. (2015). Scipy lecture notes. Retrieved from https://scipy-lectures.org/

#### Software packages

* grmpy (2018). *grmpy: A Python package for the simulation and estimation of the generalized Roy model.* Retrieved from http://doi.org/10.5281/zenodo.1162640

* respy (2018). *respy: A Python package for the simulation and estimation of a prototypical finite-horizon dynamic discrete choice model.* Retrieved from http://doi.org/10.5281/zenodo.1189209

## Iterations <a name="iterations"></a>

* **Summer Quarter 2019**, Graduate Program at the University of Bonn, please see [here](https://github.com/HumanCapitalAnalysis/microeconometrics/tree/master/iterations/bonn_ss_19/README.md) for details.

[![Build Status](https://travis-ci.org/HumanCapitalAnalysis/microeconometrics.svg?branch=master)](https://travis-ci.org/HumanCapitalAnalysis/microeconmetrics) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/HumanCapitalAnalysis/microeconometrics/blob/master/LICENSE)
