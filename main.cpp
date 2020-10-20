#include "unitin.hpp"
#include <iostream>
#include <any>
#include <string>

using namespace std;

bool pass_strong(string pass, string)
{
    bool result = true;
    if(pass.size() < 8)
        result &= false;
    if(pass.find("@") == string::npos)
        result &= false;
    return result;
}

bool wrapper_pass_strong(bool (*test_func)(string, string), pair<bool, vector<any>> one_case)
{
    return test_func(any_cast<const char *>(one_case.second[0]), any_cast<const char *>(one_case.second[1])) == one_case.first;
}

int main()
{
    vector<pair<bool, vector<any>>> cases
    {
        make_pair(false, vector<any>{"12345678", ""}),
        make_pair(false, vector<any>{"12345678", ""}),
        make_pair(false, vector<any>{"pass@", ""}),
        make_pair(true, vector<any>{"1@345678", ""})
    };
    UnitIn<bool, string, string> test(pass_strong, wrapper_pass_strong, cases);
    test.run_test();
    cout << (test.is_passed() ? "Passed!" : "Not passed!") << endl;
    return 0;
}
