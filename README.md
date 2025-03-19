# Solar Elemental Abundances
This is a digitalisation of Table 1 from [Asplund et al. (2009)](https://www.annualreviews.org/content/journals/10.1146/annurev.astro.46.060407.145222), covering the photospheric elemental abundances of the Sun. In general, the abundances of each element ($\alpha_\mathrm{X}$) are given as

$$
\alpha_\mathrm{X} = \log_{10}\left(\frac{N_\mathrm{X}}{N_\mathrm{H}}\right) + 12,
$$
where $N$ represents a number density. To derive the usual values associated with these elements (i.e. C/O or similar ratios), the abundances are converted via
$$
\tilde{X} = \frac{\mathrm{X}}{\mathrm{H}} = 10^{\alpha_\mathrm{X} - 12},
$$
where uncertainties are propagated via Gaussian error propagation, or
$$
\delta \tilde{X} = \sqrt{(\ln(10) \cdot \tilde{X})^2 \cdot (\delta \alpha_\mathrm{X})^2}.
$$
Lastly, element ratios are calculated through
$$
R = \frac{\mathrm{X}}{\mathrm{Y}} = \frac{\tilde{X}}{\tilde{Y}},
$$
with error propagation performed in the same way,
$$
\delta R = \sqrt{\left(\frac{1}{\tilde{Y}}\right)^2 \cdot (\delta \tilde{X})^2 + \left(-\frac{\tilde{X}}{\tilde{Y}^2}\right)^2 \cdot (\delta \tilde{Y})^2}
$$

**Note:** There is a newer version of this paper, [Asplund et al. (2021)](https://www.aanda.org/articles/aa/full_html/2021/09/aa40445-21/aa40445-21.html#S16), so I will try and update this repository.
