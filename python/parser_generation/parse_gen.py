import yaml
import argparse

args = {}
state_list = {}

class state:
    next_states = {} # dictionary will convert keys into next_states
    end_state = False # will lowk need to override this for some of them
    name = ""
    store_data = False
    loop = False

    def __init__(self, name, store_data, end_state=False):
        self.name = name
        self.end_state = end_state
        self.next_states = {}
        self.store_data = store_data
        self.loop = False

    def __str__(self):
            return f"{self.name} \n {self.next_states} \nend_state: {self.end_state}, store_data = {self.store_data}\n"

    def add_next_state(self, char_class, next_state_name):
        self.next_states[char_class] = next_state_name

    def set_end_state(self):
        self.end_state = True

    def set_loop(self):
        self.loop = True

    __repr__ = __str__


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str)
    global args
    args = parser.parse_args()

def gen_dfa(token_name, regex):
    global state_list
    print(regex)
    stage = 0
    prev_state_name = "start"
    while len(regex) > 0:
        char_class_len = 1
        if(regex[0] != '['):
            char_class = regex[0]
            store_data = False
        else:
            while(regex[char_class_len] != ']'):
                char_class_len += 1
            char_class_len += 1
            char_class = regex[:char_class_len]
            store_data = True
        regex = regex[char_class_len:]
        state_list[prev_state_name].add_next_state(char_class, f"{token_name}[{stage}]")
        state_list[f"{token_name}[{stage}]"] = state(f"{token_name}[{stage}]", store_data)
        if(len(regex) > 0):
            if(regex[0] == '+'):
                # state_list[prev_state_name].set_end_state()
                state_list[f"{token_name}[{stage}]"].add_next_state(char_class, f"{token_name}[{stage}]")
                state_list[f"{token_name}[{stage}]"].set_loop()
                regex = regex[1:]
            elif(regex[0] == '*'):
                state_list[prev_state_name].set_end_state()
                state_list[f"{token_name}[{stage}]"].add_next_state(char_class, f"{token_name}[{stage}]")
                state_list[f"{token_name}[{stage}]"].set_loop()
                regex = regex[1:]
        prev_state_name = f"{token_name}[{stage}]"
        stage += 1
    state_list[prev_state_name].set_end_state()

def parse_tokens():
    input_file = open(args.input_file, "r")
    output_file = open("out.tokens", "w")
    curr_state = "start"
    character = input_file.read(1)
    stored_token = ""
    while(character):
        print(character)
        if character in state_list[curr_state].next_states.keys():
            curr_state = state_list[curr_state].next_states[character]
            stored_token += character
        elif character in (" ", "\n", "\t"):
            if(state_list[curr_state].end_state == True):
                if(state_list[curr_state].store_data == True):
                    output_file.write(f"{curr_state[:-3]} ({stored_token})\n")
                else:
                    output_file.write(f"{curr_state[:-3]}\n")
                curr_state = "start"
                stored_token = ""
            character = input_file.read(1)
            continue
        else:
            in_range = False
            for key in state_list[curr_state].next_states.keys():
                if key[0] != "[":
                    continue
                i = 1
                while i < len(key) - 1:
                    range_start = key[i]
                    if(key[i + 1] == '-'):
                        range_end = key[i + 2]
                        next_i = i + 3
                    else:
                        range_end = key[i]
                        next_i = i + 1
                    if ord(character) >= ord(range_start) and ord(character) <= ord(range_end):
                        in_range = True
                    i = next_i
                if(in_range):
                    curr_state = state_list[curr_state].next_states[key]
                    stored_token += character
                    break
            #none found - kill loop and double check
            if(in_range):
                character = input_file.read(1)
                continue
            if(state_list[curr_state].end_state == True):
                print(state_list[curr_state].next_states.keys())
                if(state_list[curr_state].store_data == True):
                    output_file.write(f"{curr_state[:-3]} ({stored_token})\n")
                else:
                    output_file.write(f"{curr_state[:-3]}\n")
                curr_state = "start"
                stored_token = ""
                if character in state_list[curr_state].next_states.keys():
                    curr_state = state_list[curr_state].next_states[character]
                    stored_token += character
                else:
                    print("ERROR")
            else:
                print("ERROR")

        if state_list[curr_state].end_state == True and state_list[curr_state].loop == False:
            print(state_list[curr_state].next_states.keys())
            if(state_list[curr_state].store_data == True):
                output_file.write(f"{curr_state[:-3]} ({stored_token})\n")
            else:
                output_file.write(f"{curr_state[:-3]}\n")
            curr_state = "start"
            stored_token = ""

        character = input_file.read(1)

    input_file.close()
    output_file.close()


def main():
    token_yaml = open("tokens.yml", "r")
    token_yaml = yaml.safe_load(token_yaml)
    # now the goofy ahh part to generate automata
    # idea 1 (dumb) do the 608 combinatorial approach of iterate every single path
    # idea 2 (less dumb) - separate out individual next states and then groups
    # shit will also need some way to parse the regex part as well
    # could parse each regex and create an automata for that then merge them later on
    token_list = token_yaml["tokens"]
    state_list["start"] = state("start", False)
    for key in token_list.keys():
        gen_dfa(key, token_list[key])

    print(state_list)
    parse_args()
    parse_tokens()


if __name__ == "__main__":
    main()