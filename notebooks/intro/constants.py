#!/usr/bin/env python3

R_d = 8.314462618 / 28.96546e-3 # R / Md, (J/(mol*K)) / (kg/mol) = J/(kg*K)
c_p = 1.4 * R_d / (1.4 - 1) # J/(kg*K)
c_v = c_p - R_d
gravity = 9.80665 # m/(s^(2))
p0 = 1.0e5
