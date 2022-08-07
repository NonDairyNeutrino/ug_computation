/*
Program Objective: Take user given edges between hard coded vertices to create and display the adjacency matrix of the resulting graph
Author: Nathan Chapman
Date: 06/30/2022
*/

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Graph {
  // CLASS VARIABLES
  private static int[][] graph;
  private static String[] vertexNames = new String[5];
  private static final int numVertices = 5;

  // METHODS

  // initializes a fully incomplete graph as an adjacency matrix of zeros
  private static void createGraph () {
    graph = new int[numVertices][numVertices];
    System.out.println("Graph created.");
  }

  // displays the names of the vertices of the graph
  private static void printVertexNames () {
    System.out.println("The vertices are:");
    // for (int k = 0; k < numVertices; k++) {
    //   System.out.println(vertexNames[k]);
    // }
    for (String name : vertexNames) {
      System.out.println(name);
    }
    System.out.println();
  }

  // creates the vertex list of the graph
  private static void createGraphVertexNames () {
    String[] names = {"apple", "grape", "banana", "orange", "pineapple"};
    for (int k = 0; k < numVertices; k++) {
      vertexNames[k] = names[k];
    }
    System.out.println("Vertices added to graph.");
  }

  // gets the index at which a given vertex is located
  private static int getVertexID (String vertexName) {
    int vertexID = -1;
    for (int k = 0; k < numVertices; k++) {
      if (vertexNames[k].equals(vertexName)) {
        vertexID = k;
        break;
      }
    }
    return vertexID;
  }

  // displays the adjacency matrix representaion of the graph
  private static void printGraph () {
    for (int j = 0; j < numVertices; j++) {
      for (int k = 0; k < numVertices; k++) {
        System.out.print("| " + graph[j][k] + " ");
      }
      System.out.println("| " + vertexNames[j]);
    }
    System.out.println();
  }

  // adds an edge between given vertices by setting the corresponding position in the adjacency matrix to 1
  private static void addEdge (String vertex1, String vertex2) {
    int row = getVertexID(vertex1), col = getVertexID(vertex2);
    if (row != -1 && col != -1) {
      graph[row][col] = graph[col][row] = 1;
      System.out.println("Added edge " + vertex1 + "-" + vertex2 + " to graph\n");
    }
    else if (row == -1) {
      System.out.println("Cannot add edge " + vertex1 + "-" + vertex2 + "; " + vertex1 + " is not a vertex.\n");
    }
    else {
      System.out.println("Cannot add edge " + vertex1 + "-" + vertex2 + "; " + vertex2 + " is not a vertex.\n");
    }
  }

  // requests the user for input of vertices to connect and adds an edge between them if both vertices exist
  private static void promptEdgeInput () throws IOException {
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    String vertex = "", vertex1, vertex2;
    while (! vertex.equals("done")) {
      System.out.print("Enter first vertex: " ); vertex1 = in.readLine();
      System.out.print("Enter second vertex: "); vertex = vertex2 = in.readLine();
      if (! vertex.equals("done")) {
        addEdge(vertex1, vertex2);
      }
    }
    System.out.println();
  }

  // MAIN
  public static void main(String[] args) throws IOException {
    createGraph();
    createGraphVertexNames();
    printVertexNames();
    promptEdgeInput();
    printGraph();
  }
}
