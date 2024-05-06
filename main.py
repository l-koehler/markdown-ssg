import sys, math

input_data = open(sys.argv[1]).read()
output_data = ""
output_file = sys.argv[2]

class State:
    # Overriding all formatting
    escaping = False
    
    # Overriding all inline formatting
    block_math = False
    block_code = False
    
    # Overriding other inline formatting
    inline_code = False
    
    # Inline formatting
    italics = False
    bold = False
    strike = False
    highlight = False
    superscript = False
    subscript = False

state = State()
# used for parsing only, not relevant to the output
# set at runtime, dont change
indent_size = 0

for char_i in range(len(input_data)):
    is_last  = (char_i == len(input_data)-1)
    is_first = (char_i == 0)
    char = input_data[char_i]
    match char:
        case "\\":
            if state.escaping:
                output_data += "\\"
            state.escaping = not state.escaping
        case "\n":
            if state.block_code:
                output_data += "\n"
            elif state.escaping:
                state.escaping = False
            else:
                output_data += "<br>"
        case "*" if not state.escaping or state.block_code:
            # only ever process the first occurence,
            # skip other occurences
            skip = False
            if not is_first and input_data[char_i-1] == '*':
                skip = True
            count = 1
            while len(input_data) > (char_i+count) and not skip:
                if input_data[char_i+count] == '*':
                    count += 1
                else:
                    break
            while count and not skip:
                if count >= 2:
                    state.bold = not state.bold
                    if state.bold:
                        output_data += "<b>"
                    else:
                        output_data += "</b>"
                    count -= 2
                else:
                    state.italics = not state.italics
                    if state.italics:
                        output_data += "<i>"
                    else:
                        output_data += "</i>"
                    count -= 1
        case "-":
            # -1: not a list
            nesting_level = -1
            preceding = 1
            
            # totally sane and comprehensible algorithm :D
            while len(input_data) > (char_i + preceding) and nesting_level == -1:
                prev = input_data[char_i-preceding]
                if prev not in [' ', '\n']:
                    break
                else:
                    if prev == '\n':
                        nesting_level = 0
                    else:
                        preceding += 1
            if nesting_level != 0:
                # not a list
                output_data += "-"
            else:
                # nesting_level is one and currently inaccurate
                preceding -= 1 # remove the newline
                if preceding == 0:
                    nesting_level = 0
                elif indent_size == 0:
                    indent_size = preceding
                    nesting_level = 1
                else:
                    nesting_level = math.ceil(preceding / indent_size)
                # at this point, nesting level is accurate and zero-indexed
        case _:
            output_data += char

open(output_file, 'w').write(output_data)