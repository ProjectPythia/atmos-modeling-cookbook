# Finite Differencing

Here we compile the standard finite difference schemes of various orders on uniform grids.

Consider the derivative $du/dx$ of a function $u(x)$, where $x$ can be any independent variable (e.g., time, space, etc.). Finite-difference approximations are used to represent the continuous function $u(x)$ by a set of discrete points $u_n$ at evenly spaced intervals, where $n$ is the index of the point in the grid. The spacing between these points is denoted as $\Delta x$.

:::{figure} 1d-grid.png
:label: 1d-grid
Example of a one-dimensional grid with uniform spacing $\Delta x$.
:::

:::{important} Big $\mathcal{O}$ Notation
The notation $\mathcal{O}(\cdot)$, known as Big $\mathcal{O}$ notation, describes the truncation error of the approximation. It provides insight into how quickly the error shrinks as you decrease the step size, $\Delta x$.

| Feature | First-Order Error ($\mathcal{O}(\Delta x)$) | Second-Order Error ($\mathcal{O}(\Delta x^2)$) |
|:-----------------------------:|:-----------------------------------------------:|:--------------------------------------------------:|
| **Proportionality** | Error is proportional to the step size, $\Delta x$. | Error is proportional to the **square** of the step size, $\Delta x^2$. |
| **Convergence Rate** | Linear | **Quadratic** |
| **Effect of Halving $\Delta x$** | Error is reduced by a factor of 2 (halved). | Error is reduced by a factor of 4 (**quartered**). |
| **Accuracy** | Lower | Higher |

:::

## Forward Difference

### First Derivative $(\frac{\partial u}{\partial x})$

| $\mathcal{O}(\Delta x)$ | $\mathcal{O}(\Delta x^2)$ |
| :---: | :---: |
| $$\label{forward_first_o1}\frac{u_{n+1} - u_n}{\Delta x}$$ | $$\label{forward_first_o2}\frac{-u_{n+2} + 4u_{n+1} - 3u_n}{2\Delta x}$$ |

### Second Derivative $(\frac{\partial^2 u}{\partial x^2})$

| $\mathcal{O}(\Delta x)$ | $\mathcal{O}(\Delta x^2)$ |
| :---: | :---: |
| $$\label{forward_second_o1}\frac{u_{n+2} - 2u_{n+1} + u_n}{\Delta x^2}$$ | $$\label{forward_second_o2}\frac{-u_{n+3} + 4u_{n+2} - 5u_{n+1} + 2u_n}{\Delta x^2}$$ |

### Third Derivative $(\frac{\partial^3 u}{\partial x^3})$

| $\mathcal{O}(\Delta x)$ | $\mathcal{O}(\Delta x^2)$ |
| :---: | :---: |
| $$\label{forward_third_o1}\frac{u_{n+3} - 3u_{n+2} + 3u_{n+1} - u_n}{\Delta x^3}$$ | $$\label{forward_third_o2}\frac{-3u_{n+4} + 14u_{n+3} - 24u_{n+2} + 18u_{n+1} - 5u_n}{2\Delta x^3}$$ |

### Fourth Derivative $(\frac{\partial^4 u}{\partial x^4})$

| $\mathcal{O}(\Delta x)$ | $\mathcal{O}(\Delta x^2)$ |
| :---: | :---: |
| $$\label{forward_fourth_o1}\frac{u_{n+4} - 4u_{n+3} + 6u_{n+2} - 4u_{n+1} + u_n}{\Delta x^4}$$ | $$\label{forward_fourth_o2}\frac{-2u_{n+5} + 11u_{n+4} - 24u_{n+3} + 26u_{n+2} - 14u_{n+1} + 3u_n}{\Delta x^4}$$ |

---

## Backward Difference

### First Derivative $(\frac{\partial u}{\partial x})$

| $\mathcal{O}(\Delta x)$ | $\mathcal{O}(\Delta x^2)$ |
| :---: | :---: |
| $$\label{backward_first_o1}\frac{u_n - u_{n-1}}{\Delta x}$$|$$\label{backward_first_o2}\frac{3u_n - 4u_{n-1} + u_{n-2}}{2\Delta x}$$ |

### Second Derivative $(\frac{\partial^2 u}{\partial x^2})$

| $\mathcal{O}(\Delta x)$ | $\mathcal{O}(\Delta x^2)$ |
| :---: | :---: |
| $$\label{backward_second_o1}\frac{u_n - 2u_{n-1} + u_{n-2}}{\Delta x^2}$$|$$\label{backward_second_o2}\frac{2u_n - 5u_{n-1} + 4u_{n-2} - u_{n-3}}{\Delta x^2}$$ |

### Third Derivative $(\frac{\partial^3 u}{\partial x^3})$

| $\mathcal{O}(\Delta x)$ | $\mathcal{O}(\Delta x^2)$ |
| :---: | :---: |
| $$\label{backward_third_o1}\frac{u_n - 3u_{n-1} + 3u_{n-2} - u_{n-3}}{\Delta x^3}$$|$$\label{backward_third_o2}\frac{5u_n - 18u_{n-1} + 24u_{n-2} - 14u_{n-3} + 3u_{n-4}}{2\Delta x^3}$$ |

### Fourth Derivative $(\frac{\partial^4 u}{\partial x^4})$

| $\mathcal{O}(\Delta x)$ | $\mathcal{O}(\Delta x^2)$ |
| :---: | :---: |
| $$\label{backward_fourth_o1}\frac{u_n - 4u_{n-1} + 6u_{n-2} - 4u_{n-3} + u_{n-4}}{\Delta x^4}$$|$$\label{backward_fourth_o2}\frac{3u_n - 14u_{n-1} + 26u_{n-2} - 24u_{n-3} + 11u_{n-4} - 2u_{n-5}}{\Delta x^4}$$ |

---

## Central Difference

### First Derivative $(\frac{\partial u}{\partial x})$

| $\mathcal{O}(\Delta x^2)$ | $\mathcal{O}(\Delta x^4)$ |
| :---: | :---: |
| $$\label{central_first_o2}\frac{u_{n+1} - u_{n-1}}{2\Delta x}$$|$$\label{central_first_o4}\frac{-u_{n+2} + 8u_{n+1} - 8u_{n-1} + u_{n-2}}{12\Delta x}$$ |

### Second Derivative $(\frac{\partial^2 u}{\partial x^2})$

| $\mathcal{O}(\Delta x^2)$ | $\mathcal{O}(\Delta x^4)$ |
| :---: | :---: |
| $$\label{central_second_o2}\frac{u_{n+1} - 2u_n + u_{n-1}}{\Delta x^2}$$|$$\label{central_second_o4}\frac{-u_{n+2} + 16u_{n+1} - 30u_n + 16u_{n-1} - u_{n-2}}{12\Delta x^2}$$ |

### Third Derivative $(\frac{\partial^3 u}{\partial x^3})$

| $\mathcal{O}(\Delta x^2)$ | $\mathcal{O}(\Delta x^4)$ |
| :---: | :---: |
| $$\label{central_third_o2}\frac{u_{n+2} + 2u_{n+1} - 2u_{n-1} - u_{n-2}}{2\Delta x^3}$$|$$\label{central_third_o4}\frac{-u_{n+3} + 8u_{n+2} - 13u_{n+1} + 13u_{n-1} - 8u_{n-2} + u_{n-3}}{8\Delta x^3}$$ |

### Fourth Derivative $(\frac{\partial^4 u}{\partial x^4})$

| $\mathcal{O}(\Delta x^2)$ | $\mathcal{O}(\Delta x^4)$ |
| :---: | :---: |
| $$\label{central_fourth_o2}\frac{u_{n+2} - 4u_{n+1} + 6u_n - 4u_{n-1} + u_{n-2}}{\Delta x^4}$$|$$\label{central_fourth_o4}\frac{-u_{n+3} + 12u_{n+2} - 39u_{n+1} + 56u_n - 39u_{n-1} + 12u_{n-2} - u_{n-3}}{6\Delta x^4}$$ |
