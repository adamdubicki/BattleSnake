#About Code Style
 - We will use tabs instead of spaces. Easier for debugging.
 - Try to keep code as clean as possible. If you need comments to understand the code it is not clear enough.
 - Variables will be named with camelCase not under_scores.
 - Variables should be named to express their purpose within the function.
 
 ## Why does naming variables matter?
 The following is an example from the book Clean Code.
 ```
 public List<int[]> getThem() {
 List<int[]> list1 = new ArrayList<int[]>();
 for (int[] x : theList)
      if (x[0] == 4)
        list1.add(x);
    return list1;
 }
 ```
 This code is only a few lines but it is still somewhat confusing. What is *them*? Why is it called *list1* when there is no list2? If there was a *list2*, would its purpose be better understood? What is the signifigance of 4? 
 
 From this code, nothing can really be understood about the application and function of this code.
 ```
 public List<int[]> getFlaggedCells() {
    List<int[]> flaggedCells = new ArrayList<int[]>();
      for (int[] cell : gameBoard)
      if (cell[STATUS_VALUE] == FLAGGED)
        flaggedCells.add(cell);
    return flaggedCells;
 }
 ```
 This code does the exact same thing but gives context for what the code is actually doing. We now understand that 4 signifies that a cell has been flagged. And when speaking of *them* we are refering to flagged cells.
 
 
