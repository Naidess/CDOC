# C Code Documenter

## Description
This program processes C source files to extract special comments that document functions, such as their name, parameters, return values, and other details. It generates a styled HTML page presenting this information in a readable format.

## Requirements

### Required Python Libraries
- `customtkinter`
- `tkinter`

### Required Files
- **C source code** with comments structured in a special format.
- `styles.css` file for styling the generated HTML (included in the project).

## Project Structure
The project includes the following files:
- `CDOC.py`: Main program code.
- `styles.css`: CSS file for the HTML output.
- `README.md`: Program instructions.
- `division.c`: C code example.

## Usage

1. **Prepare the C source file:**
   - The source code must include comments in the following format:
     ```c
     /**
      * @name Function name
      * @param name Parameter description
      * @return Return value description
      * @error Possible error descriptions
      * @extra Any additional information
      **/
     ```

2. **View the result:**
   - The program provides an option to open the generated webpage, redirecting to it when selected. 
    It will also create an HTML file in the project folder named `(source_file_name)_documentation.html`. 

---
