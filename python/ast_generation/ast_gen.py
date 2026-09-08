import argparse
import yaml
import ast_nodes

args = {}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str)
    global args
    args = parser.parse_args()

def parse_tokens(construct_list, token_list, python_file):
    node_idxes = {}
    i = 0
    while i < len(token_list):
        for construct in construct_list.keys():
            for pattern in construct_list[construct].keys():
                split_pattern = pattern.split(" ")
                match = False
                if token_list[i].split(" ")[0].strip() == split_pattern[0].strip():
                    match = True
                    for j in range(1, len(split_pattern)):
                        if(i + j < len(token_list) and token_list[i + j].split(" ")[0].strip() != split_pattern[j].strip()):
                            match = False

                if(match == False):
                    continue
                else:
                    print(f"token pattern match found: \n {pattern}")
                    token_segment = token_list[i:i + len(split_pattern)]
                    new_token = construct
                    #need to figure out how to add the relevant context part here
                    param_list = []
                    construct_params = construct_list[construct][pattern].split(",")
                    node_type = construct_params[0].split("(")[0] + "("
                    construct_params[0] = construct_params[0].split("(")[1]
                    if(node_type != "append("):
                        if node_type in node_idxes.keys():
                            node_idxes[node_type] += 1
                        else:
                            node_idxes[node_type] = 0
                        write_string = f"{node_type[:-5]}{node_idxes[node_type]} = {node_type}"
                        node_name = f"{node_type[:-5]}{node_idxes[node_type]}"
                    else:
                        write_string = "StatementList0.append("
                    for param in construct_params:
                        param, type = param.strip().strip(",").strip(")").strip("$").split(".")
                        # print(param)
                        # print(len(token_segment))
                        for j in range(0, len(token_segment)):
                            # print(token_segment[j])
                            token = token_segment[j]
                            if param == token.split("(")[0].strip():
                                if(len(param_list) > 0):
                                    write_string += ", "
                                if(type == "node"):
                                    write_string += token.split("(")[1].strip().strip(")")
                                elif(type == "value"):
                                    write_string += "\"" + token.split("(")[1].strip().strip(")") + "\""
                                else:
                                    print("Error: invalid type of parameter for semantic action")
                                param_list.append(token.split("(")[1].strip(")"))
                                token_segment.pop(j)
                                break
                    write_string += ")\n"
                    python_file.write(write_string)
                    new_token += f" ({node_name})"
                    token_list = token_list[:i] + [new_token + "\n"] + token_list[i + len(split_pattern):]
                    i = 0

        i += 1
    return token_list

def main():
    parse_args()
    construct_list = open("../parser_generation/tokens.yml", "r")
    construct_list = yaml.safe_load(construct_list)
    construct_list = construct_list["constructs"]
    token_file = open(args.input_file, "r")
    token_list = token_file.readlines()
    output_file = open("out.ast", "w")
    python_file = open("generated_ast.py", "w")
    python_file.write("from ast_nodes import *\n")
    python_file.write("StatementList0 = StatementListNode()\n")
    for construct in construct_list:
        curr_list = construct_list[construct].split("|")
        construct_list[construct] = {}
        for config in curr_list:
            print(config)
            key, code = config.split(";")
            key = key.strip()
            code = code.strip()
            construct_list[construct][key] = code

    print(construct_list)

    ast_list = parse_tokens(construct_list, token_list, python_file)
    output_file.writelines(ast_list)
    python_file.write("traversal = open(\"out.traversal\", \"w\")\n")
    python_file.write("StatementList0.print(traversal, 0)\n")
    token_file.close()
    output_file.close()
    python_file.close()


if __name__ == "__main__":
    main()