from typing import List,Counter
from collections import Counter
words_list:List[str]=["abc","abc", "abc", "bba","bba", "ccc"]
words_list_counter=Counter(words_list)

print(words_list_counter)

duplicates_list: List[str]= [ string for string in words_list_counter if words_list_counter.get(string)>1]
print(f"Duplicate List: {duplicates_list}")
