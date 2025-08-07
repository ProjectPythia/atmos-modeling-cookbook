# Introductory Concepts in Atmospheric Modeling

Welcome to the Fundamentals of Atmospheric Modeling Cookbook! This cookbook is designed to act as a first foray into simulating atmospheric phenomena, focusing on two simple 2D approaches, and will briefly familiarize you with fundamental principles and terminology used in atmospheric sciences and modeling, including basic meteorological and mathematical concepts and numerical methods. The work done here takes advantage of the Python package Numba {cite:p}`lam2015numba` and its ability to accelerate a subset of Python code pertaining to numerical computation, like mathematical operations and loops. The foundations of this book are based on {cite:t}`Klemp1978-dq`, which laid the groundwork for modern atmospheric modeling and is a great jumping-off point to begin your journey through this process.

## What is Numerical Modeling, and how is it used in Atmospheric Science?

In general, numerical modeling involves solving a set mathematical equations that describe physical processes using computational algorithms. In atmospheric science, the equations of interest are those that govern the behavior of the atmosphere, such as the Navier-Stokes equations for fluid flow, the thermodynamic energy equation, and the continuity equation for mass conservation, among others. These equations are integrated forward in time to make predictions about the future state of the atmosphere based on current conditions. These equations are very complex (as will be seen later) and difficult to solve, and small variations in the initial conditions (the state of the atmosphere at time 0) and the boundary conditions (the state of the atmosphere on the edges of the domain of interest) can yield wildly different results. Modeling with the use of numerical solving methods is necessary to make these predictions as it allows us to simplify those complicated physical processes via discretization and utilize numerical integration to simulate a plausible future state of the atmosphere.

Now that you know what an atmospheric model is and how it uses numerical integration to make its projections, we're ready to discuss the process of building your own!

## Key Steps in Numerical Modeling:



- Formulate the Equations: Start with the fundamental equations that describe atmospheric dynamics. These include the Navier-Stokes equations, thermodynamic equations, and continuity equations.

- Simplify the Equations: The full set of atmospheric equations can be very complex. Simplifications, such as assuming a dry atmosphere or neglecting certain forces, make the problem more manageable.

- Discretize the Equations: Convert the continuous equations into discrete forms that can be solved numerically. This involves dividing the atmosphere into a grid and approximating derivatives with finite differences.

- Solve the Equations: Use numerical methods to solve the discretized equations. This requires implementing algorithms to integrate the equations forward in time and space.

- Analyze the Results: Interpret the output from the numerical model to understand atmospheric behavior and validate the model against observations.


## Meteorological Concepts (needs adjusting)

In order to effectively model the atmosphere, it's important to determine and define the variables of interest.


- Temperature: A measure of the warmth or coldness of the atmosphere, in Kelvins (K).
- Pressure: The force exerted by the weight of the air above a certain point. Measured in units such as Pascals (Pa) or millibars (mb).
- Wind: The movement of air relative to the Earth's surface. Described by speed and direction (two-dimensional in our case).

...