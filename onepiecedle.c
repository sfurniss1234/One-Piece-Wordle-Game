#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "jsmn.h"

#define MAX_TOKENS 100000

int main()
{
	FILE *file;
	char *buffer;
	long file_size;

	// Open character database
	file = fopen("completecharlist.json", "r");

	if (file == NULL) {
		printf("Error opening character database.\n");
		return 1;
	}

	// Get file size
	fseek(file, 0, SEEK_END);
	file_size = ftell(file);
	rewind(file);

	buffer = malloc(file_size + 1);

	if (buffer == NULL) {
		fclose(file);
		return 1;
	}

	fread(buffer, 1, file_size, file);
	buffer[file_size] = '\0';
	fclose(file);

	// Parse JSON
	jsmn_parser parser;
	jsmntok_t tokens[MAX_TOKENS];

	jsmn_init(&parser);

	int token_count = jsmn_parse(
		&parser, buffer, strlen(buffer),
		tokens, MAX_TOKENS
	);

	if (token_count < 0) {
		printf("Error parsing JSON.\n");
		free(buffer);
		return 1;
	}

	// Store eligible character token positions
	int *eligible_characters = malloc(token_count * sizeof(int));

	if (eligible_characters == NULL) {
		free(buffer);
		return 1;
	}

	int eligible_count = 0;

	// Find each character object
	for (int i = 1; i < token_count; i++)
	{
		if (tokens[i].type != JSMN_OBJECT)
		{
			continue;
		}

		int missing_attributes = 0;
		int name_token = -1;

		// Examine the object's key-value pairs
		int end = tokens[i].end;
		int j = i + 1;

		while (j < token_count && tokens[j].start < end)
		{
			int key = j;
			int value = j + 1;

			if (value >= token_count)
			{
				break;
			}

			// Check for the name field
			if (tokens[key].end - tokens[key].start == 4 && strncmp(buffer + tokens[key].start, "name", 4) == 0)
			{
				name_token = value;
			}

			// Count [FILL IN] values
			if (tokens[value].type == JSMN_STRING && tokens[value].end - tokens[value].start == 10 && strncmp(buffer + tokens[value].start, "[FILL IN]", 10) == 0)
			{
				missing_attributes++;
			}

			// Move to the next key-value pair
			j = value + 1;

			while (j < token_count && tokens[j].start < end && tokens[j].start < tokens[value].end)
			{
				j++;
			}
		}

		// Include characters with fewer than 2 missing attributes
		if (missing_attributes < 2 && name_token != -1)
		{
			eligible_characters[eligible_count] = name_token;
			eligible_count++;
		}
	
		i = j - 1;
	}
	
	if (eligible_count == 0)
	{
		printf("No eligible characters found.\n");
		free(eligible_characters);
		free(buffer);
		return 1;
	}

	// Select random character
	srand(time(NULL));

	int random_index = rand() % eligible_count;
	int selected_token = eligible_characters[random_index];

	// Print selected character
	int name_length = tokens[selected_token].end - tokens[selected_token].start;

	char *name = malloc(name_length + 1);

	if (name == NULL)
	{
		free(eligible_characters);
		free(buffer);
		return 1;
	}

	strncpy(name, buffer + tokens[selected_token].start, name_length);
	name[name_length] = '\0';

	printf("Eligible characters: %d\n", eligible_count);
	printf("Selected character: %s\n", name);

	free(name);
	free(eligible_characters);
	free(buffer);
	
	return 0;
}
