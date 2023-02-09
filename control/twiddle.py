# twiddle.py
def twiddle(parameters, cost, tolerance=0.2):
    """ 
    This function generates a local set of best parameters from a cost function.
    @parameters     list of parameters to optimize
    @cost           cost function to minimize
    @tolerance      tolerance for the change in parameters
    returns         best set of parameters, cost from best set of parameters
    """
    parameters_change = [1] * len(parameters)
    best_error = cost(parameters)
    upper_guess = parameters
    lower_guess = parameters
    while sum(parameters_change) > tolerance:
        for count in len(parameters):
            upper_guess[count] = parameters[count] + parameters_change[count]
            lower_guess[count] = parameters[count] - parameters_change[count]
            upper_error = cost(upper_guess)
            lower_error = cost(lower_guess)
            if upper_error < best_error:
                best_error = upper_error
                parameters = upper_guess
                parameters_change[count] *= 1.1
            elif lower_error < best_error:
                best_error = lower_error
                parameters = lower_guess
                parameters_change[count] *= 1.1
            else:
                parameters_change[count] *= 0.9
            # reset guesses
            upper_guess = parameters
            lower_guess = parameters
    return parameters, cost(parameters)
