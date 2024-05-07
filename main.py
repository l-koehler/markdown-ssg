import sys, math

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

    def allow_inline(self):
        return not (self.escaping | self.block_math | self.block_code | self.inline_code)

class Deps:
    highlight = False
    mathjax = False

state = State()
deps = Deps()

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
        case "*" if state.allow_inline():
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

        case "[" if state.allow_inline():
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
            if input_data[char_i+1] == "\n" and state.tag_stack[-1:] in [["ul"],["ol"]]:
                state.skip_next += 1
            if state.tag_stack[-1:] == ["ul"]:
                output_data += "</li></ul>"
                state.tag_stack.pop()
            elif state.tag_stack[-1:] == ["ol"]:
                output_data += "</li></ol>"
                state.tag_stack.pop()
            else:
                output_data += "]"
        case '=' if state.allow_inline():
            if input_data[char_i-1] == '=':
                pass
            elif input_data[char_i+1] != '=':
                output_data += "="
            elif state.highlight:
                output_data += "</span>"
                state.highlight = False
            else:
                output_data += "<span style=\"background-color:yellow;\">"
                state.highlight = True
        case '~' if state.allow_inline():
            if input_data[char_i-1] == '~':
                pass
            elif input_data[char_i+1] != '~':
                output_data += '~'
            elif state.strike:
                output_data += "</s>"
                state.strike = False
            else:
                output_data += "<s>"
                state.strike = True
        case '`' if not state.escaping:
            # if not the first, quit
            if input_data[char_i-1] == '`':
                pass
            else:
                count = 1
                while input_data[char_i+count] == '`':
                    count += 1
                if count >= 3:
                    state.block_code = not state.block_code
                    if state.block_code:
                        # get the language to use (might be none)
                        lang = ""
                        i = 0
                        while input_data[char_i+i] not in [' ', '\n', '\\']:
                            l_char = input_data[char_i+i]
                            if l_char != "`":
                                lang += l_char
                            i += 1
                        state.skip_next += len(lang) + count
                        if lang == "":
                            lang = "plaintext"
                        output_data += f"<pre><code class=\"language-{lang}\">"
                        deps.highlight = True
                    else:
                        output_data += "</code></pre>"
                elif not state.block_code:
                    state.inline_code = not state.inline_code
                    if state.inline_code:
                        output_data += "<code>"
                    else:
                        output_data += "</code>"
        case "_" if state.allow_inline():
            state.subscript = not state.subscript
            if state.subscript:
                output_data += "<sub>"
            else:
                output_data += "</sub>"
        case "^" if state.allow_inline():
            state.superscript = not state.superscript
            if state.superscript:
                output_data += "<sup>"
            else:
                output_data += "</sup>"
        case _:
            state.escaping = False
            output_data += char
# add javascript dependencies
if deps.highlight:
    output_data = "<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/default.min.css\"><script src=\"https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js\"></script><script>hljs.highlightAll();</script>" + output_data

open(output_file, 'w').write(output_data)
