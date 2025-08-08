# Introductory Concepts in Atmospheric Modeling

Welcome to the Fundamentals of Atmospheric Modeling Cookbook! This cookbook is designed to act as a first foray into simulating atmospheric phenomena, focusing on two simple 2D approaches, and will briefly familiarize you with fundamental principles and terminology used in atmospheric sciences and modeling, including basic meteorological and mathematical concepts and numerical methods. The work done here takes advantage of the Python package Numba {cite:p}`lam2015numba` and its ability to accelerate a subset of Python code pertaining to numerical computation, like mathematical operations and loops. The foundations of this book are based on {cite:t}`Klemp1978-dq`, a cloud model that uses a prognostic equation for pressure, which lets us streamline its numerical implementation, thus making it a great jumping-off point to begin your journey through this process.

## What is Numerical Modeling, and how is it used in Atmospheric Science?

In general, numerical modeling involves solving a set of mathematical equations that describe physical processes using computational algorithms. In atmospheric science, the equations of interest are those that govern the behavior of the atmosphere, such as the Navier-Stokes equations for fluid flow, the thermodynamic energy equation, and the continuity equation for mass conservation, among others. These equations are integrated forward in time to make predictions about the future state of the atmosphere based on current conditions. These equations are very complex (as will be seen later) and difficult to solve, and small variations in the initial conditions (the state of the atmosphere at time 0) and the boundary conditions (the state of the atmosphere on the edges of the domain of interest) can yield wildly different results. Modeling with the use of numerical solving methods is necessary to make these predictions, as it allows us to simplify those complicated physical processes via discretization and utilize numerical integration to simulate a plausible future state of the atmosphere.

## What Meteorological Information Will My Model Use?

Atmospheric models range from huge simulations of the entire Earth as a coupled system, considering the atmosphere, ocean, land, and ice and how they interact with one another, to those that focus on the microscale processes that can't be seen and are challenging to understand (think: cloud microphysics, radiation, turbulent processes), and everything in between! Because the applicable variables will change depending on the model's purpose, there's no catch-all list of what information you'll be giving the model to work with. That said, there are many that are essential to the function of all parts of the atmosphere that you should anticipate working with:

- Temperature ($T$): the thermal energy (i.e. hotness or coldness) of the air, measured in Kelvins (K)
- Pressure ($p$): the total force exerted by a parcel of air, measured in Pascals (Pa)
- Density ($\rho$): the total mass per unit volume of air, measured in kg m<sup>-3</sup>
- Wind speed: the rate of movement of an air parcel in the zonal ($u$), meridional ($v$), and vertical ($w$) directions, measured in m s<sup>-1</sup>

There are also many constants that you will likely encounter in an atmospheric model, like the gas constant and specific heat. Many more variables exist that are essential to many existing models used for the weather predictions you receive each day, but for this cookbook, we'll be focusing mostly on those listed above.

## What are the Steps of Building a Numerical Model?

Before any model building begins, make sure you have a clear idea of what you want your model to be. As previously mentioned, different models serve very different purposes, so choosing the scope of your model---what process(es) it will simulate, what information it must be given, and what output you're looking to receive---beforehand will save you some headache. Once you've got your plans laid out, you're ready to start constructing your atmospheric model!

General Numerical Modeling Steps:

- Formulate the Equations: Start with the fundamental equations that describe atmospheric dynamics. These include the momentum, thermodynamic, and continuity equations. These equations can be expressed in many different ways, such as in different coordinate systems or with different approximations, so take care to be consistent when building the equations you'll use in your model.

- Simplify the Equations: The full set of atmospheric equations are very complex. Simplifications, such as assuming a dry atmosphere or neglecting certain forces, make the problem more manageable. Make the desired adjustments to your equation set before implementing into your model.

- Discretize the Equations: Convert the continuous equations into discrete forms that can be solved numerically. This most commonly involves dividing the atmosphere into a grid and approximating derivatives with finite differences or other numerical differentiation methods.

- Determine your Initial and Boundary Conditions: as mentioned earlier, even small changes to the initial and boundary conditions give lead your model to generate very different results. These conditions should be chosen with care, ensuring they are physically plausible and are in line with what you're looking to test using your model.

- Solve the Equations: Use numerical solving methods, such as finite differencing and leapfrog time integration, to solve the discretized equations and integrate forward in time. This requires implementing algorithms to progress the equations forward in time and space.

- Analyze the Results: Interpret the output from the numerical model to understand atmospheric behavior. Depending on the purpose of your model, you may also choose to validate your results using observations and implement bias correction methods, or make further tweaks as needed.

Following these steps will allow you to simulate the atmosphere in a physically constrained way and yield results that can further your knowledge (and the knowledge of others) of atmospheric processes.

## What Else Should I Expect From This Cookbook?

In the following chapters, we'll go into many of the above steps in greater detail using two different simple atmospheric models. We'll also discuss troubleshooting and refining your model when issues arise. By the end of this cookbook, you will be all set to build your atmospheric model that takes advantage of the computational benefits of Numba!
