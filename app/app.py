from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['lesson_times']
collection = db['schedule']

def merge_time_intervals(intervals):
    intervals.sort(key=lambda x: x['start'])  # Sort intervals by start time
    merged_intervals = [intervals[0]]

    for interval in intervals[1:]:
        prev_interval = merged_intervals[-1]

        # If the current interval overlaps with the last merged interval, merge them
        if interval['start'] <= prev_interval['end']:
            prev_interval['end'] = max(interval['end'], prev_interval['end'])
        else:
            merged_intervals.append(interval)

    return merged_intervals

# lesson_times: [
#       { start: '13:00', end: '14:30' },
#       { start: '10:00', end: '11:30' }
#     ]

def generate_free_times(intervals):
    gaps = []

    # Sort the intervals by start time
    sorted_intervals = sorted(intervals, key=lambda x: x['start'])

    for i in range(1, len(sorted_intervals)):
        start_time = sorted_intervals[i - 1]['end']
        end_time = sorted_intervals[i]['start']

        # Check if there is a gap between intervals within the 13:00 - 21:00 range
        if '13:00' <= start_time <= '21:00' and '13:00' <= end_time <= '21:00':
            gap = {'start': start_time, 'end': end_time}
            gaps.append(gap)
        # Check if there is a gap between intervals starting before '21:00' and ending after '21:00'
        elif start_time < '21:00' and end_time > '21:00':
            gaps.append({'start': start_time, 'end': '21:00'})

    # Check the gap between the end of the last interval and 21:00
    last_end_time = sorted_intervals[-1]['end']
    if last_end_time < '21:00':
        gaps.append({'start': last_end_time, 'end': '21:00'})

    # Adjust gaps to fit within the '13:00' to '21:00' range
    adjusted_gaps = [{'start': max(gap['start'], '13:00'), 'end': min(gap['end'], '21:00')} for gap in gaps]

    # Filter out invalid gaps
    adjusted_gaps = [gap for gap in adjusted_gaps if gap['start'] < gap['end']]

    return adjusted_gaps

@app.route('/')
def index():
    # Retrieve data from MongoDB
    schedule_data = collection.find()

    merged_schedule = []
    for schedule in schedule_data:
        date = schedule['date']
        lesson_times = schedule['lesson_times']
        merged_intervals = merge_time_intervals(lesson_times)
        free_times = generate_free_times(merged_intervals)
        merged_schedule.append({'date': date, 'free_times': free_times})

    return render_template('index.html', schedule=merged_schedule)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # Assuming the file is a CSV file with date and lesson time columns
    for line in file.read().decode('utf-8').splitlines():
        date, start_time, end_time = line.split(',')
        schedule = {
            'date': date.strip(),
            'lesson_times': [{'start': start_time.strip(), 'end': end_time.strip()}]
        }

        # Update MongoDB collection
        collection.update_one({'date': date.strip()}, {'$push': {'lesson_times': {'$each': schedule['lesson_times']}}}, upsert=True)

    return "File uploaded successfully"

if __name__ == '__main__':
    app.run(debug=True)
