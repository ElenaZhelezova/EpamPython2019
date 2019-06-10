from functools import reduce


#problem_6
square_sum_difference = sum([i for i in range(101)])**2 - sum([i**2 for i in range(101)])


#problem 9
product_pythagorean_triplet = list(map(lambda j: j[0]*j[1]*(1000-j[0]-j[1]),
                                       filter(lambda i: i[0]**2+i[1]**2 == (1000-i[0]-i[1])**2,
                                              [[a, b] for a in range(1, 1000) for b in range(a+1, 1000)])))[0]


#problem 40
product_digits = reduce(lambda x, y: x*y, [int((''.join([str(i) for i in range(2*10**5)]))[10**j]) for j in range(7)])


#problem 48
last_ten_digits = str(sum([i**i for i in range(1, 1001)]))[-10:]
