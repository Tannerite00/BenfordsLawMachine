import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import tkinter.simpledialog
import json

class TemplateEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Audit Template Editor")

        # Create a list to store templates
        self.templates = []
        self.current_template = None

        # Create a frame to hold the template editor
        template_frame = ttk.LabelFrame(root, text="Audit Template")
        template_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Create a text field to enter audit steps
        self.step_entry = ttk.Entry(template_frame)
        self.step_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Create a button to add steps
        add_button = ttk.Button(template_frame, text="Add Step", command=self.add_step)
        add_button.grid(row=0, column=1, padx=5, pady=5)

        # Create a listbox to display added steps
        self.step_listbox = tk.Listbox(template_frame, selectmode="single", height=10)
        self.step_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Create a button to delete selected steps
        delete_button = ttk.Button(template_frame, text="Delete Step", command=self.delete_step)
        delete_button.grid(row=2, column=0, padx=5, pady=5)

        # Create a frame for saving and loading templates
        save_load_frame = ttk.LabelFrame(root, text="Save/Load Template")
        save_load_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Create buttons for saving and loading templates
        save_button = ttk.Button(save_load_frame, text="Save Template", command=self.save_template)
        save_button.grid(row=0, column=0, padx=5, pady=5)

        load_button = ttk.Button(save_load_frame, text="Load Template", command=self.load_template)
        load_button.grid(row=0, column=1, padx=5, pady=5)

        # Create a dropdown for selecting templates
        self.template_dropdown = ttk.Combobox(save_load_frame, values=[template["name"] for template in self.templates])
        self.template_dropdown.grid(row=0, column=2, padx=5, pady=5)
        self.template_dropdown.bind("<<ComboboxSelected>>", self.select_template)

    def add_step(self):
        step_text = self.step_entry.get()
        if step_text:
            self.current_template = step_text
            self.templates.append(step_text)
            self.step_listbox.insert(tk.END, step_text)
            self.step_entry.delete(0, tk.END)


    def delete_step(self):
        selected_index = self.step_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.current_template["steps"].pop(index)
            self.step_listbox.delete(index)

    def save_template(self):
        if self.current_template:
            # Create a new template with a name entered by the user
            template_name = tk.simpledialog.askstring("Template Name", "Enter a name for the template:")
            if template_name:
                new_template = {"name": template_name, "steps": self.current_template["steps"]}
                self.templates.append(new_template)

                # Update the template dropdown
                self.template_dropdown["values"] = [template["name"] for template in self.templates]
                self.template_dropdown.set(template_name)


    def load_template(self):
        selected_template_name = self.template_dropdown.get()
        for template in self.templates:
            if template["name"] == selected_template_name:
                self.current_template = template
                self.step_listbox.delete(0, tk.END)
                for step in self.current_template["steps"]:
                    self.step_listbox.insert(tk.END, step)
                break

    def select_template(self, event):
        selected_template_name = self.template_dropdown.get()
        for template in self.templates:
            if template["name"] == selected_template_name:
                self.current_template = template
                self.step_listbox.delete(0, tk.END)
                for step in self.current_template["steps"]:
                    self.step_listbox.insert(tk.END, step)
                break

def main():
    root = tk.Tk()
    app = TemplateEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
