# The Basic Equations

### Starting Equations (from WK78)



#### Diagnostics
    
DEQ 1. Equation of State (2.1) 
$$
p = \rho R_{d} T
$$ 
* $p$: Pressure
* $\rho$: Density
* $R_{d}$: Specific gas constant for dry air
* $T: Temperature
<br>

DEQ 2. Exner Function (2.2)
$$
\Pi = (\frac{p}{p_{0}})^\frac{R_{d}}{c_{p}}
$$
* $\Pi$: Non-Dimensional Pressure
* $p$: Pressure
* $p_{0}$: Reference Pressure
* $R_{d}$: Specific gas constant for dry air
* $c_{p}$: Specific heat at constant pressure    
<br>


#### Prognostics
    
PEQ 1-2. Momentum Equation (Zonal & Vertical; 2.4)
$$
\underset{1}{\frac{du_{i}}{dt}}+ 
\underset{2}{c_{p} \overline{\theta_{v}} \frac{\partial \pi}{\partial x_{i}} }=
\underset{3}{\delta_{i_{3}}} 
\underset{4}{g}\left[
\underset{5}{\frac{\theta}{\overline{\theta}} - 1}+
\underset{6}{0.61(q_{v}-\overline{q_{v}})}-
\underset{7}{q_{c}-q_{r}}\right]-
\underset{8}{\epsilon_{ij_{3}}}fu_{i}+ 
\underset{9}{D_{u_i}}
$$

1. Lagrangian of Wind
2. PGF Term
3. Kronecker Delta (i.e., the term that follows only appears form dimension 3, the vertical)
4. Gravity
5. Dry Buoyancy Contribution
6. Moist Buoyancy Contribution
7. Water Loading
8. Coriolis Term
9. Turblence Term

<i>Derived via Navier-Stokes equations, along with DEQ1-2, Hydrostatic Function, and Linearized Pressure Term. Tensor Notation is used for simplicity.</i>
<br> 
 
PEQ 3. Prognostic Equations (2.5)
$$
\underset{1}{\frac{d\phi}{dt}}=
\underset{2}{M_{\phi}}+ 
\underset{3}{D_{\phi}}
$$

1. Lagrangian of Prognositc Variable
2. Microphysical Term 
3. Turbulence Term
        
<i>$\phi$ is representative of either $\theta, q_{v}, q_{r},$ or  $q_{c}$</i>
<br>
    
PEQ 4. Pressure Equation (2.7a)
$$
\underset{1}{\frac{\partial\pi}{\partial t}}+
\underset{2}{\frac{ \overline{c}^2}{c_{p}{\overline\rho\overline{\theta_{v}^2}}}
{\frac{\partial}{\partial x_{j}}(\overline{\rho}\overline{\theta_{v}}} u_{j})}=
\underset{3}{f_{\pi}}
$$

1. Eularian of Pressure
2. Pressure Adjustment Term
3. Non-Relevant Terms for Sound & Gravity Waves (<i>See KW78 2.7b</i>)

<i>Derived using Compressible Continuity & Thermodynamic Equations; Tensor Notation Used for Simplicity</i>
...