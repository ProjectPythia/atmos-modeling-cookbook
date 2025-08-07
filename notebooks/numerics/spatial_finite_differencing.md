# Spatial Finite Differencing

Here we compile the standard finite difference schemes of various orders on uniform grids. This will include the forward, backward, and centered differences 

:::{important} Big $\mathcal{O}$ Notation
The notation $\mathcal{O}(\cdot)$, known as Big $\mathcal{O}$ notation, describes the truncation error of the approximation. It provides insight into how quickly the error shrinks as you decrease the step size, $\Delta t$.

| Feature | First-Order Error ($\mathcal{O}(\Delta t)$) | Second-Order Error ($\mathcal{O}(\Delta t^2)$) |
|:-----------------------------:|:-----------------------------------------------:|:--------------------------------------------------:|
| **Proportionality** | Error is proportional to the step size, $\Delta t$. | Error is proportional to the **square** of the step size, $\Delta t^2$. |
| **Convergence Rate** | Linear | **Quadratic** |
| **Effect of Halving $\Delta t$** | Error is reduced by a factor of 2 (halved). | Error is reduced by a factor of 4 (**quartered**). |
| **Accuracy** | Lower | Higher |

:::

## Forward Difference

### First Derivative $(\frac{\partial u}{\partial t})$

| $\mathcal{O}(\Delta t)$ | $\mathcal{O}(\Delta t^2)$ |
| :---: | :---: |
| $$\label{eq:forward_first_o1}\frac{u^{n+1} - u^n}{\Delta t}$$ | $$\label{eq:forward_first_o2}\frac{-u^{n+2} + 4u^{n+1} - 3u^n}{2\Delta t}$$ |

### Second Derivative $(\frac{\partial^2 u}{\partial t^2})$

| $\mathcal{O}(\Delta t)$ | $\mathcal{O}(\Delta t^2)$ |
| :---: | :---: |
| $$\label{eq:forward_second_o1}\frac{u^{n+2} - 2u^{n+1} + u^n}{\Delta t^2}$$ | $$\label{eq:forward_second_o2}\frac{-u^{n+3} + 4u^{n+2} - 5u^{n+1} + 2u^n}{\Delta t^2}$$ |

### Third Derivative $(\frac{\partial^3 u}{\partial t^3})$

| $\mathcal{O}(\Delta t)$ | $\mathcal{O}(\Delta t^2)$ |
| :---: | :---: |
| $$\label{eq:forward_third_o1}\frac{u^{n+3} - 3u^{n+2} + 3u^{n+1} - u^n}{\Delta t^3}$$ | $$\label{eq:forward_third_o2}\frac{-3u^{n+4} + 14u^{n+3} - 24u^{n+2} + 18u^{n+1} - 5u^n}{2\Delta t^3}$$ |

### Fourth Derivative $(\frac{\partial^4 u}{\partial t^4})$

| $\mathcal{O}(\Delta t)$ | $\mathcal{O}(\Delta t^2)$ |
| :---: | :---: |
| $$\label{eq:forward_fourth_o1}\frac{u^{n+4} - 4u^{n+3} + 6u^{n+2} - 4u^{n+1} + u^n}{\Delta t^4}$$ | $$\label{eq:forward_fourth_o2}\frac{-2u^{n+5} + 11u^{n+4} - 24u^{n+3} + 26u^{n+2} - 14u^{n+1} + 3u^n}{\Delta t^4}$$ |

---

## Backward Difference

### First Derivative $(\frac{\partial u}{\partial t})$

| $\mathcal{O}(\Delta t)$ | $\mathcal{O}(\Delta t^2)$ |
| :---: | :---: |
| $$\label{eq:backward_first_o1}\frac{u^n - u^{n-1}}{\Delta t}$$|$$\label{eq:backward_first_o2}\frac{3u^n - 4u^{n-1} + u^{n-2}}{2\Delta t}$$ |

### Second Derivative $(\frac{\partial^2 u}{\partial t^2})$

| $\mathcal{O}(\Delta t)$ | $\mathcal{O}(\Delta t^2)$ |
| :---: | :---: |
| $$\label{eq:backward_second_o1}\frac{u^n - 2u^{n-1} + u^{n-2}}{\Delta t^2}$$|$$\label{eq:backward_second_o2}\frac{2u^n - 5u^{n-1} + 4u^{n-2} - u^{n-3}}{\Delta t^2}$$ |

### Third Derivative $(\frac{\partial^3 u}{\partial t^3})$

| $\mathcal{O}(\Delta t)$ | $\mathcal{O}(\Delta t^2)$ |
| :---: | :---: |
| $$\label{eq:backward_third_o1}\frac{u^n - 3u^{n-1} + 3u^{n-2} - u^{n-3}}{\Delta t^3}$$|$$\label{eq:backward_third_o2}\frac{5u^n - 18u^{n-1} + 24u^{n-2} - 14u^{n-3} + 3u^{n-4}}{2\Delta t^3}$$ |

### Fourth Derivative $(\frac{\partial^4 u}{\partial t^4})$

| $\mathcal{O}(\Delta t)$ | $\mathcal{O}(\Delta t^2)$ |
| :---: | :---: |
| $$\label{eq:backward_fourth_o1}\frac{u^n - 4u^{n-1} + 6u^{n-2} - 4u^{n-3} + u^{n-4}}{\Delta t^4}$$|$$\label{eq:backward_fourth_o2}\frac{3u^n - 14u^{n-1} + 26u^{n-2} - 24u^{n-3} + 11u^{n-4} - 2u^{n-5}}{\Delta t^4}$$ |

---

## Central Difference

### First Derivative $(\frac{\partial u}{\partial t})$

| $\mathcal{O}(\Delta t^2)$ | $\mathcal{O}(\Delta t^4)$ |
| :---: | :---: |
| $$\label{eq:central_first_o2}\frac{u^{n+1} - u^{n-1}}{2\Delta t}$$|$$\label{eq:central_first_o4}\frac{-u^{n+2} + 8u^{n+1} - 8u^{n-1} + u^{n-2}}{12\Delta t}$$ |

### Second Derivative $(\frac{\partial^2 u}{\partial t^2})$

| $\mathcal{O}(\Delta t^2)$ | $\mathcal{O}(\Delta t^4)$ |
| :---: | :---: |
| $$\label{eq:central_second_o2}\frac{u^{n+1} - 2u^n + u^{n-1}}{\Delta t^2}$$|$$\label{eq:central_second_o4}\frac{-u^{n+2} + 16u^{n+1} - 30u^n + 16u^{n-1} - u^{n-2}}{12\Delta t^2}$$ |

### Third Derivative $(\frac{\partial^3 u}{\partial t^3})$

| $\mathcal{O}(\Delta t^2)$ | $\mathcal{O}(\Delta t^4)$ |
| :---: | :---: |
| $$\label{eq:central_third_o2}\frac{u^{n+2} + 2u^{n+1} - 2u^{n-1} - u^{n-2}}{2\Delta t^3}$$|$$\label{eq:central_third_o4}\frac{-u^{n+3} + 8u^{n+2} - 13u^{n+1} + 13u^{n-1} - 8u^{n-2} + u^{n-3}}{8\Delta t^3}$$ |

### Fourth Derivative $(\frac{\partial^4 u}{\partial t^4})$

| $\mathcal{O}(\Delta t^2)$ | $\mathcal{O}(\Delta t^4)$ |
| :---: | :---: |
| $$\label{eq:central_fourth_o2}\frac{u^{n+2} - 4u^{n+1} + 6u^n - 4u^{n-1} + u^{n-2}}{\Delta t^4}$$|$$\label{eq:central_fourth_o4}\frac{-u^{n+3} + 12u^{n+2} - 39u^{n+1} + 56u^n - 39u^{n-1} + 12u^{n-2} - u^{n-3}}{6\Delta t^4}$$ |