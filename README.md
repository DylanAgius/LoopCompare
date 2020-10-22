# Functionality

* A function to compare simulated and experimental hysteresis loops to provide a metric of accuracy.
* The currently functionality assumes the experimental data was gathered in strain-control since it fits polynomials to the stress data.  This will be extended in a future iteration to include stress-controlled data. 
* A different number of data points for the simulation and experimental can be used since it will fit a polynomial to both sets of data and use common x-values to extract the corresponding y-values to compare accuracy.

# How it works
Hystersis loop data is read through an excel file named *hysteresis* found in the *data* folder.  In this file, there are two sheets:
* one named *Exp* which will contain the experimental hystersis loop data with strain first, and then stress;
* the other name *Sim* which will contain the simulated hysteresis loop data with strain first, and then stress.
You can supply has many loops as you look to compare between but they must be as separate columns.  Therefore, you can follow the following order:
<img src="/figures/minimum_pipeline.png" width="200" height="200">
