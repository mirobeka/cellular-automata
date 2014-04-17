class Objective(object):
    """This is just abstract class to be extended. Extend this class for your
    objective that should be optimized.
    """

    def error_function(self, pattern, lattice):
        """ error funtion compare given latice with desired pattern and returns
        scalar value describing difference between those 2 lattices

        This method should be implemented to reflect objective that should be
        optimized.

        For example, if I want to optimized structure and topology of cellular
        automata(CA), in this function should be compared resulting lattice
        and  defined pattern and thid comparison reflected by scalar value.

        In other case, I we want to optimise structure and also states of CA
         se should compare states and structure and then sum this error and
         return scalar value
        """
        raise NotImplementedError("error function not implemented")

    def objective_function(self, vector):
        """ Objective funtion is main function that is minimized by cma-es
        algorithm. In our case, we are optimizing weights of neural network,
        but we can optimize anything we want.

        On the input of objective_function is optimized vector of values. On
        the output of objective_function must be scalar value that is minimized.


        This method should be implemented in a way that suits your
        optimalization needs.
        """
        raise NotImplementedError("method objective_function not implemented")

