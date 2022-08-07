/*
Program Objective: A program to create a linked list implementation of a graph using user provided edges via the command line
Author: Nathan Chapman
Date: 07/14/2022
*/

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class WeightedDirGraph {
  // requests the user for input of vertices to connect and adds an edge between them if both vertices exist
  private static Graph promptEdgeInput () throws IOException {
    // instantiate a buffered reader
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    // prompt the user how many vertices there exist in the graph
    System.out.print("How many vertices? ");
    int numVertices = Integer.valueOf(in.readLine());
    Graph graph = new Graph(numVertices); // create an object of type Graph, with as many vertices as the user specifies

    // input instructions
    System.out.println("Input from, to, then cost.  Type ''end'' to finish.");

    String input = "";
    int step= 0, edgeFrom = 0, edgeTo = 0, edgeCost = 1;
    // the user can end the program by entering "end" at any stage
    while (! input.equals("end")) {
      switch (step) {
        case 0:
          // prompt the user to provide from
          System.out.print("From vertex "); input = in.readLine();
          if (!input.equals("end")) {
            edgeFrom = Integer.valueOf(input);
            step++;
          }
          // extra: check if the initial vertex is in the graph
          if (edgeFrom > numVertices - 1) {
            System.out.println("That vertex is not in the graph.  Please enter a valid vertex.");
            step = 1;
          }
          break;
        case 1:
          // prompt the user to provide to
          System.out.print("To vertex "); input = in.readLine();
          if (!input.equals("end")) {
            edgeTo = Integer.valueOf(input);
            step++;
          }
          // extra: check if the incident vertex is in the graph
          if (edgeTo > numVertices - 1) {
            System.out.println("That vertex is not in the graph.  Please enter a valid vertex.");
            step = 1;
          }
          break;
        case 2:
          // prompt the user to provide cost
          System.out.print("Cost "); input = in.readLine();
          if (!input.equals("end")) {
            edgeCost = Integer.valueOf(input);
          }
          graph.addEdge(edgeFrom, edgeTo, edgeCost); // edge inserted into graph via addEdge
          step = 0;
          break;
      }
    }
    return graph;
  }

// MAIN
  public static void main(String[] args) throws IOException {
    promptEdgeInput().printGraph();
  }
}
