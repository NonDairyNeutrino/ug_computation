/*
Program Objective: Convert a text file to a binary search tree and give an analysis of the words in the file.
Author: Nathan Chapman
Date: 07/24/22
*/

// packages needed for user input and file processing
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.*;

public class AnalyzeTextStream {
// CLASS VARIABLES
  private static Node[] mostCommonWords = new Node[3]; // initialize the collection of the 3 most common words for the ANALAYZE query

// METHODS

  // parse the text file into an array of the words in the file
  public static String[] processFile (String filePathInput) {
    Path filePath = Path.of(filePathInput); //get the path to the file
    String file_string = "";
    try {
      file_string = Files.readString(filePath); // import the whole file as a single string
    } catch(IOException e) {
      e.printStackTrace();
    };
    file_string = file_string.toLowerCase();
    file_string = file_string.replaceAll("-", " ");         // dashes are treated as white space
    file_string = file_string.replaceAll("\\d ", "");       // ignore digits
    file_string = file_string.replaceAll("\\p{Punct}", ""); // ignore punctuation
    file_string = file_string.replaceAll("\n", " ");        // make the whole file on one line
    String[] words = file_string.split(" ");                // split the file string at new lines
    return words;
  }

  // if user says ANALYZE, return the stats of the three most common words in the file
  public static void analyze (Node node) {
    // return on a leaf
    if (node == null) {
      return;
    }
    else {
      analyze(node.left); // go all the way left
      // if the word appears less than the words in mostCommonWords, don't add it
      if (node.al.size() < mostCommonWords[0].al.size()) {
        return;
      }
      // if the word appears more than the least common, replace it
      else if (node.al.size() <= mostCommonWords[1].al.size()) {
        mostCommonWords[0] = node;
      }
      // if the word appears more than the second least common, replace it
      else if (node.al.size() <= mostCommonWords[2].al.size()) {
        mostCommonWords[1] = node;
      }
      // if the word appears more than the most common, replace it
      else {
        mostCommonWords[2] = node;
      }

      analyze(node.right); // go all the way right
    }
  }

// MAIN
  public static void main(String[] args) {
    // instantiate class variables
    String[] words;
    BST bst = new BST();
    // instantiate mostCommonWords
    for (int k = 0; k < mostCommonWords.length; k++) {
      mostCommonWords[k] = new Node("");
    }

    // parse the text file into an array of strings
    words = processFile(args[0]);

    // build the bst
    for (int k = 0; k < words.length; k++) {
      bst.insert(words[k], k);
    }

    // proceed based on user input
    if (args[1].equals("ANALYZE")) {
      analyze(bst.overallRoot); // get the three most common words and their stats
      for (Node word : mostCommonWords) {
        System.out.print(word);
      }
    }
    else {
      for (int k = 1; k < args.length; k++) { // for each given word
        Node wordNode = bst.overallRoot.findNode(args[k]); // try to find the node that contains that word
        if (wordNode != null) { // if the node exists in the tree, return it and its stats
          System.out.print(wordNode);
        }
        else { // if the node doesn't exist, return saying so
          System.out.print(args[k] + ":0 ");
        }
      }
    }
  }
}
