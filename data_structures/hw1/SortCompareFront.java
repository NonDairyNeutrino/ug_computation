// Program Objective: Provide the front end functionality for SortCompare
// Author: Nathan Chapman
// Date: 06/24/2022

import java.util.Scanner; // use to get user input
import java.util.Random;  // use to make random array

public class SortCompareFront {
// CLASS VARIABLES
  private static Random rng = new Random();
  // input variables
  public int[] rand_array;
  public String sorting_method;
  // output variables
  public int comp_count;
  public int[] sorted_array;

// METHODS
  // INPUT METHODS

  // makes an array of random integers of a given length n such that each element is in the interval [-n, n]
  private static int[] make_random_array (int array_length) {
    int[] array = new int[array_length];
    for (int k = 0; k < array_length; k++) {
      array[k] = -array_length + rng.nextInt(2 * array_length); // rng.nextInt generates a random integer between 0 and 2 * array_length
    }
    return array;
  }

  // takes in user input
  public void get_input () {
    Scanner input = new Scanner(System.in);
    // gets the desired length of the array
    System.out.println("How many entries?");
    int array_length = input.nextInt();
    input.nextLine();
    this.rand_array = make_random_array(array_length); // makes the array to be sorted

    // gets sorting method to use
    System.out.println("Which sort {m, i, all}?");
    this.sorting_method = input.nextLine();
  }

  // OUTPUT METHODS

  // displays in the front end which sorting method was used
  private void show_method (String sorting_method) {
    switch (sorting_method) {
      case "i":
        System.out.println("\ninsertion sort");
        break;
      case "m":
        System.out.println("\nmerge sort");
        break;
    }
    System.out.println("==============");
  }

  // displays in the front end the unsorted and sorted arrays
  private void show_arrays (int[] array) {
    // if the length of the arrays is 20 or more, the arrays are not displayed
    if (array.length < 20) {
      System.out.print("Unsorted array: "); for (int elem : array) {System.out.print(elem + " ");}
      System.out.println();
      System.out.print("Sorted array: "); for (int elem : this.sorted_array) {System.out.print(elem + " ");}
      System.out.println();
    }
  }

  // displays in the front end the number of comparisons that were made
  private void show_comp_num () {
    System.out.println("Num comparisons: " + this.comp_count + "\n");
  }

  // displays in the front end the formatted results of the unsorted and sorted arrays, and the number of comparisons that were made
  public void give_output (SortCompareFront input) {
    // if the input sorting method is all, sort with each method and print to front end
    if (input.sorting_method.equals("all")) {
      input.sorting_method = "i";
      give_output(input);
      input.sorting_method = "m";
      give_output(input);
    }
    // if the input sorting method is either i or m, only sort and return with that method
    else {
      show_method(input.sorting_method);
      show_arrays(input.rand_array);
      show_comp_num();
    }
  }

// MAIN
  public static void main(String[] args) {

  }
}
