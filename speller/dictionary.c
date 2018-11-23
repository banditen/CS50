// Implements a dictionary's functionality

#include <stdbool.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Define structure and set up linked list
typedef struct node
{
    char word[LENGTH + 1];
    struct node* next;
}
node;

// Hash function prototype
unsigned int hash_word(const char* word);

// Set the node pointer to hashtable
node *hashtable[HASHSIZE];

// Counter for words in the dictionary
int counter = 0;

// Tracking loading stage
bool loaded = false;

// Returns true if word is in dictionary, otherwise false
bool check(const char *word)
{
    // Convert word to lowercase word
    int n = strlen(word);
    char copy[n + 1];

    // Need to add null terminator at the end of the word
    copy[n] = '\0';

    for(int i = 0; i < n; i++)
    {
        copy[i] = tolower(word[i]);
    }

    // Send lower case word to hash function to creat an index
    int index = hash_word(copy) % HASHSIZE;

    // Set head of the linked list
    node* head = hashtable[index];

    if (head != NULL)
    {
        // Points the pointer to the same location
        node* pointer = head;

        // Loop the linked list
        while(pointer != NULL)
        {
            if(strcmp(copy, pointer->word) == 0)
            {
                // Return true if word matches the word in our dictionary
                return true;
            }

            // Else move pointer to the next linked list
            pointer = pointer->next;
        }
    }

    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{

    // Open dictionary for reading
    FILE *file = fopen(dictionary, "r");

    // Check if dictionary is empty
    if (file == NULL)
    {
        fprintf(stderr, "Unable to open %s.\n", dictionary);
        return false;
    }

    // Add a buffer
    char buffer[LENGTH + 1];

    int n = LENGTH + 2;

    // loop through the dictionary until a null character
    while (fgets(buffer, n, file) != NULL)
    {

        // add null terminator to the end of the word
        buffer[strlen(buffer) - 1] = '\0';


        // Hash the word
        int index = hash_word(buffer) % HASHSIZE;

    	// Create a new node
    	node* new_node = malloc(sizeof(node));

    	// Test to see if node is null
    	if (new_node == NULL)
    	{
    	    fclose(file);
    	    return false;
    	}

        // Move to the next node in the list
    	strcpy(new_node -> word, buffer);
        new_node -> next = hashtable[index];

        hashtable[index] = new_node;
        counter++;
    }

    // Close dictionary
    fclose(file);
    loaded = true;
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (loaded)
    {
        return counter;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // For each node in hashtable
    for (int i = 0; i < HASHSIZE; i++)
    {
        // Check the table at that node
        node *pointer = hashtable[i];
        while (pointer != NULL)
        {
            // Create temp node
            node* temp = pointer;
            pointer = pointer->next;
            free(temp);
        }
    }
    return true;
}

/* Hash function
 * By Neel Mehta from
 * http://stackoverflow.com/questions/2571683/djb2-hash-function.
 */
unsigned int hash_word(const char* word)
 {
     unsigned long hash = 5381;
     for (const char* ptr = word; *ptr != '\0'; ptr++)
     {
         hash = ((hash << 5) + hash) + tolower(*ptr);
     }
     return hash % HASHSIZE;
 }

