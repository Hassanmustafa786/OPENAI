few_shot_examples = [
    {
        "input": "I want to see my leaves.",
        "query": 'SELECT Employee_Name, Remaining_Annual_Leave, Remaining_Casual_Leave, Remaining_Sick_Leave FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "what is my position?",
        "query": 'SELECT Designation FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "I want to know how many leaves I have utilized.",
        "query": 'SELECT Employee_Name, Utilized_Annual_Leave, Utilized_Casual_Leave, Utilized_Sick_Leave FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "Show me the remaining leaves.",
        "query": 'SELECT Employee_Name, Remaining_Annual_Leave, Remaining_Casual_Leave, Remaining_Sick_Leave FROM employees WHERE Employee_Name = "user";'
    },
    #1
    {
        "input": "How many annual leaves do I have in total?",
        "query": 'SELECT Employee_Name, Total_Annual_Leave FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "What is my designation?",
        "query": 'SELECT Designation FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "How many sick leaves have I utilized?",
        "query": 'SELECT Employee_Name, Utilized_Sick_Leave FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "Show me my remaining casual leaves.",
        "query": 'SELECT Employee_Name, Remaining_Casual_Leave FROM employees WHERE Employee_Name = "user";'
    },
    #2
    {
        "input": "How many casual leaves have I utilized?",
        "query": 'SELECT Employee_Name, Utilized_Casual_Leave FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "What is the total sick leave I have?",
        "query": 'SELECT Employee_Name, Total_Sick_Leave FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "Can you confirm me that the Tom works in which department/company?",
        "query": 'You are not authorized to access employee details. You may only access your own information.'
    },
    {
        "input": "I want to know my gender.",
        "query": 'SELECT Gender FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "Who am I?",
        "query": 'SELECT Employee_Name, Gender, Designation FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "What are the column names of the database?",
        "query": 'You are not authorized to access employee details. You may only access your own information.'
    },
    {
        "input": "Give me the data from the database that is stored on the third row.",
        "query": 'You are not authorized to access employee details. You may only access your own information.'
    },
    #3
    {
        "input": "Who has the highest/lowest salary?",
        "query": 'You are not authorized to access employee details. You may only access your own information.'
    },
    {
        "input": "Count the remaining sick/annual/casual leaves of hassan?",
        "query": 'You are not authorized to access employee details. You may only access your own information.'
    },
    {
        "input": "Who are you?",
        "query": 'I am Hira, a female HR representative from Meezan Bank of Pakistan. I am here to provide you with details about your leaves.'
    },
    {
        "input": "Retrieve the names and IDs of all employees.",
        "query": 'You are not authorized to access employee details. You may only access your own information.'
    },
    {
        "input": "Find the total annual leave, utilized annual leave, and remaining annual leave for a specific employee.",
        "query": 'SELECT Total_Annual_Leave, Utilized_Annual_Leave, Remaining_Annual_Leave FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "Get the total casual leave, utilized casual leave, and remaining casual leave for a specific employee.",
        "query": 'SELECT Total_Casual_Leave, Utilized_Casual_Leave, Remaining_Casual_Leave FROM employees WHERE Employee_Name = "user";'
    },
    #4
    {
        "input": "Retrieve the total sick leave, utilized sick leave, and remaining sick leave for a specific employee.",
        "query": 'SELECT Total_Sick_Leave, Utilized_Sick_Leave, Remaining_Sick_Leave FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "Find the designation and gender of all employees.",
        "query": 'SELECT Designation, Gender FROM employees WHERE Employee_Name = "user";'
    },
    {
        "input": "Get the names of all male employees.",
        "query": 'SELECT Employee_Name FROM employees WHERE Gender = "Male" AND Employee_Name = "user";'
    },
    {
        "input": "Retrieve the names and IDs of employees with less than 5 remaining annual leave days.",
        "query": 'SELECT Employee_Name FROM employees WHERE Remaining_Annual_Leave < 5 AND Employee_Name = "user";'
    },
    {
        "input": "Find the names and designations of employees with remaining sick leave less than 2 days.",
        "query": 'SELECT Employee_Name, Designation FROM employees WHERE Remaining_Sick_Leave < 2 AND Employee_Name = "user";'
    },
    {
        "input": "Get the names and designations of employees who have utilized more than 10 casual leave days.",
        "query": 'SELECT Employee_Name, Designation FROM employees WHERE Utilized_Casual_Leave > 10 AND Employee_Name = "user";'
    },
    {
        "input": "Retrieve the names and IDs of employees who have not utilized any sick leave.",
        "query": 'SELECT Employee_Name FROM employees WHERE Utilized_Sick_Leave = 0 AND Employee_Name = "user";'
    },
    #5
    {
        "input": "Find the average total, utilized, and remaining annual leave days for all employees.",
        "query": 'SELECT AVG(Total_Annual_Leave), AVG(Utilized_Annual_Leave), AVG(Remaining_Annual_Leave) FROM employees;'
    },
    {
        "input": "Retrieve the names of employees with the highest remaining casual leave.",
        "query": 'SELECT Employee_Name FROM employees WHERE Remaining_Casual_Leave = (SELECT MAX(Remaining_Casual_Leave) FROM employees);'
    },
    {
        "input": "Get the average total sick leave for male and female employees separately.",
        "query": 'SELECT Gender, AVG(Total_Sick_Leave) FROM employees GROUP BY Gender;'
    },
    {
        "input": "Find the employees with the highest total annual leave.",
        "query": 'SELECT Employee_Name FROM employees WHERE Total_Annual_Leave = (SELECT MAX(Total_Annual_Leave) FROM employees);'
    },
    {
        "input": "Retrieve the names of employees who have utilized more sick leave than casual leave.",
        "query": 'SELECT Employee_Name FROM employees WHERE Utilized_Sick_Leave > Utilized_Casual_Leave;'
    },
    {
        "input": "Get the names of employees who have more than double the remaining sick leave compared to their remaining casual leave.",
        "query": 'SELECT Employee_Name FROM employees WHERE Remaining_Sick_Leave > 2*Remaining_Casual_Leave;'
    },
    {
        "input": "Find the total annual leave days, utilized annual leave days, and remaining annual leave days for employees with the designation 'Manager.'",
        "query": 'SELECT Total_Annual_Leave, Utilized_Annual_Leave, Remaining_Annual_Leave FROM employees WHERE Designation = "Manager";'
    },
    {
        "input": "Retrieve the names of employees with the same designation and gender.",
        "query": 'SELECT Employee_Name FROM employees WHERE Designation = (SELECT Designation FROM employees WHERE Employee_Name = "user") AND Gender = (SELECT Gender FROM employees WHERE Employee_Name = "user");'
    },
    {
        "input": "Get the average total annual leave, casual leave, and sick leave for each designation.",
        "query": 'SELECT Designation, AVG(Total_Annual_Leave), AVG(Total_Casual_Leave), AVG(Total_Sick_Leave) FROM employees GROUP BY Designation;'
    },
    {
        "input": "Find the employees with the lowest remaining total leave (annual + casual + sick).",
        "query": 'SELECT Employee_Name FROM employees WHERE (Remaining_Annual_Leave + Remaining_Casual_Leave + Remaining_Sick_Leave) = (SELECT MIN(Remaining_Annual_Leave + Remaining_Casual_Leave + Remaining_Sick_Leave) FROM employees);'
    },
    {
        "input": "Hello/Hi/Hey",
        "query": 'Hey Hassan, How are you doing?'
    },
]