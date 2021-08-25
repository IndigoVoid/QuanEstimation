
"""Top-level package for quanestimation."""

from quanestimation import AsymptoticBound
# from quanestimation import Bayes
from quanestimation import Common
from quanestimation import Control
from quanestimation import Dynamics
from quanestimation import Resources

from quanestimation.AsymptoticBound import (CramerRao, Holevo, CFIM, LLD, QFIM, RLD, SLD, )
from quanestimation.Common import (common, dRHO, dydt, mat_vec_convert, suN_generator, )
from quanestimation.Control import (DDPG, DiffEvo, GRAPE, PSO, ddpg_actor, ddpg_critic, )
from quanestimation.Dynamics import (dynamics, learning_env, Lindblad,  env, )
from quanestimation.Resources import (Resources, )

# import julia
from julia import Main

Main.include('QuanEstimation/quanestimation/JuliaSrc/QuanEstimation.jl')

__all__ = ['AsymptoticBound', 'Common', 'Control', 'Dynamics', 'Resources',
            'CramerRao', 'Holevo', 'common', 'DDPG', 'DiffEvo',  'GRAPE', 'PSO', 'dynamics', 'learning_env', 'Resources',
            'DDPG', 'ddpg_actor', 'ddpg_critic', 'env', 'Lindblad',
            'CFIM', 'SLD', 'LLD', 'RLD', 'QFIM', 'dydt', 'dRHO', 'mat_vec_convert', 'suN_generator']
