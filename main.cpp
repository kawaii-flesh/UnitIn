#include "unitin.hpp"
#include <iostream>
#include <any>
#include <string>

using namespace std;

bool pass_strong(string pass, string wrong)
{
    bool result = true;
    if(pass.size() < 8)
        result &= false;
    if(pass.find("@") == string::npos)
        result &= false;
    if(pass == wrong)
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
        make_pair(false, vector<any>{"12345678", "qwerty123"}),
        make_pair(false, vector<any>{"12345678", "qwerty123"}),
        make_pair(false, vector<any>{"pass@", "qwerty123"}),
        make_pair(true, vector<any>{"1@345678", "qwerty123"}),
        make_pair(true, vector<any>{"qwerty123", "qwerty123"}) // wrong
    };
    UnitIn<bool, string, string> test(pass_strong, wrapper_pass_strong, cases, "bool pass_strong(string, string): main.cpp");
    test.run_test(true);
    return 0;
}
