#!/usr/bin/env python
import sys

def plot_ascii_graph(prices, times=None, width=80, height=20):
    """
    Convert an array of numbers into a continuous ASCII line graph with both Y and X axes,
    and append an extra row of X-axis time labels as well as an extra column showing all time stamps.
    
    Args:
        prices: List of numerical values (prices) to plot.
        times: List of time strings corresponding to each price.
               Expected format "YYYY-MM-DD HH:MM:SS" (or similar).
        width: Width of the graph in characters (default: 80).
        height: Height of the graph in characters (default: 20). This is the plotting area height.
    
    Returns:
        A string containing the ASCII graph with axes and appended time stamps.
    """
    if not prices:
        return "No data to plot"
    
    # Determine min and max prices for scaling.
    min_price = min(prices)
    max_price = max(prices)
    price_range = max_price - min_price
    if price_range == 0:
        price_range = 1
    
    # Reserve space for Y-axis labels.
    y_axis_width = 6  # Columns 0 to 5 will be used for price labels.
    usable_width = width - y_axis_width
    x_step = (usable_width - 1) / (len(prices) - 1) if len(prices) > 1 else 0
    
    positions = []
    # For each price, compute (x, y) position in the graph.
    for i, price in enumerate(prices):
        # x is shifted right by y_axis_width.
        x = y_axis_width + int(i * x_step)
        # y is scaled to fit between row 0 and row (height - 2), leaving the (height - 1) row for the X-axis.
        y = height - 2 - int((price - min_price) / price_range * (height - 3))
        positions.append((x, y))
    
    # Increase canvas height by 1 to create an extra row for x-axis labels.
    canvas_height = height + 1
    graph = [[' ' for _ in range(width)] for _ in range(canvas_height)]
    
    # Draw the Y-axis on the plotting area (rows 0 to height-1).
    y_axis_pos = y_axis_width - 1
    for r in range(height):
        graph[r][y_axis_pos] = '|'
    
    # Draw the X-axis (horizontal line) on the row immediately above the extra label row.
    x_axis_pos = height - 1
    for x in range(y_axis_width, width):
        graph[x_axis_pos][x] = '-'
    # Mark the intersection of axes.
    graph[x_axis_pos][y_axis_pos] = '+'
    
    # --- Add Y-axis labels ---
    # For rows 0 to x_axis_pos - 1, compute and fill in the corresponding price.
    for r in range(x_axis_pos):
        # When r is 0 (top), label is close to max_price.
        label_price = min_price + ((height - 2) - r) / (height - 3) * price_range
        label_str = f"{label_price:6.2f}"
        for i, ch in enumerate(label_str):
            if i < y_axis_pos:
                graph[r][i] = ch
    # --- End Y-axis labels ---
    
    # Draw the line connecting the data points.
    for i in range(len(positions) - 1):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        
        if x1 == x2:
            # Vertical line.
            for y in range(min(y1, y2), max(y1, y2) + 1):
                graph[y][x1] = '|'
        elif y1 == y2:
            # Horizontal line.
            for x in range(x1, x2 + 1):
                graph[y1][x] = '_'
        else:
            # Diagonal line: choose slope character.
            slope_char = '/' if y2 < y1 else '\\'
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy
            cur_x, cur_y = x1, y1
            while cur_x != x2 or cur_y != y2:
                graph[cur_y][cur_x] = slope_char
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    cur_x += sx
                if e2 < dx:
                    err += dx
                    cur_y += sy
            graph[y2][x2] = '*'
    
    # Optionally mark the first data point.
    if positions:
        x, y = positions[0]
        graph[y][x] = '*'
    
    # --- Add X-axis tick marks and time labels onto the extra bottom row ---
    # We'll use the last row of the canvas for time labels.
    if times and len(prices) > 1:
        label_row = canvas_height - 1  # This is the extra row.
        # For clarity, we display approximately 10 labels if possible.
        step = max(1, len(prices) // 10)
        for i in range(0, len(prices), step):
            x_tick = y_axis_width + int(i * x_step)
            if x_tick < width:
                # Retrieve the time string.
                time_str = times[i]
                # If time string contains a space, assume "YYYY-MM-DD HH:MM:SS" and extract "HH:MM".
                if ' ' in time_str:
                    time_str = time_str.split(' ')[1]
                label_str = time_str[:5]  # Take the first 5 characters (HH:MM)
                # Center the label about the tick mark.
                start = max(y_axis_width, x_tick - len(label_str) // 2)
                for j, ch in enumerate(label_str):
                    if start + j < width:
                        graph[label_row][start + j] = ch
    # --- End X-axis tick labels ---
    
    # Convert the 2D canvas into a single string.
    result = ''
    for row in graph:
        result += ''.join(row) + '\n'
    
    # Append a legend.
    result += f"\nMin: {min_price:.2f} | Max: {max_price:.2f} | Y-axis: Price | X-axis: Time\n"
    
    # --- Append an extra column of time stamps after the legend (for full reference) ---
    if times:
        result += "\nAll Time Stamps:\n"
        for t in times:
            result += t + "\n\n"
    # --- End appended time stamps ---
    
    return result

def main():
    # Expecting two arguments: a comma-separated list of prices and a comma-separated list of times.
    if len(sys.argv) < 3:
        print("Usage: python ASCII_plotter.py <prices_csv> <times_csv>")
        sys.exit(1)
    
    try:
        prices = [float(p) for p in sys.argv[1].split(',')]
        times  = sys.argv[2].split(',')
    except ValueError as e:
        print("Error: Could not parse input. Ensure prices are numbers and times are valid strings.")
        sys.exit(1)
    
    chart = plot_ascii_graph(prices, times=times)
    print(chart)

if __name__ == "__main__":
    main()