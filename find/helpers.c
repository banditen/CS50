// Helper functions

#include <cs50.h>

#include "helpers.h"

// Returns true if value is in array of n values, else false
bool search(int value, int values[], int n)
{

    // Determine min and max
    int min = 0;
    int max = n - 1;

    // Use binary search to go through values
    while (min <= max)
    {
        // Determine middle value
        int middle = min + ((max - min) / 2);

        // If middle value equals the value searched, return true
        if (values[middle] == value)
        {
            return true;
        }

        // If middle value is larger than value searched, search left part
        else if (values[middle] > value)
        {
            max = middle - 1;
        }

        // If middle value is smaller than value searched, search right part
        else if (values[middle] < value)
        {
            min = middle + 1;
        }
    }

    // If value not found, return false
    return false;

}

// Sorts array of n values
void sort(int values[], int n)
{

    // Implement selection sorting algorithm to sort n
    for (int i = 0; i < n - 1; i++)
    {
        // Set minimum value
        int min = i;

        // Find the index of minimum value
        for (int index = i; index < n; index++)
        {
            // If min is larger than the index, set new min
            if (values[min] > values[index])
            {
                min = index;
            }
        }

        // Check if minimum value changed
        if (min != i)
        {

            // Swap the i'th value the lowest value
            int swap = values[min];
            values[min] = values[i];
            values[i] = swap;
        }
    }

    return;
}
