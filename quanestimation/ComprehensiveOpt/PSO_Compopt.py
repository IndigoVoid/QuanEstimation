from julia import Main
import quanestimation.ComprehensiveOpt.ComprehensiveStruct as Comp


class PSO_Compopt(Comp.ComprehensiveSystem):
    """
    Attributes
    ----------
    > **savefile:** `bool`
        -- Whether or not to save all the optimized variables (probe states, 
        control coefficients and measurements).  
        If set `True` then the optimized variables and the values of the 
        objective function obtained in all episodes will be saved during 
        the training. If set `False` the optimized variables in the final 
        episode and the values of the objective function in all episodes 
        will be saved.

    > **particle_num:** `int`
        -- The number of particles.

    > **psi0:** `list of arrays`
        -- Initial guesses of states.

    > **ctrl0:** `list of arrays`
        -- Initial guesses of control coefficients.

    > **measurement0:** `list of arrays`
        -- Initial guesses of measurements.

    > **max_episode:** `int or list`
        -- If it is an integer, for example max_episode=1000, it means the 
        program will continuously run 1000 episodes. However, if it is an
        array, for example max_episode=[1000,100], the program will run 
        1000 episodes in total but replace states of all  the particles 
        with global best every 100 episodes.
  
    > **c0:** `float`
        -- The damping factor that assists convergence, also known as inertia weight.

    > **c1:** `float`
        -- The exploitation weight that attracts the particle to its best previous 
        position, also known as cognitive learning factor.

    > **c2:** `float`
        -- The exploitation weight that attracts the particle to the best position  
        in the neighborhood, also known as social learning factor.

    > **seed:** `int`
        -- Random seed.

    > **eps:** `float`
        -- Machine epsilon.
    """

    def __init__(
        self,
        savefile=False,
        particle_num=10,
        psi0=[],
        ctrl0=[],
        measurement0=[],
        max_episode=[1000, 100],
        c0=1.0,
        c1=2.0,
        c2=2.0,
        seed=1234,
        eps=1e-8,
    ):

        Comp.ComprehensiveSystem.__init__(
            self, savefile, psi0, ctrl0, measurement0, seed, eps
        )

        self.p_num = particle_num
        self.max_episode = max_episode
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2
        self.seed = seed

        ini_particle = (self.psi0, self.ctrl0)
        self.alg = Main.QuanEstimation.PSO(
            self.max_episode,
            self.p_num,
            ini_particle,
            self.c0,
            self.c1,
            self.c2,
            self.seed,
        )

    def SC(self, W=[], M=[], target="QFIM", LDtype="SLD"):
        """
        Comprehensive optimization of the probe state and control (SC).

        Parameters
        ----------
        > **W:** `matrix`
            -- Weight matrix.

        > **M:** `list of matrices`
            -- A set of positive operator-valued measure (POVM). The default measurement 
            is a set of rank-one symmetric informationally complete POVM (SIC-POVM).

        > **target:** `string`
            -- Objective functions for searching the minimum time to reach the given 
            value of the objective function. Options are:  
            "QFIM" (default) -- choose QFI (QFIM) as the objective function.  
            "CFIM" -- choose CFI (CFIM) as the objective function.  
            "HCRB" -- choose HCRB as the objective function.  

        > **LDtype:** `string`
            -- Types of QFI (QFIM) can be set as the objective function. Options are:  
            "SLD" (default) -- QFI (QFIM) based on symmetric logarithmic derivative (SLD).  
            "RLD" -- QFI (QFIM) based on right logarithmic derivative (RLD).  
            "LLD" -- QFI (QFIM) based on left logarithmic derivative (LLD). 

        **Note:** 
            SIC-POVM is calculated by the Weyl-Heisenberg covariant SIC-POVM fiducial state 
            which can be downloaded from [http://www.physics.umb.edu/Research/QBism/solutions.html
            ](http://www.physics.umb.edu/Research/QBism/solutions.html).
        """

        super().SC(W, M, target, LDtype)

    def CM(self, rho0, W=[]):
        """
        Comprehensive optimization of the control and measurement (CM).

        Parameters
        ----------
        > **rho0:** `matrix`
            -- Initial state (density matrix).

        > **W:** `matrix`
            -- Weight matrix.
        """

        super().CM(rho0, W)

    def SM(self, W=[]):
        """
        Comprehensive optimization of the probe state and measurement (SM).

        Parameters
        ----------
        > **W:** `matrix`
            -- Weight matrix.
        """

        super().SM(W)

    def SCM(self, W=[]):
        """
        Comprehensive optimization of the probe state, the control and measurements (SCM).

        Parameters
        ----------
        > **W:** `matrix`
            -- Weight matrix.
        """

        super().SCM(W)
