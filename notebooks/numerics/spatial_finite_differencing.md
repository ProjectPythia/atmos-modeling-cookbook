# Spatial Finite Differencing

## Forward Difference

### First Order Derivative
$$
\frac{\partial u}{\partial t} \approx \frac{u^{n+1} - u^n}{\Delta t}
$$

### Second Order Derivative
$$
\frac{\partial^2 u}{\partial t^2} \approx \frac{u^{n+2} - 2u^{n+1} + u^n}{\Delta t^2}
$$

### Third Order Derivative
$$
\frac{\partial^3 u}{\partial t^3} \approx \frac{-u^n + 3u^{n+1} - 3u^{n+2} + u^{n+3}}{\Delta t^3}
$$

### Fourth Order Derivative
$$
\frac{\partial^4 u}{\partial t^4} \approx \frac{u^n - 4u^{n+1} + 6u^{n+2} - 4u^{n+3} + u^{n+4}}{\Delta t^4}
$$
