/*
Program Objective: this program is to create a graph object with associated methods
Author: Nathan Chapman
Date: 07/14/2022
*/

import java.util.LinkedList;

public class Graph {
// CLASS VARIABLES
  int vertices; // number of vertices in the graph
  LinkedList<Edge>[] adjList; // each index corresponds to a vertex and each edge in that index goes from that vertex
  /* vertex0             | vertex1
     ------------        | ---------
     edge from v0 to v3  | edge from v1 to v45
     edge from v0 to v1  | .
     edge from v0 to v74 | .
     .                     .
     .
     .
  */

// METHODS
  // constructor
  // create a graph with a given number of vertices and no edges
  Graph (int numVertices) {
    this.vertices = numVertices;
    this.adjList  = new LinkedList[numVertices];
    for (int k = 0; k < this.adjList.length; k++) {
      this.adjList[k] = new LinkedList<Edge>();
    }
  }

  // add an edge to the graph using given vertices and cost
  public void addEdge (int from, int to, int cost) {
    Edge edge = new Edge(from, to, cost);
    this.adjList[from].addFirst(edge);
  }

  // display the graph via listing the weighted edges using their initial and incident vertices
  public void printGraph() {
    LinkedList<Edge> initial_vertex;
    Edge edge;
    for (int k = 0; k < this.adjList.length; k++) { // loop through vertices
      initial_vertex = this.adjList[k];
      for (int j = 0; j < this.adjList[k].size(); j++) { // loop through edges
        edge = initial_vertex.get(j);
        System.out.println("vertex " + edge.from + " connected to " + edge.to + " at cost " + edge.cost);
      }
    }
  }

// MAIN
  public static void main(String[] args) {

  }
}
