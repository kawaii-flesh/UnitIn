#include <vector>
#include <utility>
#include <any>
#include <iostream>

using namespace std;

// RT - tested function return type
// TFVT - tested function args type
template <typename RT, typename ... TFVT>
class UnitIn
{
private:
    RT (*m_func)(TFVT ...); // tested function
    bool (*m_wrapper)(RT (*)(TFVT ...), pair<RT, vector<any>>); // test fuction(wrapper)
    vector<pair<RT, vector<any>>> m_cases; // cases(expected value, args ...)
    bool m_passed; // test result
    string m_test_name;
public:
    // Passed to the constructor:
    // a_func - tested function(pointer)
    // a_wrapper - wrapper function(pointer)
    // the type of wrapper must be:
    // bool (*)(TF type, pair<TF return type, vector<any>) TF - test function
    explicit UnitIn(RT (*a_func)(TFVT ...), bool (*a_wrapper)(RT (*)(TFVT ...), pair<RT, vector<any>>), vector<pair<RT, vector<any>>> &a_cases, string &&a_test_name = "UnitIn") :
        m_func(a_func), m_wrapper(a_wrapper), m_cases(a_cases), m_passed(false), m_test_name(a_test_name){}
    vector<pair<bool, pair<RT, vector<any>>>> run_test(bool = false);
    vector<pair<RT, vector<any>>> &get_cases(){return m_cases;}
    bool is_passed(){return m_passed;}
};

template <typename RT, typename ... TFVT>
vector<pair<bool, pair<RT, vector<any>>>> UnitIn<RT, TFVT ...>::run_test(bool cout_log)
{
    m_passed = true;
    vector<pair<bool, pair<RT, vector<any>>>> tests;
    if(cout_log)
        cout << m_test_name << "\n";
    for(int i = 0; i < m_cases.size(); ++i)
    {
        bool result = m_wrapper(m_func, m_cases[i]);
        m_passed &= result;
        tests.push_back(make_pair(result, m_cases[i]));        
		if(cout_log)
            cout << "Test [" << i << "] - " << (result ? "Good!\n" : "Bad!\n");
    }
    if(cout_log)
        cout << m_test_name << (m_passed ? " - Passed!\n" : " - Failed!\n");
    return tests;
}
