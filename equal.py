def Solution(str1,str2):
   for char in list(str1):
      if char in list(str2):
         return True
      else:
         return False
print(Solution("mareczek", "mzerkec"))
