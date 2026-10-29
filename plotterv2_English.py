"""Electric Charges and Fields Plotter."""

# A.M. - Itzlofer

from sys import exit as sys_exit

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk

# Icon credits:
# Atom science molecule medical Icon by Icon Factory on
# https://icon-icons.com/authors/1444-icon-factory

# Fonts and colors:
BACKGROUND_COLOR, ACCENT_COLOR = "#f4f6fa", "#2f6fed"
TITLE_FONT = ("Segoe UI", 14, "bold")
TEXT_FONT = ("Segoe UI", 10, "bold")

# Main window:
root = tk.Tk()
root.title("Charges and Fields Plotter")
root.configure(bg=BACKGROUND_COLOR)

# Button styles:
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=TEXT_FONT, padding=6)
style.configure(
    "Acento.TButton",
    font=("Segoe UI", 10, "bold"),
    padding=6,
    foreground=BACKGROUND_COLOR,
    background=ACCENT_COLOR,
)
style.map("Acento.TButton", background=[("active", ACCENT_COLOR)])

# Header and text:
tk.Label(
    root,
    text="Charges and Fields Plotter V2",
    font=TITLE_FONT,
    bg=BACKGROUND_COLOR,
).pack(pady=(20, 5))

label1 = tk.Label(
    root,
    text=(
        "Click the button to add charges. Then enter the "
        "X, Y, and charge values in each row."
    ),
    wraplength=320,
    font=TEXT_FONT,
    bg=BACKGROUND_COLOR,
    justify="center",
)
label1.pack(pady=(0, 15), padx=20)

# Icon credits:
icon_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
icon_frame.pack(pady=5, side="bottom")
tk.Label(
    icon_frame,
    text=(
        "Icon used: Atom science molecule medical Icon by Icon "
        "Factory on https://icon-icons.com/authors/1444-icon-factory"
    ),
).pack(side="bottom", padx=20)

# Canvas and scrollbar for inputs:
scroll_container_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
scroll_container_frame.pack(pady=5, fill="both", expand=True)

input_canvas = tk.Canvas(
    scroll_container_frame, bg=BACKGROUND_COLOR, highlightthickness=0, height=250
)
input_scrollbar = ttk.Scrollbar(
    scroll_container_frame, orient="vertical", command=input_canvas.yview
)
input_canvas.configure(yscrollcommand=input_scrollbar.set)
input_canvas.pack(side="left", fill="both", expand=True)
input_scrollbar.pack(side="right", fill="y")

inputs_frame = tk.Frame(input_canvas, bg=BACKGROUND_COLOR)
inputs_frame.grid_columnconfigure(0, weight=1)
canvas_window_id = input_canvas.create_window(
    (0, 0), window=inputs_frame, anchor="nw"
)

# Grid density control:
density_var = tk.IntVar(value=30)

density_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
density_frame.pack(pady=(0, 10))
tk.Label(
    density_frame,
    text="Vector density:",
    font=TEXT_FONT,
    bg=BACKGROUND_COLOR,
).pack(side="left", padx=(0, 8))
tk.Scale(
    density_frame,
    from_=5,
    to=200,
    orient="horizontal",
    variable=density_var,
    showvalue=True,
    length=200,
    bg=BACKGROUND_COLOR,
    highlightthickness=1,
    troughcolor=ACCENT_COLOR,
).pack(side="left")
ttk.Button(
    density_frame,
    text="Default density",
    style="TButton",
    command=lambda: density_var.set(30),
).pack(side="right", padx=6)


# Scrolling and resizing the input area:
def update_scroll_region(event=None):
    """Recalculate the scrollable area based on the canvas content."""
    input_canvas.configure(scrollregion=input_canvas.bbox("all"))


def adjust_frame_width(event):
    """Match the inner frame width to the canvas when resizing."""
    input_canvas.itemconfig(canvas_window_id, width=event.width)


def on_mouse_wheel(event):
    """Scroll vertically through the canvas using the mouse wheel."""
    input_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


inputs_frame.bind("<Configure>", update_scroll_region)
input_canvas.bind("<Configure>", adjust_frame_width)
input_canvas.bind_all("<MouseWheel>", on_mouse_wheel)


# Adjust an Entry width to fit its content:
def adjust_entry_width(event):
    """Adjust an Entry width to fit its content."""
    event.widget.config(width=int(min(30, len(event.widget.get()))))


# Input rows (X, Y, charge value):
current_row = 0
x_entries, y_entries, charge_entries = [], [], []

# Each item: (row_frame, x_entry, y_entry, charge_entry, number_label)
row_widgets = []


def renumber_rows():
    """Update the number shown in each row after one is deleted."""
    for i, (_, _, _, _, number_label) in enumerate(row_widgets):
        number_label.config(text=f"Charge {i + 1}:")


def delete_row(row_frame, input1, input2, input3):
    """Delete an input row and its associated widgets."""
    row_frame.destroy()
    x_entries.remove(input1)
    y_entries.remove(input2)
    charge_entries.remove(input3)
    row_widgets[:] = [f for f in row_widgets if f[0] != row_frame]
    renumber_rows()


def create_input_row(row_index):
    """Create an input row (X, Y, charge value) in the form."""
    row_frame = tk.Frame(
        inputs_frame,
        bg=BACKGROUND_COLOR,
        highlightbackground=ACCENT_COLOR,
        highlightthickness=1,
        bd=0,
    )
    # Without sticky, the widget is centered in the cell.
    row_frame.grid(row=row_index, column=0, pady=6)
    row_widgets.append([row_frame, None, None, None, None])

    number_label = tk.Label(
        row_frame,
        font=TEXT_FONT,
        text=f"Charge {row_index + 1}:",
        bg=BACKGROUND_COLOR,
        fg=ACCENT_COLOR,
    )
    number_label.grid(row=0, column=0, padx=(8, 10), pady=6, sticky="e")

    tk.Label(
        row_frame, font=TEXT_FONT, text="X:", bg=BACKGROUND_COLOR
    ).grid(row=0, column=1, padx=(0, 1), pady=4)
    input1 = tk.Entry(
        row_frame,
        width=2,
        font=TEXT_FONT,
        highlightthickness=1,
        highlightcolor=ACCENT_COLOR,
    )
    input1.grid(row=0, column=2, padx=(0, 6), pady=4)
    input1.bind("<KeyRelease>", adjust_entry_width)
    x_entries.append(input1)

    tk.Label(
        row_frame, font=TEXT_FONT, text="Y:", bg=BACKGROUND_COLOR
    ).grid(row=0, column=3, padx=(0, 1), pady=4)
    input2 = tk.Entry(
        row_frame,
        width=2,
        font=TEXT_FONT,
        highlightthickness=1,
        highlightcolor=ACCENT_COLOR,
    )
    input2.grid(row=0, column=4, padx=(0, 6), pady=4)
    input2.bind("<KeyRelease>", adjust_entry_width)
    y_entries.append(input2)

    tk.Label(
        row_frame,
        font=TEXT_FONT,
        text="Charge value:",
        bg=BACKGROUND_COLOR,
    ).grid(row=0, column=5, padx=(0, 2), pady=4)
    input3 = tk.Entry(
        row_frame,
        width=2,
        font=TEXT_FONT,
        highlightthickness=1,
        highlightcolor=ACCENT_COLOR,
    )
    input3.grid(row=0, column=6, padx=(0, 4), pady=4)
    input3.bind("<KeyRelease>", adjust_entry_width)
    charge_entries.append(input3)

    delete_button = tk.Button(
        row_frame,
        text="✕",
        font=TEXT_FONT,
        fg="white",
        bg="#e0453c",
        bd=0,
        padx=6,
        command=lambda: delete_row(row_frame, input1, input2, input3),
    )
    delete_button.grid(row=0, column=7, padx=(4, 8), pady=4)

    row_widgets[-1] = [row_frame, input1, input2, input3, number_label]


create_input_row(current_row)  # First row (KEEP AS AN EXAMPLE)


def add_input():
    """Add a new input row for an additional charge."""
    global current_row
    current_row += 1
    create_input_row(current_row)


# Buttons:
frame_botones = tk.Frame(root, bg=BACKGROUND_COLOR)
frame_botones.pack(side="bottom", pady=20)
ttk.Button(
    frame_botones,
    text="+ Add charge",
    style="TButton",
    command=add_input,
).pack(side="right", padx=6)

# Saved charges and plotting style:
charges_list = []
plot_streamlines = False


def save_values(boton):
    """Read, validate, and save the entered values, then plot them."""
    global plot_streamlines
    plot_streamlines = (boton != 1)
    charges_list.clear()

    for ex, ey, ec in zip(x_entries, y_entries, charge_entries):
        if any(elemento == "" for elemento in (ex.get(), ey.get(), ec.get())):
            label1.config(
                text="One or more charges with missing information have been ignored."
                ""
            )
            continue
        try:
            charges_list.append([
                float(eval(ex.get())),
                float(eval(ey.get())),
                float(eval(ec.get())),
            ])
        except (TypeError, ValueError, SyntaxError, NameError) as error:
            label1.config(text=f"Input error: {error}")
            return False

    if not charges_list:
        label1.config(text="Missing data")
        return False

    plot_field()
    return True


ttk.Button(
    frame_botones,
    text="Plot with vectors (Recommended)",
    style="Acento.TButton",
    command=lambda: save_values(1),
).pack(side="left", padx=6)
ttk.Button(
    frame_botones,
    text="Plot with streamlines (Experimental)",
    style="Acento.TButton",
    command=lambda: save_values(2),
).pack(side="right", padx=6, pady=5)

root.protocol("WM_DELETE_WINDOW", sys_exit)


# Total electric field, vectorized (all charges at once):
def calculate_total_field(charges, x_grid, y_grid):
    """Calculate the total electric field from all charges on the grid."""
    qs = np.array([c[2] for c in charges])
    xs = np.array([c[0] for c in charges])
    ys = np.array([c[1] for c in charges])

    r_x = x_grid[None, :, :] - xs[:, None, None]
    r_y = y_grid[None, :, :] - ys[:, None, None]
    length_r = np.sqrt(r_x**2 + r_y**2)

    with np.errstate(divide="ignore", invalid="ignore"):
        factor = np.where(length_r != 0, qs[:, None, None] / length_r**3, 0)

    return np.sum(factor * r_x, axis=0), np.sum(factor * r_y, axis=0)


def plot_field():
    """Plot the charges and their electric field (vectors or streamlines)."""
    plt.figure()

    coords_x = [c[0] for c in charges_list]
    coords_y = [c[1] for c in charges_list]
    density = density_var.get()

    x, y = np.meshgrid(
        np.linspace(min(coords_x) - 5, max(coords_x) + 5, density),
        np.linspace(min(coords_y) - 5, max(coords_y) + 5, density),
    )

    field_x, field_y = calculate_total_field(charges_list, x, y)
    field_magnitude = np.linalg.norm(np.array([field_x, field_y]), axis=0)

    for charge in charges_list:
        plt.plot(charge[0], charge[1], "ro")

    if not plot_streamlines:
        with np.errstate(divide="ignore", invalid="ignore"):
            dir_x = np.where(field_magnitude != 0, field_x / field_magnitude, 0)
            dir_y = np.where(field_magnitude != 0, field_y / field_magnitude, 0)
        plt.quiver(
            x, y, dir_x, dir_y, field_magnitude,
            cmap="viridis", norm=mcolors.LogNorm(),
        )
        plt.colorbar(label="Field magnitude")
    else:
        # Logarithmic scale for streamline width:
        log_norma = np.log10(field_magnitude)
        line_width = (
            5 * (log_norma - log_norma.min())
            / (log_norma.max() - log_norma.min())
        )
        line_width = np.clip(line_width, 0.3, 30)
        plt.streamplot(
            x, y, field_x, field_y, density=1.5, linewidth=line_width
        )

    plt.grid()
    plt.show()


root.mainloop()