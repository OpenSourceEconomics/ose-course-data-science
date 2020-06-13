.. Microeconometrics documentation master file, created by
   sphinx-quickstart on Mon Jun  8 20:12:30 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Microeconometrics
==================

.. image:: https://travis-ci.org/HumanCapitalAnalysis/microeconometrics.svg?branch=master
    :target: https://travis-ci.org/HumanCapitalAnalysis/microeconometrics

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://github.com/HumanCapitalAnalysis/microeconometrics/blob/master/LICENSE

.. image:: https://img.shields.io/badge/zulip-join_chat-brightgreen.svg
    :target: https://bonn-econ-teaching.zulipchat.com


This course introduces students to basic microeconmetric methods. The objective is to learn how to make and evaluate causal claims. By the end of the course, students should be able to apply each of the methods discussed and critically evaluate research based on them. Throughout the course we will make heavy use of `Python <https://www.python.org>`_ and its `SciPy ecosystem <https://www.scipy.org>`_ as well as `Jupyter Notebooks <https://jupyter.org>`_.

Counterfactual approach to causal analysis
*******************************************

* Winship, C., and Morgan, S. L. (2014). `Counterfactuals and causal inference: Methods and principles for social research <https://www.cambridge.org/de/academic/subjects/sociology/sociology-general-interest/counterfactuals-and-causal-inference-methods-and-principles-social-research-2nd-edition?format=PB>`_. Cambridge, England: Cambridge University Press.

* Frölich, M., and Sperlich, S. (2019). `Impact evaluation: Treatment effects and causal analysis <https://www.cambridge.org/core/books/impact-evaluation/F07A859F06FF131D78DA7FC81939A6DC>`_. Cambridge, England: Cambridge University Press.

* Angrist, J. D., and Pischke, J. (2009). `Mostly harmless econometrics: An empiricists companion <https://press.princeton.edu/titles/8769.html>`_. Princeton, NJ: Princeton University Press.

Potential outcome model
------------------------

*  Heckman, J. J., and Vytlacil, E. J. (2007a). `Econometric evaluation of social programs, part I: Causal effects, structural models and econometric policy evaluation <https://www.sciencedirect.com/science/article/pii/S1573441207060709>`_. In J. J. Heckman, and E. E. Leamer (Eds.), *Handbook of Econometrics* (Vol. 6B, pp. 4779–4874). Amsterdam, Netherlands: Elsevier Science.

*  Imbens G. W., and Rubin D. B. (2015). `Causal inference for statistics, social, and biomedical sciences: An introduction <https://www.cambridge.org/core/books/causal-inference-for-statistics-social-and-biomedical-sciences/71126BE90C58F1A431FE9B2DD07938AB>`_. Cambridge, England: Cambridge University Press.

* Rosenbaum, P. R. (2017). `Observation and experiment: An introduction to causal inference <https://www.hup.harvard.edu/catalog.php?isbn=9780674975576>`_. Cambridge, MA: Harvard University Press.

Directed graphs
----------------

* Pearl, J. (2014). `Causality <https://www.cambridge.org/core/books/causality/B0046844FAE10CBF274D4ACBDAEB5F5B>`_. Cambridge, England: Cambridge University Press.

* Pearl, J., and Mackenzie, D. (2018). `The book of why: The new science of cause and effect <https://www.basicbooks.com/titles/judea-pearl/the-book-of-why/9780465097609/>`_. New York, NY: Basic Books.

* Pearl J., Glymour M., and Jewell N. P. (2016). `Causal inference in statistics: A primer <https://www.wiley.com/en-us/Causal+Inference+in+Statistics%3A+A+Primer-p-9781119186847>`_. Chichester, UK: Wiley.

.. toctree::
   :maxdepth: 1

   lectures/01-introduction/lecture.ipynb
   lectures/01-introduction/tools_data_science.ipynb
   lectures/02-potential-outcome-model/lecture.ipynb
   lectures/03-causal-graphs/lecture.ipynb
   lectures/04-criteria-conditioning-estimators/lecture.ipynb
   lectures/04-criteria-conditioning-estimators/back-door-identification.ipynb
   lectures/05-matching-estimators/lecture.ipynb
   lectures/06-regression-estimators/lecture.ipynb
   lectures/07-selection-heterogeneity-graphs/lecture.ipynb
   lectures/08-instrumental-variable/lecture.ipynb
   lectures/09-mechanisms-causal-explanation/lecture.ipynb
   lectures/09-mechanisms-causal-explanation/front-door-identification.ipynb
   lectures/10-repeated-observations/lecture.ipynb
   lectures/11-regression-discontinuity/notebook.ipynb
   lectures/12-nonstandard-standard/notebook.ipynb
   lectures/13-generalized-moments/notebook.ipynb
   problem-sets/01-potential-outcome-model/problem-set-01-potential-outcome-model.ipynb
   problem-sets/02-matching-estimators/problem-set-02-matching-estimators.ipynb
   

We collect a list of additional, more general, reading recommendations `here <https://github.com/HumanCapitalAnalysis/general-resources>`__.


Handouts
********

We curate a list of handouts that summarize selected issues.

* `Causal graphs: Definitions, patterns, and strategies <https://github.com/HumanCapitalAnalysis/microeconometrics/blob/master/handouts/01-causal-graphs/handout-1-casual-graphs.pdf>`_

Resources
**********

We provide some additional resources that are useful for our course work in general.

**Textbooks**

* Wooldridge, J. M. (2009). `Econometric analysis of cross section and panel data <https://mitpress.mit.edu/books/econometric-analysis-cross-section-and-panel-data>`_. Cambridge, MA: The MIT Press.

* Angrist, J. D., and Pischke, J. (2014). `Mastering 'metrics <http://masteringmetrics.com>`_. Princeton, NJ: Princeton University Press.

* Stock, J. H., and Watson, M. W. (2019). `Introduction to econometrics <https://www.pearson.com/us/higher-education/program/Stock-Introduction-to-Econometrics-Plus-My-Lab-Economics-with-Pearson-e-Text-Access-Card-Package-4th-Edition/PGM2416966.html>`_. New York, NY: Pearson.

**Datasets**

The textbooks above provide an impressive amount of data from research articles. We provide them in a central place `here <https://github.com/HumanCapitalAnalysis/microeconometrics/tree/master/datasets>`__.

**Tools**

We maintain a list of useful resources around the tooling used in the course `here <https://github.com/HumanCapitalAnalysis/general-resources#scientific-software-development>`__.

Iterations
***********

* **Summer Quarter 2020**, Graduate Program at the University of Bonn, please see `here <https://github.com/HumanCapitalAnalysis/microeconometrics/tree/master/iterations/bonn-ss-20>`__ for details.

* **Summer Quarter 2019**, Graduate Program at the University of Bonn, please see `here <https://github.com/HumanCapitalAnalysis/microeconometrics/tree/master/iterations/bonn-ss-19>`__ for details.
