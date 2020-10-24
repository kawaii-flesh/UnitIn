#include <iostream>
#include <ctime>
#include <cstdlib>
#include <cmath>

using namespace std;

//start_needed
class A
{
	int a;
	int b;
public:
    A(int aa, int ab) : a(aa), b(ab){}
    int sum(int);
};
//end_needed

/*m(A;A a = A(1,2);a.)
[A] - Class name
[A a = A(1,2)] - Initialization instance
[a.] - How to call a method
*/
//unitin:m(A;A a = A(1,2);a.):sum:ar
//2:5
//3:6
//-3:0
//end_cases
int A::sum(int n)
{
    return a + b + n;
}
//end_code

/*[//unitin] - key word
[f] - type(f - function, m - method)
[adder] - test function/method name
[or] - log type(or - only results, ar - arguments, results)
*/
//unitin:f:adder:ar
//1,2:3
//2,-1:1
//end_cases
int adder(const int a, const int b)
{
	return a + b;
}
//end_code

int main(int argc, char** argv)
{
	//start_needed
	unsigned int n;
	//end_needed
	cout << "Enter n: ";
	cin >> n;
	double *arr = new double[n];
	srand(time(NULL));
	for(int i = 0; i < n; ++i)
		arr[i] = (rand() % 100 / 100. + rand() % 100) * ((rand() % 2 == 0) ? 1 : -1); 
	cout << "Original array:\n";
	for(int i = 0; i < n; ++i)
		cout << arr[i] << " ";
	cout << "\n";
	
	double sum{};	
	for(int i = 0; i < n; ++i)
		if(arr[i] > 0)
			sum += arr[i];
	
	double min = abs(arr[0]), max = abs(arr[0]);
	int min_index = 0, max_index = 0;
	for(int i = 0; i < n; ++i)
	{
		if(abs(arr[i]) < min)
		{
			min = abs(arr[i]);
			min_index = i;
		}
		if(abs(arr[i]) > max)
		{
			max = abs(arr[i]);
			max_index = i;
		}
	}
	double prod = 1;
	if(abs(max_index - min_index) == 1)
		prod = 0;
	else if(min_index < max_index)
		for(int i = min_index + 1; i < max_index; ++i)
			prod *= arr[i];
	else
		for(int i = max_index + 1; i < min_index; ++i)
			prod *= arr[i];	
	cout << "Sum of positive elements: " << sum << "\n";
	cout << "The product of the elements: " << prod << "\n";
	for(int i = 0; i < n - 1; ++i)
	{
		if(arr[i] < arr[i + 1])
		{
			double b = arr[i];
			arr[i] = arr[i + 1];
			arr[i + 1] = b;
			i = -1;
		}
	}
	cout << "Sorted array:\n";
	for(int i = 0; i < n; ++i)
		cout << arr[i] << " ";
	cout << "\n";
	delete [] arr;
	return 0;
}
