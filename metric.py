"""
There we will calculate distance
"""

# TODO: metric:     move distance function to this file
# TODO: metric:     add at least 7 top metrics

"""
Metrics intended for real-valued vector spaces:

identifier	        class name	        args	        distance function
“euclidean”	        EuclideanDistance	                sqrt(sum((x - y)^2))
“manhattan”	        ManhattanDistance                   sum(|x - y|)
“chebyshev”	        ChebyshevDistance                   max(|x - y|)
“minkowski”	        MinkowskiDistance	p	            sum(|x - y|^p)^(1/p)
“wminkowski”	    WMinkowskiDistance	p, w	        sum(|w * (x - y)|^p)^(1/p)
“seuclidean”	    SEuclideanDistance	V	            sqrt(sum((x - y)^2 / V))
“mahalanobis”	    MahalanobisDistance	V or VI	        sqrt((x - y)' V^-1 (x - y))
"""