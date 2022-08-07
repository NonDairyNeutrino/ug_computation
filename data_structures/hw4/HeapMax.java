/*
Program Objective: Create functionality to store a max heap and it's properties.
Author: Nathan Chapman
Date: 7/31/2022
*/

// HeapMax Class
public class HeapMax {
	// CLASS VARIABLES
	private int[] Heap;
	private int size;
	private int maxSize;

	// METHODS
	// constructor
	public HeapMax (int maxSize) {
		this.maxSize = maxSize;
		this.size = 0;
		this.Heap = new int[maxSize + 1];
		this.Heap[0] = -273;
	}

	// Returns position of parent
	private int getParent(int pos) {
		return pos/2;
	}
	// Calculate the index positions of the left and right children
	private int getLeftChild (int pos) {
		return 2 * pos;
	}

	private int getRightChild (int pos) {
		return 2 * pos + 1;
	}

	// Boolean if node is a leaf
	private boolean isLeaf (int pos) {
		return pos > this.size / 2;
	}

	// standard function to swap two values
	private void swap (int index1, int index2) {
		int dummy = this.Heap[index1];
		this.Heap[index1] = this.Heap[index2];
		this.Heap[index2] = dummy;
	}

	// Inserts a new element into the heap
	public void insert (int element) {
		// give the heap an extra spot at the end
		this.size++;

		// put the given element into the new spot at the end
		this.Heap[size] = element;

		// if the parent is smaller and not at index 0
		// swap the new element with its parent
		int elementIndex = this.size;
		while (this.Heap[elementIndex] > this.Heap[getParent(elementIndex)] && getParent(elementIndex) != 0) {
			this.swap(elementIndex, getParent(elementIndex));
			elementIndex = getParent(elementIndex);
		}
	}

	// print the contents of the heap
	public void printMaxHeap () {

		int def = this.Heap[0];
		for (int k = 1; k < this.size + 1; k++) {
			// remember yourself
			int nodeValue  = this.Heap[k];

			// assume you don't have children
			int leftChild  = def;
			int rightChild = def;

			// if the node is a leaf
			// just remember yourself
			if (!isLeaf(k)) {
				// if you at least have a left child
				// remember it
				leftChild = this.Heap[getLeftChild(k)];

				// if you also have a right child
				// remember it as well
				if (2 * k + 1 <= this.size) {
					rightChild = this.Heap[getRightChild(k)];
				}
			}
			// show yourself and your children
			String nodeString       = "Heap Node: " + nodeValue + ", ";
			String leftChildString  = "left child: " + ((leftChild != def) ? leftChild : "NA") + ", ";
			String rightChildString = "right child: " + ((rightChild != def) ? rightChild : "NA");
			System.out.println(nodeString + leftChildString + rightChildString);
		}
	}

}
