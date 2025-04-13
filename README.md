👨‍💻 EYESCRIBE KEYBOARD: Enhanced Assistive Technology 👨‍💻





🔑 Global Variables:

root: The heart of the application. It creates the main window using ThemedTk() from the ttkthemes library to add a sleek, modern theme to the UI.

style: A variable that holds the style settings for the elements, giving you control over the fonts, colors, and general appearance of the interface.

timeout_id: Stores the ID for the timeout function that updates the suggestions dynamically after a brief delay, allowing for smooth and non-intrusive interaction.

suggestion_labels: A list that stores all the suggestion labels shown on the interface. These labels are updated in real-time based on user input.

word_freq_dist: A FreqDist object from NLTK, leveraging the Brown corpus. This allows the system to predict commonly used words for an enhanced predictive typing experience.






📚 Custom Dictionary Handling:

custom_dictionary: A set that contains user-added words, ensuring no duplicates and keeping the vocabulary unique for each user.

save_custom_dictionary: This function saves the custom dictionary to a JSON file, ensuring that user-added words are retained across application sessions, offering persistence.

load_custom_dictionary: Loads the custom dictionary from the JSON file (if available). If not found, it returns an empty set, allowing the user to build their dictionary from scratch or continue from the last session.





💡 Suggestion System:

update_suggestion_labels(suggestions): A dynamic function that clears existing suggestion labels (to avoid overlap) and updates them with new suggestions. Each suggestion is displayed with appropriate padding and consistent fonts, ensuring a clean, professional UI.





🔮 Word Prediction & User Customization:

Frequency Distribution: FreqDist analyzes the Brown corpus, making the suggestion system smarter by predicting commonly used words. This predictive model ensures the suggestions are meaningful and intuitive.

Custom Dictionary & User Input: When a user types a word that isn’t in the standard dictionary but is in their custom dictionary, the system will suggest it. This adds a personalized touch and allows users to further customize their experience. Users can easily add new words to their dictionary via an interface option, and these words will be saved for future use.





🎨 Enhanced UI/UX:

Suggestions Display: The interface dynamically updates the suggestions, which are shown either horizontally at the top or side of the keyboard, ensuring a fluid and responsive user experience.

Styling: The use of the ttkthemes library gives the interface a modern, visually appealing look. Styling options allow for adjusting fonts, background colors, and other visual elements to fit your personal preferences or accessibility needs.




🔄 Working Flow of Eyescribe Keyboard:


User Input: When the user begins typing, the system listens to each keystroke and processes the input.

Word Prediction: Using the NLTK FreqDist object, the system analyzes the user's input and predicts the next word, offering suggestions based on common usage and context.

Custom Word Check: If the typed word isn’t in the standard dictionary, the system checks the custom_dictionary. If found, it offers that word as a suggestion, giving the user the ability to select it instantly.

Displaying Suggestions: As the user types, the update_suggestion_labels function updates the displayed suggestions, showing words the user might want to type next. Suggestions are clickable and input automatically when selected.

Adding Custom Words: If the user types a new word, they can add it to their custom dictionary by clicking an "Add Word" button, which updates the dictionary and saves it for future use.

Saving & Loading Data: The custom_dictionary is saved to a JSON file and loaded at startup, ensuring all custom words remain across sessions.



