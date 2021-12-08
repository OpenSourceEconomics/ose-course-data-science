########
Lectures
########

We provide a set of lectures that are all provided as Jupyter Notebooks.

============
Introduction
============

We briefly introduce the course and discuss some basic ideas about counterfactuals and causal inference. We touch on the two pillars of the counterfactual approach to casusal analysis. We first explore the basic ideas of the potential outcome model and then preview the use of causal graphs.

.. toctree::
   :maxdepth: 1

   introduction/notebook.ipynb

=======================
Potential outcome model
=======================

We discuss the core conceptual model of the course. We initially discuss the individual-level treatment effect but then quickly scale back our ambitions to learn about population-level parameters instead. Then we turn to the stable-unit treatment assumption and address the challenges to the naive estimation of average causal effects in observational studies. We conclude with some examples that illustrate the flexibility of the potential outcome model to more than a simple binary treatment.

.. toctree::
   :maxdepth: 1

   potential-outcome-model/notebook.ipynb

=============
Causal graphs
=============

We explore the usefulness of causal graphs for the visualization of complex causal systems and the clarification of alternative identification strategies for causal effects. After establishing their basic notation and some key concepts, we link them to structural equations and the potential outcome model.

.. toctree::
   :maxdepth: 1

   causal-graphs/notebook.ipynb

==========================
Randomized Experiments
==========================

A lecture on randomized experiments will be part of the next iteration of the OSE data science course, summer semester 2022. Details on this lecture will be realized soon.

.. toctree::
   :maxdepth: 1

   experiments/notebook.ipynb

=======================
Conditioning estimators
=======================

We study the basic conditioning strategy for the estimation of causal effects. We first link the concept of conditioning to direct graphs and start discussing the concept of a back-door path. Then we illustrate in a simulated example how collider variables induce a conditional association between two independent variables. Finally, we discuss the back-door criterion and work through some examples.

.. toctree::
   :maxdepth: 1

   conditioning-estimators/notebook.ipynb

===================
Matching estimators
===================

We review the fundamental concepts of matching such as stratification of data, weighting to achieve balance, and propensity scores. We explore several alternative implementations as we consider matching as conditioning via stratification, matching as a weighing approach, and matching as a data analysis algorithm. Throughout we heavily rely on simulated examples to explore some practical issues such as sparsity of data.

.. toctree::
   :maxdepth: 1

   matching-estimators/notebook.ipynb

=====================
Regression estimators
=====================

We study the most common form of data analysis by looking at simple regression estimators. We first study them as a basic descriptive tool that provides the best linear approximation to the conditional expectation function. Then we turn to the more demanding interpretation that it allows to determine causal effects. We contrast the issues of omitted-variable bias and selection bias. Finally, we conclude with an illustration of Freedman's paradox to showcase some of the challenges in applied empirical work.

.. toctree::
   :maxdepth: 1

   regression-estimators/notebook.ipynb

===========================================
Heterogeneity, selection, and causal graphs
===========================================

We revisit the issues of treatment effect heterogeneity and individuals' selecting their treatment status based on gains unobserved by the econometrician. We lay the groundwork to estimate causal effects using instrumental variables, front-door identification with causal mechanisms, and conditioning estimators using pretreatment variables. We work through an elaborate panel data demonstration that illustrates the shortcoming of conditioning estimators in the presence of self-selection.

.. toctree::
   :maxdepth: 1

   selection-heterogeneity-graphs/notebook.ipynb

======================
Instrumental variables
======================

We review basic instrumental variables estimation using a simulated example inspired by random assignment of school vouchers. We look at the Wald and 2SLS estimator and discuss its interpretation as a Local Average Treatment Effect in the presence of treatment effect heterogeneity. We conclude with a discussion of seminal papers in the literature and also elevate a more critical assessment to discussion.

.. toctree::
   :maxdepth: 1

   instrumental-variable/notebook.ipynb

=====================
Repeated observations
=====================

We now explore models in which we have multiple observations at different points in time. We start with the interrupted time series model and then explore difference-in-difference estimation using `Card & Krueger (1994) <https://www.jstor.org/stable/2118030>`_.  We then return to the earlier example of school choice to benchmark the performance of alternative estimators as we vary the economics of individual decision-making.

.. toctree::
   :maxdepth: 1

   repeated-observations/notebook.ipynb

===============================
Regression discontinuity design
===============================

We study regression discontinuity design in more detail. We discuss identification, issues in interpretation, and challenges to its application based on the seminal review by `Lee & Lemieux (2010) <https://www.aeaweb.org/articles?id=10.1257/jel.48.2.281>`_. We look at different conditional mean functions and the issue of bandwidth choice. We reproduce and check the robustness of some of the results in `Lee (2008) <https://reader.elsevier.com/reader/sd/pii/S0304407607001121?token=B2B8292E08E07683C3CAFB853380CD4C1E5D1FD17982228079F6EE672298456ED7D6692F0598AA50D54463AC0A849065>`_.

.. toctree::
   :maxdepth: 1

   regression-discontinuity/notebook.ipynb

=============================
Difference in difference
=============================

A lecture on difference-in-difference method will be part of the next iteration of the OSE data science course, summer semester 2022. Details on this lecture will be realized soon.

.. toctree::
   :maxdepth: 1

   difference-in-difference/notebook.ipynb


=============================
Synthetic Control
=============================

A lecture on synthetic control method will be part of the next iteration of the OSE data science course, summer semester 2022. Details on this lecture will be realized soon.

.. toctree::
   :maxdepth: 1

   synthethic-control/notebook.ipynb
