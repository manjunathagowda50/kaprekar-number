def kaprekarRec(n, prev):
    if(n==0):
        return 0
    else:
        for i in range(100):
            prev=n
            digits = [0] * 4  
            for j in range(4): 
                digits[j] = n % 10 
                n = int(n / 10)   
            digits.sort()
            asc = 0;  
            for k in range(4): 
                asc = asc * 10 + digits[k]
            digits.sort()  
            desc = 0  
            for m in range(3, -1, -1): 
                desc = desc * 10 + digits[m]    
            diff = abs(asc - desc)  
            print(f"ascending order is {asc}, desceding order is {desc} and difference is {diff}")
            n=diff
            if (diff == prev):
                print(f"number of iterations is {i}")
                break
            else:
                continue

def kaprekar(n):  
    rev = 0  
    return kaprekarRec(n, rev)  
x=int(input("enter a number "))
kaprekar(x)
