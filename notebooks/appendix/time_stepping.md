# Time Stepping

In numerical weather prediction and climate modeling, time stepping refers to the process of advancing the simulation in time. This is typically done by discretizing the time domain into small intervals, or "time steps," and updating the state of the system at each time step based on the governing equations.

There are several methods for time stepping, each with its own advantages and disadvantages. This section is a reference of the most commonly used algorithms.


Given an equation for the tendency of a random variable

$$
\frac{\partial u}{\partial t} = Q(t,u)
$$

## Euler methods

These methods are used to approximate the solution to a differential equation by starting at an initial point and taking a series of small, discrete steps forward in time.


| Method | Scheme | Order |
| :---: | :--- | :---: |
| **Explicit** | $$\tilde{u}^{\tau+1} = \tilde{u}^\tau + \Delta t Q^\tau$$|$\Delta t$ |
| **Implicit** | $$\tilde{u}^{\tau+1} = \tilde{u}^\tau + \Delta t Q^{\tau+1}$$|$\Delta t$ |
| **Trapezoidal** | $$\tilde{u}^{\tau+1} = \tilde{u}^\tau + \frac{\Delta t}{2}(Q^\tau + Q^{\tau+1})$$|$\Delta t^2$ |
| **General** | $$\tilde{u}^{\tau+1} = \tilde{u}^\tau + \Delta t((1-\alpha)Q^\tau + \alpha Q^{\tau+1})$$|$\Delta t$ |

:::{note} General Method
This is a flexible framework that combines the explicit and implicit methods using a weighting factor, $\alpha$.

- If $\alpha=0$, it is the fully explicit method.
- If $\alpha=1$, it is the fully implicit method.
- If $\alpha=0.5$, it becomes the trapezoidal rule.

This allows for a tunable balance between the computational ease of the explicit method and the stability of the implicit method.
:::

## Multistep methods

Unlike single-step methods that only use information from the most recent time step, multistep methods increase accuracy by using information from several previous steps to compute the next step.


| Method | Scheme | Truncation Order |
| :---: | :--- | :---: |
| **Leapfrog** | $$\tilde{u}^{\tau+1} = \tilde{u}^{\tau-1} + 2\Delta t Q^\tau$$|$\Delta t^2$ |
| **Adams-Bashforth** | $$\tilde{u}^{\tau+1} = \tilde{u}^\tau + \frac{\Delta t}{2}(-Q^{\tau-1} + 3Q^\tau)$$|$\Delta t^2$ |
| **Adams-Moulton** | $$\tilde{u}^{\tau+1} = \tilde{u}^\tau + \frac{\Delta t}{12}(-Q^{\tau-1} + 8Q^\tau + 5Q^{\tau+1})$$|$\Delta t^3$ |
| **Adams-Bashforth** | $$\tilde{u}^{\tau+1} = \tilde{u}^\tau + \frac{\Delta t}{12}(5Q^{\tau-2} - 16Q^{\tau-1} + 23Q^{\tau+1})$$|$\Delta t^3$ |

:::{note} Leapfrog
The leapfrog method is an explicit, second-order method that is popular for simulating physical systems. It gets its name because it "leaps" over the current point ($u^\tau$) to calculate the next point ($u^{\tau+1}$) using the derivative at $u^\tau$ and the value from the previous point, $u^{\tau-1}$. This structure helps conserve energy in long-term simulations but can sometimes lead to instability.
:::

## Multistage methods

Multistage methods calculate the solution at the next time step by performing several intermediate calculations, or "stages," within a single time interval. Instead of using data from previous time steps (like multistep methods), they evaluate the derivative function multiple times *between* the current and next points to get a more accurate slope estimate.


The core idea is to take a "trial" step, re-evaluate the derivative at this new trial position, and then use this more accurate information to take the final, full step.

  * **2nd-Order RK:** Often called the **midpoint method**, this scheme first takes a half-step to the midpoint of the time interval. It then uses the derivative calculated at that midpoint to compute the full step, which is more accurate than just using the derivative from the start of the interval.

  * **4th-Order RK:** This is one of the most widely used numerical methods for solving differential equations. It achieves very high accuracy by cleverly performing four derivative evaluations within each time step: one at the beginning, two at the midpoint, and one at the end of the interval. These are combined in a weighted average to produce a result that is remarkably accurate and robust.


| Method | Scheme | Order |
| :---: | :--- | :---: |
| **Runge-Kutta** (2nd Order) | $$\begin{aligned} \tilde{u}^{\tau+1/2} &= \tilde{u}^\tau + \frac{\Delta t}{2}Q(t^\tau, \tilde{u}^\tau) \\ \tilde{u}^{\tau+1} &= \tilde{u}^\tau + \Delta t Q(t^{\tau+1/2}, \tilde{u}^{\tau+1/2}) \end{aligned}$$|$\Delta t^2$ |
| **Runge-Kutta** (4th Order) | $$\begin{aligned} \tilde{u}_a^{\tau+1/2} &= \tilde{u}^\tau + \frac{\Delta t}{2}Q(t^\tau, \tilde{u}^\tau) \\ \tilde{u}_b^{\tau+1/2} &= \tilde{u}^\tau + \frac{\Delta t}{2}Q(t^{\tau+1/2}, \tilde{u}_a^{\tau+1/2}) \\ \tilde{u}^* &= \tilde{u}^\tau + \Delta t Q(t^{\tau+1/2}, \tilde{u}_b^{\tau+1/2}) \\ \tilde{u}^{\tau+1} &= \tilde{u}^\tau + \frac{\Delta t}{6} \big( Q(t^\tau, \tilde{u}^\tau) + 2Q(t^{\tau+1/2}, \tilde{u}_a^{\tau+1/2}) \\ &+ 2Q(t^{\tau+1/2}, \tilde{u}_b^{\tau+1/2}) + Q(t^{\tau+1}, \tilde{u}^*) \big) \end{aligned}$$|$\Delta t^4$ |
