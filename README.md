# circacompare
This is a Python package that allows for the statistical analyses and comparison of two circadian rhythms.
The Python implementation which you're looking at is an replication of this [R-package](https://github.com/RWParsons/circacompare). However, it comes with the added functionality of having control over the loss function used (opposed to least squares, which is used in the R-package).

This work is published [here](https://academic.oup.com/bioinformatics/article-abstract/doi/10.1093/bioinformatics/btz730/5582266) and can be cited as: 

Rex Parsons, Richard Parsons, Nicholas Garner, Henrik Oster, Oliver Rawashdeh, CircaCompare: A method to estimate and statistically support differences in mesor, amplitude, and phase, between circadian rhythms, Bioinformatics, https://doi.org/10.1093/bioinformatics/btz730

# Usage
##  `circa_single` and `circa_single_plot`
`circa_single` is used when there is only a single group of data being analysed. The result returned includes the point-estimates and 95% confidence intervals for parameters representing:
1. Mesor
2. Amplitude
3. Phase

`circa_single_plot` is used in the same way as `circa_single` but rather than returning results, it returns a plot of the data and the curve of best fit (the sinusoidal function constructed from point estimates from `circa_single`). As this is a simple wrapper of `circa_single` it requires the same arguments.

### Example

	import numpy as np
	from compare import circa_single
	from plot import circa_single_plot
	from generator import generate_data
	
	
	time = np.linspace(0, 2 * np.pi, 100)   # time is given in radian hours 
	measure = generate_data(t=time, k=1, a=10, p=4, noise=0.5)
	
	result = circa_single(t0=time, y0=measure)
	print(result.x)                         # result.x contains the estimates for the mesor, amplitude, and phase of the rhythm
	print(result.confidence_intervals)      # result.confidence_intervals contains the confidence intervals for the above estimates
	
	circa_single_plot(t0=time, y0=measure)

## `circacompare` and `circacompare_plot`
`circacompare` is used when there are two groups of rhythmic data to be compared to each other, group 0 and group 1.  The result returned includes the point-estimates and 95% confidence intervals for:
1. Mesor of group 0
2. Change in Mesor from group 0 to group 1
3. Amplitude of group 0
4. Change in Amplitude from group 0 to group 1
5. Phase of group 0
6. Change in Phase from group 0 to group 1

`circacompare_plot` is used in the same way as `circacompare` but rather than returning results, it returns a plot of the data and the curve of best fit (the sinusoidal function constructed from point estimates from `circacompare`). As this is a simple wrapper of `circacompare` it requires the same arguments.

### Example

    time = np.linspace(0, 2 * np.pi, 100)
    measure = np.concatenate(
        (generate_data(t=time, k=1, a=10, p=4, noise=0.4), generate_data(t=time, k=5, a=3, p=1, noise=0.2)))
    group = np.concatenate((np.zeros(len(time)), np.ones(len(time))))
    time = np.concatenate((time, time))

    result = circacompare(t0=time, y0=measure, g0=group)
    print(result.x)                     # has estimates for all parameters
    print(result.confidence_intervals)  # has confidence intervals for all parameters

    circacompare_plot(t0=time, y0=measure, g0=group)

# Additional Information
[R-package and Shiny App](https://github.com/RWParsons/circacompare).

If you're having troubles or have suggestions for improvement, please create an issue or email me (rex.parsons94@gmail.com).

Please cite the [original paper](https://academic.oup.com/bioinformatics/article-abstract/doi/10.1093/bioinformatics/btz730/5582266) when used.

 