// Implements a dictionary's functionality
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include "dictionary.h"

typedef struct WordNode
{
    char *data;
    struct WordNode *next;
}WordNode;

int hash(const char *word);
const int HASHSIZE = 5000;

WordNode *hashtable[HASHSIZE];
int numWords = 0;;

void addToHashTable(char *word)
{
    int spotInArr = hash(word);

    WordNode *newNode =  (WordNode *)malloc(sizeof(WordNode));
    newNode->data = NULL;
    newNode->data = (char *)malloc(strlen(word) * sizeof(char));
    memcpy(newNode->data, word, strlen(word));

    if (hashtable[spotInArr] == NULL)
    {
        hashtable[spotInArr] = newNode;
    }
    else
    {
        WordNode *tmp = hashtable[spotInArr];
        hashtable[spotInArr] = newNode;
        newNode->next = tmp;
    }
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    char *lowerWord = (char *)malloc(1 + strlen(word) * sizeof(char));
    char c = word[0];
    int i = 0;
    while (c != '\0')
    {
        lowerWord[i] = tolower(c);
        i++;
        c = word[i];
    }
    lowerWord[i] = '\0';

    int spot = hash(lowerWord);
    bool found = false;
    WordNode *current = hashtable[spot];

    while (current != NULL)
    {
        if (current->data != NULL && strcmp(lowerWord, current->data) == 0)
        {
            found = true;
            break;
        }
        current = current->next;
    }
    free(lowerWord);
    return found;
}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionaryFileName)
{
    FILE *inptr = fopen(dictionaryFileName, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Unable to open file %s\n", dictionaryFileName);
        return 2;
    }

    char *word = (char *)malloc(46  * sizeof(char));

    while (fscanf(inptr, "%s", word) != EOF)
    {
        addToHashTable(word);
        numWords++;
        free(word);
        word = (char *)malloc(46  * sizeof(char));
    }

    free(word);
    fclose(inptr);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return numWords;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    WordNode *current = NULL;
    WordNode *tmp = NULL;
    for (int i = 0; i < HASHSIZE; i++)
    {
        current = hashtable[i];
        tmp = hashtable[i];
        while (current != NULL)
        {
            tmp = current->next;
            free(current->data);
            free(current);
            current = tmp;
        }
    }
    return true;
}

int hash(const char *word)
{
    unsigned long long hashval = 0;

    char c = word[0];
    int i = 1;
    while (c != '\0')
    {
        hashval = c + 13 * hashval;
        c = word[i];
        i++;
    }
    return hashval % HASHSIZE;
}
