def find_gaps(intervals):
    gaps = []

    for i in range(1, len(intervals)):
        start_time = intervals[i - 1][1]
        end_time = intervals[i][0]

        # Check if there is a gap between intervals within the 13:00 - 21:00 range
        if '13:00' <= start_time <= '21:00' and '13:00' <= end_time <= '21:00':
            gap = [start_time, end_time]
            gaps.append(gap)
        # Check if there is a gap between intervals starting before '21:00' and ending after '21:00'
        elif start_time < '21:00' and end_time > '21:00':
            gaps.append([start_time, '21:00'])

    # Check the gap between the end of the last interval and 21:00
    last_end_time = intervals[-1][1]
    if last_end_time < '21:00':
        gaps.append([last_end_time, '21:00'])

    # Adjust gaps to fit within the '13:00' to '21:00' range
    adjusted_gaps = [[max(gap[0], '13:00'), min(gap[1], '21:00')] for gap in gaps]

    # Filter out invalid gaps
    adjusted_gaps = [gap for gap in adjusted_gaps if gap[0] < gap[1] and gap[0] != gap[1]]

    return adjusted_gaps


# Example usage
input_intervals1 = [['09:30', '10:00'], ['10:30', '11:00'], ['11:45', '13:30'], ['15:00', '19:00'], ['22:45', '23:00']]
input_intervals2 = [['09:30', '10:00'], ['10:30', '11:00']]
input_intervals3 = [['09:30', '14:05']]
input_intervals4 = [['20:30', '20:50'], ['23:11', '23:59']]

inputs_all = [input_intervals1, input_intervals2, input_intervals3, input_intervals4]

def print_output_all(input_intervals):
    for i, input_list in enumerate(input_intervals):
        print(f"Input Intervals {i+1}:")
        print(input_list)

        output_list = find_gaps(input_list)
        print(f"\nOutput {i+1}:")
        print(output_list)
        print('\n#########\n')

print_output_all(inputs_all)