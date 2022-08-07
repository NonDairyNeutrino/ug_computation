/*
Program Objective: make a node structure to be used in a binary search tree
Author: Nathan Chapman
Date: 07/24/2022
*/

import java.util.ArrayList; // used for the list of word positions

public class Node {
// CLASS VARIABLES
  public String val; // the value or "key" of the node
  public ArrayList<Integer> al = new ArrayList<Integer>(); // list containing the positions of the word in the given text file
  public Node left = null, right = null;  // the left and right children of the node

//METHODS
  // create a node with a given value and null children
  public Node(String val) {
    this.val = val;
  }

  // insert a value into a bst based on the value of the given node
  public void insert (String val, int position) {
    // check which side to insert
    if (this.val.compareTo(val) > 0) { // compare strings lexographically
      // check if the node is a leaf
      if (this.left != null) {
        this.left.insert(val, position); //
      }
      else {
        // if the node is a leaf, create a new child and add the position to the list
        this.left = new Node(val);
        this.left.al.add(position + 1);
      }
    }
    else if (this.val.compareTo(val) < 0) {
      // check if the node is a leaf
      if (this.right != null) {
        this.right.insert(val, position);
      }
      else {
        // if the node is a leaf, create a new child and add the position to the list
        this.right = new Node(val);
        this.right.al.add(position + 1);
      }
    }
    // if the word is one that has already been encountered, just add the position to the list
    else { // this.val.compareTo(val) == 0
      this.al.add(position + 1);
    }
  }

  // find the node of a specific word
  public Node findNode (String word) {
    Node output = null;
    if (this.val.compareTo(word) > 0) { // does this word come before this node?
      if (this.left != null) {          // if you can go left, do so
        output = this.left.findNode(word);
      }
      // if you should go left, but you can't, return that the word doesn't exist in the file
    }
    else if (this.val.compareTo(word) < 0) { // does this word come after this node?
      if (this.right != null) {              // if you can go right, do so
        output = this.right.findNode(word);
      }
      // if you should go right, but you can't, return that the word doesn't exist in the file
    }
    // if this node matches the word, you've found it and return this node!
    else { // this.val.compareTo(val) == 0
      output = this;
    }
    return output;
  }

  // print the values of the nodes of the tree using the "in order" algorithm
  public static void printInOrder (Node node) {
    if (node != null) {
      printInOrder(node.left);
      System.out.print(node.val + " "); System.out.println(node.al);
      printInOrder(node.right);
    }
  }

  // add functionality to display the stats of a single node
  public String toString () {
    return this.val + ":" + this.al.size() + ":" + this.al + " ";
  }

//MAIN
  public static void main(String[] args) {

  }
}
