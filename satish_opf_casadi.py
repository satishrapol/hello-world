import numpy as np
import casadi

# Node 0, 1, 2, 3, 4
# Node 0 neighbours : 1 and 2
G = np.array([ \
    [2247.319255, -355.871886, 0.000000, -328.947368, -1562.500000], \
    [-355.871886, 1281.797812, -925.925926, 0.000000, 0.0000000000], \
    [0.000000, -925.925926, 1262.626263, -336.700337, 0.0000000000], \
    [-328.947368, 0.000000, -336.700337, 1002.348042, -336.700337], \
    [-1562.50000, 0.000000, 0.000000, -336.700337, 1899.200337], \
    ])
# P_load = np.array([3.00, 3.00, 3.00,4.00, 0.00])
P_load = np.array([3.00, 3.00, 3.00,4.00, 0.00])


alpha = 0.1
beta  = 14
gamma = 1
total_nodes = 5

#---------------------------------------------------Node 0-------------------------------------------------------------#
# Lower bounds of the system components
Pgq_min  = 0
Pqnq_min = -5
Pq_min   = -5
Iqnq_min = -5
Vq_min   =  0.9

# Upper bounds of the system components
Pgq_max =  2.1
Pqnq_max =  5
Pq_max   =  5
Iqnq_max =  5
Vq_max   =  1.1


q = 0                   # Node 0
neighbours_of_node_q = [0, 1, 0, 1, 1]

sum_of_neighbours = int(sum(neighbours_of_node_q))
opti     = casadi.Opti()
Vq       = opti.variable(5)
Pgq      = opti.variable(5)
Pq       = opti.variable(5)
Pqnq     = opti.variable(total_nodes)
Iqnq     = opti.variable(total_nodes)
Iq = 0

#  Applying KCL at node q
for nq in range(total_nodes):
    # if neighbours_of_node_q[nq] == 1:
    Iq = Iq + G[q,nq]*Vq[nq]

# Defining the cost function

cost = alpha + beta * (P_load[q] + Pq[q]) \
       + gamma * (P_load[q] + Pq[q])*(P_load[q] + Pq[q])

opti.minimize(cost)

# Declaring all the equality constraints first
opti.subject_to(Pq[q] == Vq[q]*Iq)
opti.subject_to(Pgq[q] == P_load[q] + Pq[q])

for nq in range(total_nodes):
    if neighbours_of_node_q[nq] == 1:
        opti.subject_to(Iqnq[nq] == G[q,nq]*(Vq[nq]-Vq[q]))
        opti.subject_to(Pqnq[nq] == Vq[q]*Iqnq[nq])

# # Inequality constraints
# Pgq_min  =  0
# Pqnq_min = -5
# Pq_min   = -5
# Pgq[q] == P_load[q] + Pq[q]
# 0 == 0 + 0
opti.subject_to(Pgq[0] >= Pgq_min)
opti.subject_to(Pqnq[0] >= Pqnq_min)
opti.subject_to(Pq[0] >= Pq_min)
opti.subject_to(Iqnq[:] >= Iqnq_min)
opti.subject_to(Vq[:] >= Vq_min)
#
opti.subject_to(Pgq[0] <= Pgq_max)
opti.subject_to(Pqnq[0] <= Pqnq_max)
opti.subject_to(Pq[0] <= Pq_max)
opti.subject_to(Iqnq[:] <= Iqnq_max)
opti.subject_to(Vq[:] <= Vq_max)
opti.set_initial(Vq[:],1)
opti.set_initial(Pq[0],0)
opti.set_initial(Pqnq[0],0)

# Solver type and its parameters are defined here
p_opts = {"ipopt.print_level": False, "print_time": False, "verbose": False, "ipopt.max_iter": 100000}
opti.solver('ipopt', p_opts)

# try:
sol = opti.solve()
# except:
#     print("Please recheck Problem Formulation again")

print('Voltage', sol.value(Vq[:]))
print('Current', sol.value(Iqnq[:]))
print('Power_nq', sol.value(Pqnq[:]))
print('Power_q', sol.value(Pq[:]))
print('Power_gq', sol.value(Pgq[:]))

#---------------------------------------------------Node 1-------------------------------------------------------------#

# Lower bounds of the system components
Pgq_min  = 0
Pqnq_min = -5
Pq_min   = -5
Iqnq_min = -5
Vq_min   =  0.9

# Upper bounds of the system components
Pgq_max =  0
Pqnq_max =  5
Pq_max   =  5
Iqnq_max =  5
Vq_max   =  1.1


q = 1                   # Node 1
neighbours_of_node_q = [1, 0, 1, 0, 0]

sum_of_neighbours = int(sum(neighbours_of_node_q))
opti     = casadi.Opti()
Vq       = opti.variable(5)
Pgq      = opti.variable(5)
Pq       = opti.variable(5)
Pqnq     = opti.variable(total_nodes)
Iqnq     = opti.variable(total_nodes)
Iq = 0

#  Applying KCL at node q
for nq in range(total_nodes):
    # if neighbours_of_node_q[nq] == 1:
    Iq = Iq + G[q,nq]*Vq[nq]

# Defining the cost function

cost = alpha + beta * (P_load[q] + Pq[q]) \
       + gamma * (P_load[q] + Pq[q])*(P_load[q] + Pq[q])

opti.minimize(cost)

# Declaring all the equality constraints first
opti.subject_to(Pq[q] == Vq[q]*Iq)
opti.subject_to(Pgq[q] == P_load[q] + Pq[q])

for nq in range(total_nodes):
    if neighbours_of_node_q[nq] == 1:
        opti.subject_to(Iqnq[nq] == G[q,nq]*(Vq[nq]-Vq[q]))
        opti.subject_to(Pqnq[nq] == Vq[q]*Iqnq[nq])

# # Inequality constraints
# Pgq_min  =  0
# Pqnq_min = -5
# Pq_min   = -5
# Pgq[q] == P_load[q] + Pq[q]
# 0 == 0 + 0
opti.subject_to(Pgq[0] >= Pgq_min)
opti.subject_to(Pqnq[0] >= Pqnq_min)
opti.subject_to(Pq[0] >= Pq_min)
opti.subject_to(Iqnq[:] >= Iqnq_min)
opti.subject_to(Vq[:] >= Vq_min)
#
opti.subject_to(Pgq[0] <= Pgq_max)
opti.subject_to(Pqnq[0] <= Pqnq_max)
opti.subject_to(Pq[0] <= Pq_max)
opti.subject_to(Iqnq[:] <= Iqnq_max)
opti.subject_to(Vq[:] <= Vq_max)
opti.set_initial(Vq[:],1)
opti.set_initial(Pq[0],0)
opti.set_initial(Pqnq[0],0)

# Solver type and its parameters are defined here
p_opts = {"ipopt.print_level": False, "print_time": False, "verbose": False, "ipopt.max_iter": 100000}
opti.solver('ipopt', p_opts)

# try:
sol = opti.solve()
# except:
#     print("Please recheck Problem Formulation again")

print('Voltage', sol.value(Vq[:]))
print('Current', sol.value(Iqnq[:]))
print('Power_nq', sol.value(Pqnq[:]))
print('Power_q', sol.value(Pq[:]))
print('Power_gq', sol.value(Pgq[:]))

#---------------------------------------------------Node 2-------------------------------------------------------------#

# Lower bounds of the system components
Pgq_min  = 0
Pqnq_min = -5
Pq_min   = -5
Iqnq_min = -5
Vq_min   =  0.9

# Upper bounds of the system components
Pgq_max =  5.2
Pqnq_max =  5
Pq_max   =  5
Iqnq_max =  5
Vq_max   =  1.1


q = 2                   # Node 2
neighbours_of_node_q = [0, 1, 0, 1, 0]

sum_of_neighbours = int(sum(neighbours_of_node_q))
opti     = casadi.Opti()
Vq       = opti.variable(5)
Pgq      = opti.variable(5)
Pq       = opti.variable(5)
Pqnq     = opti.variable(total_nodes)
Iqnq     = opti.variable(total_nodes)
Iq = 0

#  Applying KCL at node q
for nq in range(total_nodes):
    # if neighbours_of_node_q[nq] == 1:
    Iq = Iq + G[q,nq]*Vq[nq]

# Defining the cost function

cost = alpha + beta * (P_load[q] + Pq[q]) \
       + gamma * (P_load[q] + Pq[q])*(P_load[q] + Pq[q])

opti.minimize(cost)

# Declaring all the equality constraints first
opti.subject_to(Pq[q] == Vq[q]*Iq)
opti.subject_to(Pgq[q] == P_load[q] + Pq[q])

for nq in range(total_nodes):
    if neighbours_of_node_q[nq] == 1:
        opti.subject_to(Iqnq[nq] == G[q,nq]*(Vq[nq]-Vq[q]))
        opti.subject_to(Pqnq[nq] == Vq[q]*Iqnq[nq])

# # Inequality constraints
# Pgq_min  =  0
# Pqnq_min = -5
# Pq_min   = -5
# Pgq[q] == P_load[q] + Pq[q]
# 0 == 0 + 0
opti.subject_to(Pgq[0] >= Pgq_min)
opti.subject_to(Pqnq[0] >= Pqnq_min)
opti.subject_to(Pq[0] >= Pq_min)
opti.subject_to(Iqnq[:] >= Iqnq_min)
opti.subject_to(Vq[:] >= Vq_min)
#
opti.subject_to(Pgq[0] <= Pgq_max)
opti.subject_to(Pqnq[0] <= Pqnq_max)
opti.subject_to(Pq[0] <= Pq_max)
opti.subject_to(Iqnq[:] <= Iqnq_max)
opti.subject_to(Vq[:] <= Vq_max)
opti.set_initial(Vq[:],1)
opti.set_initial(Pq[0],0)
opti.set_initial(Pqnq[0],0)

# Solver type and its parameters are defined here
p_opts = {"ipopt.print_level": False, "print_time": False, "verbose": False, "ipopt.max_iter": 100000}
opti.solver('ipopt', p_opts)

# try:
sol = opti.solve()
# except:
#     print("Please recheck Problem Formulation again")

print('Voltage', sol.value(Vq[:]))
print('Current', sol.value(Iqnq[:]))
print('Power_nq', sol.value(Pqnq[:]))
print('Power_q', sol.value(Pq[:]))
print('Power_gq', sol.value(Pgq[:]))

#---------------------------------------------------Node 3-------------------------------------------------------------#

# Lower bounds of the system components
Pgq_min  = 0
Pqnq_min = -5
Pq_min   = -5
Iqnq_min = -5
Vq_min   =  0.9

# Upper bounds of the system components
Pgq_max =  2
Pqnq_max =  5
Pq_max   =  5
Iqnq_max =  5
Vq_max   =  1.1


q = 3                   # Node 3
neighbours_of_node_q = [1, 0, 1, 0, 1]

sum_of_neighbours = int(sum(neighbours_of_node_q))
opti     = casadi.Opti()
Vq       = opti.variable(5)
Pgq      = opti.variable(5)
Pq       = opti.variable(5)
Pqnq     = opti.variable(total_nodes)
Iqnq     = opti.variable(total_nodes)
Iq = 0

#  Applying KCL at node q
for nq in range(total_nodes):
    # if neighbours_of_node_q[nq] == 1:
    Iq = Iq + G[q,nq]*Vq[nq]

# Defining the cost function

cost = alpha + beta * (P_load[q] + Pq[q]) \
       + gamma * (P_load[q] + Pq[q])*(P_load[q] + Pq[q])

opti.minimize(cost)

# Declaring all the equality constraints first
opti.subject_to(Pq[q] == Vq[q]*Iq)
opti.subject_to(Pgq[q] == P_load[q] + Pq[q])

for nq in range(total_nodes):
    if neighbours_of_node_q[nq] == 1:
        opti.subject_to(Iqnq[nq] == G[q,nq]*(Vq[nq]-Vq[q]))
        opti.subject_to(Pqnq[nq] == Vq[q]*Iqnq[nq])

# # Inequality constraints
# Pgq_min  =  0
# Pqnq_min = -5
# Pq_min   = -5
# Pgq[q] == P_load[q] + Pq[q]
# 0 == 0 + 0
opti.subject_to(Pgq[0] >= Pgq_min)
opti.subject_to(Pqnq[0] >= Pqnq_min)
opti.subject_to(Pq[0] >= Pq_min)
opti.subject_to(Iqnq[:] >= Iqnq_min)
opti.subject_to(Vq[:] >= Vq_min)
#
opti.subject_to(Pgq[0] <= Pgq_max)
opti.subject_to(Pqnq[0] <= Pqnq_max)
opti.subject_to(Pq[0] <= Pq_max)
opti.subject_to(Iqnq[:] <= Iqnq_max)
opti.subject_to(Vq[:] <= Vq_max)
opti.set_initial(Vq[:],1)
opti.set_initial(Pq[0],0)
opti.set_initial(Pqnq[0],0)

# Solver type and its parameters are defined here
p_opts = {"ipopt.print_level": False, "print_time": False, "verbose": False, "ipopt.max_iter": 100000}
opti.solver('ipopt', p_opts)

# try:
sol = opti.solve()
# except:
#     print("Please recheck Problem Formulation again")

print('Voltage', sol.value(Vq[:]))
print('Current', sol.value(Iqnq[:]))
print('Power_nq', sol.value(Pqnq[:]))
print('Power_q', sol.value(Pq[:]))
print('Power_gq', sol.value(Pgq[:]))

#---------------------------------------------------Node 4-------------------------------------------------------------#

# Lower bounds of the system components
Pgq_min  = 0
Pqnq_min = -5
Pq_min   = -5
Iqnq_min = -5
Vq_min   =  0.9

# Upper bounds of the system components
Pgq_max =  2
Pqnq_max =  5
Pq_max   =  5
Iqnq_max =  5
Vq_max   =  1.1


q = 4                   # Node 4
neighbours_of_node_q = [1, 0, 0, 1, 0]

sum_of_neighbours = int(sum(neighbours_of_node_q))
opti     = casadi.Opti()
Vq       = opti.variable(5)
Pgq      = opti.variable(5)
Pq       = opti.variable(5)
Pqnq     = opti.variable(total_nodes)
Iqnq     = opti.variable(total_nodes)
Iq = 0

#  Applying KCL at node q
for nq in range(total_nodes):
    # if neighbours_of_node_q[nq] == 1:
    Iq = Iq + G[q,nq]*Vq[nq]

# Defining the cost function

cost = alpha + beta * (P_load[q] + Pq[q]) \
       + gamma * (P_load[q] + Pq[q])*(P_load[q] + Pq[q])

opti.minimize(cost)

# Declaring all the equality constraints first
opti.subject_to(Pq[q] == Vq[q]*Iq)
opti.subject_to(Pgq[q] == P_load[q] + Pq[q])

for nq in range(total_nodes):
    if neighbours_of_node_q[nq] == 1:
        opti.subject_to(Iqnq[nq] == G[q,nq]*(Vq[nq]-Vq[q]))
        opti.subject_to(Pqnq[nq] == Vq[q]*Iqnq[nq])

# # Inequality constraints
# Pgq_min  =  0
# Pqnq_min = -5
# Pq_min   = -5
# Pgq[q] == P_load[q] + Pq[q]
# 0 == 0 + 0
opti.subject_to(Pgq[0] >= Pgq_min)
opti.subject_to(Pqnq[0] >= Pqnq_min)
opti.subject_to(Pq[0] >= Pq_min)
opti.subject_to(Iqnq[:] >= Iqnq_min)
opti.subject_to(Vq[:] >= Vq_min)
#
opti.subject_to(Pgq[0] <= Pgq_max)
opti.subject_to(Pqnq[0] <= Pqnq_max)
opti.subject_to(Pq[0] <= Pq_max)
opti.subject_to(Iqnq[:] <= Iqnq_max)
opti.subject_to(Vq[:] <= Vq_max)
opti.set_initial(Vq[:],1)
opti.set_initial(Pq[0],0)
opti.set_initial(Pqnq[0],0)

# Solver type and its parameters are defined here
p_opts = {"ipopt.print_level": False, "print_time": False, "verbose": False, "ipopt.max_iter": 100000}
opti.solver('ipopt', p_opts)

# try:
sol = opti.solve()
# except:
#     print("Please recheck Problem Formulation again")

print('Voltage', sol.value(Vq[:]))
print('Current', sol.value(Iqnq[:]))
print('Power_nq', sol.value(Pqnq[:]))
print('Power_q', sol.value(Pq[:]))
print('Power_gq', sol.value(Pgq[:]))


print('Endgame')
