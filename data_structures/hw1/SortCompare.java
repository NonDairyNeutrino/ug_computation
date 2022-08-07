/*
Program Objective: Compare the efficiency between insertion and merge sort
Author: Nathan Chapman
Date: 06/XX/2022
*/

// TODO: Make count table and plot (submit to Canvas)

public class SortCompare {
// METHODS
  // sorts the randomly generated array based on the input sorting method
  static int[] sort (SortCompareFront input) {
    int[] count_array = {};
    int[] sorted;
    // choose how to sort based on given sorting method
    switch (input.sorting_method) {
      // insertion sort
      case "i":
        sorted       = SortCompareBack.insertionSort(input.rand_array.clone()); // sort the array
        count_array  = SortCompareBack.prepend(sorted, SortCompareBack.comp_count_insertion); // prepend the comparison count to the sorted array
        break;
      // merge sort
      case "m":
        sorted       = SortCompareBack.mergeSort(input.rand_array.clone(), 0, input.rand_array.length - 1); // sort the array
        count_array  = SortCompareBack.prepend(sorted, SortCompareBack.comp_count_merge); // prepend the comparison count to the sorted array
        break;
    }
    return count_array;
  }

  // bridges the input given from the front end/user input to the back end and then back to the front end to give the result back to the user
  private static void bridge (SortCompareFront input, SortCompareFront output) {
    int[] count_array;

    count_array         = sort(input);
    output.comp_count   = count_array[0]; // get comparison count
    output.sorted_array = new int[count_array.length - 1];
    for (int k = 0; k < count_array.length - 1; k++) {output.sorted_array[k] = count_array[k + 1];} // get sorted array
    output.give_output(input); // output the comparison count and sorted array back to the front end
  }

// MAIN
  public static void main(String[] args) {
    SortCompareFront input  = new SortCompareFront();
    SortCompareFront output = new SortCompareFront();

    input.get_input(); // starts the front end and gets the user input

    // chooses single method versus all method
    if (input.sorting_method.equals("all")) {
      input.sorting_method = "i";
      bridge(input, output);
      input.sorting_method = "m";
      bridge(input, output);
    }
    else {
      bridge(input, output);
    }
  }
}
