/*
Program Objective: add fucntionality to build and insert into a binary search tree
Author: Nathan Chapman
Date: 07/24/22
*/

public class BST {
// CLASS VARIABLES

  public Node overallRoot; // root of the bst

// METHODS
  // create an empty bst
  public BST () {
    overallRoot = null;
  }

  // insert a value into the bst
  public void insert (String val, int position) {
    // check if the tree is empty
    if (overallRoot != null) {
      // if non-empty, insert the value into the tree
      overallRoot.insert(val, position);
    }
    else{
      // if the tree is empty, create the root using the given value
      overallRoot = new Node(val);
      overallRoot.al.add(position + 1);
    }
  }

// MAIN
  public static void main(String[] args) {

  }
}
