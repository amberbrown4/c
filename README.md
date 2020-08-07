# Cache-Simulator

A cache simulator written in Python

Parameters that you can adjust:
  • Total cache size
  • Block size
  • Unified vs. split I- and D-caches (Von Neumann. vs. Harvard)
  • Associativity
  • Write back vs. write through
  • Write allocate vs. write no-allocate
Output:
  • Number of instruction references
  • Number of data references
  • Number of instruction misses
  • Number of data misses
  • Number of words fetched from memory
  • Number of words copied back to memory
  
The reference number specifies what type of memory reference is being performed with the following encoding:
  0 Data load reference
  1 Data store reference
  2 Instruction load reference
  
Input format:
 https://github.com/zahrasalarian/Cache-Simulator/blob/master/Input_format.PNG
 
To see more examples check https://github.com/zahrasalarian/Cache-Simulator/tree/master/PubliclyAvailableTestCases/traces.
