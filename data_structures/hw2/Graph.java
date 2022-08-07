/*
Program Objective: create a graph structure with applicable methods with the end goal of creating a minimum spanning tree
Author: Nathan Chapman
Date: 07/12/2022
*/
import java.util.ArrayList;     // use for the edge set
import java.util.HashMap;       // use for the vertex set so there's a bridge between the names and the adjMat indices
import java.util.PriorityQueue; // use for the mst queue of vertices to search from
import java.util.Random;        // use to randomly choose between equally weighted edges when adding to the mst

public class Graph {
// CLASS VARIABLES
  public HashMap<String, Integer> vertices;
  public HashMap<Integer, String> verticesInverse = new HashMap<>(); // "inverse vertex set" to have a map between the vertex's adjMat index and its name
  public ArrayList<Edge> edges;
  public int[][] adjMat;
  private Random rng = new Random();

  // needs to have integers assocaited with the vertices for the adjacency matrix representation of the graph
  public void getVertices (String[][] edge_input) {
    int vertexID = 0;
    // go through the edge input file and add all the distinct vertices to the vertex set and the "inverse vertex set"
    for (int j = 0; j < edge_input.length; j++) {
      for (int k = 0; k < 2; k++) {
        if (! this.vertices.containsKey(edge_input[j][k])) {
          this.vertices.put(edge_input[j][k], vertexID);
          this.verticesInverse.put(vertexID++, edge_input[j][k]);
        }
      }
    }
  }

  // go through the edge input file and add each edge to the graph, adding a "backwards" edge if it's a 2 way edge
  public void getEdges (String[][] edge_input) {
    int from, to, weight;
    Edge edge;
    for (String[] line : edge_input) {
      from   = vertices.get(line[0]);
      to     = vertices.get(line[1]);
      weight = Integer.valueOf(line[3]);
      edge   = new Edge(from, to, weight);
      this.edges.add(edge);
      // if it's a bidirectional edge, add another edge from the incident vertex to the initial vertex
      if (line[2].equals("2way")) {
        edge = new Edge(to, from, weight);
        this.edges.add(edge);
      }
    }
  }

  // make the weighted adjacency matrix for the graph
  // adjacency matrix indices DO correspond to the IDs of the vertices
  public void makeAdjMat () {
    // initialize the dimension of the adjacency matrix to include all vertices up to the one with the largest index
    int maxVert = 0;
    for (int val : this.vertices.values()) {
      maxVert = Math.max(maxVert, val);
    }
    int[][] mat = new int[maxVert + 1][maxVert + 1];

    // initialize all elements of adjMat to -1 to signal that this entry does not represent an edge
    for (int j = 0; j < mat.length; j++) {
      for (int k = 0; k < mat[j].length; k++) {
        mat[j][k] = -1;
      }
    }
    // replace all values in the adjMat with the weight of the corresponding edge, if it exists
    for (Edge edge : this.edges) {
      mat[edge.from][edge.to] = edge.weight;
    }
    this.adjMat = mat;
  }

  // contruct a null graph
  public Graph () {
    this.vertices = new HashMap<>();
    this.edges = new ArrayList<>();
  }

  // construct a graph for given vertex and edge sets
  public Graph (HashMap<String, Integer> vertices, ArrayList<Edge> edges) {
    this.vertices = vertices;
    this.edges    = edges;
    makeAdjMat();
  }

  // for a given graph object, output the vertex HashMap and the graph's weighted adjacency matrix
  public String toString () {
    // get the vertices' names and their indices in the adjMat
    String str = String.join(" ", this.vertices.toString(), "\n");
    // go through the adjMat and get and format each element
    for (int[] row : this.adjMat) {
      for (int elem : row) {
        str = String.join("| ", str, String.valueOf(elem));
      }
      str = String.join(" ", str, "\n");
    }
    return str;
  }

  // add the vertex to the graph's vertex set and inverse vertex set
  public void addVertex (String name, int index) {
    this.vertices.put(name, index);
    this.verticesInverse.put(index, name);
  }

  // add the edge to the edge set of the graph
  public void addEdge (Edge edge) {
    this.edges.add(edge);
  }

  // build the minimum spanning tree via Prim's algorithm
  // BUG: minSpanTree doesn't see zero edge weights???
  public Graph minSpanTree (String root) {
    Graph mst = new Graph(); // start with a null graph and call it the mst
    mst.addVertex(root, this.vertices.get(root)); // add the given root to to the vertex set of the mst

    /*
    The following comments are just how I made sense of Prim's algorithm in my head.

    You, Samantha, are at a party alone because your friends Jack, Daniel, and Teal'c are watching Star Wars and eating pizza.
    You want to make more friends and have them join your group.
    You recognize that not everyone will vibe with everyone.
    */
    int you = mst.vertices.get(root), key, choice;
    String vertexName;
    PriorityQueue<Integer> needsToSearch = new PriorityQueue<>(1);
    ArrayList<Integer> equalWeights = new ArrayList<>();

    needsToSearch.add(you); // you are first in line to search for people to add to your group
    // the people in your group keep searching for more people to add until there are no more people in your group that need to search
    while (!needsToSearch.isEmpty()) {
      // look at everyone around you
      for (int potential_connection = 0; potential_connection < this.adjMat[you].length; potential_connection++) {
        // but you only want to talk to strangers outside your group that you CAN talk to
        if (!mst.vertices.containsValue(potential_connection) && this.adjMat[you][potential_connection] >= 0) {
          key = Integer.MAX_VALUE;
          equalWeights.clear();
          // then you have them look at everyone around them
          for (int other_partier = 0; other_partier < this.adjMat[potential_connection].length; other_partier++) {
            // but only at the ones that are in your group that can talk TO THEM
            if (mst.vertices.containsValue(other_partier) && this.adjMat[other_partier][potential_connection] >= 0) {
              // turns out everyone here is an empath and can tell how well they would get along
              // if they deem the conversation would be less work than with anyone else they've looked at, they remember how much work it would be
              key = Math.min(key, this.adjMat[other_partier][potential_connection]);
              // if there are multiple people that are equally interested in them, they put them all in a list
              if (key == this.adjMat[other_partier][potential_connection]) {
                equalWeights.add(other_partier);
              }
            }
          }
          // then they come back to you and compare you with your friends
          if (this.adjMat[you][potential_connection] <= key) {
            choice = 0; // dummy initialization to make the compiler shut up because if it gets here, choice will necessarily be declared

            // if you're equally as easy to talk to as the other people they found, they add you to their list and then randomly choose someone from the list to talk to
            if (this.adjMat[you][potential_connection] == key) {
              equalWeights.add(you);
              choice = equalWeights.get(rng.nextInt(equalWeights.size()));
            }
            // if you're easier to talk to than anyone they looked, they choose you
            else if(this.adjMat[you][potential_connection] < key) {
              choice = you;
            }
            // they talk to either you or your friend and join your group and help you on your quest
            vertexName = this.verticesInverse.get(potential_connection);
            mst.addVertex(vertexName, potential_connection);
            mst.addEdge(new Edge(choice, potential_connection, this.adjMat[choice][potential_connection]));
            mst.makeAdjMat();
            // they get behind you to form a line of people to search for others
            needsToSearch.add(potential_connection);
          }
          // if they like someone else in your group more, they will wait for them to come around
        }
      }
      // now you're all done and it's someone else's turn
      // you leave the line and the next person steps up
      you = needsToSearch.poll();
    }
    // after everyone in your group has talked to everyone they can
    // return to Jack, Daniel, and Teal'c just as the Rebel fleet is engaging the Death Star and show them all the friends you made
    // and that everyone has a best friend in the group
    return mst;
  }

  public static void main(String[] args) {

  }
}
