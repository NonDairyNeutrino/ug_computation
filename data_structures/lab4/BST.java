/*
Program Objective: Print Pre-, Post-, and InOrder traversals of a binary search tree with nodes given by the using.
Author: Nathan Chapman
Date: 07/17/22
*/
// all imports needed for user input
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class BST {
// CLASS VARIABLES

  public static Node overallRoot;

// METHODS
  // create an empty bst
  public BST () {
    overallRoot = null;
  }
  // get the root of the bst
  public static Node getRoot () {
    return overallRoot;
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

// MAIN
  public static void main(String[] args) throws IOException {
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    BST tree = new BST();
    System.out.println("Type integers, press return after each one.\nType ''end'' when done");

    String input = in.readLine();
    while (!input.equals("end")) {
      insert(Integer.valueOf(input));
      input = in.readLine();
    }

    System.out.print("Inorder traversal: "); printInOrder(getRoot());
    System.out.println();
    System.out.print("Preorder traversal: "); printPreOrder(getRoot());
    System.out.println();
    System.out.print("Postorder traversal: "); printPostOrder(getRoot());
  }
}
