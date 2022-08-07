/*
Program Objective: demonstrate unit-tested rotation and traversal functions of a binary search tree
Author: Nathan Chapman
Date: 07/21/22
*/
// all imports needed for user input
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class BST {
// CLASS VARIABLES

  public static Node overallRoot;
  private static String inOrderTraverseStr = "";

// METHODS
  // create an empty bst
  public BST () {
    overallRoot = null;
  }
  // get the root of the bst
  public static Node getRoot () {
    return overallRoot;
  }
  // update root
  public void updateRoot (Node node) {
    overallRoot = node;
  }
  // insert a value into the bst
  public static void insert (int value) {
    // check if the tree is empty
    if (overallRoot != null) {
      // if non-empty, insert the value into the tree
      overallRoot.insert(value);
    }
    else{
      // if the tree is empty, create the root using the given value
      overallRoot = new Node(value);
    }
  }
  // print the values of the nodes of the tree using the "in order" algorithm
  public static void printInOrder (Node node) {
    if (node != null) {
      printInOrder(node.left);
      System.out.print(node.getValue() + " ");
      printInOrder(node.right);
    }
  }
  // print the values of the nodes of the tree using the "pre order" algorithm
  public static void printPreOrder (Node node) {
    if (node != null) {
      System.out.print(node.getValue() + " ");
      printPreOrder(node.left);
      printPreOrder(node.right);
    }
  }
  // print the values of the nodes of the tree using the "post order" algorithm
  public static void printPostOrder (Node node) {
    if (node != null) {
      printPostOrder(node.left);
      printPostOrder(node.right);
      System.out.print(node.getValue() + " ");
    }
  }
  // build a string of node values sandwiched between each of their children's value
  public static void inOrderTraverse (Node node) {
    String appendee;
    // if the node doesn't exist, just break
    if (node == null) {
      return;
    }
    else {
      Node leftChild = node.getLeftChild(), rightChild = node.getRightChild();
      // go down the left side
      inOrderTraverse(leftChild);

      // choose which character to add to the traversal string for the left child
      if (leftChild != null) {
        appendee = String.valueOf(leftChild.getValue());
      }
      else {
       appendee = "n" ;
      }
      inOrderTraverseStr = inOrderTraverseStr.concat(appendee);

      // aappend the value of the current node
      inOrderTraverseStr = inOrderTraverseStr.concat(String.valueOf(node.getValue()));

      // choose which character to add to the traversal string for the right child
      if (rightChild != null) {
        appendee = String.valueOf(rightChild.getValue());
      }
      else {
        appendee = "n";
      }
      inOrderTraverseStr = inOrderTraverseStr.concat(appendee);
      // go down the right side
      inOrderTraverse(rightChild);
    }
  }

  // perform a right rotation on a tree around the root as the pivot
  public static Node rightRotate (Node pivot) {
    Node aNode  = pivot.left;
    pivot.left  = pivot.left.right; // break left connection and connect to right child of left child
    aNode.right = pivot;            // lower root and replace with pivot
    return aNode;                   // return new root
  }

  // unit test for inOrderTraverse
  private static void treeTest_1 () {
    BST tree = new BST();
    int[] test = {4,2,1,3,9,8};
    for(int k : test) {
      insert(k);
    }

    System.out.println("==========\ntreeTest_1\n==========");
    System.out.print("Inorder traversal : "); printInOrder(getRoot()); System.out.println(); // show the tree with just the node values

    inOrderTraverse(getRoot());
    System.out.println("nodeChildrenTrav: " + inOrderTraverseStr); // show the tree with the node and child values

    if (inOrderTraverseStr.equals("n1n123n3n249n8n89n")) { // compare to known result
      System.out.println("treeTest_1 passed");
    }
    else{
      System.out.println("treeTest_1 failed");
    }
  }

  // unit test for rightRotate
  private static void rightRotateTest_1 () {
    BST tree = new BST();
    int[] test = {4,2,1,3,9,8};
    for(int k : test) {
      insert(k);
    }

    System.out.println("=================\nrightRotateTest_1\n=================");
    System.out.print("Inorder traversal : "); printInOrder(getRoot()); System.out.println(); // show the tree with just the node values

    inOrderTraverseStr = ""; inOrderTraverse(getRoot());
    System.out.println("preRotation:  " + inOrderTraverseStr); // show the tree with the node and child values

    tree.updateRoot(rightRotate(getRoot())); // rotate the tree
    inOrderTraverseStr = ""; inOrderTraverse(getRoot());
    System.out.println("postRotation: " + inOrderTraverseStr); // show the tree with the node and child values AFTER a right rotation

    if (inOrderTraverseStr.equals("n1n124n3n349n8n89n")) { // compare to known result
      System.out.println("rightRotateTest_1 passed");
    }
    else{
      System.out.println("rightRotateTest_1 failed");
    }
  }

// MAIN
  public static void main(String[] args) throws IOException {
    // set up user input
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    BST tree = new BST();
    System.out.println("Type integers, press return after each one.\nType ''end'' when done");
    // get user input and build bst
    String input = in.readLine();
    while (!input.equals("end")) {
      insert(Integer.valueOf(input));
      input = in.readLine();
    }
    System.out.print("Inorder traversal : "); printInOrder(getRoot());  System.out.println(); // show the tree with just the node values

    System.out.println();
    treeTest_1(); // show inOrderTraverse unit test results
    System.out.println();
    rightRotateTest_1(); // show rightRotate unit test results
  }
}
