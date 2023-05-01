import requests
import tkinter as tk
from tkinter import ttk, scrolledtext
from bs4 import BeautifulSoup
import threading
import webbrowser
import NexusWebScraperAlgorithm
import time

# .exe made with PyInstaller
# PyInstaller --onefile --noconsole NexusEZFileFinder.py

url = "https://www.nexusmods.com/newvegas/mods/76811?tab=files&file_id={}"
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

def update_title():
    if find_deleted_mod.is_running:
        elapsed_time = time.time() - find_deleted_mod.start_time
        elapsed_time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        window.title("Nexus EZ Deleted Mod File Finder - {}".format(elapsed_time_str))
        window.after(1000, update_title)
    else:
        window.title("Nexus EZ Deleted Mod File Finder")

def get_increment():
    if auto_search_var.get():
        return 0
    else:
        increment_value = searchID_entry.get()
        try:
            increment = int(increment_value)
        except ValueError:
            error_label.config(text="Invalid increment value entered", fg="red")
            return
        return increment

def find_deleted_mod():
    if not hasattr(find_deleted_mod, "is_running"):
        # First time the button is pressed, initialize the variable
        find_deleted_mod.is_running = False

    # Get the mod URL from the entry box and check if it's valid
    mod_url = url_entry.get()
    file_id_error = "URL must not include file ID"
    if "https://www.nexusmods.com" not in mod_url:
        error_label.config(text="Invalid URL entered", fg="red")
        return
    
    if not any(char.isdigit() for char in mod_url):
        error_label.config(text="Invalid URL entered", fg="red")
        return

    elif "?tab=files&file_id=" in mod_url:
        error_label.config(text=file_id_error, fg="red")
        return
    
    elif "?" in mod_url:
        error_label.config(text=file_id_error, fg="red")
        return
    
    elif "users" in mod_url:
        error_label.config(text=file_id_error, fg="red")
        return    
    
    elif "tab" in mod_url:
        error_label.config(text=file_id_error, fg="red")
        return
    
    elif "=" in mod_url:
        error_label.config(text=file_id_error, fg="red")
        return
    
    elif "file" in mod_url:
        error_label.config(text=file_id_error, fg="red")
        return
    
    elif "id" in mod_url:
        error_label.config(text=file_id_error, fg="red")
        return
    
    else:
        error_label.config(text="")

    if find_deleted_mod.is_running:
        # Stop web scraping loop
        find_deleted_mod.is_running = False
        log_scroll_box.insert(tk.END, "Web scraping stopped\n")
        find_button.config(text="Find Deleted Mod", relief=tk.RAISED)
    else:
        # Start web scraping loop
        error_label.config(text="Valid URL entered", fg="green")
        find_deleted_mod.is_running = True
        find_deleted_mod.start_time = time.time()
        update_title()

        # Get the increment value entered by the user
        try:
            increment = get_increment()
            found_mods_scroll_box.insert(tk.END, "Calculating starting file ID \n (Application may hang, please wait...) \n \n")
            found_mods_scroll_box.update_idletasks()
            found_mods_scroll_box.after(1)
            if auto_search_var.get():
                NexusWebScraperAlgorithm.num_pages = int(pageScrape_entry.get())
                increment = int(NexusWebScraperAlgorithm.main(url_entry.get()))
        except ValueError:
            error_label.config(text="Invalid increment value entered", fg="red")
            return
        # Set the URL to the mod page and add the file ID suffix
        url = f"{mod_url}?tab=files&file_id={{}}"
        found_mods_scroll_box.insert(tk.END, "Starting at file ID " + str(increment) + "\n \n")
        found_mods_scroll_box.update_idletasks()

        def scrape():
            nonlocal increment  # Declare increment as a nonlocal variable
            while find_deleted_mod.is_running:
                # Try to connect to the website
                try:
                    response = session.get(url.format(increment), timeout=60)
                    log_scroll_box.insert(tk.END, "Connected to: " + response.url + "\n" + "\n")
                    log_scroll_box.see(tk.END)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    main_content = soup.find('div', {'id': 'mainContent', 'class': 'wrapper'})
                    text_spans = main_content.find_all('span')
                    # Check if the string exists in the content
                    if "This file has been removed" in response.text:
                        increment += 1
                        continue
                    elif "Object not found." in response.text:
                        increment += 1

                    elif "The mod you were looking for couldn't be found" in response.text:
                        increment += 1
                        continue

                    elif "The author of this mod has not published it yet" in response.text:
                        increment += 1
                        continue

                    elif "This mod has been set to hidden" in response.text:
                        increment += 1
                        continue

                    elif "If you're unable to see a file you've previously downloaded, it may have been archived." in response.text:
                        increment += 1
                        continue

                    else:
                        found_mods_scroll_box.insert(tk.END, text_spans[1].text.strip() + "\n")
                        found_mods_scroll_box.insert(tk.END, response.url + "\n\n", ("hyperlink", response.url))
                        found_mods_scroll_box.see(tk.END)
                        increment += 1
                        continue

                # Handle connection errors
                except requests.exceptions.RequestException as e:
                    log_scroll_box.insert(tk.END, str(e) + "\n")
                    found_mods_scroll_box.insert(tk.END, "Connection error, please try again...\n",  fg="red")
                    break

            # Reset button properties when web scraping loop is finished
            find_button.config(text="Find Deleted Mod", relief=tk.RAISED)

        # Update button properties and start web scraping in a separate thread
        find_button.config(text="Stop Searching", relief=tk.SUNKEN)
        log_scroll_box.delete('1.0', tk.END)  # Clear the log
        thread = threading.Thread(target=scrape)
        thread.start()
        # Periodically check for new messages to display in the log scroll box
        window.after(100, check_log_scroll_box, thread)

def check_log_scroll_box(thread):
    if window.winfo_exists():
        window.after(100, check_log_scroll_box, thread)
        # This is needed to update the GUI from the main thread
        log_scroll_box.update_idletasks()
    else:
        thread.join()

# Create GUI window
window = tk.Tk()
window.geometry("500x500")
window.resizable(False, False)
window.title("Nexus EZ Deleted Mod File Finder")


# Create notebook for tabs
notebook = ttk.Notebook(window)
notebook.pack(pady=10)

# Create Found Mods tab
found_mods_tab = tk.Frame(notebook)
notebook.add(found_mods_tab, text="Find Mods")

my_label1 = tk.Label(found_mods_tab, text="Nexus EZ Deleted Mod File Finder", font="Arial")
my_label1.pack(pady=12)

# Create error label for invalid URLs
error_label = tk.Label(found_mods_tab, text="", fg="red")
error_label.pack()

def limit_input(*args):
    value = entry.get()
    if len(value) > 10:
        entry.set(value[:100])

entry = tk.StringVar()
entry.trace("w", limit_input)

# Create entry box for mod URL
url_entry = tk.Entry(found_mods_tab, width=50, textvariable=entry)
url_entry.pack(pady=10)

# Create Find Deleted Mod button
find_button = tk.Button(found_mods_tab, text="Find Deleted Files", command=find_deleted_mod)
find_button.pack(pady=20)

my_label2 = tk.Label(found_mods_tab, text="Files Found:", font="Arial")
my_label2.pack(pady=12)

# Create scroll box to display found mod URLs
found_mods_scroll_box = scrolledtext.ScrolledText(found_mods_tab, height=10, width=45)
found_mods_scroll_box.pack(pady=10)

def open_hyperlink(event):
    index = found_mods_scroll_box.index(tk.CURRENT)
    tags = found_mods_scroll_box.tag_names(index)

    if "hyperlink" in tags:
        url = found_mods_scroll_box.get(index + " linestart", index + " lineend")
        webbrowser.open(url)

# Bind function to left mouse click event on hyperlink tags
found_mods_scroll_box.tag_configure("hyperlink", foreground="blue", underline=True)
found_mods_scroll_box.bind("<Button-1>", open_hyperlink)

# Create error label for invalid URLs
date_version = tk.Label(found_mods_tab, text="Ver 0.2 | 09/04/2023", anchor="e")
date_version.pack()

# Create Log tab
log_tab = tk.Frame(notebook)
notebook.add(log_tab, text="Log")

# Create scroll box to display log
log_scroll_box = scrolledtext.ScrolledText(log_tab, height=20, width=50)
log_scroll_box.pack(pady=10)

# Create Search Options tab
search_options_tab = tk.Frame(notebook)
notebook.add(search_options_tab, text="Search Options")

def validate_entry(value):
    if value.isdigit():
        return True
    elif value == "":
        return True
    else:
        return False

validate_int = window.register(validate_entry)

my_label6 = tk.Label(search_options_tab, text="Max Pages to Scrape +/-", wraplength=400, anchor="nw")
my_label6.grid(row=1, column=0, pady=(10, 0), padx=10, sticky="nw")

pageScrape_entry = tk.Entry(search_options_tab, width=10, validate="key", validatecommand=(validate_int, "%P"))
pageScrape_entry.insert(0, 5)
pageScrape_entry.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="nw")

my_label4 = tk.Label(search_options_tab, text="Search Manually from File ID:", wraplength=400, anchor="nw")
my_label4.grid(row=2, column=0, pady=(10, 0), padx=10, sticky="nw")

searchID_entry = tk.Entry(search_options_tab, width=10, validate="key", validatecommand=(validate_int, "%P"))
searchID_entry.insert(1, 1)
searchID_entry.grid(row=2, column=1, pady=(10, 0), padx=10, sticky="nw")

entry1 = pageScrape_entry.get()
entry2 = searchID_entry.get()

def auto_search_checkbox_clicked():
    if auto_search_var.get():
        searchID_entry.config(state="disabled")
        pageScrape_entry.config(state="normal")
        searchID_entry.insert(0, entry2)
    else:
        searchID_entry.config(state="normal")
        pageScrape_entry.config(state="disabled")
        pageScrape_entry.insert(0, entry1)

auto_search_var = tk.BooleanVar(value=True)
auto_search_checkbox = tk.Checkbutton(search_options_tab, text="Auto-Search Algorithm Enabled", variable=auto_search_var, command=auto_search_checkbox_clicked)
auto_search_checkbox.grid(row=0, column=0, padx=10, pady=10, sticky="w")
auto_search_checkbox_clicked()

# Create Help tab
help_tab = tk.Frame(notebook)
notebook.add(help_tab, text="Help")

my_label3 = tk.Label(help_tab, text="\n \n \n \n URL format must be: https://www.nexusmods.com/gamenamehere/mods/1234 or else the scraping process won't work. It also must not include any file ID within the URL. \n \n The searching algorithm may not always be accurate based on the sample data, so it can be useful to disable it and cross-reference file IDs from files published at similar dates and times from that game's Nexus page, in order to start from a specific number manually. \n \n Please note that this only applies to Nexus mods deleted after July-August 2021 due to their newer policy of file archiving. I cannot account for any permanently deleted files before that date.", font="Arial", wraplengt=400, anchor="w")
my_label3.pack(pady=10)

searchID_entry.insert(0, 1)

# Start GUI event loop
window.mainloop()