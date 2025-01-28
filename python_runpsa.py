import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import json
import sv_ttk
import pywinstyles, sys


# Change the current working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)  # Set the current working directory

# File to store the path of the last used config file
LAST_USED_CONFIG_FILE = os.path.join(script_dir, "last_used_config.json")

# Initialize the GUI
root = tk.Tk()

# Global variables for the configuration values
raw_file_var = tk.StringVar()
psa_dir_var = tk.StringVar()
executables_dir_var = tk.StringVar()
output_file_var = tk.StringVar()
executables = []
sbedataprocessing_exe = ""

# Create an empty list to store the frames for each PSA file
psa_frames = []
psa_files_frame = tk.Frame(root)  # Initialize psa_files_frame as a Tkinter frame

# Function to override sv_ttk checkbox style
def override_checkbox_style():
    # Override the style for Checkbuttons
    style = ttk.Style()

    # Modify the default style used by Checkbuttons
    style.configure('TCheckbutton',
                    background='#2c2c2c',  # Dark background for the checkbox (for dark theme)
                    foreground='#ffffff',  # White text for the checkbox label
                    font=('Arial', 10))  # Adjust font if necessary

    # Ensure the focus highlights are appropriate
    style.map('TCheckbutton', foreground=[('active', 'yellow')])

# Function to select multiple raw .hex files
def select_raw_file():
    file_paths = filedialog.askopenfilenames(title="Select Raw .hex Files", filetypes=[("HEX files", "*.hex")])
    if file_paths:
        # Join the selected file paths into a single string with semicolons
        raw_file_var.set("; ".join(file_paths))  # Store the file paths in the StringVar

def select_psa_directory():
    # Prompt the user to select a directory
    dir_path = filedialog.askdirectory(title="Select Directory Containing .psa Files")
    
    if dir_path:  # Check if a directory was selected
        print(f"Directory selected: {dir_path}")  # Debugging line
        psa_dir_var.set(dir_path)
        load_psa_files(dir_path)  # Load the PSA files from the selected directory
    else:
        print("No directory selected.")  # Debugging line


# Function to edit the XML file for a selected PSA file
def edit_xml_file(psa_file, psa_dir):
    # Derive the path of the XML file based on the full PSA file path
    xml_file_path = os.path.splitext(os.path.join(psa_dir, psa_file))[0] + '.xml'  # Assuming XML file has the same name as PSA file

    if not os.path.isfile(xml_file_path):
        messagebox.showerror("Error", f"XML file not found for {psa_file}.")
        return

    # Open the XML file and load it into an ElementTree
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Create a simple text editor to allow the user to modify the XML
        editor_window = tk.Toplevel(root)  # Create a new window for editing
        editor_window.title(f"Editing {xml_file_path}")
        editor_window.geometry("600x400")

        text_editor = tk.Text(editor_window)
        text_editor.pack(fill=tk.BOTH, expand=True)
        text_editor.insert(tk.END, ET.tostring(root, encoding="unicode", method="xml"))

        # Function to save the changes made in the editor back to the XML file
        def save_xml_changes():
            try:
                # Save the updated XML content back to the file
                updated_xml_content = text_editor.get("1.0", tk.END)
                updated_tree = ET.ElementTree(ET.fromstring(updated_xml_content))
                updated_tree.write(xml_file_path)
                messagebox.showinfo("Success", f"XML file for {psa_file} has been updated successfully.")
                editor_window.destroy()  # Close the editor window after saving
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save XML changes: {e}")

        # Add a "Save" button to save the changes
        save_button = ttk.Button(editor_window, text="Save Changes", command=save_xml_changes)
        save_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to open XML file: {e}")

# Global variable to store the selected PSA directory
select_psa_directory = ""  # Global variable to store the selected PSA directory


def open_in_sbedataprocessing(psa_dir, psa_file, executable_name):
    # Construct the full path to the executable based on the provided executable name
    sbedataprocessing_exe = os.path.join(executables_dir_var.get(), executable_name)
    print(executable_name)

    # Check if the executable exists
    if not os.path.isfile(sbedataprocessing_exe):
        messagebox.showerror("Error", f"Executable '{executable_name}' not found in the selected executables directory: {executables_dir_var.get()}")
        return

    # Construct the full path to the PSA file
    psa_file_path = os.path.join(psa_dir, psa_file)
    
    # Normalize the paths to ensure consistent separators
    psa_file_path = os.path.normpath(psa_file_path)

    # Check if the PSA file exists
    if not os.path.isfile(psa_file_path):
        messagebox.showerror("Error", f"The PSA file '{psa_file}' does not exist.")
        return

    # Log the command to check for issues
    print(f"Running: {executable_name} {psa_file_path}")

    # Launch the executable with the PSA file as an argument
    try:
        result = subprocess.run([executable_name, '/p', psa_file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        print('RUN SUBPROCESS', result)
        print("Output:", result.stdout)
        print("Error:", result.stderr)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Executable '{executable_name}' not found at: {executable_name}")
    except subprocess.CalledProcessError as e:
        # Capture and display any error output
        messagebox.showerror("Error", f"Failed to open PSA file with {executable_name}: {e.stderr}")

def load_psa_files(psa_dir):
    global select_psa_directory  # Ensure we can check/set the path when necessary

    select_psa_directory = psa_dir  # Set the global PSA directory

    # Clear previous frames
    for frame in psa_frames:
        frame[0].destroy()  # Destroy only the frame widget (frame[0])

    psa_frames.clear()  # Clear the list of frames to avoid reusing old frames

    # List all .psa files in the selected directory
    psa_files = [f for f in os.listdir(psa_dir) if f.endswith('.psa')]

    if not psa_files:
        messagebox.showwarning("No Files Found", "No .psa files found in the selected directory.")
        return

    # Update the scrollable area with the PSA file entries
    update_psa_entries(psa_files)  # Pass the list of psa_files to the update_psa_entries function


def update_psa_entries(psa_files):
    # Clear the current PSA file entries
    for widget in psa_entries_frame.winfo_children():
        widget.destroy()

    # Create a row for each PSA file loaded dynamically
    for idx, psa_file in enumerate(psa_files):  # Use the psa_files passed to this function
        psa_frame = tk.Frame(psa_entries_frame)  # Add each file's row to the scrollable frame
        psa_frame.grid(row=idx, sticky="ew", pady=5)

        # PSA file name label
        psa_label = tk.Label(psa_frame, text=psa_file, width=30)
        psa_label.grid(row=0, column=0, padx=5)

        executable_dropdown = ttk.Combobox(psa_frame, values=["Select Executable Path"] + executables)
        executable_dropdown.grid(row=0, column=1, padx=5)

        # Order number entry (initially 1)
        order_entry = tk.Entry(psa_frame, width=5)
        order_entry.insert(0, str(idx + 1))  # Default order number is idx + 1
        order_entry.grid(row=0, column=2, padx=5)

        # Select/Deselect checkbox
        select_var = tk.BooleanVar(value=True)  # Default is selected
        select_checkbox = ttk.Checkbutton(psa_frame, text="Run", variable=select_var, style="TCheckbutton")
        select_checkbox.grid(row=0, column=3, padx=5)

        # Edit PSA Button to open the file in SBEDataprocessing
        edit_button = ttk.Button(psa_frame, text="Edit PSA", command=lambda psa_file=psa_file, psa_dir=select_psa_directory, executable_dropdown=executable_dropdown: open_in_sbedataprocessing(psa_dir, psa_file, executable_dropdown.get()))
        edit_button.grid(row=0, column=4, padx=5)

        # Store the widgets in a tuple for later use
        psa_frames.append((psa_frame, psa_file, executable_dropdown, order_entry, select_var, select_checkbox, edit_button))

    # Update the scrollable region of the canvas based on the number of entries
    psa_entries_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Function to load a configuration file
def load_config():
    # Prompt the user to select a configuration file
    config_file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if not config_file_path:
        messagebox.showerror("Error", "No configuration file selected.")
        return

    try:
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
            # Save the path of the selected config file as the new "last used config file"
            save_last_used_config(config_file_path)
            load_config_to_gui(config)  # Update the GUI with the loaded config
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load configuration: {e}")

def save_last_used_config(file_path):
    try:
        normalized_path = os.path.normpath(file_path)
        with open(LAST_USED_CONFIG_FILE, "w") as file:
            json.dump({"config_file_path": normalized_path}, file)
    except Exception as e:
        print(f"Error saving last used config: {e}")

def load_last_used_config():
    print("Attempting to load last used config...")
    print(f"LAST_USED_CONFIG_FILE: {LAST_USED_CONFIG_FILE}")
    if os.path.exists(LAST_USED_CONFIG_FILE):
        try:
            # First, load the LAST_USED_CONFIG_FILE to get the path to the actual config file
            with open(LAST_USED_CONFIG_FILE, "r") as file:
                last_used_config = json.load(file)
                config_file_path = last_used_config.get("config_file_path")
                print(config_file_path)
                
                if config_file_path and os.path.exists(config_file_path):
                    # Now, load the actual config file
                    with open(config_file_path, "r") as config_file:
                        config = json.load(config_file)
                        
                        # Handle missing keys gracefully
                        psa_dir = config.get("psa_dir", "")
                        if not psa_dir:
                            print("Warning: 'psa_dir' not found in the configuration.")
                            messagebox.showwarning("Warning", "'psa_dir' not found in the configuration.")

                        load_config_to_gui(config)
                else:
                    messagebox.showerror("Error", "The config file path is invalid or does not exist.")
        except Exception as e:
            print(f"Error loading last used config: {e}")  # Debugging line
            messagebox.showerror("Error", f"Error loading last used config: {e}")
    else:
        print("No last used config file found.")
        messagebox.showwarning("Warning", "No last used config file found.")

def load_config_to_gui(config):
    # Update the GUI with values from the loaded configuration
    raw_file_var.set(config.get("raw_file", ""))
    psa_dir_var.set(config.get("psa_dir", ""))
    executables_dir_var.set(config.get("executables_dir", ""))
    output_file_var.set(config.get("output_file", ""))

    # Load executables list
    global executables
    executables = config.get("executables", [])

    # Load PSA files and their respective data
    load_psa_files(config["psa_dir"])

    # Update PSA file data from the config
    for psa_data in config["psa_files"]:
        for psa_frame, psa_file, executable_dropdown, order_entry, select_var, select_checkbox, edit_button in psa_frames:  # Updated loop
            # Check if the psa_frame has the correct PSA file
            if psa_file == psa_data["psa_file"]:
                # Update the executable dropdown
                executable = psa_data["executable"]
                executable_name = os.path.basename(executable) if executable else "Select Executable Path"
                executable_dropdown.set(executable_name)

                # Update the order entry
                order_entry.delete(0, tk.END)
                order_entry.insert(0, psa_data["order"])

                # Update the checkbox
                select_var.set(psa_data["selected"])  # Set the checkbox state

                # Update the Checkbutton state
                if select_var.get():
                    select_checkbox.state(["selected"])
                else:
                    select_checkbox.state(["!selected"])

# Function to select the directory containing executable files
def select_executables_directory():
    # Allow the user to select the directory containing executable files
    dir_path = filedialog.askdirectory(title="Select Directory Containing Executables")
    if dir_path:
        # List all executable files in the selected directory
        global executables
        executables = [f for f in os.listdir(dir_path) if f.endswith('.exe')]
        print(f"Available executables: {executables}")

        # Update dropdowns with the available executables
        for _, executable_dropdown, _, _ in psa_frames:
            executable_dropdown["values"] = ["Select Executable Path"] + executables
            executable_dropdown.set("Select Executable Path")

# Function to save the current configuration to a user-selected config file
def save_config():
    # Ask the user for the file path where the configuration should be saved
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if not file_path:
        return  # If no file is selected, exit the function

    config = {
        "raw_file": raw_file_var.get(),
        "psa_dir": psa_dir_var.get(),
        "executables_dir": executables_dir_var.get(),
        "executables": executables,
        "output_file": output_file_var.get(),  # Add output file path
        "psa_files": []
    }

    for psa_frame, psa_file, executable_dropdown, order_entry, select_var, select_checkbox, edit_button in psa_frames:  # Unpack the 6 values and ignore the 6th value (edit_button)
        executable = executable_dropdown.get()
        order = order_entry.get()

        # Save the executable file path instead of just the name
        executable_path = ""
        if executable != "Select Executable Path":
            executable_path = os.path.join(executables_dir_var.get(), executable)

        selected = select_var.get()

        config["psa_files"].append({
            "psa_file": psa_file,
            "executable": executable_path,
            "order": order,
            "selected": selected
        })

    try:
        with open(file_path, "w") as f:
            json.dump(config, f, indent=4)
        messagebox.showinfo("Configuration Saved", "Your configuration has been saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save configuration: {e}")

def process_data():
    raw_files = raw_file_var.get().split("; ")  # Split the file paths back into a list
    psa_dir = psa_dir_var.get()
    output_file_dir = output_file_var.get()

    if not raw_files or not all(os.path.isfile(f) for f in raw_files):
        messagebox.showerror("Error", "Please select valid raw .hex files.")
        return

    if not os.path.isdir(psa_dir):
        messagebox.showerror("Error", "Please select a valid directory containing .psa files.")
        return

    if not output_file_dir:
        messagebox.showerror("Error", "Please select an output file path.")
        return

    selected_psa_files = []
    for psa_frame, psa_file, executable_dropdown, order_entry, select_var, select_checkbox, edit_button in psa_frames:
        if select_var.get():
            selected_executable = executable_dropdown.get()
            if selected_executable == "Select Executable Path":
                messagebox.showerror("Error", f"Please select an executable for {psa_file}.")
                return
            try:
                order = int(order_entry.get())
            except ValueError:
                messagebox.showerror("Error", f"Invalid order number for {psa_file}. Please enter a valid integer.")
                return

            executable_path = os.path.join(executables_dir_var.get(), selected_executable) if selected_executable != "Select Executable Path" else ""
            selected_psa_files.append((psa_file, executable_path, order))

    if not selected_psa_files:
        messagebox.showerror("Error", "Please select at least one .psa file to process.")
        return

    selected_psa_files.sort(key=lambda x: x[2])

    # Process each selected raw file
    for raw_file in raw_files:
        for psa_file, executable, _ in selected_psa_files:
            psa_file_path = os.path.join(psa_dir, psa_file)
            print(f"Running {executable} for {psa_file} with raw file {raw_file}")

            base_name = os.path.splitext(os.path.basename(raw_file))[0]
            output_file = f"{base_name}.cnv"

            if "DatCnvW" in os.path.basename(executable):
                input_file = raw_file
            else:
                input_file = os.path.join(output_file_dir, output_file)

            command = [
                executable,
                f"/i{input_file}",
                f"/o{output_file_dir}",
                f"/f{output_file}",
                f"/p{psa_file_path}",
                "/s"
            ]

            try:
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
                if result.returncode != 0:
                    messagebox.showerror("Error", f"Error running {executable} for {psa_file}: {result.stderr}")
                    return  # Stop further processing if there's an error
                else:
                    print(f"{executable} ran successfully for {psa_file}: {result.stdout}")
            except FileNotFoundError:
                messagebox.showerror("Error", f"Executable not found at: {command[0]}")
                return  # Stop further processing if executable is not found
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
                return  # Stop further processing if any other unexpected error occurs

    messagebox.showinfo("Processing Complete", "Selected .psa files have been processed.")


def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#242424" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

# First, apply the theme
sv_ttk.set_theme("dark")

# Call the override function to fix the checkbox behavior
override_checkbox_style()

# Then, apply the title bar theme
apply_theme_to_titlebar(root)

root.title("CTD Processor ")

# Set window icon
try:
    root.iconphoto(True, tk.PhotoImage(file=r"C:\Users\bonny\github\ctd_processing\icon.png"))  # Ensure the file path is correct
except Exception as e:
    print(f"Error setting icon: {e}")

# Set window size and background color
root.minsize(670, 300)

# Configure the grid layout
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=0)
root.grid_rowconfigure(6, weight=0)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Variables
raw_file_var = tk.StringVar()
psa_dir_var = tk.StringVar()
executables_dir_var = tk.StringVar()
output_file_var = tk.StringVar()
psa_frames = []
executables = []

# Layout (unchanged, just for reference)
tk.Label(root, text="Select Raw .hex File:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=raw_file_var, width=50).grid(row=0, column=1, padx=10, pady=5, sticky="ew")
ttk.Button(root, text="Browse", command=select_raw_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Select Directory Containing .psa Files:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=psa_dir_var, width=50).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
ttk.Button(root, text="Browse", command=select_psa_directory).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Select Directory Containing Executables:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=executables_dir_var, width=50).grid(row=2, column=1, padx=10, pady=5, sticky="ew")
ttk.Button(root, text="Browse", command=select_executables_directory).grid(row=2, column=2, padx=10, pady=5)

tk.Label(root, text="Select Output File Directory:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=output_file_var, width=50).grid(row=3, column=1, padx=10, pady=5, sticky="ew")
ttk.Button(root, text="Browse", command=lambda: output_file_var.set(filedialog.askdirectory(title="Select Output Directory"))).grid(row=3, column=2, padx=10, pady=5)

# Frame for PSA files with scrolling functionality
psa_files_frame = tk.Frame(root)
psa_files_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

# Create a canvas to enable scrolling
canvas = tk.Canvas(psa_files_frame)
canvas.grid(row=0, column=0, sticky="nsew")

# Create a vertical scrollbar and attach it to the canvas
scrollbar = ttk.Scrollbar(psa_files_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the PSA file entries
psa_entries_frame = tk.Frame(canvas)

# Add this frame to the canvas window (a special canvas feature)
canvas.create_window((0, 0), window=psa_entries_frame, anchor="nw")

# Make the canvas expandable so that it fills the available space
psa_files_frame.grid_rowconfigure(0, weight=1)
psa_files_frame.grid_columnconfigure(0, weight=1)

# Process Data Button
ttk.Button(root, text="Process Data", command=process_data).grid(row=5, column=1, padx=10, pady=20)

# Save Configuration Button
ttk.Button(root, text="Save Configuration", command=save_config).grid(row=6, column=0, padx=10, pady=20)

# Load Configuration Button
ttk.Button(root, text="Load Configuration", command=load_config).grid(row=6, column=2, padx=10, pady=20)

sv_ttk.set_theme("dark")

def start_application():
    print('Starting application...')
    load_last_used_config()  # Try loading the last used config on startup

    # After loading the config, start the main event loop
    print('Starting main event loop.')
    root.mainloop()

# Main entry point
if __name__ == "__main__":
    print("Script executed directly.")
    try:
        start_application()  # Ensure the application starts
    except Exception as e:
        print(f"Error starting application: {e}")



