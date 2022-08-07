/*
Program Objective: Determine if a an edge exists between given vertices for the minimum spanning tree of a given edge set
Author: Nathan Chapman
Date: 07/12/2022
*/

import java.util.ArrayList;
import java.util.HashMap;

public class CalcRoadsMaintain {
  public static void main(String[] args) {
    String[][] processedFile = CalcRoadsMaintainBack.processFile(args[0]); // process the edge file into a grid of items
    Graph graph = new Graph();
    graph.getVertices(processedFile); // find the distinct vertices in the edge file and add them to the graph
    graph.getEdges(processedFile); // find the edges in the edge file and add them to the graph
    graph.makeAdjMat(); // make the adjacency matrix of the graph for the given vertices and edges
    Graph mst = graph.minSpanTree(args[1]); // make the minimum spanning tree (mst) for the graph

    String vertexFrom = args[2], vertexTo = args[3];
    if (
        mst.vertices.containsKey(vertexFrom) && // check if the initial vertex is in the mst
        mst.vertices.containsKey(vertexTo)   && // check if the incident vertex is in the mst
        mst.adjMat[mst.vertices.get(vertexFrom)][mst.vertices.get(vertexTo)] != -1 // check if the edge between the initial and incident vertices exists in the mst
      ) {
      System.out.println("yes");
    }
    else {
      System.out.println("no"); // if the initial or incident vertices are not in the mst nor is their connecting edge, print no
    }
  }
}
