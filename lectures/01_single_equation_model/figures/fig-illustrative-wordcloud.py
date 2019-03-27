import matplotlib.pyplot as plt

# default text color = orange
plt.rcParams["text.color"] = "#ff7f0e"
# default horizontal alignment of text = center
ha_def = "center"

# default vertical alignment of text = center
va_def = "center"


plt.text(0.20, 1.00, "Life-Cycle Models", ha=ha_def, va=va_def)
plt.text(0.50, 1.00, "Educational Chioce", ha=ha_def, va=va_def)
plt.text(0.80, 1.00, "Investment", ha=ha_def, va=va_def)

plt.text(0.10, 0.90, "Structural Microeconometrics", ha=ha_def, va=va_def)
plt.text(0.50, 0.90, "Psychic Costs", ha=ha_def, va=va_def)
plt.text(0.80, 0.90, "Option Values", ha=ha_def, va=va_def)

plt.text(0.20, 0.80, "Educational Choice", ha=ha_def, va=va_def)
plt.text(0.60, 0.80, "True Returns", ha=ha_def, va=va_def)

plt.text(0.10, 0.70, "Uncertainty", ha=ha_def, va=va_def)
plt.text(0.60, 0.70, "Administrative Datasets", ha=ha_def, va=va_def)


plt.text(0.5, 0.55, "Human Capital Analysis", fontsize=25, color="#1f77b4", ha=ha_def, va=va_def)
plt.text(0.5, 0.45, "Economics, Data, Computation", fontsize=15, color="#1f77b4", ha=ha_def, va=va_def)


plt.text(0.60, 0.30, "Robust Optimization", ha=ha_def, va=va_def)
plt.text(0.80, 0.20, "Markov Decision Process", ha=ha_def, va=va_def)
plt.text(0.40, 0.20, "Numerical Methods", ha=ha_def, va=va_def)
plt.text(0.60, 0.10, "Operations Research", ha=ha_def, va=va_def)

plt.text(0.20, 0.30, "Decision Theory", ha=ha_def, va=va_def)
plt.text(0.10, 0.20, "Robustness", ha=ha_def, va=va_def)
plt.text(0.25, 0.10, "Uncertainty", ha=ha_def, va=va_def)

plt.text(0.15, 0.00, "respy", ha=ha_def, va=va_def)
plt.text(0.45, 0.00, "Software Engineering", ha=ha_def, va=va_def)
plt.text(0.75, 0.00, "grmpy", ha=ha_def, va=va_def)

plt.setp(plt.gca(), frame_on=False, xticks=(), yticks=())

plt.savefig('fig-illustrative-wordcloud.png')
