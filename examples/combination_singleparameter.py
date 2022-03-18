import numpy as np
from quanestimation import *
import os

# initial state
rho0 = 0.5 * np.array([[1.0, 1.0], [1.0, 1.0]])
# Hamiltonian
omega0 = 1.0
sx = np.array([[0.0, 1.0], [1.0, 0.0]])
sy = np.array([[0.0, -1.0j], [1.0j, 0.0]])
sz = np.array([[1.0, 0.0], [0.0, -1.0]])
H0 = 0.5 * omega0 * sz
dH = [0.5 * sz]
Hc = [sx, sy, sz]
# dissipation
sp = np.array([[0.0, 1.0], [0.0, 0.0]])
sm = np.array([[0.0, 0.0], [1.0, 0.0]])
decay = [[sp, 0.0], [sm, 0.1]]
# dynamics
tspan = np.linspace(0.0, 20.0, 5000)
# initial control coefficients
cnum = tnum - 1
ctrl0 = [np.array([np.zeros(cnum), np.zeros(cnum), np.zeros(cnum)])]
ctrl_opt = ctrl0[0]
psi_opt = []

episodes = 5
for ei in range(episodes):
    # state optimization
    DE_paras = {
        "popsize": 10,
        "psi0": psi_opt,
        "max_episode": 1000,
        "c": 1.0,
        "cr": 0.5,
        "seed": 1234,
    }
    state = StateOpt(savefile=True, method="DE", **DE_paras)
    state.dynamics(
        tspan,
        H0,
        dH,
        Hc=Hc,
        ctrl=ctrl_opt,
        decay=decay,
    )
    state.QFIM(savefile=True)
    ####  load f and rename ####
    f_load = open("f.csv", "r")
    f_load = "".join([i for i in f_load])
    f_save = open("f_Sopt%d.csv" % ei, "w")
    f_save.writelines(f_load)
    f_save.close()

    s_load = open("states.csv", "r")
    s_load = "".join([i for i in s_load])
    s_save = open("states_Sopt%d.csv" % ei, "w")
    s_save.writelines(s_load)
    s_save.close()
    if os.path.exists("f.csv"):
        os.remove("f.csv")

    # control optimization
    psi_save = np.genfromtxt("states.csv", dtype=np.complex128)
    csv2npy_states(psi_save)
    psi_opt = np.load("states.npy")
    psi_opt = psi_opt.reshape(1, len(rho0))[0]
    rho_opt = np.dot(
        psi_opt.reshape(len(rho0), 1), psi_opt.reshape(1, len(rho0)).conj()
    )
    psi_opt = [psi_opt]

    DE_paras = {
        "popsize": 10,
        "ctrl0": ctrl0,
        "max_episode": 1000,
        "c": 1.0,
        "cr": 0.5,
        "seed": 1234,
    }
    control = ControlOpt(
        tspan,
        rho_opt,
        H0,
        dH,
        Hc,
        decay=decay,
        ctrl_bound=[-0.5, 0.5],
        savefile=True,
        method="DE",
        **DE_paras
    )
    control.QFIM()
    f_load = open("f.csv", "r")
    f_load = "".join([i for i in f_load])
    f_save = open("f_Copt%d.csv" % ei, "w")
    f_save.writelines(f_load)
    f_save.close()

    c_load = open("controls.csv", "r")
    c_load = "".join([i for i in c_load])
    c_save = open("controls_Copt%d.csv" % ei, "w")
    c_save.writelines(c_load)
    c_save.close()
    if os.path.exists("f.csv"):
        os.remove("f.csv")

    ctrl_save = np.genfromtxt("controls.csv")
    csv2npy_controls(ctrl_save, len(Hc))
    ctrl_opt = np.load("controls.npy")[0]
    ctrl_opt = [ctrl_opt[i] for i in range(len(Hc))]
    ctrl0 = [np.array(ctrl_opt)]

# # measurement optimization
psi_save = np.genfromtxt("states.csv", dtype=np.complex128)
csv2npy_states(psi_save)
psi_opt = np.load("states.npy")
rho_opt = np.dot(psi_opt.reshape(len(rho0), 1), psi_opt.reshape(1, len(rho0)).conj())

ctrl_save = np.genfromtxt("controls.csv")
csv2npy_controls(ctrl_save, len(Hc))
ctrl_opt = np.load("controls.npy")[0]

DE_paras = {
    "popsize": 10,
    "measurement0": [],
    "max_episode": 1000,
    "c": 1.0,
    "cr": 0.5,
    "seed": 1234,
}
m = MeasurementOpt(
    mtype="projection", minput=[], savefile=True, method="DE", **DE_paras
)
m.dynamics(tspan, rho_opt, H0, dH, Hc=Hc, ctrl=ctrl_opt, decay=decay)
m.CFIM(savefile=True)
