// Program Objective: Provide the back end functionality for SortCompare
// Author: Nathan Chapman
// Date: 06/24/2022

// References
// insertionSort, merge, and merge sort algorithms taken from CLRS (4th ed)

public class SortCompareBack {
// CLASS VARIABLES
  static int comp_count_insertion = 0;
  static int comp_count_merge     = 0;

// METHODS

  // prepends an array with the given value
  static int[] prepend (int[] array, int comps) {
    int[] prependee_array = new int[array.length + 1];
    int[] temp            = array.clone();
    prependee_array[0]    = comps;
    for (int k = 0; k < array.length; k++) {
      prependee_array[k + 1]  = temp[k];
    }
    return prependee_array;
  }

  // sorts an array via the insertion sort algorithm
  public static int[] insertionSort (int[] array) {
    for(int i = 1; i < array.length; i++) {
      int key = array[i];
      int j   = i - 1;
      while (j >= 0 && array[j] > key) {
        comp_count_insertion++; // count the times elements are compared
        array[j + 1] = array[j];
        j--;
      }
      comp_count_insertion++; // count comparison that breaks the while loop
      array[j + 1] = key;
    }
    return array;
  }

  // executes the merge algorithm for a given array and initial and terminal indices
  public static int[] merge(int[] array, int p, int q, int r) {
    int n_L = q - p + 1;
    int n_R = r - q;
    int[] L = new int[n_L];
    int[] R = new int[n_R];

    for(int i = 0; i <= n_L - 1; i++) {
      L[i] = array[p + i];
    }
    for(int j = 0; j <= n_R - 1; j++) {
      R[j] = array[q + j + 1];
    }

    int i = 0, j = 0, k = p;

    while(i < n_L && j < n_R) {
      if(L[i] <= R[j]) {
        array[k] = L[i];
        i++;
      }
      else {
        array[k] = R[j];
        j++;
      }
      k++;
      comp_count_merge++; // comparison count
    }
    while(i < n_L) {
      array[k] = L[i];
      i++; k++;
    }
    while(j < n_R) {
      array[k] = R[j];
      j++; k++;
    }
    return array;
  }

  // sorts an array via the merge sort algorithm
  public static int[] mergeSort (int[] array, int p, int r) {
    if (p >= r) {
      return array;
    }
    int   q      = (int) Math.floor((p + r) / 2); // midpoint of aray[p:r]
    int[] left   = mergeSort(array, p, q);
    int[] right  = mergeSort(array, q + 1, r);
    int[] sorted = merge(array, p, q, r);
    return sorted;
  }

// MAIN
  public static void main(String[] args) {

  }
}
