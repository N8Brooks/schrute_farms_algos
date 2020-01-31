# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:45:16 2019

@author: Nathan
"""

class trie:
    """ trie node """
    def __init__(self):
        self.children = dict()
        self.isEndOfWord = False

def insert(root, key):
    """ insert into trie structure """
    for char in key:
        root = root.children.setdefault(char, trie())
    root.isEndOfWord = True

def search(root, key):
    """ parse tree looking for word """
    for char in key:
        if char in root.children:
            root = root.children[char]
        else:
            return False

    return root.isEndOfWord 
  
# driver function 
if __name__ == '__main__':   
    # Input keys (use only 'a' through 'z' and lower case) 
    keys = ["the","a","there","anaswe","any", 
            "by","theirxy"] 
    output = ["Not present in trie", 
              "Present in trie"] 
  
    # construct trie
    t = trie() 
    for key in keys: 
        insert(t, key)
  
    # Search for different keys 
    print("{} ---- {}".format("the",output[search(t, "the")])) 
    print("{} ---- {}".format("these",output[search(t, "these")])) 
    print("{} ---- {}".format("theirx",output[search(t, "theirx")])) 
    print("{} ---- {}".format("thaw",output[search(t, "thaw")])) 
  
