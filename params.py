class Params(object):
    def __init__(self, n, seed, lam, upper_bound, t_cs, alpha, t_slice, rr_add):
        self.n = int(n)
        self.seed = int(seed)
        self.lam = float(lam)
        self.upper_bound = int(upper_bound)
        self.t_cs = int(t_cs)
        self.alpha = float(alpha)
        self.t_slice = int(t_slice)
        self.rr_add = rr_add