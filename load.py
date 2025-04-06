import pandas as pd

# Load the Excel files
enrollment_df = pd.read_excel("20_STUDENTS_ENROLLEMENT.xlsx")
program_df = pd.read_excel("ACAD_PROG.xlsx")
schedule_df = pd.read_excel("CLASS_SCHEDULE_4764.xlsx", header=1)
term_history_df = pd.read_excel("TERM_HISTORY.xlsx")

# Clean empty columns
schedule_df.dropna(axis=1, how='all', inplace=True)

def get_student_summary(emplid):
    student_courses = enrollment_df[enrollment_df['EMPLID'] == emplid]
    academic_info = program_df[program_df['EMPLID'] == emplid]
    term_info = term_history_df[term_history_df['EMPLID'] == emplid]

    if student_courses.empty:
        return "Student ID not found."

    summary = f"Student Name: {student_courses.iloc[0]['NAME_DISPLAY']}\n"
    summary += f"Academic Program: {academic_info.iloc[0]['ACAD_PROG'] if not academic_info.empty else 'N/A'}\n\n"
    summary += "📚 Enrolled Courses:\n"

    for _, row in student_courses.iterrows():
        summary += f" - {row['COURSE_TITLE_LONG']} | Grade: {row['CRSE_GRADE_OFF']} | GPA: {row['CUM_GPA']}\n"

    if not term_info.empty:
        summary += "\n📊 Term GPAs:\n"
        for _, row in term_info.iterrows():
            summary += f" - Term {row['STRM']}: GPA {row['TERM_GPA']}\n"

    return summary
