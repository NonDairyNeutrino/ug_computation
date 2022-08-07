/*
Program Objective: make a node structure to be used in a binary search tree
Author: Nathan Chapman
Date:
*/

public class Node {
// CLASS VARIABLES
  private int value; // the value or "key" of the node
  Node left = null, right = null;  // the left and right children of the node

//METHODS
  // create a node with a given value and null children
  public Node(int value) {
    this.value = value;
  }
  // get the value of the given node
  public int getValue() {
    return this.value;
  }
  // insert a value into a bst based on the value of the given node
  public void insert (int value) {
    // check which side to insert
    if (value <= this.value) {
      // check if the node is a leaf
      if (this.left != null) {
        this.left.insert(value);
      }
      else {
        // if the node is a leaf, create a new child
        this.left = new Node(value);
      }
    }
    else {
      // check if the node is a leaf
      if (this.right != null) {
        this.right.insert(value);
      }
      else {
        // if the node is a leaf, create a new child
        this.right = new Node(value);
      }
    }
  }

//MAIN
  public static void main(String[] args) {

  }
}
