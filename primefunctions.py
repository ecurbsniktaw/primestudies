import pandas as pd

#----------------------------------------------------------------
# is_prime
#	Given an integer n, return True if n is prime, else False.
#
def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# end: is_prime
#----------------------------------------------------------------

#----------------------------------------------------------------
def prime_factors(n, unique=False):
    """
    Return the prime factors of n.
    
    Parameters:
        n (int): The integer to factorize.
        unique (bool): If True, return only unique prime factors.
                       If False (default), include repeated factors.
    """
    if n < 2:
        return []
    
    factors = []
    
    # Handle 2 separately
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Check odd numbers up to sqrt(n)
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2

    # If n is still > 2, it's a prime
    if n > 2:
        factors.append(n)

    return sorted(set(factors)) if unique else factors
#----------------------------------------------------------------

#----------------------------------------------------------------
def df_factors(low, high, small=False):
#
# Accumulate data for a range of integers:
#   Number of factors
#   Number of unique factors
#   List of factors
#   List of unique factors
#
    records = []
    if low == 1:
        i = 2
    else:
        i = low
    while i <= high:
        facs    = prime_factors(i, unique=False)
        fnumber = len(facs)
        ufacs   = sorted(set(facs))
        unumber = len(ufacs)
        smfac   = min(facs)
        lgfac   = max(facs)

        if small:
            records.append({
                "N": i,
                "# Factors": fnumber
            })

        else:
            records.append({
                "N": i,
                "# Factors": fnumber,
                "# Unique": unumber,
                "small fac": smfac,
                "large fac": lgfac,
                "Factors": facs,
                "Unique": ufacs
            })

        i = i + 1

    df = pd.DataFrame(records)
    return df
#----------------------------------------------------------------

