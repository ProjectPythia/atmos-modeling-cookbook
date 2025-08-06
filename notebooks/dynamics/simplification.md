# Simplifying the Basic Equations

### Assumptions and Simplification

In this notebook we construct a two-dimensional, dry, and compressible atmospheric model that is broadly in line with KW78, though several assumptions and choice configurations were made to simplify the current model for computational and educational efficency.
<br>
1. We will only consider the zonal ($x$) and vertical ($z$) components.
2. Base-state variables are a function of $z$ only, denoted by $\overline{\phi}$.
3. Water-vapor is neglected (i.e, $q_{v}, q_{r}, q_{c} = 0$), so  $T_{v} = T$ and/or $\theta_{v} = \theta$.
4. Coriolis force, microphysics, and Turbulence are also neglected(i.e., $f, M_{\theta}, D_{\theta} = 0$).     
5. As in KW78, the $f_{\pi}$ term in Pressure Equation (PEQ4-3) is neglected due to its negligible influences on convective-scale processes along with sound and gravity waves.
6. Sub-Grid Processes require parameterizations in order to achieve model closure. For example, sub-grid turbulence is first obtained using Reynolds Averaged prognostic variables (i.e., breaking up variables into mean and turbulence components), and then must be parameterized using additional assumptions (such as the flux-gradient approach). 
7. The current test case is designed to have a calm and isentropic base-state (i.e., $\frac{\partial \overline\theta}{\partial t}$ and  $\overline{U} = 0$)

### Final Prognostic Equations

The afformentioned assumptions allowed for the derivation of the following simplified equations that serve as the foundation for the numerical model.
<br> 

EQ1. Zonal Momentum Equation  
\[
\frac{du}{dt} + c_{p} \bar{\theta} \frac{\partial \pi}{\partial x} = 0
\]

Lagrangian Derivative of Zonal Wind

PGF Term

---

EQ2. Vertical Momentum Equation  
\[
\frac{dw}{dt} + c_{p} \bar{\theta} \frac{\partial \pi}{\partial z} = g\left[\frac{\theta}{\bar{\theta}} - 1\right]
\]

Lagrangian Derivative of Vertical Wind

PGF Term

Dry Buoyancy Contribution

---

EQ3. Prognostic Equations  
\[
\frac{d\theta}{dt} = 0
\]

Lagrangian Derivative of Potential Temperature

---

EQ4. Pressure Equation  
\[
\frac{\partial \pi}{\partial t} + \frac{\overline{c}^2}{c_{p}\overline{\rho}\overline{\theta}^2} \left[ \frac{\partial}{\partial x}(\overline{\rho}\overline{\theta}u) + \frac{\partial}{\partial z}(\overline{\rho}\overline{\theta}w) \right] = 0
\]

1. Eularian Derivative of Pressure
2. Pressure Adjustment Terms