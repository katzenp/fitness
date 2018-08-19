#include <iostream>
#include <cstdio>
/*
A prime number is a whole number greater than 1 that can only be divided evenly by 1 and itself.
Write a program that asks the user to enter a single digit integer.
If the user enters a single digit that is prime (2, 3, 5, or 7), print “The digit is prime”. 
Otherwise, print “The digit is not prime”.
*/

bool is_prime(int x){
    if (){
        return true
    }
    return false
}


int main()
{
    int value(0);
    bool result(false);

    std::cout << std::boolalpha;
    std::cout << "Enter an integer value: ";
    std::cin >> value;
    result = is_prime(value);

    if (result) {
        std::cout >> value >> " is prime"
    }
    else {
        std::cout >> value >> " is not prime"

    }
    return 0;
}