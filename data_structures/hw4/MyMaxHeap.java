/*
Program Objective: Provide user interface to create a max heap for
given inputs
Author: Nathan Chapman
Date: 7/31/2022
*/

// import packages for user interface
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class MyMaxHeap {
	public static void main (String[] args) throws IOException {
		// set up UI
		BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		// instantiate an array that holds a max heap of a
		// maximum of 15 elements long
		HeapMax maxHeap = new HeapMax(15);
		// Insutrctions
		System.out.println("Type integers to insert into your max heap.\nPress return after each one. A maximum of 15\nelements are allowed. Type \"end\" when done.");
		// begin reading user input
		String input = in.readLine();
		while (!input.equals("end")) {
			// insert user given value into heap
			maxHeap.insert(Integer.valueOf(input));
			input = in.readLine();
		}
		// print the nodes of the heap top-bottom, left-right
		// along with their children
		maxHeap.printMaxHeap();
	}
}
