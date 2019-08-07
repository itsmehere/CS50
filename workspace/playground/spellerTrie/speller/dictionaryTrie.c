// Implements a dictionary's functionality
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include "dictionaryTrie.h"

typedef struct TrieNode{
    char *data;
    struct TrieNode *elements[27];
}TrieNode;

TrieNode *root = NULL;
int numWords = 0;

void addToTrie(char *word) {
    int spotInArr = 0;
    int i = 0;
    TrieNode *current = root;

    while(word[i] != '\0') {
        if (word[i] >= 'a' && word[i] <= 'z'){
            spotInArr = word[i] - 'a';
        } else {
            // The character has to be apostrophe!
            spotInArr = 26;
        }
        if(current->elements[spotInArr] == NULL){
            TrieNode *newNode = (TrieNode *)malloc(sizeof(TrieNode));
            current->elements[spotInArr] = newNode;
            current = newNode;
        } else {
            current = current->elements[spotInArr];
        }
        i++;
    }
    current->data = (char *)malloc(strlen(word) * sizeof(char) + 1);
    memcpy(current->data, word, strlen(word));
}

// Returns true if word is in dictionary else false
bool check(const char *word) {
    TrieNode *checkNode = root;
    int spotInArr = 0;

    char *lowerWord = (char *)malloc(1 + strlen(word) * sizeof(char));
    char c = word[0];
    int i = 0;
    while(c != '\0'){
        lowerWord[i] = tolower(c);
        i++;
        c = word[i];
    }
    lowerWord[i] = '\0';
    i = 0;


    while(lowerWord[i] != '\0') {
        if (lowerWord[i] >= 'a' && lowerWord[i] <= 'z') {
            spotInArr = lowerWord[i] - 'a';
        } else {
            // The character has to be apostrophe!
            spotInArr = 26;
        }
        if(checkNode->elements[spotInArr] == NULL){
            return false;
        } else {
            checkNode = checkNode->elements[spotInArr];
        }
        i++;
    }
    if(checkNode->data != NULL && strcmp(checkNode->data, lowerWord) == 0) {
        return true;
    }
    return false;
}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionaryFileName)
{
    FILE *inptr = fopen(dictionaryFileName, "r");
    if(inptr == NULL){
        fprintf(stderr, "Unable to open file %s\n", dictionaryFileName);
        return 2;
    }
    root = (TrieNode *)malloc(sizeof(TrieNode));

    char *word = (char *)malloc(46  * sizeof(char));

    while(fscanf(inptr, "%s", word) != EOF){
        addToTrie(word);
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

}
