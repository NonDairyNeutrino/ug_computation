/*
Program Objective:
Author: Nathan Chapman
Date: 07/XX/2022
*/

import java.nio.file.*;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

public class CalcRoadsMaintainBack {
// CLASS VARIABLES

// METHODS
  // take in a text file of vertices, directions, and weights to return an array of those
  public static String[][] processFile (String filePathInput) {
    Path filePath = Path.of(filePathInput); //get the path to the file
    String file_string = "";
    try {
      file_string = Files.readString(filePath); // import the whole file as a single string
    } catch(IOException e) {
      e.printStackTrace();
    };
    String[] edges_string = file_string.split("\n"); // split the file string at new lines
    String[][] edge_input = new String[edges_string.length][4];
    // initialize the edge weight as 1 by default
    for (int n = 0; n < edge_input.length; n++) {
      edge_input[n][3] = "1";
    }

    // Go through and pick out each word in each line of the file and put it in an array
    for (int j = 0; j < edges_string.length; j++) {
      String[] line_array = edges_string[j].split(" ");
      for (int k = 0; k < line_array.length; k++) {
        edge_input[j][k] = line_array[k].trim();
      }
    }
    return edge_input;
  }

// MAIN
// a "2way" edge means to one-way edges with equal weight
  public static void main(String[] args) {
    
  }
}
