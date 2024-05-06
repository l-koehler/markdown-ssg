import sys, math, re

input_data = open(sys.argv[1]).read()
output_data = ""
output_file = sys.argv[2]

class State:
    # Never affected, decremented once per loop 
    skip_next = 0
    
    # Overriding all formatting
    escaping = False
    tag_stack = []
    first_list_entry = False
    
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
    if state.skip_next != 0:
        state.skip_next -= 1
        continue
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
            elif state.tag_stack[-1:] in [['ul'], ['ol']]:
                pass
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
            segment = ""
            while count and not skip:
                if count >= 2:
                    state.bold = not state.bold
                    if state.bold:
                        segment += "<b>"
                    else:
                        segment = "</b>" + segment
                    count -= 2
                else:
                    state.italics = not state.italics
                    if state.italics:
                        segment += "<i>"
                    else:
                        segment = "</i>" + segment
                    count -= 1
            output_data += segment

        case "[" if not (state.escaping or state.block_code):
            if input_data[char_i+1:].startswith('ul') or input_data[char_i+1:].startswith('ol'):
                state.skip_next += 2
                state.first_list_entry = True
                escaping = False
                if input_data[char_i+1:].startswith('ul'):
                    state.tag_stack.append('ul')
                else:
                    state.tag_stack.append('ol')
                segment = ""
                for char in input_data[char_i+4:]:
                    if char == "\\":
                        if escaping:
                            segment += char
                        escaping = not escaping
                    elif char == "]":
                        if escaping:
                            segment += char
                            escaping = not escaping
                        else:
                            break
                    else:
                        segment += char
                if input_data[char_i+1:].startswith('ul'):
                    output_data += "<ul>"
                else:
                    output_data += "<ol>"

        case '-' if state.tag_stack[-1:] == ["ul"] and not (state.escaping or state.block_code):
            if state.first_list_entry:
                output_data += "<li>"
                state.first_list_entry = False
            else:
                output_data += "</li><li>"

        case '#' if state.tag_stack[-1:] == ["ol"] and not (state.escaping or state.block_code):
            if state.first_list_entry:
                output_data += "<li>"
                state.first_list_entry = False
            else:
                output_data += "</li><li>"

        case ']' if not (state.escaping or state.block_code):
            # if the closing bracket is on its own line, discard one newline
            if input_data[char_i+1] == "\n":
                state.skip_next += 1
            if state.tag_stack[-1:] == ["ul"]:
                output_data += "</li></ul>"
                state.tag_stack.pop()
            elif state.tag_stack[-1:] == ["ol"]:
                output_data += "</li></ol>"
                state.tag_stack.pop()
            
        case _:
            output_data += char
open(output_file, 'w').write(output_data)