

def check_student_grade(grade):
      # convert grade to int
      grade = int(grade)

      try:
            """
            IGCSE GRADE SYSTEM
            A (A-star): Exceptional performance (90-100%).
            A: Excellent (80-89%).
            B: Very Good (70-79%).
            C: Good (60-69%).
            D: Satisfactory (50-59%).
            E: Sufficient (40-49%).
            F: Acknowledges achievement (30-39%).
            G: Lowest passing grade (20-29%).
            U (Ungraded): Did not meet the standard for grade G (0-19%). 
            """

            if grade >= 90:
                  return 'A*'
            elif grade >= 80:
                  return 'A'
            elif grade >= 70:
                  return 'B'
            elif grade >= 60:
                  return 'C'
            elif grade >= 50:
                  return 'D'
            elif grade >= 40:
                  return 'E'
            elif grade >= 30:
                  return 'F'
            elif grade >= 20:
                  return 'G'
            else:
                  return 'U'
      except Exception as e:
            return str(e)
            