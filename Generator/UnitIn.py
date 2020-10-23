#!/usr/bin/python3

import sys

def generate_test(test_type, func_name, cases, code):
    test = []
    func_rt = code[0][:code[0].find(func_name)] # return type
    func_at = code[0][code[0].find(func_name + '(') + len(func_name + '('):code[0].rfind(')')] # types and names
    func_at_l = [] # only types
    for i in func_at.split(','):
        if i.count(' ') == 0:
            func_at_l += [i]
        else:
            func_at_l += [i[:i.rfind(' ')]]
    cases_l = ["    vector<pair<" + func_rt[:-1] + ", vector<any>>> cases_" + func_name + '\n    {\n']
    for i in cases:
        cases_l += ["        make_pair(" + i[i.rfind(':') + 1: -1] + ", vector<any>{" + i[:i.rfind(':')] + "}),\n"]
    cases_l[-1] = (cases_l[-1][:-2] + "\n    };\n\n")
    wrapper = []
    wrapper += ["    bool result = true;\n    int j = 0;\n"]
    wrapper += ["    for(pair<" + func_rt[:-1] + ", vector<any>> i : cases_" + func_name + ")\n    {\n"]
    wrapper += ["        " + func_rt + " ret = "]
    wrapper += [func_name + "(\n"]
    for j in range(0, len(func_at_l)):
        wrapper += ["            any_cast<" + func_at_l[j] + ">(i.second[" + str(j) + "]),\n"]
    wrapper[-1] = wrapper[-1][:-2] + ");\n"
    wrapper += ["        result &= ret == i.first;\n"]
    bstr = ""
    for j in range(0, len(func_at_l)):
        bstr += "any_cast<" + func_at_l[j] + ">(i.second[" + str(j) + "]) << " + '", " << '
    bstr = bstr[:-8]
    cstr = ""
    wrapper += ['        cout << "Test [" << j << "]: (" << ' + bstr + '") -> " << i.first << " actually = " << ret << " - " << (result ? "Good!" : "Bad!") << endl;\n']
    wrapper += ["        ++j;\n    }\n"]
    wrapper += ['\n    cout << "' + func_rt + func_name + '(' + func_at + ')" << (result ? " - Passed!" : " - Failed!") << endl;\n\n']
    return [cases_l, wrapper]

if len(sys.argv) < 2:
    print("unitin [source_file]")
    exit(1)

source = open(sys.argv[1], "r")

headers = ["#include <vector>\n", "#include <any>\n", "#include <utility>\n"]
namespaces = ["using namespace std;\n"]
lines = source.readlines()
needed = []

i = 0
while i < len(lines):
    if "#include" in lines[i]:
        headers += [lines[i]]
    elif "using namespace" in lines[i]:
        namespaces += [lines[i]]
    if "//start_needed" in lines[i]:
        i += 1
        while not ("//end_needed" in lines[i]):
            needed += [lines[i]]
            i += 1
        needed += ["\n"]
        i += 1
    if "//unitin:" in lines[i]:
        test_type = lines[i][lines[i].find(':') + 1:lines[i].rfind(':')]
        func_name = lines[i][lines[i].rfind(':') + 1:len(lines[i]) - 1]
        cases = []
        code = []
        i += 1
        while not ("//end_cases" in lines[i]):
            cases += [lines[i][2:]]
            i += 1
        i += 1
        file_line = i + 1
        while not ("//end_code" in lines[i]):
            code += [lines[i]]
            i += 1
        b = generate_test(test_type, func_name, cases, code)
    i += 1

headers = list(set(headers))
output_file_data = headers + ["\n"]
namespaces = list(set(namespaces))
output_file_data += namespaces + ["\n"]
output_file_data += needed
output_file_data += code + ["\n"]
output_file_data += ["int main(int argc, char *argv[])\n{\n"] + b[0] + b[1] + ["    return 0;\n}\n"]

file_out = open("ut_" + func_name + "_" + str(file_line) + "_" + sys.argv[1] + ".cpp", 'w')
file_out.writelines(output_file_data)
