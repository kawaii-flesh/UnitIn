#!/usr/bin/python3

import sys

def generate_test(test_type, func_name, cases, code, log_type):
    m_op = []
    if "m" in test_type:
        m_op = test_type[test_type.find('(')+1:test_type.rfind(')')].split(';')
        class_name = m_op[0] + "::"

    func_rt = code[0][:code[0].find(class_name + func_name if "m" in test_type else func_name)] # return type
    func_at = code[0][code[0].find(class_name + func_name if "m" in test_type else func_name + '(')
        + len(class_name + func_name if "m" in test_type else func_name)+1:code[0].rfind(')')] # types and names
    func_at_l = [] # only types
    for i in func_at.split(','):
        if i.count(' ') == 0:
            func_at_l += [i]
        else:
            func_at_l += [i[:i.rfind(' ')]]
    cases_l = ["    std::vector<std::pair<" + func_rt[:-1] + ", std::vector<std::any>>> cases_" + func_name + '\n    {\n']
    for i in cases:
        cases_l += ["        std::make_pair(" + i[i.rfind(':') + 1: -1] + ", std::vector<std::any>{" + i[:i.rfind(':')] + "}),\n"]
    if len(cases) == 0:
        cases_l[-1] = cases_l[-1][:-1] + "};\n"
    else:
        cases_l[-1] = (cases_l[-1][:-2] + "\n    };\n\n")
    wrapper = ['\n    std::cout << "Start test: ' + func_rt + (class_name + func_name if "m" in test_type else func_name) + '(' + func_at + ')" << std::endl;\n']
    wrapper += ["    bool result = true;\n    int j = 0;\n"]
    if "m" in test_type:
        wrapper += ["    " + m_op[1] + ";\n"]
    wrapper += ["    for(std::pair<" + func_rt[:-1] + ", std::vector<std::any>> i : cases_" + func_name + ")\n    {\n"]
    wrapper += ["        " + func_rt + " ret = "]    
    wrapper += [m_op[2] + func_name + "(" if "m" in test_type else "" + func_name + "("]
    for j in range(0, len(func_at_l)):        
        if func_at_l[j].isspace() or func_at_l[j] == "":
            if len(func_at_l) == 1:
                wrapper += ["("]
                break
            continue
        wrapper += ["            std::any_cast<" + func_at_l[j] + ">(i.second[" + str(j) + "]),\n"]
    wrapper[-1] = wrapper[-1][:-2] + ");\n"
    wrapper += ["        result &= ret == i.first;\n"]
    bstr = ""
    for j in range(0, len(func_at_l)):
        bstr += "std::any_cast<" + func_at_l[j] + ">(i.second[" + str(j) + "]) << " + '", " << '
    bstr = bstr[:-8]
    cstr = ""
    if("or" in log_type):
        wrapper += ['        std::cout << "Test [" << j << "]: - " << (result ? "Good!" : "Bad!") << std::endl;\n']
    else:
        wrapper += ['        std::cout << "Test [" << j << "]: (" << ' + bstr + '") -> " << i.first << " actually = " << ret << " - " << (result ? "Good!" : "Bad!") << std::endl;\n']
    wrapper += ["        ++j;\n    }\n"]
    wrapper += ['\n    std::cout << "' + func_rt + (class_name + func_name if "m" in test_type else func_name) + '(' + func_at + ')" << (result ? " - Passed!" : " - Failed!") << std::endl;\n\n']
    return [cases_l, wrapper]

if len(sys.argv) < 2:
    print("unitin [source_file]")
    exit(1)

source = open(sys.argv[1], "r")

headers = ["#include <vector>\n", "#include <any>\n", "#include <utility>\n"]
namespaces = []
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
        options = lines[i].split(':')
        test_type = options[1]
        func_name = options[2]
        log_type = options[3]
        
        cases = []
        code = []
        i += 1
        while not ("//end_cases" in lines[i]):
            cases += [lines[i][2:]]
            i += 1
        i += 1
        while not ("//end_code" in lines[i]):
            code += [lines[i]]
            i += 1
        b = generate_test(test_type, func_name, cases, code, log_type)
        
        headers = list(set(headers))
        output_file_data = headers + ["\n"]
        namespaces = list(set(namespaces))
        output_file_data += namespaces + ["\n"]
        output_file_data += needed
        output_file_data += code + ["\n"]
        output_file_data += ["int main(int argc, char *argv[])\n{\n"] + b[0] + b[1] + ["    return 0;\n}\n"]

        file_out = open("ut_" + func_name + "_" + sys.argv[1] + "_.cpp", 'w')
        file_out.writelines(output_file_data)
    i += 1
    
    
