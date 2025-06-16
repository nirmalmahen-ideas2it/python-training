import re
def manipulate_str(input_str:str):
    if len(input_str)<3:
        print(input_str)
    else:
       if input_str.endswith("ing"):
           print(input_str+"ly")
       else:
            print(input_str+"ing")

manipulate_str("continue")
manipulate_str("continuing")
        